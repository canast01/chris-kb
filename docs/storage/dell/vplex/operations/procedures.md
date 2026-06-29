---
tags:
  - dell
  - operations
---
# Dell VPLEX — Procedures

<div class="kb-summary">
Procedures reference covering Change Readiness, Maintenance Window, Post-Change Validation, Consistency Groups, Metro Operations.

*Applies to: VPLEX*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Change Readiness

Verify these items before performing any VPLEX change — GeoSynchrony upgrades, director replacements, back-end storage changes, or storage view modifications.

```d2
direction: right

startChange: "Maintenance window requested" {shape: rectangle}
ddCheck: "ll /distributed-storage/distributed-devices/*/health-indications/\nAll devices health-state: ok?" {shape: rectangle}
witnessChk: "ll /metro-node/*/witness/\nWitness connected from both clusters?" {shape: rectangle}
cgChk: "ll /distributed-storage/consistency-groups/\nAll CGs operational-status: ok?" {shape: rectangle}
hostPathChk: "powermt display dev=all\nmultipath -ll\nHost path counts match baseline?" {shape: rectangle}
arrayChk: "Back-end array health check\nPowerMax / Unity" {shape: rectangle}
vmsBackup: "VMS VM backup\ncurrent snapshot taken?" {shape: rectangle}
proceed: "proceed" {shape: rectangle}
holdChange: "Do not proceed\nResolve issues first" {shape: rectangle}
doChange: "Execute maintenance\nprocedure" {shape: rectangle}

startChange -> ddCheck
ddCheck -> witnessChk
witnessChk -> cgChk
cgChk -> hostPathChk
hostPathChk -> arrayChk
arrayChk -> vmsBackup
vmsBackup -> proceed
proceed -> holdChange
proceed -> doChange
```

- [ ] `ll /distributed-storage/distributed-devices/*/health-indications/` — all distributed devices show `health-state: ok`; do not start a change with any device out-of-sync
- [ ] Witness is reachable from both Metro clusters: `ll /metro-node/*/witness/` — loss of Witness during a change that takes a cluster offline will suspend I/O on consistency group volumes
- [ ] All consistency groups show `operational-status: ok`: `ll /distributed-storage/consistency-groups/`
- [ ] Host I/O validated: confirm path counts and multipath state on all hosts using VPLEX storage views (`powermt display dev=all` or `multipath -ll` on connected hosts)
- [ ] Back-end array health confirmed — run health checks on the back-end PowerMax, Unity, or other array before any VPLEX change that touches back-end storage volumes
- [ ] For GeoSynchrony upgrades: confirm target version compatibility with back-end array firmware, hypervisor versions, and host OS multipath drivers from the Dell VPLEX compatibility matrix
- [ ] Confirm VMS (VPLEX Management Server) VM is running and backed up — losing VMS during a change does not impact I/O but makes configuration recovery impossible without a backup
- [ ] Notify application and host owners of the maintenance window; confirm consistency groups can be suspended briefly if needed for the specific change type

| Item | Status | Notes |
|---|---|---|
| All distributed devices health-state: ok | | |
| Witness connected and reachable | | |
| All consistency groups ok | | |
| Host path counts match baseline | | |
| Back-end array health confirmed | | |
| VMS VM backed up | | |

## Maintenance Window

Steps for planned VPLEX maintenance — director replacement, GeoSynchrony NDU, or site-level switch for Metro workloads.

1. Notify host and application owners of the maintenance window; confirm consistency group volumes can tolerate temporary director redundancy reduction during director-level NDU
2. Confirm `ll /distributed-storage/distributed-devices/*/health-indications/` shows all devices `health-state: ok` before starting; do not start a director upgrade with any device out-of-sync
3. Confirm Witness is reachable from both clusters: `ll /metro-node/*/witness/`; for planned site switch tests, confirm the Witness is in the third failure domain
4. For GeoSynchrony NDU: upgrade one director at a time per engine; after each director upgrade, wait for `ll /engines/*/directors/*/hardware/` to confirm the director returned to healthy state before proceeding to the next
5. After all directors on an engine are upgraded, confirm distributed device health with `ll /distributed-storage/distributed-devices/*/health-indications/` before moving to the next engine
6. For a planned Metro site switch: suspend consistency group I/O cleanly, perform the site switch, verify host I/O resumes on the surviving cluster, then restore Witness and ICL before resuming the original cluster
7. Upgrade the VMS after all directors are at the new GeoSynchrony code level
8. Run `health-check --full` and confirm all clusters, directors, distributed devices, and consistency groups are healthy before closing the maintenance window

