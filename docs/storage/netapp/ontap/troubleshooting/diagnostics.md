---
tags:
  - netapp
  - troubleshooting
search:
  boost: 1.5
---
# ONTAP — Diagnostics

<div class="kb-summary">
ONTAP diagnostic commands: check cluster and HA health with <code>cluster show</code> and <code>storage failover show</code>, inspect aggregate and disk state with <code>storage aggregate show-status</code> and <code>storage disk show -broken</code>, check volume state and capacity with <code>volume show -state !online</code>, diagnose NFS/CIFS/iSCSI/FC protocols with per-protocol statistics, trace SnapMirror lag with <code>snapmirror show -health false</code>, analyse EMS events with <code>event log show -severity CRITICAL</code>, and generate an AutoSupport bundle before calling NetApp support.

*Applies to: ONTAP 9.x*
</div>
![ONTAP — Diagnostics](../../../../assets/storage-netapp-ontap-troubleshooting-diagnostics.svg)

```d2
direction: right

A: "ONTAP Issue" {shape: rectangle}
B: "cluster show: node health\nsystem health status show\nstorage failover show: HA state" {shape: rectangle}
C: "C" {shape: rectangle}
D: "system node show: state and uptime\ncluster ring show: cluster services\nstorage failover interconnect show" {shape: rectangle}
E: "aggr show -state !online\nstorage disk show -broken\ndisk show -raid-state recon" {shape: rectangle}
F: "volume show -state !online\nvolume show percent-used > 90%\nvolume efficiency show: dedup" {shape: rectangle}
G: "net int show -status-oper down\nnet int show -is-home false\ncluster ping-cluster: ICL health" {shape: rectangle}
H: "H" {shape: rectangle}
I: "nfs connected-client show\nvserver export-policy check-access\nstatistics start -object nfsv3" {shape: rectangle}
J: "vserver cifs domain info\nvserver cifs session show\nstatistics start -object smb2" {shape: rectangle}
K: "iscsi session show\nlun mapping show\nlun igroup show" {shape: rectangle}
L: "fcp adapter show\nfcp initiator show\nfcp topology show" {shape: rectangle}
M: "snapmirror show -health false\nsnapmirror lag show\nnet int show -role intercluster" {shape: rectangle}
N: "statistics start -object volume\nqos statistics performance show\nsystem node run sysstat" {shape: rectangle}
O: "autosupport invoke: all nodes\nOpen NetApp support case" {shape: rectangle}

A -> B
C -> D
C -> E
C -> F
C -> G
H -> I
H -> J
H -> K
H -> L
C -> M
C -> N
D -> O
E -> O
F -> O
G -> O
I -> O
J -> O
K -> O
L -> O
M -> O
N -> O
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_first_response: "Step 1 — First response" {shape: rectangle}
step_2_cluster_and_node_diagnostics: "Step 2 — Cluster and node diagnostics" {shape: rectangle}
step_3_storage_aggregate_and_disk_di: "Step 3 — Storage — aggregate and disk diagnostics" {shape: rectangle}
step_4_volume_diagnostics: "Step 4 — Volume diagnostics" {shape: rectangle}
step_5_network_diagnostics: "Step 5 — Network diagnostics" {shape: rectangle}
step_6_protocolspecific_diagnostics: "Step 6 — Protocol-specific diagnostics" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_first_response: investigate
symptom -> step_2_cluster_and_node_diagnostics: investigate
symptom -> step_3_storage_aggregate_and_disk_di: investigate
symptom -> step_4_volume_diagnostics: investigate
symptom -> step_5_network_diagnostics: investigate
symptom -> step_6_protocolspecific_diagnostics: investigate
step_1_first_response -> resolution
step_2_cluster_and_node_diagnostics -> resolution
step_3_storage_aggregate_and_disk_di -> resolution
step_4_volume_diagnostics -> resolution
step_5_network_diagnostics -> resolution
step_6_protocolspecific_diagnostics -> resolution
```

## Before you begin

- **Access:** SSH to cluster management IP or node management IP as admin; node shell (`system node run -node <node>`) for advanced per-node commands; SP/BMC console for unresponsive nodes
- **Gather first:** `cluster show` (node count and health), `system health status show` (overall health), the affected SVM and volume or protocol, and the specific symptom (error message, offline resource, slow response time)
- **Scope:** confirm whether the issue is cluster-wide (all SVMs affected), node-specific (one node or aggregate), SVM-specific (one protocol or tenant), or volume-specific — `event log show -severity CRITICAL` and `system health alert show` give the fastest cross-component view
- **AutoSupport:** always trigger an AutoSupport before calling NetApp — `system node autosupport invoke -node * -type all -message "case <SR> - <description>"`

---

## Step 1 — First response

Run these commands immediately on any ONTAP incident.

```bash
# Overall cluster health summary
cluster show
system health status show
system health alert show

# HA pair state
storage failover show

# Check for any broken disks
storage disk show -broken

# Check for any offline aggregates
storage aggregate show -state !online

# Check for any offline volumes
volume show -state !online

# Check network interfaces that are down
network interface show -status-oper down

# Recent CRITICAL and ERROR events
event log show -severity CRITICAL
event log show -severity ERROR -time-range 1h
```


```text title="Expected output"
Cluster Health Summary:
  Cluster Name: prod-cluster-01
  Cluster UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
  Cluster Serial Number: 4082368500
  Cluster Location: DC-East-02
  Cluster Contact: storage-team@company.com

Health Status: ok

Health Alerts: None

HA Pair State:
  Node: node-01
  Partner: node-02
  HA Administrative State: enabled
  HA Operational State: enabled
  Takeover Possible: true
  Giveback Possible: true

Broken Disks: None

Offline Aggregates: None

Offline Volumes: None

Network Interfaces Down: None

Recent CRITICAL Events (last 24h):
  Time: 2024-01-15 14:32:18 UTC
  Severity: CRITICAL
  Message: Disk shelf 1.1 lost connection
  Node: node-02

Recent ERROR Events (last 1h):
  Time: 2024-01-15 16:45:22 UTC
  Severity: ERROR
  Message: NTP synchronization lost
  Node: node-01
  Time: 2024-01-15 16:52:10 UTC
  Severity: ERROR
  Message: Aggregate aggr_ssd_01 space usage at 92%
  Node: node-02
```

