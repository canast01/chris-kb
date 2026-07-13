---
tags:
  - vmware
description: "Storage Latency Troubleshooting (VMware) reference covering Latency Thresholds, Step 1: Identify Affected VMs and Datastores, Step 2: Check Storage Paths..."
---
# Storage Latency Troubleshooting (VMware)

<div class="kb-summary">
Storage Latency Troubleshooting (VMware) reference covering Latency Thresholds, Step 1: Identify Affected VMs and Datastores, Step 2: Check Storage Paths, Step 3: Check for vSAN Resync or Rebuild, Step 4: Queue Depth and Congestion and 3 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

latency_thresholds: "Latency Thresholds" {shape: rectangle}
step_1_identify_affected_vms_and_dat: "Step 1: Identify Affected VMs and Datastores" {shape: rectangle}
step_2_check_storage_paths: "Step 2: Check Storage Paths" {shape: rectangle}
step_3_check_for_vsan_resync_or_rebu: "Step 3: Check for vSAN Resync or Rebuild" {shape: rectangle}
step_4_queue_depth_and_congestion: "Step 4: Queue Depth and Congestion" {shape: rectangle}
step_5_datastores_on_the_same_lunvol: "Step 5: Datastores on the Same LUN/Volume" {shape: rectangle}

latency_thresholds -> step_1_identify_affected_vms_and_dat: uses
step_1_identify_affected_vms_and_dat -> step_2_check_storage_paths: uses
step_2_check_storage_paths -> step_3_check_for_vsan_resync_or_rebu: uses
step_3_check_for_vsan_resync_or_rebu -> step_4_queue_depth_and_congestion: uses
step_4_queue_depth_and_congestion -> step_5_datastores_on_the_same_lunvol: uses
```

## Latency Thresholds

| Latency | State | Action |
|---|---|---|
| < 5 ms | Excellent | No action |
| 5–10 ms | Normal | No action |
| 10–20 ms | Warning | Monitor; identify source |
| 20–50 ms | Problem | Investigate immediately |
| > 50 ms | Severe | Application timeouts expected — escalate |

## Step 1: Identify Affected VMs and Datastores

```powershell
# Datastores with low free space (often correlates with high latency)
Get-Datastore | Select-Object Name,
    @{N="FreeGB";E={[math]::Round($_.FreeSpaceGB,1)}},
    @{N="UsedPct";E={[math]::Round((1-$_.FreeSpaceGB/$_.CapacityGB)*100,1)}} |
    Sort-Object UsedPct -Descending

# VMs with snapshots (delta VMDKs increase read latency)
Get-VM | Get-Snapshot | Select-Object @{N="VM";E={$_.VM.Name}}, Name, Created,
    @{N="SizeGB";E={[math]::Round($_.SizeGB,2)}}
```

## Step 2: Check Storage Paths

```bash
# Path states on the ESXi host
esxcli storage core path list | grep -E "State:|Device:|Adapter:"

# Dead paths (need recovery or failover)
esxcli storage core path list | grep "State: dead"

# Confirm active path count per device
esxcli storage nmp path list | grep -E "Active|Device"

# Current PSP (Path Selection Policy)
esxcli storage nmp device list | grep -E "Device:|PSP:"
```


```text title="Expected output"
State: active
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
Adapter: vmhba0
State: active
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
Adapter: vmhba1
State: standby
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l3
Adapter: vmhba2
State: dead
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l4
Adapter: vmhba3
Active: 2
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
Active: 1
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l3
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
PSP: VMW_PSP_RR
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l3
PSP: VMW_PSP_FIXED
Device: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l4
PSP: VMW_PSP_MRU
```

!!! warning "Common errors"
    **`Unknown command or namespace esxcli storage`** — Verify esxcli is available and you are running commands directly on an ESXi host (not vCenter); SSH to the ESXi management IP and try again.
    **`State: dead` paths persist after reboot** — Run `esxcli storage core path set --path=<path_id> --state=active` to manually recover the path, or check array-side LUN masking and fabric connectivity.
    **`grep: (standard input) is empty`** — The storage subsystem may not have detected any paths; verify LUN presentation with `esxcli storage core device list` and rescan HBAs using `esxcli storage core adapter rescan --adapter=vmhba0`.
## Step 3: Check for vSAN Resync or Rebuild

vSAN resync heavily consumes storage backend IOPS:

```bash
# Active resync (if running — latency will be elevated)
esxcli vsan debug resync list

