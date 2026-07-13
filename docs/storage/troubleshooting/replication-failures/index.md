---
tags:
  - troubleshooting
search:
  boost: 1.5
description: "Replication Failures Troubleshooting reference covering Overview, Replication Technology Classification, Diagnostic Flowchart, ONTAP SnapMirror..."
---
# Replication Failures Troubleshooting

<div class="kb-summary">
Replication Failures Troubleshooting reference covering Overview, Replication Technology Classification, Diagnostic Flowchart, ONTAP SnapMirror Troubleshooting, RecoverPoint Troubleshooting and 5 more sections.
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Overview

Replication failures degrade DR readiness and can result in RPO breaches. Each replication technology has distinct failure modes and tooling. This guide covers SRDF (Dell EMC PowerMax/VMAX), ONTAP SnapMirror, EMC RecoverPoint, vSphere Replication, and Veeam replication jobs. RPO breach assessment must happen immediately — sustained lag may trigger DR invocation.

---

## Replication Technology Classification

| Technology | Vendor | Replication Type | First-check Command | Typical RPO |
|---|---|---|---|---|
| SRDF/S | Dell EMC PowerMax/VMAX | Synchronous block | `symrdf -g <RDF_group> query` | 0 (synchronous) |
| SRDF/A | Dell EMC PowerMax/VMAX | Asynchronous block | `symrdf -g <RDF_group> query` | Seconds to minutes |
| SnapMirror | NetApp ONTAP | Async volume/SVM | `snapmirror show` | Minutes to hours |
| RecoverPoint | Dell EMC | Journal-based block | `get_group_status` / Web UI | Seconds (bookmark-based) |
| vSphere Replication | VMware | VM-level async | vCenter / VRMS UI; `Get-VM` | Minutes to hours |
| Veeam Replication | Veeam B&R | VM image-level | `Get-VBRJob`; Veeam console | Minutes to hours |

---

## Diagnostic Flowchart

```d2
direction: right

Z: "Get-VBRJob type Replica\nCheck last session result" {shape: rectangle}
AA: "Review session log\nCheck network path to replica host" {shape: rectangle}
A: "Replication Failure / Lag Alert" {shape: rectangle}
C: "symrdf -g RDF_GRP query\nCheck PAIR STATE" {shape: rectangle}
E: "Check link errors\nsymrdf -g RDF_GRP verify" {shape: rectangle}
G: "Engage network team\nCheck SRDF port stats: symrdf -g RDF_GRP -type\nRDFA list" {shape: rectangle}
H: "Check RDF group config\nresume if safe: symrdf -g RDF_GRP resume -nop" {shape: rectangle}
I: "CRITICAL: failover state\nDo NOT resume without DR assessment" {shape: rectangle}
J: "Check lag: symrdf -g RDF_GRP query\nRW state = consistent but R1 writing" {shape: rectangle}
K: "snapmirror show -fields lag-time,health" {shape: rectangle}
M: "snapmirror show -instance\nReview last-transfer-error" {shape: rectangle}
O: "ping -c4 intercluster-LIF\nCheck intercluster routes" {shape: rectangle}
P: "snapmirror abort\nsnapmirror resync" {shape: rectangle}
Q: "Check destination volume space\ndf -A" {shape: rectangle}
R: "snapmirror show -fields last-transfer-duration\nCheck bandwidth utilisation" {shape: rectangle}
S: "get_group_status\nCheck journal fullness" {shape: rectangle}
U: "Identify cause of high write rate\nExpand journal or reduce retention" {shape: rectangle}
V: "Check link status\nrpa_mgmt_cli: get_system_status" {shape: rectangle}
W: "vCenter: Monitor → vSphere Replication\nCheck VM replication status" {shape: rectangle}
Y: "Reconfigure replication\nCheck VR appliance health" {shape: rectangle}

Z -> AA
```

### SRDF Error Codes

| State | Meaning | Action |
|---|---|---|
| Suspended | Link deliberately or automatically suspended | Investigate cause; resume after fix |
| Partitioned | Network path between arrays lost | Restore connectivity; verify port status |
| Split | Volumes deliberately split (DR/test) | Do not resume without change control |
| SyncInProg | Synchronising after resume/establish | Wait; monitor cycle progress |
| Mixed | Some devices in group out of sync | Identify device; check device-level state |
| Failed Over | R2 has become primary (DR invoked) | Full DR procedure; do not reverse without planning |

---

## ONTAP SnapMirror Troubleshooting

### Check Relationship Status