!!! warning "Common errors"
    **`Error: command not found: cluster show`** — Ensure you are logged into the ONTAP cluster CLI (via SSH to cluster management IP) rather than the local node shell.
    **`Error: No such file or directory`** — Verify the ONTAP version supports the `system health` commands; upgrade or use `storage show status` on older releases.
    **`Error: Invalid query: state !online`** — Use the correct ONTAP query syntax `state !=online` (double equals with exclamation) instead of `!online`.
If any of these commands return unexpected results, follow the relevant subsystem diagnostic section below.

---

## Step 2 — Cluster and node diagnostics

```bash
# Cluster node count and status
cluster show
# All nodes should show: health=true, eligibility=true

# Detailed node status including uptime
system node show
system node show -fields node,health,state,uptime,model,serial-number

# Node-level hardware configuration (drops to node shell)
system node run -node <node_name> sysconfig -a

# Node environment (temperature, fans, power)
system node run -node <node_name> environment status

# Node-level system resource utilisation
system node run -node <node_name> sysstat -c 5 -x 2

# Check the cluster ring (internal cluster services)
cluster ring show

# Epsilon node (tiebreaker in split-brain scenarios)
cluster show -fields node,epsilon
```


```text title="Expected output"
cluster show
Node                  Health  Eligibility
--------------------- ------- -----------
ontap-node-01         true    true
ontap-node-02         true    true

system node show -fields node,health,state,uptime,model,serial-number
Node       Health State   Uptime            Model         Serial-Number
---------- ------ ------- ----------------- ------------- ---------------
ontap-node-01 true   up      127 days 14:32:18 FAS2720      701911000123
ontap-node-02 true   up      89 days 03:15:44  FAS2720      701911000456

system node run -node ontap-node-01 sysconfig -a
NetApp Release 9.12.1: Tue Jan 10 14:22:33 UTC 2023
System Serial Number: 701911000123
System Model name: FAS2720
Memory: 128GB
...

system node run -node ontap-node-01 environment status
System Environmental Status:
Ambient Temperature: 22°C
CPU0 Temp: 48°C  CPU1 Temp: 51°C
Fan1 Speed: 2400 RPM  Fan2 Speed: 2350 RPM
PSU1 Status: OK  PSU2 Status: OK

cluster ring show
Node      UFS Cluster VLDB VifMgr Bcomd DNS
--------- --- ------- ---- ------ ----- ---
ontap-node-01: master master master master master master
ontap-node-02: replica replica replica replica replica replica

cluster show -fields node,epsilon
Node          Epsilon
------------- -------
ontap-node-01 false
ontap-node-02 true
```

!!! warning "Common errors"
    **`Error: command failed: permission denied`** — Ensure your user account has cluster admin privileges using `security login show`.
    **`Error: node not found: <node_name>`** — Verify the exact node name with `cluster show` and use the correct hostname in the `system node run -node` command.
### Storage failover diagnostics

```bash
# Detailed HA failover state
storage failover show -fields node,enabled,state,partner,takeover-enabled,giveback-status

# Check interconnect link status between HA partners
storage failover interconnect show

# Test cluster interconnect ping (HA heartbeat)
cluster ping-cluster -node <node_name>

# Show failover history (recent takeovers and givebacks)
storage failover history show -node <node_name>
```


```text title="Expected output"
Node                  Enabled  State    Partner              Takeover-Enabled  Giveback-Status
--------------------- -------- -------- -------------------- ------------------- ---------------
node-01               true     ready    node-02              true                  not_attempted
node-02               true     ready    node-01              true                  not_attempted

Interconnect1 Link Status: up
Interconnect2 Link Status: up
Node node-01 to Node node-02: latency 2ms

Cluster Ping to node-01: 4 packets transmitted, 4 received, 0% packet loss, min/avg/max = 1.2/1.8/2.4 ms
Cluster Ping to node-02: 4 packets transmitted, 4 received, 0% packet loss, min/avg/max = 1.1/1.7/2.3 ms

                                    Takeover
Node          Date/Time             Reason
------------- --------------------- -------
node-01       02/14 14:32:15 +00:00  user_initiated
node-01       02/10 09:18:42 +00:00  disk_shelf_failure
node-02       02/08 11:05:33 +00:00  user_initiated
```

!!! warning "Common errors"
    **`Error: cluster ping-cluster: node "<node_name>" not found`** — Replace `<node_name>` with an actual node name from your cluster (e.g., `node-01`).
    **`Interconnect1 Link Status: down`** — Check physical cabling between HA partners and verify interconnect ports are enabled with `storage failover interconnect show -detail`.
    **`storage failover show: This command requires cluster administrative privileges`** — Run the command with cluster admin credentials or use `set -privilege advanced` first.
HA state interpretation:

| State | Meaning | Action |
|---|---|---|
| `Connected, Not in takeover` | Normal — HA active | None |
| `Connected, Waiting for Giveback` | Partner was taken over; partner is recovered and waiting | Run `storage failover giveback -ofnode <node>` |
| `In Takeover` | Active takeover in progress or complete | Wait for completion or giveback |
| `Disconnected` | HA interconnect link down | Check physical link; investigate immediately |
| `false` (enabled) | HA disabled | Run `storage failover modify -node <node> -enabled true` after investigation |

---

## Step 3 — Storage — aggregate and disk diagnostics

```bash
# Aggregate health — show any not online
storage aggregate show -state !online
storage aggregate show -fields aggr-name,node,state,raid-status,percent-used

# Aggregate RAID status detail
storage aggregate show-status -aggregate <aggr_name>
storage aggregate show-raidtree -aggregate <aggr_name>

# Disk health
storage disk show -broken -fields disk,container-type,bay,shelf,node,serial-number
storage disk show -container-type spare        # confirm spares available for rebuild
storage disk show -raid-state reconstructing   # active RAID reconstruction

# All disks with firmware revision and location
storage disk show -fields disk,bay,shelf,node,firmware-revision,rpm,size,disk-type

# Disk shelf status
storage shelf show
storage shelf show -detail
```