## Post-Change Validation

Run these checks after any VPLEX change to confirm the system is healthy and hosts have full path redundancy restored.

- [ ] `ll /clusters/*/health-indications/` — all clusters show `health-state: ok`
- [ ] `ll /distributed-storage/distributed-devices/*/health-indications/` — all distributed devices show `health-state: ok`; no devices in out-of-sync or rebuilding state
- [ ] `ll /engines/*/directors/*/hardware/` — all directors are healthy; no components in a faulted state post-change
- [ ] `ll /metro-node/*/witness/` — Witness is `connected: true` and `reachable: true` from both clusters
- [ ] `ll /distributed-storage/consistency-groups/` — all consistency groups show `operational-status: ok`
- [ ] Host path validation: `powermt display dev=all` or `multipath -ll` on representative hosts shows all paths alive and path count matches the pre-change baseline
- [ ] `health-check --full` returns no warnings or errors
- [ ] Application owners confirm I/O has resumed normally and no elevated latency is observed post-change

## Consistency Groups

Consistency groups (CGs) in VPLEX ensure that a set of virtual volumes is treated as a crash-consistent unit during failover and recovery operations.

### List Consistency Groups

![List Consistency Groups](../../../../assets/vplex-proc-list-consistency-groups.svg)

```bash
VPlexcli:/> ll /clusters/cluster-1/consistency-groups/
VPlexcli:/> ll /clusters/cluster-2/consistency-groups/
```


```text title="Expected output"
VPlexcli:/> ll /clusters/cluster-1/consistency-groups/
    Name                              Enabled  Detached  Operational  Transferring
    cg-prod-db-01                     true     false     true         false
    cg-prod-db-02                     true     false     true         false
    cg-prod-app-tier                  true     false     true         false
    cg-dr-replica-01                  true     false     false        true
    cg-archive-backup                 false    false     true         false

VPlexcli:/> ll /clusters/cluster-2/consistency-groups/
    Name                              Enabled  Detached  Operational  Transferring
    cg-prod-db-01                     true     false     true         false
    cg-prod-db-02                     true     false     true         false
    cg-prod-app-tier                  true     false     true         false
    cg-dr-replica-02                  true     false     true         false
```

!!! warning "Common errors"
    **`Error: Invalid path /clusters/cluster-2/consistency-groups/`** — Verify cluster-2 exists with `ll /clusters/` and confirm the cluster name spelling.
    **`Error: Permission denied accessing consistency-groups`** — Ensure your VPlexcli user role has read permissions for consistency group objects; contact your VPLEX administrator.
### View CG Details

![View CG Details](../../../../assets/vplex-proc-view-cg-details.svg)

```bash
VPlexcli:/> ll /clusters/cluster-1/consistency-groups/<cg_name>/
```


```text title="Expected output"
Name                                    Size      Date
consistency-group-1                     4.0 KB    2024-01-15 14:32:18
consistency-group-1/virtual-volumes     -         2024-01-15 14:32:18
consistency-group-1/snapshots           -         2024-01-15 14:32:18
consistency-group-1/recoverpoint        -         2024-01-15 14:32:18
consistency-group-1/replication-sets    -         2024-01-15 14:32:18
```

!!! warning "Common errors"
    **`No such object: /clusters/cluster-1/consistency-groups/<cg_name>/`** — Replace `<cg_name>` with the actual consistency group name (e.g., `cg-prod-db-01`).
    **`Permission denied`** — Verify your VPLEX user account has read access to the consistency group; contact your VPLEX administrator if needed.
Key attributes:
- `operational-status` — should be `ok`
- `type` — `local` or `distributed`
- `virtual-volumes` — list of member volumes

### Create a Consistency Group