```bash
# Summary view of all SnapMirror relationships
snapmirror show

# Example output:
# Source Path    Dest Path           MirrorState   LagTime   Healthy
# ------------   --------            -----------   -------   -------
# svm1:vol_db    svm2:vol_db_dp      Snapmirrored  0:05:32   true
# svm1:vol_app   svm2:vol_app_dp     Snapmirrored  2:34:11   false  ← problem

# Detailed view of a specific relationship
snapmirror show -source-path svm1:vol_app -destination-path svm2:vol_app_dp -instance

# Key fields to check:
# Last Transfer Type: scheduled (good) or update (manual resync triggered)
# Last Transfer Error: reason for last failure
# Transfer Snapshot:  name of snapshot being transferred (progress indicator)
```


```text title="Expected output"
Source Path    Dest Path           MirrorState   LagTime   Healthy
------------   --------            -----------   -------   -------
svm1:vol_db    svm2:vol_db_dp      Snapmirrored  0:05:32   true
svm1:vol_app   svm2:vol_app_dp     Snapmirrored  2:34:11   false
svm1:vol_logs  svm2:vol_logs_dp    Snapmirrored  0:12:47   true

                       Source Path: svm1:vol_app
                  Destination Path: svm2:vol_app_dp
                     Relationship ID: 12a3b4c5-6789-0def-1234-567890abcdef
                    Relationship Type: XDP
                        Mirror State: Snapmirrored
                         Lag Time: 2:34:11
                    Last Transfer Type: update
                   Last Transfer Error: Transfer aborted: destination volume is full
                   Transfer Snapshot: snapshot.2024-01-15_1430.0
                    Unhealthy Reason: Transfer failed
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: No SnapMirror relationships found` | Verify the SVMs exist and have SnapMirror licenses enabled with `system license show`. |
    | `Error: command not found: snapmirror` | Ensure you are connected to a NetApp ONTAP cluster with admin privileges; use `cluster show` to verify cluster access. |
    | `Error: Invalid source-path or destination-path specified` | Confirm the exact SVM and volume names with `volume show` and use the format `svm_name:volume_name` for both paths. |
### Diagnose and Resync

```bash
# Check what error caused failure
snapmirror show -fields last-transfer-error

# Typical errors:
# "Transfer aborted: failed to get snapshot lock" → snapshot conflict
# "Destination volume is full"                    → space issue on destination
# "Connection refused"                            → network/intercluster LIF issue

# Abort stuck transfer
snapmirror abort -source-path svm1:vol_app -destination-path svm2:vol_app_dp -foreground true

# Resync (re-establishes relationship from common snapshot baseline)
snapmirror resync -source-path svm1:vol_app -destination-path svm2:vol_app_dp

# Monitor transfer progress
snapmirror show -fields transfer-progress, lag-time

# Check intercluster LIF connectivity
network interface show -role intercluster
ping -lif intercluster_lif_svm1 -destination 192.168.10.20

# Check intercluster route
network route show -vserver svm1
```


```text title="Expected output"
Source                      Destination                 Last Transfer Error
----------------------------  ----------------------------  ----------------------------------------
svm1:vol_app                svm2:vol_app_dp             Transfer aborted: failed to get snapshot lock
svm1:vol_backup             svm2:vol_backup_dp          Destination volume is full
svm1:vol_data               svm2:vol_data_dp            (none)

Operation succeeded: SnapMirror relationship for "svm1:vol_app" aborted.

Operation succeeded: SnapMirror relationship for "svm1:vol_app" resynchronized.

Source                      Destination                 Transfer Progress  Lag Time
----------------------------  ----------------------------  ----------------  ----------
svm1:vol_app                svm2:vol_app_dp             87%                 45 minutes
svm1:vol_backup             svm2:vol_backup_dp          12%                 2 hours
svm1:vol_data               svm2:vol_data_dp            -                   0 seconds

Vserver     Interface       Address            Netmask        Status
----------  --------------  -----------------  --------------  ------
svm1        intercluster_1  192.168.10.10      255.255.255.0   up
svm1        intercluster_2  192.168.10.11      255.255.255.0   up
svm2        intercluster_1  192.168.10.30      255.255.255.0   up

PING 192.168.10.20 from 192.168.10.10: 56 data bytes
64 bytes from 192.168.10.20: icmp_seq=0 ttl=64 time=2.14 ms
64 bytes from 192.168.10.20: icmp_seq=1 ttl=64 time=1.89 ms
64 bytes from 192.168.10.20: icmp_seq=2 ttl=64 time=2.03 ms
--- 192.168.10.20 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss

Vserver  Destination     Gateway         Metric  Ifgrp
-------  ---------------  ---------------  ------  ------
svm1     0.0.0.0/0        192.168.10.1     20      -
svm1     192.168.10.0/24  0.0.0.0          10      -
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: entry doesn't have a value for this field` | Ensure the SnapMirror relationship exists and has completed at least one transfer; use `snapmirror show` without field filters to verify the relationship status. |
    | `Error: "svm1:vol_app" is not a valid SnapMirror relationship` | Verify the source and destination paths are correct and the relationship has been initialized with `snapmirror initialize`. |
    | `PING: sendto: No route to host` | Confirm the intercluster LIF is up, the destination IP is reachable, and firewall rules allow ICMP traffic between clusters on port 10666 for SnapMirror. |
