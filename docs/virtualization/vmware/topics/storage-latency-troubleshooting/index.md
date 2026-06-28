---
tags:
  - vmware
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

## Step 4: Queue Depth and Congestion

```bash
# Device queue depth
esxcli storage core device list | grep "Queue Full Threshold"

# Check if devices are hitting queue full
grep -i "queue full\|queue depth\|SCSI cmd abort" /var/log/vmkernel.log | tail -20

# Adjust queue depth for a specific device (requires reboot to persist)
esxcli storage core device set --device <naa.xxx> -O MaxQueueDepth=32
```

## Step 5: Datastores on the Same LUN/Volume

Multiple datastores sharing an underlying volume compete for IOPS:

```bash
# LUN to device mapping
esxcli storage core device list | grep -E "naa\.|Device Display"

# Check VAAI support (helps with copy offload and ATS locking)
esxcli storage core device vaai status get -d <naa.xxx>
```

## Step 6: esxtop Storage Analysis

```bash
# Launch esxtop, switch to storage view
esxtop
# Press 'u' for device view
# Key columns: DAVG/cmd (device latency), KAVG/cmd (kernel latency), QAVG/cmd (queue latency)
# DAVG > 10ms = storage backend issue
# KAVG > 2ms  = host-side queuing issue
```

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