![Create a Consistency Group](../../../../assets/vplex-proc-create-a-consistency-group.svg)

```bash
VPlexcli:/> consistency-group create --name <cg_name> --cluster-name cluster-1
```


```text title="Expected output"
VPlexcli:/> consistency-group create --name prod-cg-01 --cluster-name cluster-1
Created consistency group 'prod-cg-01' with ID: 5f8c3a2b-1e4d-47f9-9c2a-8d6e1f4a9b7c
Consistency group is now available on cluster-1
```

!!! warning "Common errors"
    **`Error: Consistency group 'prod-cg-01' already exists`** — Use a unique name or delete the existing consistency group with `consistency-group delete --name prod-cg-01` first.
    **`Error: Cluster 'cluster-1' not found or is offline`** — Verify the cluster name with `cluster list` and ensure both cluster nodes are online and communicating.
### Add Volumes to a CG

![Add Volumes to a CG](../../../../assets/vplex-proc-add-volumes-to-a-cg.svg)

```bash
VPlexcli:/> consistency-group add-virtual-volume \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg_name> \
    --virtual-volume /clusters/cluster-1/virtual-volumes/<vol_name>
```


```text title="Expected output"
VPlexcli:/> consistency-group add-virtual-volume \
    --consistency-group /clusters/cluster-1/consistency-groups/prod-cg-01 \
    --virtual-volume /clusters/cluster-1/virtual-volumes/prod-vol-app-tier
Virtual volume 'prod-vol-app-tier' successfully added to consistency group 'prod-cg-01'.
Consistency group updated. Current member count: 8
```

!!! warning "Common errors"
    **`Error: Consistency group '/clusters/cluster-1/consistency-groups/<cg_name>' not found`** — Verify the consistency group name exists using `consistency-group list` and confirm the full path is correct.
    **`Error: Virtual volume '/clusters/cluster-1/virtual-volumes/<vol_name>' is already a member of another consistency group`** — Remove the virtual volume from its current consistency group first using `consistency-group remove-virtual-volume` before adding it to a new one.
### Remove a Volume from a CG

![Remove a Volume from a CG](../../../../assets/vplex-proc-remove-a-volume-from-a-cg.svg)

```bash
VPlexcli:/> consistency-group remove-virtual-volume \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg_name> \
    --virtual-volume /clusters/cluster-1/virtual-volumes/<vol_name>
```


```text title="Expected output"
Removing virtual volume vol-prod-db-01 from consistency group cg-finance-tier1...
Virtual volume successfully removed from consistency group.
Consistency group cg-finance-tier1 now contains 3 virtual volumes (was 4).
Operation completed in 2.341 seconds.
```

!!! warning "Common errors"
    **`Error: Consistency group not found: /clusters/cluster-1/consistency-groups/<cg_name>`** — Verify the consistency group name exists by running `consistency-group list` and use the exact path shown in the output.
    **`Error: Virtual volume is not a member of this consistency group`** — Confirm the virtual volume belongs to the target consistency group using `consistency-group show --consistency-group <cg_name>` before removal.
    **`Error: Cannot remove virtual volume while replication is in progress`** — Wait for any active replication or snapshot operations to complete before attempting removal.
### Distributed Consistency Groups

![Distributed Consistency Groups](../../../../assets/vplex-proc-distributed-consistency-groups.svg)

For Metro configurations, CGs span both clusters:

```bash
VPlexcli:/> ll /clusters/cluster-1/consistency-groups/<cg_name>/
# Check: type = distributed
# Check: operational-status = ok on both clusters
```


```text title="Expected output"
VPlexcli:/> ll /clusters/cluster-1/consistency-groups/cg-prod-db-01/
    name                          cg-prod-db-01
    type                          distributed
    operational-status            ok
    transfer-size                 1048576
    cluster-1-status              ok
    cluster-2-status              ok
    visibility                    cluster-1,cluster-2
    recoverpoint-enabled          false
    recoverpoint-copy-enabled     false
    virtual-volumes              
        vv-prod-db-01-lun1
        vv-prod-db-01-lun2
        vv-prod-db-01-lun3
    storage-containers
        sc-array-1-pool-1
        sc-array-2-pool-1
```

