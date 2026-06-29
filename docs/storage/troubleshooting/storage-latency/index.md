---
tags:
  - troubleshooting
search:
  boost: 1.5
---
# Storage Latency Troubleshooting

<div class="kb-summary">
Storage Latency Troubleshooting reference covering Overview, Latency Threshold Reference, Diagnostic Flowchart, VMware ESXi esxtop Storage Analysis, PowerMax / VMAX Performance Analysis and 6 more sections.
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Overview

Storage latency is a primary cause of application performance degradation, database timeouts, and VM instability. Diagnosis requires correlating host-side metrics (iostat, esxtop) with array-side metrics (Unisphere, symstat) and multipath health. This guide covers NVMe, SSD, HDD, NFS, and iSCSI environments including PowerMax/VMAX and VMware ESXi.

---

## Latency Threshold Reference

| Storage Type | Protocol | Normal (ms) | Warning (ms) | Critical (ms) | Notes |
|---|---|---|---|---|---|
| NVMe SSD (local) | NVMe | <0.1 | 0.5 | >1.0 | Latency >1ms = hardware fault |
| All-Flash Array | FC/iSCSI | <1 | 2–5 | >5 | DAVG >5ms on AFA = investigate |
| Hybrid Array (SSD tier) | FC/iSCSI | <2 | 5 | >10 | Tiering may not be working |
| HDD Array | FC/iSCSI | <10 | 20 | >30 | Queue depth and RAID overhead |
| NFS (LAN) | NFS | <1 | 3 | >5 | Check NFS server CPU and cache |
| iSCSI (10GbE LAN) | iSCSI | <2 | 5 | >10 | MTU (jumbo frames) critical |
| VMware DAVG | FC/iSCSI | <10 | 20 | >30 | esxtop threshold; DAVG >20 = concern |
| VMware GAVG | FC/iSCSI | <10 | 25 | >50 | Includes DAVG + KAVG + QAVG |

---

## Diagnostic Flowchart

```d2
direction: right

K: "Array-side latency\nCheck PowerMax / Unisphere" {shape: rectangle}
Q: "Check multipath: dead paths?\nmultipathd show paths" {shape: rectangle}
A: "Storage Latency Alert" {shape: rectangle}
C: "iostat -x 5 3\nCheck await and %util" {shape: rectangle}
E: "Check %util\nIs device saturated?" {shape: rectangle}
F: "Storage device overloaded\nCheck multipath: multipathd show paths" {shape: rectangle}
G: "Queue depth issue or controller latency\nCheck array-side: symstat or Unisphere" {shape: rectangle}
H: "Latency within range\nCheck application layer" {shape: rectangle}
I: "esxtop → press" {shape: rectangle}
M: "VMkernel overhead\nCheck ESXi storage path / HBA driver" {shape: rectangle}
O: "VM queue depth exceeded\nReduce I/O or increase queue depth" {shape: rectangle}
P: "Latency within ESXi thresholds\nCheck guest OS metrics" {shape: rectangle}
S: "Restore dead paths\nCheck SAN zoning / HBA port" {shape: rectangle}
T: "Check array controller CPU and cache\nUnisphere → Performance Dashboard" {shape: rectangle}
V: "Working set exceeds cache\nTiering or capacity expansion needed" {shape: rectangle}
W: "Check for snapshot/replication I/O\nSchedule during maintenance window" {shape: rectangle}

K -> Q
```

### esxtop Storage Threshold Summary

| Counter | Green | Warning | Critical | Action |
|---|---|---|---|---|
| DAVG (ms) | <10 | 10–20 | >20 | Array investigation |
| KAVG (ms) | <2 | 2–5 | >5 | ESXi / HBA driver issue |
| GAVG (ms) | <15 | 15–30 | >30 | Correlate DAVG+KAVG |
| QAVG (ms) | 0 | >0 | >5 | Reduce queue depth or I/O load |
| ABRTS/s | 0 | >0 | >5 | Path or timeout issue; urgent |
| RESETS/s | 0 | >0 | >1 | HBA or storage controller fault |

---

## PowerMax / VMAX Performance Analysis

```bash
# Run symstat for array performance (requires SYMCLI)
symstat -sid 000123 -type lun -interval 10 -count 6

# Example LUN-level output:
# Device   Reads/s  Writes/s  Read MB/s  Write MB/s  Read MS  Write MS  %Busy
# 00A0     1250.0    800.0      40.0       25.0        1.2      2.1     45.0
# 00A1     2100.0    100.0      65.0        3.0       18.5      5.0     88.0  ← high
# 00A2      450.0    900.0      14.0       28.0        0.8      1.5     32.0

# Check SRDF impact on performance (SRDF/S adds write latency)
symdev -sid 000123 show 00A1 | grep -i "rdf\|srdf"

# Check director (FA port) performance
symstat -sid 000123 -type director -interval 10 -count 6

# Check frontend director (FA) port utilisation
symcfg -sid 000123 list -fa all -port all
```


