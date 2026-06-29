---
tags:
  - netapp
  - operations
---
# ONTAP — Procedures

<div class="kb-summary">
ONTAP day-2 procedures — change readiness, rolling node upgrades, volume and LUN provisioning, SVM management, snapshot and SnapMirror operations, capacity management, and incident triage.

*Applies to: ONTAP 9.x*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## SVM / Volume / LUN Hierarchy

```d2
direction: right

cluster: "Cluster" {shape: rectangle}
nodeA: "Node A" {shape: rectangle}
nodeB: "Node B" {shape: rectangle}
aggrA: "Aggregate (aggr1" {shape: rectangle}
aggrB: "Aggregate (aggr2" {shape: rectangle}
svm1: "SVM: svm-nas" {shape: rectangle}
svm2: "SVM: svm-san" {shape: rectangle}
volNFS: "Volume: vol_nfs\njunction-path /nfs" {shape: rectangle}
volSMB: "Volume: vol_smb\njunction-path /smb" {shape: rectangle}
volSAN: "Volume: vol_iscsi" {shape: rectangle}
lun1: "LUN: /vol/vol_iscsi/lun0\nigroup: esxi-cluster" {shape: rectangle}
snap1: "Snapshots\n(hourly · daily · weekly" {shape: rectangle}
nfsExport: "NFS Export\n/etc/exports equiv" {shape: rectangle}
smbShare: "SMB Share\n\\\\server\\share" {shape: rectangle}

cluster -> nodeA
cluster -> nodeB
nodeA -> aggrA
nodeB -> aggrB
aggrA -> svm1
aggrA -> svm2
aggrB -> svm1
svm1 -> volNFS
svm1 -> volSMB
svm2 -> volSAN
volSAN -> lun1
volNFS -> snap1
volNFS -> nfsExport
volSMB -> smbShare
```

## Change Readiness

- [ ] All aggregates have at least 15% free capacity to absorb workload shifts during the change
- [ ] HA failover is operational on both nodes (`storage failover show` shows `true` for takeover-enabled)
- [ ] SnapMirror lag is within RPO on all critical relationships before quiescing
- [ ] No active volume move or aggregate rebalance jobs: `volume move show` and `storage aggregate relocation show`
- [ ] AutoSupport is working — send a start-of-maintenance message: `autosupport invoke -node * -type all -message "Starting maintenance"`
- [ ] No open disk rebuild operations: `storage disk show -broken` is clean
- [ ] Snapshots taken of affected volumes before change: `snapshot create -volume <vol> -snapshot pre-change`

| Item | Status | Notes |
|---|---|---|
| Aggregate free capacity ≥ 15% | | |
| HA takeover enabled on all nodes | | |
| SnapMirror lag within RPO | | |
| No active volume moves | | |
| AutoSupport start message sent | | |

## Rolling Node Upgrade Sequence

```mermaid
sequenceDiagram
    participant Admin
    participant Node1 as Node 1 (non-epsilon)
    participant Node2 as Node 2 (HA partner)

    Admin->>Admin: autosupport invoke — start maintenance
    Admin->>Admin: snapmirror quiesce all relationships
    Admin->>Node2: storage failover takeover -ofnode node1
    Node2-->>Admin: takeover complete — node1 aggregates on node2
    Admin->>Node1: apply firmware / ONTAP upgrade
    Node1-->>Admin: node1 back online
    Admin->>Node2: storage failover giveback -ofnode node1
    Node2-->>Admin: giveback complete
    Admin->>Admin: cluster show — validate node1 healthy
    Admin->>Node1: storage failover takeover -ofnode node2
    Node1-->>Admin: takeover complete
    Admin->>Node2: apply firmware / ONTAP upgrade
    Node2-->>Admin: node2 back online
    Admin->>Node1: storage failover giveback -ofnode node2
    Admin->>Admin: snapmirror resume all relationships
    Admin->>Admin: autosupport invoke — end maintenance
```

## Maintenance Window

1. Send AutoSupport start-of-maintenance: `autosupport invoke -node * -type all -message "Maintenance window starting"`
2. Quiesce SnapMirror relationships on volumes involved in the change: `snapmirror quiesce -destination-path <svm:vol>`
3. For rolling node upgrade — upgrade the non-epsilon node first; initiate takeover on the partner: `storage failover takeover -ofnode <node>`
4. Monitor takeover completion: `storage failover show` should show `In Takeover` then the node comes back up
5. Run `storage failover giveback -ofnode <node>` after the upgraded node is back online; confirm `Waiting for Giveback` transitions to normal
6. Validate cluster health after each node: `cluster show`, `system health alert show`
7. Resume SnapMirror relationships after all changes are complete: `snapmirror resume -destination-path <svm:vol>`
8. Send AutoSupport close-of-maintenance: `autosupport invoke -node * -type all -message "Maintenance window complete"`