!!! warning "Common errors"
    **`Invalid path: /clusters/cluster-1/consistency-groups/<cg_name>/`** — Replace `<cg_name>` with the actual consistency group name (e.g., `cg-prod-db-01`).
    **`operational-status = degraded`** — Check cluster connectivity and array backend status with `ll /clusters/cluster-1/` and verify no storage array failures exist.
### Detach / Re-attach CG (Metro Failover)

![Detach / Re-attach CG (Metro Failover)](../../../../assets/vplex-proc-detach-re-attach-cg-metro-failover.svg)

```bash
# Detach from cluster-2 (planned maintenance or failover)
VPlexcli:/> consistency-group detach \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg_name>

# Re-attach after recovery
VPlexcli:/> consistency-group attach \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg_name>
```


```text title="Expected output"
Detaching consistency group cg-prod-db-01 from cluster-2...
  Status: In Progress
  Detach initiated at 2024-01-15T14:32:18Z
  Estimated time remaining: 45 seconds

Detach completed successfully.
  Consistency group: /clusters/cluster-1/consistency-groups/cg-prod-db-01
  Status: Detached
  Detach completed at 2024-01-15T14:33:03Z

Re-attaching consistency group cg-prod-db-01 to cluster-2...
  Status: In Progress
  Attach initiated at 2024-01-15T14:45:22Z
  Estimated time remaining: 60 seconds

Attach completed successfully.
  Consistency group: /clusters/cluster-1/consistency-groups/cg-prod-db-01
  Status: Attached
  Attach completed at 2024-01-15T14:46:22Z
```

!!! warning "Common errors"
    **`Error: Consistency group /clusters/cluster-1/consistency-groups/<cg_name> not found`** — Verify the consistency group name matches exactly and use `consistency-group list` to confirm it exists.
    **`Error: Cannot detach consistency group in use by active I/O operations`** — Quiesce all application I/O to the consistency group before attempting detach.
    **`Error: Cluster-2 is unreachable or in degraded state`** — Check cluster connectivity with `cluster status` and ensure both clusters are healthy before re-attaching.
## Metro Operations

VPLEX Metro stretches virtual volumes across two sites with synchronous mirroring, enabling transparent failover.

### Metro Architecture Overview

![Metro Architecture Overview](../../../../assets/vplex-proc-metro-architecture-overview.svg)

- **Cluster-1** — Site A (local cluster)
- **Cluster-2** — Site B (remote cluster)
- **WAN COM** — inter-cluster communication link (Fibre Channel or Ethernet)
- **Distributed Devices** — virtual volumes that span both clusters
- **Witness** — third-party tiebreaker for split-brain scenarios

```d2
direction: right

iclFails: "ICL failure detected" {shape: rectangle}
witnessChk: "Does Witness contact\nboth clusters?" {shape: rectangle}
witnessGrants: "Witness grants quorum\nto first requesting cluster" {shape: rectangle}
survivorIo: "Surviving cluster\ncontinues I/O normally" {shape: rectangle}
otherSuspend: "Other cluster distributed\ndevice legs suspended" {shape: rectangle}
iclRestore: "ICL restored" {shape: rectangle}
autoResync: "VPLEX auto-resync\nrebuild-progress → 100%" {shape: rectangle}
inSync: "Distributed device\nin-sync — Metro restored" {shape: rectangle}
noWitness: "Both clusters unsure\nof each other's state" {shape: rectangle}
ioSuspend: "I/O suspended on\nall CG volumes" {shape: rectangle}
manualRecover: "Manual recovery\nidentify active leg\ndevice resume" {shape: rectangle}

iclFails -> witnessChk
witnessChk -> witnessGrants
witnessGrants -> survivorIo
witnessGrants -> otherSuspend
survivorIo -> iclRestore
iclRestore -> autoResync
autoResync -> inSync
witnessChk -> noWitness
noWitness -> ioSuspend
ioSuspend -> manualRecover
```

### Check Distributed Device Status

![Check Distributed Device Status](../../../../assets/vplex-proc-check-distributed-device-status.svg)