```text title="Expected output"
Symmetrix ID: 000123

Device   Reads/s  Writes/s  Read MB/s  Write MB/s  Read MS  Write MS  %Busy
00A0     1250.0    800.0      40.0       25.0        1.2      2.1     45.0
00A1     2100.0    100.0      65.0        3.0       18.5      5.0     88.0
00A2      450.0    900.0      14.0       28.0        0.8      1.5     32.0
00A3      890.0    650.0      28.0       20.0        2.3      3.2     52.0
00A4     1560.0    420.0      48.0       13.0        1.5      1.8     61.0
00A5      720.0    1100.0     22.0       34.0        0.9      2.8     48.0

Device 00A1:
  RDF State: Synchronized
  SRDF/S Mode: Enabled
  RDF Link Latency: 12.5 ms

Director  Reads/s  Writes/s  Read MB/s  Write MB/s  Read MS  Write MS  %Busy
FA-1D     5200.0   3850.0    165.0      120.0       2.1      3.5     78.0
FA-2D     4950.0   3620.0    158.0      115.0       2.0      3.2     75.0
FA-3D     2100.0   1500.0     68.0       48.0       1.8      2.9     42.0

Symmetrix ID: 000123
FA Port Configuration:
FA-1D:0  (Online)  Link Speed: 16 Gbps  Utilization: 82%
FA-1D:1  (Online)  Link Speed: 16 Gbps  Utilization: 79%
FA-2D:0  (Online)  Link Speed: 16 Gbps  Utilization: 75%
FA-2D:1  (Online)  Link Speed: 16 Gbps  Utilization: 88%
FA-3D:0  (Online)  Link Speed: 8 Gbps   Utilization: 45%
```

!!! warning "Common errors"
    **`SYMCLI Error: Cannot connect to the Symmetrix array (000123)`** — Verify the array SID is correct and the SYMCLI server daemon is running on the management host.
    **`bash: symstat: command not found`** — Install the EMC SYMCLI package or add the SYMCLI bin directory to your PATH environment variable.
    **`SYMCLI Error: Insufficient privileges to query array`** — Ensure your user account has appropriate SYMCLI permissions or run the command with sudo.
### Unisphere for PowerMax — Key Performance Views

| View | Location in Unisphere | What to Check |
|---|---|---|
| Array-level latency | Performance → Dashboard → Latency | Overall read/write ms; trend over 24h |
| Director utilisation | Performance → Directors | FA/RA director CPU; >70% = near saturation |
| Cache hit rate | Performance → Cache | Read hit rate; <90% = working set too large |
| SRP capacity | Storage → SRP | Used capacity; >80% = tiering pressure |
| Volume performance | Storage → Volumes → select volume | Per-volume read/write latency |

---

## Multipath Issues

Dead or degraded paths cause I/O to be rerouted through remaining paths, increasing load and latency.

```bash
# Linux device mapper multipath — show all paths
multipathd show paths

# Example output:
# name      sysfs  dm-st  dev    dev_t   pri  dm-st   chk_st  next_check
# 3600507680282874fc400000000000002
#   |- sdb  running  active  ready   1  active  ready  up
#   |- sdc  running  active  ready   1  active  ready  up
#   |- sdd  running  failed  faulty  0  faulty  undef  up   ← dead path
#   |- sde  running  active  ready   1  active  ready  up

# Check multipath topology (which paths are active)
multipath -ll

# Check path failures and reinstate a path (after fixing SAN issue)
multipathd reinstate path sdd

# Show device usage to identify which LUN is affected
multipathd show maps

# Verify HBA port status (Linux)
systool -c fc_host -v | grep -E "port_state|port_id|symbolic_name"

# Check SAN fabric login (Brocade / Cisco FC switch)
# Brocade:
nsshow | grep <wwpn>
# Cisco MDS:
# show flogi database | include <wwpn>
```


```text title="Expected output"
name                                    sysfs  dm-st  dev    dev_t   pri  dm-st   chk_st  next_check
3600507680282874fc400000000000002
  |- sdb                                running  active  ready   8:16   1  active  ready  up
  |- sdc                                running  active  ready   8:32   1  active  ready  up
  |- sdd                                running  failed  faulty  8:48   0  faulty  undef  up
  |- sde                                running  active  ready   8:64   1  active  ready  up

mpatha (3600507680282874fc400000000000002) dm-0 NETAPP,LUN
size=500G features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 2:0:0:0 sdb 8:16 active ready running
| |- 3:0:0:0 sdc 8:32 active ready running
| `- 4:0:0:0 sde 8:64 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 5:0:0:0 sdd 8:48 failed faulty offline