### SnapMirror Lag Threshold Table

| Volume Tier | Schedule | Warning Lag | Critical (RPO Breach) |
|---|---|---|---|
| Tier 1 — Critical DB | Every 1 hour | >2 hours | >4 hours |
| Tier 2 — App volumes | Every 4 hours | >6 hours | >8 hours |
| Tier 3 — File shares | Every 24 hours | >36 hours | >48 hours |
| Vault (compliance) | Weekly | >10 days | >14 days |

---

## RecoverPoint Troubleshooting

```bash
# Connect to RecoverPoint Management CLI (via SSH to RPA)
ssh admin@rpa01.corp.example.com

# Check consistency group status
get_group_status

# Example output:
# Group Name       State          Link Status    Journal    Lag
# PROD-CG-01      Active         Active         12% Full   2s
# PROD-CG-02      Paused         Active         87% Full   N/A   ← journal full
# PROD-CG-03      Active         Disconnected   45% Full   N/A   ← link issue

# Check RPA system status
get_system_status

# Check journal volume fullness (journal full = replication pauses)
get_group_statistics -g PROD-CG-02

# To address journal full:
# 1. Check for access policy blocking journal recycling
# 2. Check if journal volume expansion is possible
# 3. If acceptable, reduce retention period on the consistency group
```


```text title="Expected output"
RecoverPoint CLI v8.2.1
Connected to RPA cluster: rpa01.corp.example.com
admin@rpa01> get_group_status

Group Name       State          Link Status    Journal    Lag
PROD-CG-01       Active         Active         12% Full   2s
PROD-CG-02       Paused         Active         87% Full   N/A
PROD-CG-03       Active         Disconnected   45% Full   N/A

admin@rpa01> get_system_status
System Status: HEALTHY
RPA Cluster: rpa01, rpa02, rpa03
Journal Volumes: 3/3 Online
Replication Links: 8/10 Active (2 Disconnected)
Last Sync: 2024-01-15 14:32:18 UTC

admin@rpa01> get_group_statistics -g PROD-CG-02
Consistency Group: PROD-CG-02
Journal Capacity: 500 GB
Journal Used: 435 GB (87%)
Retention Period: 72 hours
Incoming Rate: 125 MB/s
Outgoing Rate: 45 MB/s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Connection refused (111)` | Verify RPA hostname/IP is correct and SSH service is running on port 22; check firewall rules allowing admin access. |
    | `get_group_status: command not found` | Ensure you are in the RecoverPoint CLI shell (type `rpacli` if needed) and not in standard bash. |
    | `Permission denied: user 'admin' does not have access to consistency group PROD-CG-02` | Confirm the admin account has appropriate RBAC permissions for the target consistency group in RecoverPoint. |
---

## Replication Lag Threshold and RPO Breach Criteria

| Protection Tier | RPO Objective | Replication Type | Lag Threshold = Breach | Action |
|---|---|---|---|---|
| Gold (Tier 1) | 15 minutes | Synchronous / SRDF/A | Any lag >15 min | Immediate escalation; DR readiness assessment |
| Silver (Tier 2) | 4 hours | SnapMirror / SRDF/A | Lag >4 hours | Alert application owner; escalate to storage team |
| Bronze (Tier 3) | 24 hours | SnapMirror async | Lag >24 hours | Storage team investigation; no immediate DR trigger |
| Test/Dev | Best effort | Veeam replication | >48 hours | Informational only |

---

## Network Bandwidth and Latency Impact

```bash
# Measure available bandwidth between sites (install iperf3 on both sides)
# On destination site server:
iperf3 -s

# On source site:
iperf3 -c replication-dst-site-ip -t 60 -P 4

# SRDF/S (synchronous) latency budget:
# Round-trip latency between arrays should be <2ms for SRDF/S
# >2ms RTT → consider switching to SRDF/A

# Check current WAN utilisation (Cisco)
# show interface serial0/0 | include rate
#   5 minute input rate 850000000 bits/sec  ← close to 1Gbps link capacity

# Check if SRDF/A is throttling due to bandwidth
symrdf -g RDF_GRP_01 -type rdfa list | grep -i "transmit\|delay\|bandwidth"

# SnapMirror bandwidth throttling
snapmirror show -fields throttle

# Set a throttle (KB/s) to protect production workload
snapmirror modify -source-path svm1:vol_app -destination-path svm2:vol_app_dp -throttle 51200
```