```bash
VPlexcli:/> ll /distributed-storage/distributed-devices/
VPlexcli:/> ll /distributed-storage/distributed-devices/<device_name>/
```


```text title="Expected output"
VPlexcli:/> ll /distributed-storage/distributed-devices/
Name                              Capacity        Status
device-1                          2.0 TB          ok
device-2                          2.0 TB          ok
device-3                          1.5 TB          ok
device-4                          1.5 TB          ok

VPlexcli:/> ll /distributed-storage/distributed-devices/device-1/
Name                              Value
capacity                          2.0 TB
status                            ok
operational-status               ok
health-state                      healthy
rebuild-progress                  100%
```

!!! warning "Common errors"
    **`No such object: /distributed-storage/distributed-devices/<device_name>/`** — Replace `<device_name>` with an actual device name from the first command output (e.g., `device-1`).
    **`Connection refused`** — Ensure you are connected to the VPLEX CLI with valid credentials and the management server is reachable.
Key attributes:
- `service-status: running` — both legs active
- `operational-status: ok`
- `active-leg` — which cluster is currently active

### Planned Failover (Migrate Active Leg)

![Planned Failover (Migrate Active Leg)](../../../../assets/vplex-proc-planned-failover-migrate-active-leg.svg)

```bash
# Move active leg to cluster-2
VPlexcli:/> device migrate \
    --device /distributed-storage/distributed-devices/<device_name> \
    --target-cluster cluster-2
```


```text title="Expected output"
Checking device /distributed-storage/distributed-devices/prod-lun-001...
Device is currently active on cluster-1
Initiating migration to cluster-2...
Migration started: job-id 4f8c2a91-7e3a-4d2b-9f1c-6e2d5a3b8c1a
Progress: 10%
Progress: 25%
Progress: 50%
Progress: 75%
Progress: 100%
Migration completed successfully
Device /distributed-storage/distributed-devices/prod-lun-001 is now active on cluster-2
```

!!! warning "Common errors"
    **`Error: Device /distributed-storage/distributed-devices/<device_name> not found`** — Verify the device name is correct and exists by running `device list` to confirm the full path.
    **`Error: Cannot migrate device - active I/O detected on target cluster`** — Wait for I/O operations to complete or quiesce the device with `device quiesce` before retrying the migration.
    **`Error: Cluster cluster-2 is not in a healthy state`** — Check cluster-2 status with `cluster status` and resolve any connectivity or component failures before attempting migration.
### Witness Configuration

![Witness Configuration](../../../../assets/vplex-proc-witness-configuration.svg)

```bash
VPlexcli:/> ll /distributed-storage/witness/
# Check: witness-connectivity = connected
```


```text title="Expected output"
total 48
drwxr-xr-x  4 root root  4096 Nov 15 10:23 .
drwxr-xr-x 15 root root  4096 Nov 15 10:23 ..
-rw-r--r--  1 root root  2048 Nov 15 10:22 witness.conf
-rw-r--r--  1 root root  1024 Nov 15 10:22 witness.status
drwxr-xr-x  2 root root  4096 Nov 15 10:23 logs
drwxr-xr-x  2 root root  4096 Nov 15 10:23 cache

witness-connectivity = connected
```

!!! warning "Common errors"
    **`witness-connectivity = disconnected`** — Verify network connectivity between VPLEX cluster and witness appliance, and confirm witness service is running with `service witness status`.
    **`ls: cannot access '/distributed-storage/witness/': No such file or directory`** — Ensure you are logged into the VPLEX management console and the witness path is mounted; check with `df -h | grep witness`.
### Split-Brain Recovery

![Split-Brain Recovery](../../../../assets/vplex-proc-split-brain-recovery.svg)

If WAN COM link fails and both clusters believe they are active:

1. Witness should automatically resolve by suspending one cluster
2. If witness is unavailable, manual intervention required
3. Identify which cluster has the most recent I/O
4. Suspend the stale cluster leg:

```bash
VPlexcli:/> device suspend \
    --device /distributed-storage/distributed-devices/<device_name> \
    --clusters cluster-2
```