```text title="Expected output"
cluster1::> storage aggregate show -state !online
(no entries returned)

cluster1::> storage aggregate show -fields aggr-name,node,state,raid-status,percent-used
aggr-name   node      state  raid-status  percent-used
----------- --------- ------ ------------ ------------
aggr0       node-01   online raid_dp      78
aggr1       node-01   online raid_dp      62
aggr2       node-02   online raid_dp      85
aggr3       node-02   online raid_dp      71

cluster1::> storage aggregate show-status -aggregate aggr1
           Aggregate: aggr1
           Node: node-01
           Status: online
           RAID status: raid_dp
           Plex /aggr1/plex0: online, normal
             RAID group /aggr1/plex0/rg0: online
               RAID Disk Device          HA  SHELF BAY SERIAL NUMBER
               ---- ------ ------------- --- ----- --- ---------------
               dparity 1.0.0  SES Device  0a  0     0   S5K1N0JH
               parity  1.0.1  SES Device  0a  0     1   S5K1N0JK
               data    1.0.2  SES Device  0a  0     2   S5K1N0JL
               data    1.0.3  SES Device  0a  0     3   S5K1N0JM

cluster1::> storage disk show -broken -fields disk,container-type,bay,shelf,node,serial-number
(no entries returned)

cluster1::> storage disk show -container-type spare
Disk     Container Type  Shelf  Bay  Node     Serial Number
-------- --------------- ------ --- --------- ---------------
1.0.10   spare           0      10  node-01   S5K1N0JN
1.0.11   spare           0      11  node-01   S5K1N0JO
2.0.10   spare           0      10  node-02   S5K1N0JP
2.0.11   spare           0      11  node-02   S5K1N0JQ

cluster1::> storage disk show -raid-state reconstructing
(no entries returned)

cluster1::> storage disk show -fields disk,bay,shelf,node,firmware-revision,rpm,size,disk-type
disk     bay shelf node    firmware-revision rpm  size   disk-type
-------- --- ----- ------- ------------------- ---- ------ ---------
1.0.0    0   0     node-01 NA02              7200 1.2TB  SAS
1.0.1    1   0     node-01 NA02              7200 1.2TB  SAS
1.0.2    2   0     node-01 NA02              7200 1.2TB  SAS
...

cluster1::> storage shelf show
Shelf  Shelf Name  Serial Number  Status
------ ----------- -------------- --------
0      DS224C      SHF2143000123  online
1      DS224C      SHF2143000124  online

cluster1::> storage shelf show -detail
Shelf  Shelf Name  Serial Number  Status  Firmware Version  Module A  Module
```
### RAID reconstruction monitoring

When a disk fails and a spare is available, ONTAP automatically starts RAID reconstruction. Monitor progress:

```bash
# Show reconstruction status
storage disk show -raid-state reconstructing

# Show aggregate state during reconstruction
storage aggregate show -aggregate <aggr_name> -fields state,raid-status

# Watch reconstruction progress (check every 60 seconds)
storage aggregate show-status -aggregate <aggr_name>
# Look for "Parity reconstruction" or "Data reconstruction" with a percentage
```


```text title="Expected output"
Disk        Container   HA  Shelf Bay Chan   State    Rebuild Elapsed
----------  ----------- --- ----- --- ------ -------- -------
1.0.0       aggr0       A   0     0   A      Reconstructing  12%
1.0.1       aggr0       A   0     1   A      Reconstructing  12%
1.0.2       aggr1       B   0     2   B      Reconstructing   8%

Aggregate State       RAID Status
--------- ----------- ----------------
aggr0     online      raid_dp, parity reconstruction 45% complete
aggr1     degraded    raid_dp, parity reconstruction 8% complete

Status of aggregate "aggr0":
  State: online
  Parity reconstruction: 45% complete, 2 hours 15 minutes remaining
  Data reconstruction: not running
  Disk count: 12 (RAID-DP)
  Spare disks: 1
```

!!! warning "Common errors"
    **`Error: command not found: storage`** — Run this command from the ONTAP CLI (SSH to the cluster management IP), not from a Linux shell.
    **`Error: There is no entry in the Ident database for aggregate "<aggr_name>"`** — Replace `<aggr_name>` with an actual aggregate name; verify with `storage aggregate show`.
Typical reconstruction times:
- NVMe SSD: hours to a day for large capacities
- SAS HDD: 6–24 hours per TB depending on disk RPM and aggregate workload
- SATA HDD: 12–48+ hours per TB

---

## Step 4 — Volume diagnostics

```bash
# Volume state — identify offline or restricted volumes
volume show -state !online
volume show -state offline
volume show -state restricted

# Volume capacity — identify full or near-full volumes
volume show -fields vserver,volume,size,used,available,percent-used | sort -k5 -rn

# Autosize configuration
volume show -fields vserver,volume,autosize-mode,max-autosize,grow-threshold-percent

# Space guarantee and snapshot reserve
volume show -fields volume,space-guarantee,snapshot-percent,percent-snapshot-space

# Volume efficiency status (dedup / compression)
volume efficiency show -vserver <svm>

# FlexClone volumes and their parent
volume clone show
volume clone show -fields flexclone,parent-volume,parent-snapshot

# Volume move status
volume move show
```


```text title="Expected output"
Vserver     Volume       State      
----------- ------------ ---------- 
svm-prod    vol_archive  offline    
svm-dr      vol_backup   restricted 

Vserver     Volume       Size       Used       Available  Percent-Used
----------- ------------ ---------- ---------- ---------- ------------
svm-prod    vol_data01   2TB        1.8TB      200GB      90%
svm-prod    vol_logs     500GB      475GB      25GB       95%
svm-dr      vol_mirror   1.5TB      1.2TB      300GB      80%
svm-test    vol_temp     750GB      600GB      150GB      80%

Vserver     Volume       Autosize-Mode Max-Autosize Grow-Threshold-Percent
----------- ------------ ------------- ------------ -----------------------
svm-prod    vol_data01   grow          2.5TB        85%
svm-prod    vol_logs     off           -            -
svm-dr      vol_mirror   grow_shrink   2TB          80%

Volume       Space-Guarantee Snapshot-Percent Percent-Snapshot-Space
------------ --------------- ----------------- -----------------------
vol_data01   volume          5%                8.2%
vol_logs     none            10%               12.1%
vol_mirror   volume          5%                6.5%

Vserver     Volume       State      Efficiency-Op-Status
----------- ------------ ---------- --------------------
svm-prod    vol_data01   enabled    Idle
svm-prod    vol_logs     enabled    Running
svm-dr      vol_mirror   disabled   -

FlexClone                Parent-Volume       Parent-Snapshot
------------------------ -------------------- --------------------
vol_clone_test01         vol_data01           snap_20240115_0200
vol_clone_backup02       vol_mirror           snap_daily_20240114

Volume Move                      Vserver     State      Progress
-------------------------------- ----------- ---------- ----------
vol_data01_move                  svm-prod    completed  100%
```

!!! warning "Common errors"
    **`Error: command failed: No matching volumes found`** — Verify the volume name exists and the SVM context is correct using `vserver context`.
    **`Error: Invalid field name "percent-used"`** — Use the correct field name `percent-used` (with hyphen) or check ONTAP version compatibility with `system show -instance`.