# Resync byte count (estimate duration)
esxcli vsan debug resync list | grep -E "Total Bytes|Remaining"

# Check if objects are degraded
esxcli vsan debug object list | grep -v healthy
```


```text title="Expected output"
UUID                                  ResyncState  TotalBytes       ResyncedBytes    RemainingBytes   EstimatedTime
550e8400-e29b-41d4-a716-446655440000  Active       1099511627776   274877906944     824633720832     3h 45m
660e8400-e29b-41d4-a716-446655440001  Active       549755813888    137438953472     412316860416     1h 52m

Total Bytes: 1649267441664
Remaining: 412316860416

Object UUID                           State        Health   ComponentCount
770e8400-e29b-41d4-a716-446655440002  Inaccessible Degraded 3
880e8400-e29b-41d4-a716-446655440003  Accessible   Degraded 4
990e8400-e29b-41d4-a716-446655440004  Accessible   Degraded 2
```

!!! warning "Common errors"
    **`VSAN is not enabled on this host`** — Run `esxcli vsan cluster get` to verify VSAN is enabled; if not, enable it via vSphere Client or `esxcli vsan cluster new`.
    **`grep: (standard input): No such file or directory`** — Ensure the first `esxcli vsan debug resync list` command completes successfully before piping; check host connectivity and VSAN service status with `systemctl status vsanvpd`.
## Step 4: Queue Depth and Congestion

```bash
# Device queue depth
esxcli storage core device list | grep "Queue Full Threshold"

# Check if devices are hitting queue full
grep -i "queue full\|queue depth\|SCSI cmd abort" /var/log/vmkernel.log | tail -20

# Adjust queue depth for a specific device (requires reboot to persist)
esxcli storage core device set --device <naa.xxx> -O MaxQueueDepth=32
```


```text title="Expected output"
Queue Full Threshold: 64
Queue Full Threshold: 64
Queue Full Threshold: 128
Queue Full Threshold: 64

2024-01-15T09:23:47.123Z cpu15:2048)ScsiDeviceIO: 3847: SCSI cmd abort on device naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m, CmdSN 0x4521
2024-01-15T09:24:12.456Z cpu8:4096)ScsiDeviceIO: 3847: Queue full condition detected on naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m, depth 64/64
2024-01-15T09:25:33.789Z cpu22:8192)ScsiDeviceIO: 3847: SCSI cmd abort on device naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m, CmdSN 0x4533
2024-01-15T09:26:01.234Z cpu5:1024)ScsiDeviceIO: 3847: Queue full condition detected on naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m, depth 64/64

Operation completed successfully on device naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m. MaxQueueDepth set to 32. Host reboot required for changes to persist.
```

!!! warning "Common errors"
    **`Error: Unknown option --device`** — Use the correct flag format `--device=<naa.xxx>` or check esxcli storage core device set --help for valid parameters.
    **`Error: Device naa.6001405a1b2c3d4e5f6g7h8i9j0k1l2m not found`** — Verify the NAA identifier is correct by running `esxcli storage core device list` and copying the exact device name.
    **`Permission denied: /var/log/vmkernel.log`** — Run the grep command with `sudo` or as root user to access vmkernel logs.
## Step 5: Datastores on the Same LUN/Volume

Multiple datastores sharing an underlying volume compete for IOPS:

```bash
# LUN to device mapping
esxcli storage core device list | grep -E "naa\.|Device Display"

