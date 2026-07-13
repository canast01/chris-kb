---
tags:
  - troubleshooting
search:
  boost: 1.5
description: "Storage troubleshooting — APD/PDL conditions, multipath failures, replication lag, snapshot failures, host I/O errors, and array health alerts."
---
# Storage — Troubleshooting

<div class="kb-summary">
Storage troubleshooting — APD/PDL conditions, multipath failures, replication lag, snapshot failures, host I/O errors, and array health alerts.
</div>

<div class="kb-grid kb-grid-2">
<a class="kb-card" href="replication-failures/"><strong>Replication Failures</strong><span>Storage replication failure diagnosis — lag thresholds, link state, and consistency group checks.</span></a>
<a class="kb-card" href="storage-latency/"><strong>Storage Latency</strong><span>Storage latency troubleshooting — array queue depth, fabric congestion, and host-side I/O analysis.</span></a>
</div>

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
symptom_index: "Symptom Index" {shape: rectangle}
linux_host_io_diagnostics: "Linux Host I/O Diagnostics" {shape: rectangle}
vmware_apd_recovery: "VMware APD Recovery" {shape: rectangle}
replication_lag_diagnosis: "Replication Lag Diagnosis" {shape: rectangle}
array_health_check_commands: "Array Health Check Commands" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> symptom_index: investigate
symptom -> linux_host_io_diagnostics: investigate
symptom -> vmware_apd_recovery: investigate
symptom -> replication_lag_diagnosis: investigate
symptom -> array_health_check_commands: investigate
symptom_index -> resolution
linux_host_io_diagnostics -> resolution
vmware_apd_recovery -> resolution
replication_lag_diagnosis -> resolution
array_health_check_commands -> resolution
```

## Symptom Index

| Symptom | Likely Cause | First Command |
|---|---|---|
| All Paths Down (APD) in vCenter | Fabric or array outage | `esxcli storage core path list` |
| Permanent Device Loss (PDL) | LUN removed or array offline | Check array health; check zoning |
| Multipath path degraded | HBA or switch port issue | `multipath -ll` (Linux) |
| I/O latency spike | Overloaded storage pool; dedup/compression | Check array I/O stats |
| Snapshot job failing | Snapshot policy conflict; quota exceeded | Check array event log |
| Replication lag growing | WAN bandwidth; source I/O rate high | Check replication stats on array |
| Filesystem read-only | Underlying LUN error; I/O timeout | `dmesg | grep -i 'error\|read-only\|EXT4-fs'` |

## Linux Host I/O Diagnostics

```bash
# Check for multipath failures
multipath -ll
dmesg | grep -i 'scsi\|sd[a-z]\|mpath\|failed'

# I/O error log
journalctl -k | grep -i 'error\|i/o error\|EXT4\|XFS' | tail -50

# Check disk queue depth and wait
iostat -xz 1 5
# await > 20ms on SSD is abnormal

# Check LUN presence
lsblk; ls -la /dev/mapper/
```


```text title="Expected output"
mpatha (36001405a1b2c3d4e5f6g7h8i9j0k1l2m) dm-0 NETAPP,LUN C-Mode
size=2.0T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 2:0:0:0 sda 8:0  active ready running
| `- 3:0:0:0 sdb 8:16 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 4:0:0:0 sdc 8:32 active ready running
  `- 5:0:0:0 sdd 8:48 active ready running
[  142.556234] sd 2:0:0:0: [sda] Assuming drive cache: write through
[  156.823891] EXT4-fs (dm-0): mounted filesystem with ordered data mode
[  892.145672] I/O error, dev dm-0, sector 4096512 logical block 512064

Linux 5.15.0-91-generic #101-Ubuntu SMP Tue Nov 14 10:35:26 UTC 2023 x86_64
avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           12.45    0.00   18.92   34.67    0.00   33.96

Device            r/s     w/s     rMB/s     wMB/s   rrqm/s   wrqm/s  await avgqu-sz   %util
sda            156.23   89.45    12.34     8.92    2.10     5.67   24.56    3.45   78.90
dm-0           245.68  145.32    20.26    14.58    0.00     0.00   28.34    5.12   92.10
sdb            152.10   87.23    11.98     8.67    1.95     5.43   23.89    3.28   76.45

NAME                 MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
sda                    8:0    0  2.0T  0 disk
├─sda1                 8:1    0  512M  0 part  /boot
└─sda2                 8:2    0  1.9T  0 part
  └─mpatha           253:0    0  2.0T  0 mpath /data
sdb                    8:16   0  2.0T  0 disk
└─mpatha             253:0    0  2.0T  0 mpath /data

total 0
crw-rw---- 1 root disk    253,   0 Nov 14 10:45 dm-0
crw-rw---- 1 root disk    253,   1 Nov 14 10:45 dm-1
lrwxrwxrwx 1 root root         7 Nov 14 10:42 mpatha -> ../dm-0
l
```
**Expected output:** `multipath -ll` shows all paths in `active ready` state. `dmesg` grep returns no output. `iostat` shows `await` < 5 ms for SSD, < 20 ms for HDD under normal load.

## VMware APD Recovery

```bash
# Rescan datastores after fabric restoration
esxcli storage core adapter rescan --all
esxcli storage core path list | grep -E 'State:|Device:|Adapter:'