---

## Step 5 — Network diagnostics

```bash
# LIF status — identify any down interfaces
network interface show
network interface show -status-oper down
network interface show -fields lif,vserver,address,home-node,curr-node,home-port,curr-port,status-oper

# LIFs not on home port (migrated due to failover or maintenance)
network interface show -is-home false

# Port status — identify failed or degraded ports
network port show
network port show -fields node,port,health-status,link-status,speed,mtu

# Interface group (bond/LACP) status
network port ifgrp show

# VLAN configuration
network port vlan show

# Routing table
network route show

# Test connectivity from a specific LIF
network ping -lif <lif_name> -vserver <svm> -destination <target_ip>

# Check cluster interconnect connectivity
cluster ping-cluster -node <node_name>

# Trace route from a LIF (ONTAP 9.8+)
network traceroute -lif <lif_name> -vserver <svm> -destination <ip>

# DNS resolution check
vserver services name-service dns check -vserver <svm>

# LDAP connectivity check
vserver services name-service ldap check -vserver <svm>
```


```text title="Expected output"
cluster1::> network interface show
            Logical    Status     Network            Current       Current Is
Vserver     Interface  Admin/Oper Address/Mask       Node          Port    Home
----------- ---------- ---------- ------------------ ------------- ------- ----
cluster1    cluster_intercluster
                       up/up      169.254.10.1/24    node-1        e0a     true
cluster1    cluster_intercluster
                       up/up      169.254.10.2/24    node-2        e0a     true
svm-prod    data_lif_1 up/up      192.168.1.50/24    node-1        e0c     true
svm-prod    data_lif_2 up/up      192.168.1.51/24    node-2        e0c     true
svm-prod    mgmt_lif   up/down    10.0.0.100/24      node-1        e0m     true

cluster1::> network interface show -status-oper down
            Logical    Status     Network            Current       Current Is
Vserver     Interface  Admin/Oper Address/Mask       Node          Port    Home
----------- ---------- ---------- ------------------ ------------- ------- ----
svm-prod    mgmt_lif   up/down    10.0.0.100/24      node-1        e0m     true

cluster1::> network interface show -is-home false
            Logical    Status     Network            Current       Current Is
Vserver     Interface  Admin/Oper Address/Mask       Node          Port    Home
----------- ---------- ---------- ------------------ ------------- ------- ----
svm-prod    data_lif_2 up/up      192.168.1.51/24    node-1        e0d     false

cluster1::> network port show
Node      Port Link MTU  Admin Status Health Status
--------- ---- ---- ---- ----- ------ ---------------
node-1    e0a  up   1500 up    up     healthy
node-1    e0c  up   1500 up    up     healthy
node-1    e0d  up   1500 up    up     healthy
node-1    e0m  up   1500 up    down   degraded
node-2    e0a  up   1500 up    up     healthy
node-2    e0c  up   1500 up    up     healthy

cluster1::> network port ifgrp show
Node      IfGrp Ports
--------- ----- -------
node-1    a0a   e0c,e0d
node-2    a0a   e0c,e0d

cluster1::> network route show
Vserver             Destination     Gateway         Metric
------------------- --------------- --------------- ------
svm-prod            0.0.0.0/0       192.168.1.1     20
svm-prod            192.168.1.0/24  0.0.0.0         0

cluster1::> network ping -lif data_lif_1 -vserver svm-prod -destination 192.168.1.200
PING 192.168.1.200 (192.168.1.200): 56 data bytes
64 bytes from 192.168.1.200: ic
```
### MTU / Jumbo frame verification

```bash
# Check ONTAP port MTU settings
network port show -fields node,port,mtu

# Ping with large payload to test jumbo frames end-to-end
network ping -lif <lif_name> -vserver <svm> -destination <target_ip> -packet-size 8972
# 8972 bytes = 9000 byte jumbo frame minus IP/ICMP headers
```


```text title="Expected output"
Node       Port       MTU
---------- ---------- -----
node-01    e0a        1500
node-01    e0b        9000
node-01    e0c        9000
node-02    e0a        1500
node-02    e0b        9000
node-02    e0c        9000
...

PING 192.168.10.50 from 192.168.1.100 (data0): 8972 bytes of data in 4 ICMP Echo Request packets
8972 bytes from 192.168.10.50: icmp_seq=0. time=2.341 ms.
8972 bytes from 192.168.10.50: icmp_seq=1. time=2.156 ms.
8972 bytes from 192.168.10.50: icmp_seq=2. time=2.289 ms.
8972 bytes from 192.168.10.50: icmp_seq=3. time=2.412 ms.
```

!!! warning "Common errors"
    **`Error: "lif <lif_name>" does not exist`** — Verify the LIF name with `network interface show` and use the correct vserver context.
    **`PING: sendto: Message too long`** — Confirm the physical port and all intermediate switches support 9000 MTU with `network port show -fields mtu` and adjust `-packet-size` downward if needed.
    **`Error: Invalid vserver <svm>`** — List available SVMs with `vserver show` and ensure you are in the correct cluster context.
---

## Step 6 — Protocol-specific diagnostics

### NFS diagnostics

```bash
# NFS service status per SVM
vserver nfs show -vserver <svm>

# Connected NFS clients
nfs connected-client show -vserver <svm>

# NFS export policy rules
vserver export-policy rule show -vserver <svm> -policyname <policy>

# Test client IP against export policy
vserver export-policy check-access -vserver <svm> -volume <vol> -client-ip <ip> \
  -authentication-method sys -protocol nfs3

# NFS statistics (read/write ops and latency)
statistics start -object nfsv3 -sample-id nfs-diag
# wait 30 seconds
statistics stop -sample-id nfs-diag
statistics show -sample-id nfs-diag
```


```text title="Expected output"
Vserver       Enabled
------------- -------
svm-prod-01   true

Connected Clients for Vserver "svm-prod-01":
Vserver IP Address    Client IP      OpenFiles Protocol Version
---------- ----------- -------------- --------- -------- -------
svm-prod-01 192.168.1.50 10.45.22.18    12        nfs      3
svm-prod-01 192.168.1.50 10.45.22.19    8         nfs      3
svm-prod-01 192.168.1.50 10.45.23.101   156       nfs      3

Policy Name: default
Vserver     Policy Name Rule Index Access Protocol RW Rule Superuser
----------- ----------- ---------- ------ -------- -------- ---------
svm-prod-01 default     1          allow  nfs      any      sys
svm-prod-01 default     2          deny   nfs      none     none

Policy Name: default
Vserver     Volume Client IP      Authentication Protocol Allow
----------- ------ -------------- -------------- -------- -----
svm-prod-01 vol1   10.45.22.18    sys            nfs3     true

Sample-id: nfs-diag
Object: nfsv3
Timestamp: 1704067234
nfsv3_read_ops: 45821
nfsv3_write_ops: 12456
nfsv3_read_latency: 2.3ms
nfsv3_write_latency: 1.8ms
```