## Post-Change Validation

- [ ] `cluster show` — all nodes healthy, HA pairs intact
- [ ] `storage failover show` — all nodes show giveback-enabled true, no takeover active
- [ ] `storage disk show -broken` — no new disk failures introduced during maintenance
- [ ] `snapmirror show -fields lag-time,healthy` — all relationships resumed and healthy
- [ ] `volume show -fields state,percent-used` — all volumes online, no state changes
- [ ] `network interface show -status-oper down` — no LIFs went offline during the change
- [ ] `system health alert show` — no new alerts generated
- [ ] Confirm storage is serving I/O to applications — verify from host side or application monitoring

## Incident Triage

- [ ] Run `cluster show` first — identify any nodes in degraded or removed state
- [ ] Run `system health alert show` — review all active alerts for severity and subsystem
- [ ] Run `storage disk show -broken` — identify any disk failures driving the incident
- [ ] Run `storage failover show` — check whether any HA takeover has occurred
- [ ] Run `snapmirror show -fields lag-time,healthy` — check if replication is healthy or contributing to the symptom
- [ ] Check specific protocol: `network interface show`, `iscsi session show`, or `fcp show initiator`
- [ ] Review recent EMS events for the affected node: `event log show -node <nodename> -severity error`

| Question | Answer |
|---|---|
| Which node or aggregate is affected? | |
| Is HA takeover currently active? | |
| Are any disks broken or rebuilding? | |
| Is SnapMirror lag outside RPO? | |
| Which protocol is the workload using? | |

---

## SVM Management

SVMs are logical storage containers within an ONTAP cluster. Each SVM has its own namespaces, LIFs, and protocol configurations.

### List SVMs

![List SVMs](../../../../assets/ontap-proc-list-svms.svg)

```bash
vserver show
vserver show -fields type,state,admin-state
```


```text title="Expected output"
Vserver     Type       Subtype    State    Admin-State
----------- ---------- ---------- -------- -----------
cluster1    admin                 running  up
svm-prod-01 data                  running  up
svm-prod-02 data                  running  up
svm-dev-01  data                  running  up
svm-nfs-01  data                  running  up

Vserver     Type       State    Admin-State
----------- ---------- -------- -----------
cluster1    admin      running  up
svm-prod-01 data       running  up
svm-prod-02 data       running  up
svm-dev-01  data       running  up
svm-nfs-01  data       running  up
```

!!! warning "Common errors"
    **`Error: "vserver show" is not a recognized command.`** — Ensure you are connected to the ONTAP cluster management interface via SSH or console, not the node shell.
    **`Error: This operation is not permitted: Insufficient privileges to run command "vserver show".`** — Verify your user role has the "admin" or equivalent privilege level assigned in ONTAP.
### SVM Health

![SVM Health](../../../../assets/ontap-proc-svm-health.svg)

```bash
# Confirm all SVMs are running
vserver show -state !running

# Check SVM root volume health
volume show -vserver <svm_name> -volume <svm_name>_root
```


```text title="Expected output"
Vserver     State    Subtype
----------- -------- ---------
(no entries)

Vserver       Volume                       State      Status
------------- ---------------------------- ---------- ----------
prod-svm-01   prod-svm-01_root             online     healthy
```

!!! warning "Common errors"
    **`Error: command not found: vserver`** — Ensure you are connected to the ONTAP cluster management interface via SSH or the ONTAP CLI, not a local shell.
    **`Error: invalid vserver name "prod-svm-01"`** — Replace `<svm_name>` with an actual SVM name from your cluster; use `vserver show` to list all available SVMs.
### Create an SVM

![Create an SVM](../../../../assets/ontap-proc-create-an-svm.svg)

```bash
vserver create \
    -vserver <svm_name> \
    -aggregate <aggr_name> \
    -rootvolume <svm_name>_root \
    -rootvolume-security-style unix
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: command failed: Aggregate "<aggr_name>" does not exist.`** — Verify the aggregate name with `storage aggregate show` and use the correct name in the `-aggregate` parameter.
    **`Error: command failed: Vserver "<svm_name>" already exists.`** — Choose a unique SVM name or delete the existing SVM with `vserver delete` before recreating it.
    **`Error: command failed: Security style "unix" is not valid for root volume.`** — Use `mixed`, `ntfs`, or `unix` (ensure UNIX is capitalized); verify ONTAP version supports the chosen style for root volumes.
### LIF Management

![LIF Management](../../../../assets/ontap-proc-lif-management.svg)