```text title="Expected output"
VPlexcli:/> device suspend \
    --device /distributed-storage/distributed-devices/dev-lun-prod-01 \
    --clusters cluster-2
Suspending device dev-lun-prod-01 on cluster-2...
Device suspension initiated. Device will enter suspended state.
Current device status: SUSPENDED
Cluster-2 node-2: Device I/O suspended
Cluster-2 node-1: Device I/O suspended
Suspension completed successfully.
```

!!! warning "Common errors"
    **`Error: Device not found at path /distributed-storage/distributed-devices/<device_name>`** — Verify the device name exists by running `device list` and use the correct path from the output.
    **`Error: Cluster cluster-2 is not reachable or does not exist`** — Confirm cluster-2 is online and accessible using `cluster list`, then retry the suspension.
    **`Error: Device is already in SUSPENDED state`** — The device is already suspended; use `device resume` if you need to restore I/O operations.
5. After link recovery, resync:

```bash
VPlexcli:/> device rebuild \
    --device /distributed-storage/distributed-devices/<device_name>
```


```text title="Expected output"
Rebuild initiated for device: dev-lun-prod-01
Device: /distributed-storage/distributed-devices/dev-lun-prod-01
Status: REBUILDING
Progress: 0%
Estimated time remaining: 4h 32m
Current rebuild rate: 125 MB/s
Rebuild started at: 2024-01-15 14:23:47 UTC
```

!!! warning "Common errors"
    **`Device not found: /distributed-storage/distributed-devices/<device_name>`** — Verify the device name exists by running `device list` and use the correct path from the output.
    **`Device is already rebuilding`** — Wait for the current rebuild to complete or cancel it with `device rebuild --cancel` before initiating a new rebuild.
    **`Insufficient cluster resources for rebuild operation`** — Check cluster health with `cluster status` and ensure both nodes have adequate free capacity before retrying.
### WAN COM Health

![WAN COM Health](../../../../assets/vplex-proc-wan-com-health.svg)

```bash
VPlexcli:/> ll /clusters/cluster-1/connectivity/
```


```text title="Expected output"
Name                                    Size      Date
cluster-1-node-a                        -         Nov 15 10:23
cluster-1-node-b                        -         Nov 15 10:23
san-fabric-a                            -         Nov 15 10:18
san-fabric-b                            -         Nov 15 10:18
iscsi-initiators                        -         Nov 15 09:45
fc-initiators                           -         Nov 15 09:45
backend-storage-arrays                  -         Nov 15 10:12
```

!!! warning "Common errors"
    **`Invalid path /clusters/cluster-1/connectivity/`** — Verify the cluster name with `ll /clusters/` and confirm the connectivity directory exists in your VPLEX version.
    **`Permission denied`** — Ensure your VPLEX user account has read permissions for the cluster connectivity paths; contact your VPLEX administrator to grant access.
Monitor inter-cluster latency — VPLEX Metro requires < 5ms RTT between sites.

### Common Metro Issues

![Common Metro Issues](../../../../assets/vplex-proc-common-metro-issues.svg)

| Issue | Check | Action |
|---|---|---|
| Device degraded | Check WAN COM link | Investigate network |
| Split-brain | Witness connectivity | Manual suspension of stale leg |
| High replication lag | WAN latency | Check inter-cluster network |
| Device suspended | Prior split-brain event | Resync after link recovery |

## Create a Virtual Volume

A VPLEX virtual volume is built from a backend storage LUN through a four-step process: claim the backend storage volume, create an extent, create a device, and expose it as a virtual volume to a host cluster.

```bash
# Step 1 — Claim backend storage volume into VPLEX
VPlexcli:/> storage-volume claim-storage-volumes \
    --storage-volumes /clusters/cluster-1/storage-elements/storage-volumes/<sv-name>

# Step 2 — Create an extent from the claimed storage volume
VPlexcli:/> extent create \
    --storage-volume /clusters/cluster-1/storage-elements/storage-volumes/<sv-name> \
    --name <extent-name>

# Step 3 — Create a local device from the extent
VPlexcli:/> device create \
    --extents /clusters/cluster-1/storage-elements/extents/<extent-name> \
    --geometry raid-0 \
    --name <device-name>

# Step 4 — Create a virtual volume from the device
VPlexcli:/> virtual-volume create \
    --device /clusters/cluster-1/devices/<device-name> \
    --name <vv-name>
```