!!! warning "Common errors"
    **`Error: "svm-prod-01" is not a valid Vserver name`** — Verify the SVM name exists with `vserver show` and use the exact name from the Vserver column.
    **`Error: policy "custom-policy" does not exist`** — Confirm the export policy name with `vserver export-policy show -vserver <svm>` before running the rule show command.
    **`Error: command is ambiguous`** — Use the full command path `vserver nfs show` instead of abbreviated forms, and ensure all required parameters like `-vserver` are explicitly specified.
### CIFS/SMB diagnostics

```bash
# CIFS server and domain status
vserver cifs show -vserver <svm>
vserver cifs domain info -vserver <svm>

# CIFS domain controller connectivity
vserver cifs domain discovered-servers show -vserver <svm>

# Active CIFS sessions
vserver cifs session show -vserver <svm>
vserver cifs session show -vserver <svm> -fields node,connection-count,open-files

# Open files on an SVM
vserver cifs session file show -vserver <svm>

# CIFS SMB statistics
statistics start -object smb2 -sample-id smb2-diag
# wait 30 seconds
statistics stop -sample-id smb2-diag
statistics show -sample-id smb2-diag
```


```text title="Expected output"
Vserver: svm-prod-01
CIFS Server Name: ONTAP-SVR-01
Enabled: true
NetBIOS Aliases: 
Comment: Production CIFS Server
Domain: corp.example.com
Workgroup: 
Authentication Style: domain
Encryption Required: false

Vserver: svm-prod-01
Domain Name: corp.example.com
Domain FQDN: corp.example.com
Fully Qualified Domain Name: ontap-svr-01.corp.example.com
Forest FQDN: corp.example.com
Organizational Unit: CN=Computers,DC=corp,DC=example,DC=com

Vserver: svm-prod-01
Domain: corp.example.com
Preferred Server: dc-01.corp.example.com (192.168.1.50)
Discovered Servers: dc-01.corp.example.com (192.168.1.50)
                    dc-02.corp.example.com (192.168.1.51)

Vserver: svm-prod-01
Node: node-01
Connection Count: 12
Open Files: 47

Vserver: svm-prod-01
Node: node-02
Connection Count: 8
Open Files: 23

Vserver: svm-prod-01
Node: node-01
Connection-ID: 4294967295
File-ID: 0x00000001
File-Name: /shares/data/report.xlsx
Open-Mode: read
...

Sample ID: smb2-diag
Object: smb2
Elapsed Time (secs): 30.2
smb2_ops: 15847
smb2_read_ops: 4521
smb2_write_ops: 3892
smb2_tree_connect_ops: 156
smb2_session_setup_ops: 12
```

!!! warning "Common errors"
    **`Error: "Vserver <svm> not found"`** — Verify the SVM name is correct using `vserver show` and ensure you are connected to the correct cluster.
    **`Error: "Domain <domain> not reachable"`** — Check network connectivity to domain controllers and verify DNS resolution with `network name-service dns show`.
    **`Error: "Statistics object smb2 not found"`** — Ensure SMB2 protocol is enabled on the SVM with `vserver cifs show -vserver <svm>` and confirm the sample-id is unique.
### iSCSI diagnostics

```bash
# iSCSI service status
iscsi show -vserver <svm>

# iSCSI sessions (connected initiators)
iscsi session show -vserver <svm>
iscsi session show -vserver <svm> -fields initiator-name,lif,tpgroup,connection-count

# iSCSI target portal groups
iscsi tpgroup show -vserver <svm>

# LUN mapping — confirm host can see LUNs
lun show -vserver <svm>
lun mapping show -vserver <svm>
lun mapping show -vserver <svm> -igroup <igroup_name>

# igroup membership
lun igroup show -vserver <svm>
```


```text title="Expected output"
Vserver: svm-prod-01
  iSCSI Status: up
  Target Alias: svm-prod-01.example.com
  Target Name: iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6

Vserver: svm-prod-01
Initiator Name: iqn.1991-05.com.emc:01.005056b34d67
LIF: 10.20.30.45:3260
TPGROUP: tpg_1
Connection Count: 2

Vserver: svm-prod-01
Target Portal Group: tpg_1
Portals: 10.20.30.45:3260, 10.20.30.46:3260
Status: up

Vserver: svm-prod-01
  LUN Path: /vol/data_vol/lun_prod_01
  Size: 500GB
  State: online
  LUN Path: /vol/data_vol/lun_prod_02
  Size: 250GB
  State: online

Vserver: svm-prod-01
  LUN: /vol/data_vol/lun_prod_01
  igroup: ig_esx_cluster_01
  LUN ID: 0

Vserver: svm-prod-01
  igroup: ig_esx_cluster_01
  Protocol: iscsi
  Initiators: iqn.1991-05.com.emc:01.005056b34d67, iqn.1991-05.com.emc:01.005056b34d68
```

!!! warning "Common errors"
    **`Error: command failed: Vserver "svm-prod-01" does not exist.`** — Verify the SVM name with `vserver show` and ensure you are connected to the correct cluster.
    **`Error: No iSCSI sessions found for Vserver "svm-prod-01".`** — Confirm iSCSI service is running with `iscsi show -vserver <svm>` and that initiators have successfully logged in.
### FC / FCoE diagnostics

```bash
# FC service status
fcp show -vserver <svm>

# FC adapter status (physical ports)
fcp adapter show -fields node,adapter,state,speed,fabric-established

# FC initiators (logged-in hosts)
fcp initiator show -vserver <svm>

# FC interface status (FC LIFs)
fcp interface show -vserver <svm>

# FC topology information
fcp topology show
```