```bash
# List LIFs for an SVM
network interface show -vserver <svm_name>

# Create a data LIF
network interface create \
    -vserver <svm_name> \
    -lif <lif_name> \
    -role data \
    -home-node <node_name> \
    -home-port e0c \
    -address <ip> \
    -netmask <mask> \
    -data-protocol nfs,cifs

# Migrate a LIF to a different port
network interface migrate -vserver <svm_name> -lif <lif_name> -dest-node <node> -dest-port <port>
```


```text title="Expected output"
Vserver          Interface      IP Address      Status   Home Node/Port    Current Node/Port
--------         ---------      ----------      ------   ---------------   -----------------
prod-svm         nfs_lif_01     192.168.1.50    up       node1/e0c         node1/e0c
prod-svm         cifs_lif_01    192.168.1.51    up       node2/e0d         node2/e0d
prod-svm         mgmt_lif       192.168.1.10    up       node1/e0a         node1/e0a
prod-svm         iscsi_lif_01   192.168.1.60    up       node2/e0e         node2/e0e

(no output — command completes silently)

[Job 123] Job succeeded: network interface migrate completed successfully.
```

!!! warning "Common errors"
    **`Error: command failed: The specified home-port "e0c" does not exist on node "node1".`** — Verify the port exists on the target node using `network port show -node <node_name>`.
    **`Error: command failed: Cannot migrate LIF "nfs_lif_01" because it is currently hosting an active connection.`** — Migrate during a maintenance window or use `network interface migrate -force-administrative-vlan true` if necessary.
### DNS Configuration per SVM

![DNS Configuration per SVM](../../../../assets/ontap-proc-dns-configuration-per-svm.svg)

```bash
vserver services name-service dns show -vserver <svm_name>

vserver services name-service dns create \
    -vserver <svm_name> \
    -domains <domain> \
    -name-servers <dns_ip1>,<dns_ip2>
```


```text title="Expected output"
Vserver: svm-prod-01
Domains: corp.example.com, example.com
Name Servers: 8.8.8.8, 8.8.4.4
Timeout (secs): 2
Attempts: 1

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: "svm-prod-01" is not a valid vserver name`** — Verify the SVM name exists with `vserver show` and use the exact name from the Vserver column.
    **`Error: DNS create failed: Name servers already configured`** — Delete the existing DNS configuration first using `vserver services name-service dns delete -vserver <svm_name>` before creating a new one.
### NIS / LDAP Lookup

![NIS / LDAP Lookup](../../../../assets/ontap-proc-nis-ldap-lookup.svg)

```bash
vserver services name-service ns-switch show -vserver <svm_name>
vserver services name-service ldap show -vserver <svm_name>
```

### Stop / Start an SVM

![Stop / Start an SVM](../../../../assets/ontap-proc-stop-start-an-svm.svg)

```bash
vserver stop -vserver <svm_name>
vserver start -vserver <svm_name>
```

### Delete an SVM

![Delete an SVM](../../../../assets/ontap-proc-delete-an-svm.svg)

```bash
# Ensure no volumes except root
volume show -vserver <svm_name>

# Delete root volume and SVM
vserver delete -vserver <svm_name>
```

### SVM Common Issues

![SVM Common Issues](../../../../assets/ontap-proc-svm-common-issues.svg)

| Issue | Check | Action |
|---|---|---|
| SVM not running | Admin-state | `vserver start` |
| LIF not reachable | LIF status / port | Migrate LIF or fix port |
| Protocol not serving | Service enabled? | `vserver nfs create` or equivalent |
| DNS resolution failing | SVM DNS config | Verify DNS server IPs |

---

## Volume Management

### List Volumes

![List Volumes](../../../../assets/ontap-proc-list-volumes.svg)

```bash
volume show
volume show -vserver <svm_name>
volume show -fields size,used,available,percent-used,state
```

### Volume Health

![Volume Health](../../../../assets/ontap-proc-volume-health.svg)

```bash
# Show offline or restricted volumes
volume show -state !online

# Show volumes nearing capacity
volume show -fields percent-used | awk '$2 > 80'
```

### Create a Volume

![Create a Volume](../../../../assets/ontap-proc-create-a-volume.svg)

```bash
volume create \
    -vserver <svm_name> \
    -volume <vol_name> \
    -aggregate <aggr_name> \
    -size 500G \
    -junction-path /<vol_name> \
    -security-style unix
```

### Resize a Volume

![Resize a Volume](../../../../assets/ontap-proc-resize-a-volume.svg)

```bash
volume size -vserver <svm_name> -volume <vol_name> -new-size 1T
```

### Volume Autosize

![Volume Autosize](../../../../assets/ontap-proc-volume-autosize.svg)

```bash
volume autosize -vserver <svm_name> -volume <vol_name> \
    -mode grow_shrink \
    -maximum-size 2T \
    -grow-threshold-percent 85
```

### Volume Efficiency (Deduplication / Compression)