reinstated path sdd

name                                    sysfs  dm-st  dev    dev_t   pri  dm-st   chk_st  next_check
mpatha                                  dm-0   NETAPP,LUN  500G  active  ready
mpathb                                  dm-1   NETAPP,LUN  250G  active  ready

ClassDevice = "fc_host0"
  port_state              = "Online"
  port_id                 = "0x010203"
  symbolic_name           = "QLogic QLE2562 FCoE Initiator"
ClassDevice = "fc_host1"
  port_state              = "Online"
  port_id                 = "0x010204"
  symbolic_name           = "QLogic QLE2562 FCoE Initiator"

PWWN: 50:00:14:40:5a:2b:c1:e0  NWWN: 50:00:14:40:5a:2b:c1:e1  State: Online
```

!!! warning "Common errors"
    **`multipathd: command not found`** — Install device-mapper-multipath package with `apt-get install multipath-tools` or `yum install device-mapper-multipath`.
    **`reinstate path sdd: path does not exist`** — Verify the path name with `multipathd show paths` and ensure the device is visible to the kernel before reinstatement.
    **`systemctl status multipathd` shows inactive`** — Start the multipath daemon with `systemctl start multipathd && systemctl enable multipathd`.
---

## Snapshot and Replication Impact on Latency

Snapshots consume array resources during creation and maintenance. Active snapshots increase write latency.

```bash
# Check VMware snapshot count on VMs (PowerCLI)
Get-VM | Where-Object {$_.ExtensionData.Snapshot} |
    Select-Object Name,
        @{N='SnapCount';E={(Get-Snapshot -VM $_).Count}},
        @{N='SnapAgeDays';E={(Get-Snapshot -VM $_ | Sort-Object Created | Select-Object -First 1).Created}} |
    Sort-Object SnapCount -Descending | Select-Object -First 10

# Check ONTAP volume snapshot count
volume snapshot show -vserver svm1 -volume vol_db

# Check snapshot space consumption
volume show -vserver svm1 -volume vol_db -fields size,used,percent-snapshot-space

# PowerMax: check snapshot count per device
symsnap -sid 000123 -name snap_* list

# Check SRDF/A journal consumption (high journal = SRDF/A falling behind)
symrdf -g RDF_GRP_01 -type rdfa list | grep -i journal
```


```text title="Expected output"
Name                          SnapCount SnapAgeDays
----                          --------- -----------
prod-db-vm-03                        47 2024-01-15 09:23:14
web-app-vm-12                        32 2024-01-18 14:07:22
backup-staging-vm-08                 28 2024-01-20 11:45:33
legacy-app-vm-01                      19 2024-02-02 08:12:09
test-vm-04                            12 2024-02-05 16:33:41

  Vserver Volume   Snapshot Count
  ------- -------- ---------------
  svm1    vol_db   23

  Vserver Volume   Size     Used     Percent Snapshot Space
  ------- -------- -------- -------- ----------------------
  svm1    vol_db   500GB    387GB    18%

Symmetrix ID: 000123
Device Name: snap_prod_001
Snapshot Name: snap_prod_001_20240215
Tracks: 2457600
Timestamp: 02/15/2024 03:45:22

RDF Group: RDF_GRP_01
Journal Tracks Used: 89456
Journal Tracks Total: 102400
Journal Utilization: 87%
```

!!! warning "Common errors"
    **`Get-VM : The term 'Get-VM' is not recognized as the name of a cmdlet`** — Load the VMware PowerCLI module with `Import-Module VMware.PowerCLI` before running the command.
    **`volume snapshot show: command not found`** — SSH into the ONTAP cluster management IP and authenticate with valid credentials before running ONTAP commands.
    **`symsnap: command not found`** — Ensure the EMC Solutions Enabler (SE) package is installed and the `$PATH` includes `/opt/emc/SYMCLI/bin`.
---

## Storage Controller CPU and Cache Hit Rate

```bash
# ONTAP: check node CPU and cache
statistics show -object system -instance node01 -counter cpu_busy

# Cache performance
statistics show -object wafl -instance node01 -counter read_cache_hit_percent

# Example healthy output:
# read_cache_hit_percent: 97%   ← good
# read_cache_hit_percent: 64%   ← working set larger than cache — latency will increase

# PowerMax: cache stats via symstat
symstat -sid 000123 -type cache -interval 10 -count 3

# Check ONTAP aggregate (disk group) performance
statistics show -object aggr -instance aggr0 -counter total_ops,read_latency,write_latency
```