```text title="Expected output"
cluster1::> fcp show -vserver svm_prod
Vserver: svm_prod
  FCP Admin Status: up
  FCP Operational Status: up

cluster1::> fcp adapter show -fields node,adapter,state,speed,fabric-established
node     adapter state  speed fabric-established
-------- ------- ------ ----- ------------------
node-1   0a      online 16Gb  true
node-1   0b      online 16Gb  true
node-2   0a      online 16Gb  true
node-2   0b      online 16Gb  true

cluster1::> fcp initiator show -vserver svm_prod
Vserver     Initiator WWPN           Logged In
----------- ----------------------- ----------
svm_prod    50:00:14:40:5a:2b:c1:01 true
svm_prod    50:00:14:40:5a:2b:c1:02 true
svm_prod    50:00:14:40:5a:2b:c2:01 true

cluster1::> fcp interface show -vserver svm_prod
Vserver   Interface     Status  Node   Adapter
--------- ------------- ------- ------ -------
svm_prod  fc_lif_01     up      node-1 0a
svm_prod  fc_lif_02     up      node-1 0b
svm_prod  fc_lif_03     up      node-2 0a
svm_prod  fc_lif_04     up      node-2 0b

cluster1::> fcp topology show
Node: node-1
  Adapter 0a: WWNN 50:0a:09:80:12:34:56:78, WWPN 50:0a:09:81:12:34:56:78
  Adapter 0b: WWNN 50:0a:09:80:12:34:56:79, WWPN 50:0a:09:81:12:34:56:79
Node: node-2
  Adapter 0a: WWNN 50:0a:09:80:12:34:56:7a, WWPN 50:0a:09:81:12:34:56:7a
  Adapter 0b: WWNN 50:0a:09:80:12:34:56:7b, WWPN 50:0a:09:81:12:34:56:7b
```

!!! warning "Common errors"
    **`Invalid vserver name "<svm>"`** — Replace `<svm>` with the actual SVM name (e.g., `svm_prod`) or use `vserver show` to list available SVMs.
    **`FCP service is not enabled on Vserver <svm>`** — Enable FCP on the SVM using `vserver fcp create -vserver <svm>` and ensure FC licenses are installed.
    **`fabric-established: false`** — Verify FC switch connectivity, check switch zoning configuration, and confirm physical cable connections to the FC adapters.
---

## Step 7 — SnapMirror diagnostics

```bash
# All relationships with health and lag
snapmirror show -fields source-path,destination-path,lag-time,healthy,state,last-transfer-end-timestamp

# Only unhealthy relationships
snapmirror show -health false

# Transfer progress (active transfers)
snapmirror show -transfer-progress

# Transfer history for a specific relationship
snapmirror history show -destination-path <dest_svm>:<dest_vol>

# Lag for all relationships (compact view)
snapmirror lag show

# SnapMirror network statistics (bandwidth usage)
statistics start -object snapmirror -sample-id sm-diag
# wait 30 seconds
statistics stop -sample-id sm-diag
statistics show -sample-id sm-diag

# Check intercluster LIF status (required for cross-cluster SnapMirror)
network interface show -role intercluster
```


```text title="Expected output"
Source Path                Destination Path           Lag Time State    Healthy Last Transfer End Timestamp
--------------------------- --------------------------- -------- -------- ------- --------------------------
svm1:vol_data              svm2:vol_data_mirror       00:15:32 snapmirrored true    2024-01-15 14:32:18 +00:00
svm1:vol_logs              svm2:vol_logs_mirror       02:45:18 snapmirrored true    2024-01-15 12:02:45 +00:00
svm3:vol_archive           svm4:vol_archive_dr        06:22:41 snapmirrored false   2024-01-15 08:15:22 +00:00
svm5:vol_temp              svm6:vol_temp_backup       00:08:09 snapmirrored true    2024-01-15 14:39:51 +00:00

Source Path                Destination Path           State      Healthy
--------------------------- --------------------------- ---------- -------
svm3:vol_archive           svm4:vol_archive_dr        broken-off false

Source Path                Destination Path           Progress   Bytes Transferred
--------------------------- --------------------------- ---------- ------------------
svm1:vol_data              svm2:vol_data_mirror       87%        2.4 TB

Destination Path           Number of Transfers  Last Transfer Size  Last Transfer Duration
--------------------------- -------------------- -------------------- ----------------------
svm2:vol_data_mirror       1247                 1.8 TB               00:42:15
svm2:vol_logs_mirror       892                  542 GB               00:28:33

Source Path                Destination Path           Lag Time
--------------------------- --------------------------- --------
svm1:vol_data              svm2:vol_data_mirror       00:15:32
svm1:vol_logs              svm2:vol_logs_mirror       02:45:18
svm3:vol_archive           svm4:vol_archive_dr        06:22:41
svm5:vol_temp              svm6:vol_temp_backup       00:08:09

Sample-id: sm-diag
Object: snapmirror
Instance: svm1:vol_data->svm2:vol_data_mirror
Counter                                                     Value
--------------------------------------------------------------- --------
snapmirror_network_recv_data_rate                           125.4 MB/s
snapmirror_network_send_data_rate                           128.7 MB/s
snapmirror_network_total_bytes_sent                         847.2 GB
snapmirror_network_total_bytes_recv                         851.6 GB

Vserver     Interface      Role         Status  Data Protocol
----------- -------------- ------------ ------- ----------------
cluster1    ic_lif_01      intercluster up      tcp
cluster1    ic_lif_02      intercluster up      tcp
cluster2    ic_lif_01      intercluster up      tcp
cluster2    ic_lif_02      intercluster up      tcp
```

!!! warning "Common errors"
    **`Error: command failed: No SnapMirror relationships found.`** — Verify relationships exist with `snapmirror show` and confirm source and destination SVMs are initialized.
    **`Error: command failed: Intercluster L
---

## Step 8 — Performance diagnostics

ONTAP statistics require a start/stop sample cycle. Let it run for at least 30 seconds before stopping to get meaningful data.

```bash
# Volume-level performance statistics
statistics start -object volume -sample-id vol-perf
# wait 30–60 seconds
statistics stop -sample-id vol-perf
statistics show -sample-id vol-perf

# Filter for key latency metrics (microseconds)
statistics show -sample-id vol-perf | grep -E "total_latency|read_latency|write_latency"

# Filter for IOPS
statistics show -sample-id vol-perf | grep -E "total_ops|read_ops|write_ops"

# Volume-specific statistics (single volume)
statistics show -object volume -instance <vol_name> -counter read_latency,write_latency,total_ops

# QoS workload statistics (shows throttling and floor/ceiling hit rates)
qos statistics performance show
qos statistics workload performance show