![Volume Efficiency (Deduplication / Compression)](../../../../assets/ontap-proc-volume-efficiency-deduplication-compression.svg)

```bash
# Check efficiency state
volume efficiency show -vserver <svm_name> -volume <vol_name>

# Enable efficiency
volume efficiency on -vserver <svm_name> -volume <vol_name>

# Run deduplication manually
volume efficiency start -vserver <svm_name> -volume <vol_name>
```

### Move a Volume (Between Aggregates)

![Move a Volume (Between Aggregates)](../../../../assets/ontap-proc-move-a-volume-between-aggregates.svg)

```bash
volume move start \
    -vserver <svm_name> \
    -volume <vol_name> \
    -destination-aggregate <dest_aggr>

volume move show
```

### Take a Volume Offline / Online

![Take a Volume Offline / Online](../../../../assets/ontap-proc-take-a-volume-offline-online.svg)

```bash
volume offline -vserver <svm_name> -volume <vol_name>
volume online -vserver <svm_name> -volume <vol_name>
```

### Delete a Volume

![Delete a Volume](../../../../assets/ontap-proc-delete-a-volume.svg)

```bash
# Offline first
volume offline -vserver <svm_name> -volume <vol_name>

# Delete
volume delete -vserver <svm_name> -volume <vol_name>
```

### Volume Common Issues

![Volume Common Issues](../../../../assets/ontap-proc-volume-common-issues.svg)

| Issue | Check | Action |
|---|---|---|
| Volume full | Percent-used | Resize or enable autosize |
| Volume offline | State | Bring online or investigate |
| Poor efficiency | Dedup/compress off | Enable volume efficiency |
| Mount fails | Junction path | Verify `-junction-path` set |

---

## Protocols

ONTAP supports NFS, SMB/CIFS, iSCSI, FCP (Fibre Channel), and NVMe over Fabrics. Protocol access is configured per SVM.

### NFS

![NFS](../../../../assets/ontap-proc-nfs.svg)

```bash
# Check NFS service status per SVM
nfs show -vserver <svm_name>

# List NFS exports
vserver nfs export-policy rule show -vserver <svm_name>

# Show NFS clients connected
nfs connected-client show -vserver <svm_name>
```

### SMB/CIFS

![SMB/CIFS](../../../../assets/ontap-proc-smb-cifs.svg)

```bash
# Check CIFS server status
cifs show -vserver <svm_name>

# List CIFS shares
vserver cifs share show -vserver <svm_name>

# Show active CIFS sessions
cifs session show -vserver <svm_name>
```

### iSCSI

![iSCSI](../../../../assets/ontap-proc-iscsi.svg)

```bash
# Check iSCSI service status
iscsi show -vserver <svm_name>

# List iSCSI LIFs
network interface show -vserver <svm_name> -data-protocol iscsi

# Show connected iSCSI initiators
iscsi initiator show -vserver <svm_name>

# Show iSCSI target portal groups
iscsi tpgroup show -vserver <svm_name>
```

### FCP (Fibre Channel)

![FCP (Fibre Channel)](../../../../assets/ontap-proc-fcp-fibre-channel.svg)

```bash
# Check FCP service status
fcp show -vserver <svm_name>

# List FCP LIFs (FC target ports)
network interface show -vserver <svm_name> -data-protocol fcp

# Show connected FC initiators
fcp initiator show -vserver <svm_name>

# Show FC target adapter status
system node hardware unified-connect show
```

### Protocol on LIF Verification

![Protocol on LIF Verification](../../../../assets/ontap-proc-protocol-on-lif-verification.svg)

```bash
# Show all data LIFs and their protocols
network interface show -role data -fields vserver,lif,address,data-protocol
```

### Enable/Disable a Protocol on an SVM

![Enable/Disable a Protocol on an SVM](../../../../assets/ontap-proc-enable-disable-a-protocol-on-an-svm.svg)

```bash
# Enable NFS
vserver nfs create -vserver <svm_name> -v3 enabled -v4.1 enabled

# Enable CIFS (requires AD join)
cifs setup -vserver <svm_name>

# Enable iSCSI
iscsi create -vserver <svm_name>
```

### Protocol Common Issues

![Protocol Common Issues](../../../../assets/ontap-proc-protocol-common-issues.svg)

| Issue | Check | Action |
|---|---|---|
| NFS mount fails | Export policy rules | Verify client IP matches export rule |
| CIFS share inaccessible | CIFS server joined to AD | Re-join AD if needed |
| iSCSI sessions dropping | LIF and network status | Check LIF availability and switch ports |
| FC initiator not logging in | Zoning and WWPN masking | Verify SAN zoning and LUN masking |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Ontap — Health Checks](../health-checks/)
- [Ontap — CLI Reference](../cli-reference/)
- [Ontap — Common Issues](../../troubleshooting/common-issues/)