```text title="Expected output"
node01> statistics show -object system -instance node01 -counter cpu_busy
    cpu_busy: 42%

node01> statistics show -object wafl -instance node01 -counter read_cache_hit_percent
    read_cache_hit_percent: 89%

Symmetrix ID: 000123
                    Cache Statistics (10 second interval)
Timestamp           Read Hit %    Write Hit %    MB/sec Read    MB/sec Write
14:32:15            94.2          87.6           1245.3         892.1
14:32:25            93.8          88.1           1198.7         915.4
14:32:35            94.5          87.9           1267.2         901.3

node01> statistics show -object aggr -instance aggr0 -counter total_ops,read_latency,write_latency
    total_ops: 8642
    read_latency: 2.3ms
    write_latency: 1.8ms
```

!!! warning "Common errors"
    **`Error: object "wafl" is not valid`** — Verify the object name is correct for your ONTAP version; use `statistics show -objects` to list available objects.
    **`Symmetrix ID 000123 not found`** — Confirm the array SID with `symcfg list` and ensure the Symmetrix is online and accessible.
    **`statistics: unknown counter "read_latency"`** — Use `statistics show -object aggr -fields` to verify the exact counter name for your ONTAP release.
---

## Queue Depth Analysis

```bash
# Check current queue depth for a device (Linux)
cat /sys/block/sdb/queue/nr_requests
# Default: 128 for HDD, 1024 for NVMe

# Check HBA queue depth
cat /sys/class/scsi_host/host0/cmd_per_lun

# VMware: check queue depth for an adapter (esxcli)
esxcli storage core adapter list
esxcli storage core device list | grep -A5 "Queue Full"

# Set queue depth for Fibre Channel HBA (Emulex example) — requires reboot
esxcli system module parameters set -m lpfc -p "lpfc_lun_queue_depth=64"

# Check if queue full events are occurring
esxcli storage core device stats get -d naa.6006016011602d00abcd | grep -i queue
```


```text title="Expected output"
128
32
Name: lpfc
Driver: lpfc
Queue Depth: 32
Max Queue Depth: 256

Device: naa.6006016011602d00abcd
  Vendor: EMC
  Model: SYMMETRIX
  Queue Full Count: 0
  Queue Depth: 32
  Outstanding Commands: 8
```

!!! warning "Common errors"
    **`cat: /sys/block/sdb/queue/nr_requests: No such file or directory`** — Verify the device exists with `lsblk` and use the correct device name (e.g., `/sys/block/sda` instead of `/sys/block/sdb`).
    **`Error: Unknown option set for module lpfc`** — Check the exact parameter name with `modinfo lpfc | grep parm` and ensure the module is loaded before setting parameters.
    **`Device naa.6006016011602d00abcd not found`** — Run `esxcli storage core device list` to retrieve the correct NAA identifier for your storage device.
---

## Common Causes and Fixes

| Symptom | Root Cause | Fix |
|---|---|---|
| DAVG >20ms, KAVG <2ms | Array-side latency; controller overloaded | Check array director utilisation; balance LUN distribution |
| KAVG >2ms, DAVG normal | ESXi HBA driver issue or PSP misconfigured | Update HBA driver; check path selection policy (Round Robin) |
| await spikes during backup window | Backup I/O competing with production | Schedule backup during off-peak; enable backup throttling |
| QAVG >5ms | Queue depth exceeded; I/O queuing in VMkernel | Increase LUN queue depth; reduce VM I/O or add paths |
| Intermittent latency spikes | Dead multipath causing path failover | Fix dead path; check SAN switch zoning |
| High write latency only | Write-cache disabled on array | Re-enable write cache; check SP battery/vault |
| Latency after snapshot creation | Too many active snapshots on volume | Remove old snapshots; evaluate snapshot policy |
| NFS latency high | NFS server CPU/memory pressure | Check NFS server load; consider moving to dedicated NFS volume |
| iSCSI timeouts | MTU mismatch (jumbo frames not configured end-to-end) | Verify MTU=9000 on all iSCSI interfaces and switches |

---

## Escalation Criteria

Escalate to storage team or vendor TAC when:

- DAVG >30ms sustained for >5 minutes impacting production VMs
- ABRTS/s >0 on any production LUN (I/O abort indicates path or controller failure)
- Multipath dead path count >50% of total paths for any device (I/O risk)
- Array controller CPU >85% sustained (storage vendor must investigate)
- Cache hit rate <80% (working set analysis and capacity planning required)
- SRDF/A falling behind during SRDF performance degradation (RPO impact)
- Storage array reporting hardware fault in Unisphere or SYMCLI health check
- Queue full conditions occurring repeatedly (storage fabric or array tuning required)
- Latency cannot be correlated to a specific cause after 30 minutes of investigation

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

## See also

- [Storage — Replication Failures](../replication-failures/)
- [Storage — Known Issues](../known-issues.md)
- [Storage — Troubleshooting Overview](../)