# Node-level CPU and disk utilisation (node shell)
system node run -node <node_name> sysstat -c 10 -x 2
```


```text title="Expected output"
cluster1::> statistics start -object volume -sample-id vol-perf
cluster1::> statistics stop -sample-id vol-perf
cluster1::> statistics show -sample-id vol-perf
Object: volume
Instance: vol_data_01
Counter                                                     Value
------------------------------------------------------------ --------------------------------
total_latency                                               4521 us
read_latency                                                3847 us
write_latency                                               5203 us
total_ops                                                   18456
read_ops                                                    12340
write_ops                                                   6116

cluster1::> qos statistics performance show
Workload                          IOPS      Throughput    Latency
-----------                       ----      ----------    -------
vol_data_01                       1245      487 MB/s      4.2 ms
vol_backup_02                     342       156 MB/s      8.7 ms
vol_logs_03                       5621      2.1 GB/s      1.8 ms

cluster1::> system node run -node node-01 sysstat -c 10 -x 2
    CPU    User    Nice  System    Idle     INTR    CTXT
     10      23       0      18      59       45      892
     10      25       1      17      57       48      921
```

!!! warning "Common errors"
    **`Error: sample-id "vol-perf" already exists`** — Use a unique sample-id or delete the existing one with `statistics delete -sample-id vol-perf` before restarting.
    **`Error: object "volume" is not a valid statistics object`** — Verify the object name is correct; use `statistics catalog` to list available objects like `volume_ops` or `vserver_ops`.
    **`Error: No such file or directory`** — Ensure you are in the cluster shell (not node shell) for `statistics` commands; use `exit` to return to cluster prompt if needed.
### Latency interpretation

| Metric | Acceptable | Warning | Critical |
|---|---|---|---|
| NFS read latency | < 2 ms | 2–10 ms | > 10 ms |
| NFS write latency | < 3 ms | 3–10 ms | > 10 ms |
| iSCSI/FC read latency | < 1 ms | 1–5 ms | > 5 ms |
| iSCSI/FC write latency | < 1 ms | 1–5 ms | > 5 ms |
| Volume total_latency | < 2 ms | 2–10 ms | > 10 ms |

High latency root causes to investigate:
- Aggregate over 80% used (WAFL metadata overhead)
- QoS ceiling throttling the workload: `qos statistics performance show`
- Network MTU mismatch (NFS/NVMe/TCP): check jumbo frames end-to-end
- SnapMirror or efficiency jobs running during production peak hours

---

## Step 9 — EMS event log analysis

```bash
# Recent events by severity
event log show -severity EMERGENCY
event log show -severity ALERT
event log show -severity CRITICAL
event log show -severity ERROR

# Events in the last hour
event log show -severity ERROR -time-range 1h

# Events from a specific node
event log show -node <node_name> -severity ERROR

# Search for a specific message name (pattern)
event log show -messagename wafl.vol.full
event log show -messagename raid.*
event log show -messagename disk.*

# Events related to SnapMirror
event log show -messagename snapmirror.*

# Show event details including description
event log show -messagename <message_name> -detail
```


```text title="Expected output"
cluster1::> event log show -severity EMERGENCY
There are no entries matching your query.

cluster1::> event log show -severity ALERT
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-15 14:32:18 node-01          ALERT         ntp.sync.lost
 2024-01-15 09:15:42 node-02          ALERT         cifs.vserver.auth.failed

cluster1::> event log show -severity CRITICAL
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-14 22:47:05 node-01          CRITICAL      wafl.vol.full
 2024-01-14 18:23:19 node-02          CRITICAL      raid.disk.failed

cluster1::> event log show -severity ERROR
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-15 16:52:33 node-01          ERROR         snapmirror.xfer.failed
 2024-01-15 15:18:47 node-02          ERROR         disk.shelf.offline
 2024-01-15 14:05:22 node-01          ERROR         nfs.export.denied
 ...

cluster1::> event log show -severity ERROR -time-range 1h
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-15 16:52:33 node-01          ERROR         snapmirror.xfer.failed

cluster1::> event log show -node node-01 -severity ERROR
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-15 16:52:33 node-01          ERROR         snapmirror.xfer.failed
 2024-01-15 14:05:22 node-01          ERROR         nfs.export.denied

cluster1::> event log show -messagename wafl.vol.full
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-14 22:47:05 node-01          CRITICAL      wafl.vol.full

cluster1::> event log show -messagename raid.*
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-14 18:23:19 node-02          CRITICAL      raid.disk.failed
 2024-01-13 10:15:44 node-01          ERROR         raid.rebuild.started

cluster1::> event log show -messagename disk.*
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-15 15:18:47 node-02          ERROR         disk.shelf.offline
 2024-01-14 18:23:19 node-02          CRITICAL      raid.disk.failed

cluster1::> event log show -messagename snapmirror.*
 Time                Node             Severity      Event
 ------------------- ---------------- ------------- ---------------------------
 2024-01-15 16:52:33 node-01          ERROR         snapmirror.xfer.failed
 2024-01-
```
Common EMS messages and their meaning:

| EMS Message | Severity | Meaning |
|---|---|---|
| `wafl.vol.full` | ERROR | Volume is 100% used; writes will fail |
| `wafl.vol.autoSize.fail` | ERROR | Autogrow attempted but aggregate is full |
| `raid.config.phy.degraded` | ERROR | RAID group degraded due to disk failure |
| `diskown.diskNotFound` | ERROR | A disk is missing from an aggregate |
| `callhome.disk.failure` | ALERT | Disk failure detected; AutoSupport sent |
| `snapmirror.dest.lag.warn` | WARNING | SnapMirror lag exceeds warning threshold |
| `ha.takeover.occurred` | NOTICE | HA takeover has happened |
| `LIF.compatibility.change` | NOTICE | LIF has been migrated to a different port |

---

## Step 10 — Coredump and panic analysis

```bash
# List core dump files
system node coredump show

# Show core dump details
system node coredump show -node <node_name> -fields state,type,panic-string,uptime-before-crash

# Delete processed core dumps (after AutoSupport upload)
system node coredump delete -node <node_name> -corefile <filename>

# Check Service Processor logs for pre-panic system events
system service-processor log show -node <node_name>
system service-processor log show -node <node_name> -num-rows 100
```


```text title="Expected output"
Node: cluster-node-01
Coredump Count: 2
Coredump Filename: vmcore.0
Coredump State: Saved
Coredump Type: Kernel
Coredump Size: 2.1GB
Coredump Timestamp: Mon Jan 15 09:23:47 UTC 2024

Node: cluster-node-02
Coredump Count: 1
Coredump Filename: vmcore.1
Coredump State: Saved
Coredump Type: Kernel
Coredump Size: 1.8GB
Coredump Timestamp: Fri Jan 12 14:51:22 UTC 2024