# Check VAAI support (helps with copy offload and ATS locking)
esxcli storage core device vaai status get -d <naa.xxx>
```


```text title="Expected output"
Device Display Name: NETAPP Fibre Channel Disk (naa.60a98000572d534b4e6d396f59386b41)
Device Display Name: NETAPP Fibre Channel Disk (naa.60a98000572d534b4e6d396f59386b42)
Device Display Name: PURE FlashArray//X Fibre Channel Disk (naa.624a9370abcd1234ef567890abcd1234)
Device Display Name: EMC VMAX Fibre Channel Disk (naa.60000970000192700533533030303031)
Device Display Name: NETAPP Fibre Channel Disk (naa.60a98000572d534b4e6d396f59386b43)

VAAI Status:
   ATS/Locking: supported
   Clone: supported
   Delete: supported
   Unmap: supported
   Write Same: supported
   Xcopy: supported
```

!!! warning "Common errors"
    **`Device naa.60a98000572d534b4e6d396f59386b41 not found`** — Verify the NAA identifier is correct by running `esxcli storage core device list` without the `-d` flag to list all available devices.
    **`Unknown command or namespace`** — Ensure you are running this command on an ESXi host with VAAI-capable storage; older ESXi versions may not support the `vaai status get` subcommand.
## Step 6: esxtop Storage Analysis

```bash
# Launch esxtop, switch to storage view
esxtop
# Press 'u' for device view
# Key columns: DAVG/cmd (device latency), KAVG/cmd (kernel latency), QAVG/cmd (queue latency)
# DAVG > 10ms = storage backend issue
# KAVG > 2ms  = host-side queuing issue
```


```text title="Expected output"
CPU  MEMORY  DISK  NETWORK  SWAP  POWER  DUMPPART  SCSI  NETWORK  RESOURCE  STORAGE  HELP
Press 'u' to switch to device view...

DEVICE                READS/s  WRITES/s  DAVG/cmd  KAVG/cmd  QAVG/cmd  ACTV  QUED  %UTIL
naa.60060e8007e3a00001234567890abcd  145.2  89.7  8.3ms  1.1ms  0.2ms  12  2  67%
naa.60060e8007e3a00001234567890cdef  203.1  156.4  14.7ms  2.8ms  1.5ms  18  8  89%
naa.60060e8007e3a00001234567890ef01  98.5  42.3  3.2ms  0.9ms  0.1ms  6  0  34%
naa.60060e8007e3a00001234567890gh23  167.8  201.5  22.1ms  3.4ms  2.9ms  24  14  94%
naa.60060e8007e3a00001234567890ij45  112.3  67.9  6.8ms  1.3ms  0.3ms  9  1  52%

Press 'q' to quit esxtop
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are logged into an ESXi host directly (SSH) or use vSphere Client; esxtop only runs on ESXi, not vCenter.
    **`DAVG/cmd column not visible`** — Press 'f' to customize fields and enable DAVG, KAVG, and QAVG columns in the storage device view.
## Common Causes Reference

| Cause | Indicator | Fix |
|---|---|---|
| vSAN resync | `resync list` shows bytes remaining | Wait for completion; avoid additional disk removal |
| Snapshot chain | Delta VMDK in `ls -lah` is large | Remove/consolidate snapshots |
| Dead paths | `path list` shows dead state | Rescan adapters; check physical SAN connectivity |
| Queue depth saturation | vmkernel.log "queue full" | Reduce queue depth per device or balance VMs |
| Storage array overload | DAVG high on all VMs | Redistribute VMs; check array CPU/cache hit rate |
| All-Paths-Down (APD) | APD in vmkernel.log | Recover connectivity; check SAN zoning and HBAs |
| Thin provisioning overcommit | Datastore > 90% used | Add capacity immediately — thin disks can pause on overcommit |