```text title="Expected output"
VPlexcli:/> storage-volume claim-storage-volumes \
    --storage-volumes /clusters/cluster-1/storage-elements/storage-volumes/sv-prod-lun-01
Storage volume sv-prod-lun-01 claimed successfully.
Capacity: 500.00 GB

VPlexcli:/> extent create \
    --storage-volume /clusters/cluster-1/storage-elements/storage-volumes/sv-prod-lun-01 \
    --name extent-prod-01
Extent extent-prod-01 created successfully.
Extent ID: 7a3f8c2e-91d4-4b6a-9e1f-2c5d8a7b4e9f
Size: 500.00 GB

VPlexcli:/> device create \
    --extents /clusters/cluster-1/storage-elements/extents/extent-prod-01 \
    --geometry raid-0 \
    --name device-prod-01
Device device-prod-01 created successfully.
Device ID: 4d2e1a9c-7f5b-4e8d-a3c6-9b2f1e7d5a8c
Total Capacity: 500.00 GB

VPlexcli:/> virtual-volume create \
    --device /clusters/cluster-1/devices/device-prod-01 \
    --name vv-prod-01
Virtual volume vv-prod-01 created successfully.
Virtual Volume ID: 8f9e2d1c-5a7b-4c3e-9f1a-6d8b2e4c7a9f
Capacity: 500.00 GB
```

!!! warning "Common errors"
    **`Error: Storage volume sv-prod-lun-01 is already claimed`** — Verify the storage volume is unclaimed using `storage-volume list` and unclaim it if necessary with `storage-volume unclaim-storage-volumes`.
    **`Error: Extent extent-prod-01 already exists`** — Use a unique extent name or delete the existing extent with `extent delete --name extent-prod-01` before recreating.
    **`Error: Device path /clusters/cluster-1/devices/device-prod-01 not found`** — Ensure the device was created successfully in the previous step and verify the exact device name matches the path.
After creation, expose the virtual volume to hosts by adding it to a storage view: `storage-view add-virtual-volumes --storage-view /clusters/cluster-1/exports/storage-views/<sv-name> --virtual-volumes /clusters/cluster-1/virtual-volumes/<vv-name>`.

## Add a Storage Volume to a Device

Extend an existing VPLEX device to increase its capacity by adding a new extent. This is used to grow a virtual volume without disrupting host access.

```bash
# Extend an existing device with a new extent
VPlexcli:/> device extend \
    -d <device-name> \
    -e <new-extent>

# Verify device redundancy and extent membership after extension
VPlexcli:/> device show <device-name>
```


```text title="Expected output"
VPlexcli:/> device extend -d device_lun_01 -e extent_005
Device device_lun_01 extended successfully.
New extent extent_005 added to device.
Rebuild initiated: 34% complete

VPlexcli:/> device show device_lun_01
Device Name:           device_lun_01
Device State:          REBUILDING
Redundancy:            RAID-1
Extents:               extent_001, extent_002, extent_005
Extent States:         CLEAN, CLEAN, REBUILDING
Capacity:              2.0 TB
Rebuild Progress:      34%
Last Modified:         2024-01-15 14:22:33 UTC
```

!!! warning "Common errors"
    **`Error: Extent extent_005 is already in use by device device_lun_02`** — Choose a different extent that is not currently assigned to another device.
    **`Error: Device device_lun_01 does not support additional extents (max capacity reached)`** — Verify the device's extent limit has not been exceeded or create a new device instead.
Confirm the device shows the expected number of extents and that `operational-status` is `ok` before considering the procedure complete. If the device is part of a distributed virtual volume, allow time for the Metro resync to complete.

## Migrate a Virtual Volume to New Storage

Data migration moves a virtual volume's backend data from one set of storage to another without host disruption. Use this when decommissioning old arrays or rebalancing across backends.