Node                State  Type    Panic-String                          Uptime-Before-Crash
cluster-node-01     Saved  Kernel  PANIC: Memory allocation failure      45d 3h 22m
cluster-node-02     Saved  Kernel  PANIC: NVMe controller timeout        38d 18h 15m

Coredump vmcore.0 deleted successfully.

Service Processor Log for cluster-node-01:
Jan 15 09:23:12 UTC: CRITICAL - CPU temperature threshold exceeded (92°C)
Jan 15 09:22:58 UTC: WARNING - Memory ECC error detected on DIMM_A3
Jan 15 09:22:45 UTC: INFO - System entering panic sequence
Jan 15 09:22:30 UTC: WARNING - Disk I/O latency spike detected (>500ms)
Jan 15 09:22:15 UTC: CRITICAL - Power supply voltage fluctuation
...
```

!!! warning "Common errors"
    **`Error: Invalid node name "node_name"`** — Replace `<node_name>` with the actual node name from the cluster (e.g., `cluster-node-01`).
    **`Error: Coredump file not found: <filename>`** — Verify the exact coredump filename using `system node coredump show` before attempting deletion.
    **`Error: This operation requires admin or diag privileges`** — Ensure your user account has the necessary ONTAP role permissions; contact your cluster administrator if needed.
A node panic followed by an automatic HA takeover is normal ONTAP behavior — the key diagnostic information is in the panic string and the EMS log immediately preceding the panic. Always generate an AutoSupport when an unexpected panic occurs.

---

## Step 11 — AutoSupport bundle

AutoSupport bundles are the primary support artifact. Generate one before calling NetApp support:

```bash
# Generate AutoSupport tied to a support case
system node autosupport invoke -node * -type all -message "case <SR-number> - <description>"

# Verify delivery
system node autosupport history show -node * -most-recent 5
# Status should show: sent-successful
```


```text title="Expected output"
Invoking AutoSupport on all nodes. This may take a few minutes...
Node: cluster1-01
   Invocation ID: 550e8400-e29b-41d4-a716-446655440000
   Status: SENT_SUCCESSFUL

Node: cluster1-02
   Invocation ID: 550e8400-e29b-41d4-a716-446655440001
   Status: SENT_SUCCESSFUL

Node                 Invocation-id                            Sent Time              Status
-------------------- ---------------------------------------- ---------------------- ------------------
cluster1-01          550e8400-e29b-41d4-a716-446655440000     11/15/2024 14:32:18    sent-successful
cluster1-01          550e8400-e29b-41d4-a716-446655440002     11/15/2024 13:15:42    sent-successful
cluster1-02          550e8400-e29b-41d4-a716-446655440001     11/15/2024 14:31:55    sent-successful
cluster1-02          550e8400-e29b-41d4-a716-446655440003     11/15/2024 13:14:28    sent-successful
cluster1-01          550e8400-e29b-41d4-a716-446655440004     11/15/2024 12:08:11    sent-successful
```

!!! warning "Common errors"
    **`Error: AutoSupport is not enabled on node cluster1-01`** — Enable AutoSupport with `system node autosupport modify -node <node-name> -state enable`.
    **`Error: Failed to send AutoSupport on cluster1-02: SMTP server unreachable`** — Verify SMTP server connectivity and configuration with `system node autosupport show -node cluster1-02` and check firewall rules.
If AutoSupport delivery is failing:

```bash
# Check AutoSupport configuration
system node autosupport show

# Test connectivity to NetApp endpoints
system node autosupport check show

# Check proxy configuration
system node autosupport show -fields proxy-url,transport
```


```text title="Expected output"
Node: cluster1-01
  Enabled: true
  Transport: https
  Proxy URL: -
  From Address: autosupport@cluster1.example.com
  To Addresses: support@netapp.com
  Mail Hosts: -
  SMTP Authentication Enabled: false
  Notifier Enabled: true

Node: cluster1-02
  Enabled: true
  Transport: https
  Proxy URL: -
  From Address: autosupport@cluster1.example.com
  To Addresses: support@netapp.com
  Mail Hosts: -
  SMTP Authentication Enabled: false
  Notifier Enabled: true

AutoSupport Connectivity Check Results:
Node: cluster1-01
  Destination: support.netapp.com
  Status: PASSED
  Response Time: 245ms

Node: cluster1-02
  Destination: support.netapp.com
  Status: PASSED
  Response Time: 312ms

Node: cluster1-01
  Proxy URL: -
  Transport: https

Node: cluster1-02
  Proxy URL: -
  Transport: https
```

!!! warning "Common errors"
    **`Error: command not found: system node autosupport show`** — Ensure you are connected to the ONTAP cluster CLI (ssh to cluster management IP) rather than the local shell.
    **`AutoSupport Connectivity Check Results: Node: cluster1-01 Status: FAILED`** — Verify firewall rules allow outbound HTTPS (port 443) to support.netapp.com and check DNS resolution with `system services dns check`.
    **`Error: Invalid field name "proxy-url"`** — Use the correct field name `proxy_url` (underscore instead of hyphen) in the `-fields` parameter.
---

## Log locations

| Log Source | Location / Command |
|---|---|
| EMS event log | `event log show` (CLI); `/mroot/etc/log/ems` (node shell) |
| AutoSupport history | `system node autosupport history show -node <node>` |
| Audit log (admin actions) | `security audit log show` |
| CIFS/SMB audit | SVM-level audit log configured to NAS volume via `vserver audit` |
| Crash dumps / core files | `system node coredump show`; files at `/mroot/etc/crash/` |
| Disk firmware log | `storage disk show -fields firmware-revision`; in AutoSupport |
| Node syslog | `system node run -node <node> syslog` (node shell) |
| SP / BMC logs | `system service-processor log show -node <node>` |
| Core file listing | `system node coredump show -node <node>` |

---

## See also

- [ONTAP — Common Issues](../common-issues/)
- [ONTAP — Escalation](../escalation/)

## Verify resolution

- `cluster show` returns all nodes with `health: true` and `eligibility: true`
- `storage failover show` shows `Connected, Not in takeover` for all HA pairs
- `system health status show` returns `ok`
- `storage disk show -broken` returns no broken disks (or the same pre-existing broken disks that were there before the incident)
- `volume show -state !online` returns no unexpectedly offline volumes
- `network interface show -status-oper down` returns no operationally-down LIFs
- For SnapMirror: `snapmirror show -health false` returns no unhealthy relationships
- `event log show -severity CRITICAL -time-range 1h` shows no new critical events after the fix was applied