```text title="Expected output"
---iperf3 Server Output (destination)---
Server listening on 5201
Accepted connection from 10.45.120.88, port 52847
[  5] local 10.45.120.99 port 5201 connected to 10.45.120.88 port 52847
[ ID] Interval           Transfer     Bitrate
[  5]   0.00-60.00  sec  6.82 GBytes   976 Mbps

---iperf3 Client Output (source)---
Connecting to 10.45.120.99, port 5201
[  4] local 10.45.120.88 port 52847 connected to 10.45.120.99 port 5201
[ ID] Interval           Transfer     Bitrate         Retr
[  4]   0.00-60.00  sec  6.82 GBytes   976 Mbps        12

---Cisco WAN Interface Check---
5 minute input rate 850000000 bits/sec, 125000 packets/sec
5 minute output rate 920000000 bits/sec, 118000 packets/sec

---SRDF/A Bandwidth Check---
Transmit Queue Depth: 2847 MB
Transmit Rate: 45.2 MB/sec
Bandwidth Throttle: Disabled
RDF Link Delay: 1.8 ms

---SnapMirror Throttle Status---
Source Path          Destination Path          Throttle
svm1:vol_app         svm2:vol_app_dp           unlimited
svm1:vol_backup      svm2:vol_backup_dp        25600

---SnapMirror Throttle Applied---
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `iperf3: command not found` | Install iperf3 on both servers using `apt-get install iperf3` (Ubuntu/Debian) or `yum install iperf3` (RHEL/CentOS). |
    | `symrdf: command not found` | Ensure the EMC Solutions Enabler package is installed and the `symcli` environment is properly configured in your PATH. |
    | `Error: command not found at vserver "svm1"` | Verify the source SVM name is correct and the cluster peer relationship is established with `cluster peer show`. |
---

## vSphere Replication Troubleshooting

```powershell
# PowerCLI: check replication state for all VMs
Get-VM | Get-VIObjectByVIView -MORef {$_.ExtensionData.Datastore} |
    Get-HciReplicationState  # requires Site Recovery Manager PowerCLI module

# Alternative: check via vCenter Web UI
# Monitor → Site Recovery → vSphere Replication → Virtual Machines

# Reconfigure replication if VR appliance loses connection
# vCenter → Host and Clusters → VR Appliance → Manage → VR Configuration

# Check VR appliance health via SSH
ssh admin@vr-appliance.corp.example.com
hbr-cfg status
```

---

## Veeam Replication Job Troubleshooting

```powershell
Add-PSSnapin VeeamPSSnapIn

# List replication jobs and last status
Get-VBRJob -Type Replica | Select-Object Name,
    @{N='LastResult';E={$_.GetLastResult()}},
    @{N='LastRun';E={$_.ScheduleOptions.LatestRunLocal}} |
    Format-Table -AutoSize

# Get failed session details
$job = Get-VBRJob -Name "Replica-PROD-SQL"
$session = Get-VBRReplicaSession | Where-Object {$_.JobName -eq $job.Name} |
    Sort-Object EndTime -Descending | Select-Object -First 1
$session.GetTaskSessions() | Select-Object Name, Status, Info

# Check replica VM state at target site
Get-VBRRestorePoint -Name "vm-prod-sql01-replica" | Select-Object CreationTime, IsConsistent
```

---

## Escalation Criteria — When to Invoke DR

Escalate immediately to DR coordinator / management when:

- SRDF group enters **Split** or **Failed Over** state unexpectedly (not during a planned DR test)
- RPO breach confirmed for any **Gold/Tier-1** system exceeding 30 minutes
- Replication link is down and cannot be restored within the RPO window
- RecoverPoint journal is >90% full and cannot be extended — replication will pause
- SnapMirror resync is failing repeatedly (>3 attempts) on a critical volume
- Both primary site and DR replication paths are simultaneously degraded (dual failure)
- Disaster scenario confirmed at primary site — initiate DR runbook immediately
- Any situation where last known good replication point is older than the RPO objective

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Storage — Storage Latency Troubleshooting](../storage-latency/)
- [Storage — Known Issues](../known-issues.md)
- [Storage — Troubleshooting Overview](../)