```bash
# Navigate to the VPLEX management server via browser or CLI
# VPLEX GUI: Data Services → Data Migration → New Migration

# Step 1 — Select the source virtual volume in the migration wizard
# Step 2 — Select the target backend storage (new array LUNs claimed into VPLEX)
# Step 3 — Start the migration and monitor progress

# Monitor migration progress via CLI
VPlexcli:/> data-migration show
# Check: transfer-size, completion-percentage, status
```


```text title="Expected output"
VPlexcli:/> data-migration show
    Migration Name: vol-prod-db-001_migration
    Source Volume: vol-prod-db-001
    Target Volume: vol-prod-db-001-new
    Transfer Size: 2.5 TB
    Completion Percentage: 67%
    Status: in-progress
    Elapsed Time: 2h 14m
    Estimated Time Remaining: 1h 06m
    Throughput: 412 MB/s
    Migration ID: migration-uuid-a7f2c9e1-4b8d-11ed-9e2a
```

!!! warning "Common errors"
    **`data-migration show: command not found`** — Ensure you are logged into the VPLEX CLI with proper credentials and in the correct management context (use `connect-mgmt-server` first).
    **`Error: No active migrations found`** — Verify the migration was actually started in the GUI under Data Services → Data Migration and that the source and target volumes are properly claimed into VPLEX.
    **`Permission denied: insufficient privileges for data-migration operations`** — Confirm your VPLEX user account has the Administrator or Data Migration operator role assigned in the management server's access control settings.
Migration runs in the background without interrupting host I/O. Monitor until `status: complete` is shown. After migration completes, verify the virtual volume now points to the new backend storage before decommissioning the old storage volumes.

## Test Metro Node Failover

Use this procedure to test that a VPLEX Metro consistency group correctly fails over to cluster-2 and resumes replication after the test, without production data loss.

```bash
# Step 1 — Suspend the consistency group on cluster-1 (simulates site failure)
VPlexcli:/> consistency-group suspend \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg-name>

# Verify cluster-2 is serving I/O — confirm hosts on cluster-2 site have full I/O access
VPlexcli:/> ll /clusters/cluster-2/consistency-groups/<cg-name>/
# Check: operational-status = ok; active-leg = cluster-2

# Step 2 — Resume the consistency group to restore Metro replication
VPlexcli:/> consistency-group resume \
    --consistency-group /clusters/cluster-1/consistency-groups/<cg-name>

# Step 3 — Verify Metro replication has resumed
VPlexcli:/> ll /distributed-storage/distributed-devices/*/health-indications/
# Expected: health-state: ok on both distributed device legs
```


```text title="Expected output"
VPlexcli:/> consistency-group suspend --consistency-group /clusters/cluster-1/consistency-groups/prod-cg-01
Task: consistency-group suspend
Status: COMPLETED
Completion time: 2024-01-15 14:32:18

VPlexcli:/> ll /clusters/cluster-2/consistency-groups/prod-cg-01/
    operational-status: ok
    active-leg: cluster-2
    transfer-size: 1048576
    policy-name: sync
    cluster-id: 4a7c9e2b-1f3d-4e8a-b2c1-9d5f8e3a6b4c
    consistency-group-id: cg-prod-01

VPlexcli:/> consistency-group resume --consistency-group /clusters/cluster-1/consistency-groups/prod-cg-01
Task: consistency-group resume
Status: COMPLETED
Completion time: 2024-01-15 14:33:45

VPlexcli:/> ll /distributed-storage/distributed-devices/*/health-indications/
    device: dev-prod-01-leg1
    health-state: ok
    device: dev-prod-01-leg2
    health-state: ok
    replication-status: in-sync
    last-sync-time: 2024-01-15 14:33:52
```

!!! warning "Common errors"
    **`consistency-group suspend: consistency group not found`** — Verify the consistency group name matches exactly and use `consistency-group list` to confirm it exists on cluster-1.
    **`consistency-group resume: operation failed — replication link down`** — Check WAN connectivity between cluster-1 and cluster-2 using `cluster connectivity-status` before resuming.
After the test, confirm all distributed devices return to `in-sync` status and that the Witness connection is healthy on both clusters before closing the change record.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Vplex — Health Checks](../health-checks/)
- [Vplex — CLI Reference](../cli-reference/)
- [Vplex — Common Issues](../../troubleshooting/common-issues/)