# If APD persists after fabric is restored:
# 1. Put host in maintenance mode
# 2. Remove and re-add storage adapter in vCenter
# 3. Rescan
```


```text title="Expected output"
Rescan of adapter vmhba0 started.
Rescan of adapter vmhba1 started.
Rescan of adapter vmhba2 started.
Rescan of adapter vmhba3 started.
Device: naa.60060e8008073000002707338d3ae411
State: Active
Adapter: vmhba0
Device: naa.60060e8008073000002707338d3ae412
State: Active
Adapter: vmhba1
Device: naa.60060e8008073000002707338d3ae413
State: Dead
Adapter: vmhba2
Device: naa.60060e8008073000002707338d3ae414
State: Active
Adapter: vmhba3
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown command or namespace rescan` | Verify you are running this command on an ESXi host (not vCenter) with esxcli available in PATH. |
    | `Error: Could not get list of paths` | Ensure the storage adapter is not in a completely failed state; if APD persists, proceed with adapter removal in vCenter before rescanning. |
**Expected output:** `esxcli storage core path list` shows `State: active` for all paths. APD condition resolves in vCenter (datastore no longer shows "All Paths Down").

## Replication Lag Diagnosis

```bash
# Pure FlashArray — check active replication
purepod list
purepod show replication --pod <pod_name>

# Dell PowerMax SRDF — check link state
symrdf -g <dg_name> query

# Generic: check WAN utilisation
iperf3 -c <target-site-ip> -t 10   # bandwidth test between sites
```


```text title="Expected output"
Name                          Enabled  Replication Status
pod-prod-01                   True     Synced
pod-prod-02                   True     Synced
pod-dr-backup                 False    Idle

Pod Name: pod-prod-01
Direction: Outbound
Target: pod-dr-backup
Status: Synced
RPO: 0 seconds
Bytes Replicated: 2.847 TB

Symmetrix ID: 000297123456
Group Name: PROD_SRDF_GRP_01
Link State: SYNCED
RDF Mode: Synchronous
Pair State: Synchronized
Percent Complete: 100%

Connecting to 10.45.82.19 port 5201
[  5] local 10.32.14.8 port 52847 connected to 10.45.82.19 port 5201
[ ID] Interval           Transfer     Bitrate         Retr  Cwnd
[  5]   0.00-1.00   sec  112 MBytes   939 Mbits/sec    0   2.45 MBytes
[  5]   1.00-2.00   sec  118 MBytes   991 Mbits/sec    0   2.45 MBytes
[  5]   2.00-10.00   sec  1.04 GBytes   892 Mbits/sec    8   1.89 MBytes
- - - - - - - - - - - - - - - - - - - - - - - - - -
[ ID] 0.00-10.00  sec  1.27 GBytes   909 Mbits/sec    8             sender
[ ID] 0.00-10.00  sec  1.27 GBytes   908 Mbits/sec             receiver
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `purepod: command not found` | Install the Pure Storage Python SDK or ensure the FlashArray CLI tools are in your PATH. |
    | `symrdf: command not found` | Install Dell EMC Solutions Enabler (SE) and verify the SYMCLI_CONNECT environment variable is set. |
    | `connect failed: No route to host` | Verify network connectivity and firewall rules allow iperf3 traffic (default port 5201) between source and target sites. |
## Array Health Check Commands

```bash
# Pure FlashArray
purearray monitor             # latency, IOPS, bandwidth
purevolume monitor <volume>   # per-volume stats

# Dell PowerMax
symcfg show -sid <sid>        # array health summary
symdev list -sid <sid>        # device list

# NetApp ONTAP
storage aggregate show -state !online   # degraded aggregates
volume show -state !online
```


```text title="Expected output"
=== Pure FlashArray Monitoring ===
Name                          Latency(us)  IOPS      Bandwidth(MB/s)
pure-array-01                 245          156800    4521.3
pure-array-02                 312          98450     2847.9

Volume: prod-db-vol-001
Latency(us): 187  IOPS: 45230  Bandwidth(MB/s): 1203.4
Writes: 28934  Reads: 16296

=== Dell PowerMax Array Health ===
Symmetrix ID: 000297900001
Array Model: PowerMax 8000
Health Status: Healthy
Capacity: 2.4 PB  Used: 1.8 PB

Device List (sample):
Dev#  Attr  Cap(GB)  Config  Status
0000  RDF   1024     TDEV    Ready
0001  RDF   1024     TDEV    Ready
0002  RDF   1024     TDEV    Ready
...

=== NetApp ONTAP Degraded Resources ===
(no output — no degraded aggregates found)

(no output — all volumes online)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `command not found: purearray` | Verify Pure Storage CLI tools are installed and added to $PATH, or use full path `/opt/purestorage/bin/purearray`. |
    | `Error: Invalid SID <sid>` | Confirm the Symmetrix ID is correct by running `symcfg list` to enumerate available arrays. |
    | `Error: command requires ONTAP admin credentials` | Authenticate to the ONTAP cluster first using `ssh admin@<cluster-mgmt-ip>` or configure SSH keys for passwordless access. |