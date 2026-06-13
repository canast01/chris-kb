---
tags:
  - operations
  - vmware
  - vsan
  - vsphere-8
---
# vSAN Operations — CLI Reference


<div class="kb-summary">
Commonly used ESXi shell and PowerCLI commands for managing and troubleshooting vSAN clusters. vSAN is VMware's hyper-converged storage solution — it pools the local disks of multiple ESXi hosts into a shared datastore.

*Applies to: vSAN 7.x / 8.x*
</div>

```text
┌──────────────────────────────────────── vSAN — CLI Reference ─────────────────────────────────────────┐
│                                                                                                       │
│  vSAN CLI operations use esxcli on hosts, RVC (Ruby vSphere Console), PowerCLI,                       │
│  and the vSphere Client UI for health, disk, and object management.                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               esxcli Commands                │  │                 RVC Commands                │   │
│   │           esxcli vsan cluster get            │  │           vsan.health.health_test           │   │
│   │           esxcli vsan storage list           │  │            vsan.disks_info <host>           │   │
│   │           esxcli vsan network list           │  │            vsan.obj_status_report           │   │
│   │           esxcli vsan debug object           │  │            vsan.resync_dashboard            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  esxcli runs on the ESXi host shell; RVC runs from the vCenter or jump host.                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              PowerCLI Commands               │  │            Object & Disk Commands           │   │
│   │         Get-VsanClusterConfiguration         │  │           esxcli vsan debug object          │   │
│   │           Get-VsanDisk | Ft Status           │  │          cmmds-tool find (metadata)         │   │
│   │            Test-VsanClusterHealth            │  │           vsanObserver (perf data)          │   │
│   │           Get-VsanView (advanced)            │  │            esxcli vsan trace cat            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  All commands execute against host or vCenter management plane; cmmds-tool                            │
│  is host-local only and reads cluster metadata database.                                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  esxcli vsan   = vSAN management namespace in ESXi CLI                                                │
│  RVC           = Ruby vSphere Console; legacy; still used for vSAN diag                               │
│  cmmds-tool    = Cluster Monitoring, Membership, Directory Service tool                               │
│  CMMDS         = cluster metadata store; tracks object component locations                            │
│  vsanObserver  = performance observability tool; requires RVC                                         │
│  obj_status    = per-object health report; shows degraded/absent                                      │
│  resync_dash   = RVC command showing active resync bytes/throughput                                   │
│  debug object  = detailed per-object component and placement info                                     │
│  vsan trace    = per-host vSAN trace log; crash and I/O analysis                                      │
│  health_test   = runs all vSAN health checks programmatically                                         │
│  Get-VsanDisk  = PowerCLI; lists disk status across cluster                                           │
│  Test-VsanCluster= PowerCLI; triggers health check run                                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Quick Reference

| Task | Command |
|---|---|
| Cluster membership and health | `esxcli vsan cluster get` |
| Run all health checks | `esxcli vsan health cluster get` |
| Health failures only | `esxcli vsan health cluster get \| grep -i fail` |
| List disk groups | `esxcli vsan storage list` |
| Object health summary | `esxcli vsan debug object list \| grep -v healthy` |
| Resync queue | `esxcli vsan debug resync summary get` |
| Resync detail | `esxcli vsan debug resync list` |
| Check resync throttle | `esxcli vsan debug resync throttle get` |
| Set resync throttle | `esxcli vsan debug resync throttle set --throttle 500` |
| Network connectivity test | `esxcli vsan debug network test` |
| MTU jumbo frame test | `vmkping -I vmk2 -d -s 8972 <peer_vmk_ip>` |
| Add disk group | `esxcli vsan storage add -s <ssd_naa> -d <cap_naa>` |
| Remove disk group | `esxcli vsan storage remove -s <ssd_naa>` |
| Performance service status | `esxcli vsan perf get` |
| Per-VMDK performance stats | `esxcli vsan debug vmdk list` |
| Disk-level IOPS/latency stats | `esxcli vsan storage stats get` |

---

## Skyline Health

**From vCenter UI:**
Cluster → Monitor → vSAN → Skyline Health

Equivalent CLI commands (run from any host in the cluster):

```bash
esxcli vsan health cluster get | grep -i fail
esxcli vsan health cluster get | grep -i warning
```

Check performance service status:

```bash
esxcli vsan perf get
```

---

## Health & Diagnostics

vSAN health checks validate everything from disk capacity to network connectivity to object compliance. Run these after any hardware change or when investigating performance issues.

```bash
# Summary health (pass/fail for all health checks)
esxcli vsan health cluster get
esxcli vsan health summary get

# Detailed trace output
esxcli vsan trace get

# List all VM object components and their health
esxcli vsan debug object list

# Show only unhealthy objects (not accessible or degraded)
esxcli vsan debug object list | grep -i unhealthy

# Objects with absent components (data on a failed or removed host)
esxcli vsan debug object list | grep -i absent

# Active resync operations (rebuilds, rebalances, migrations)
esxcli vsan debug resync list
esxcli vsan debug resync summary get

# Component status (individual chunks of VM data)
esxcli vsan debug component list
```

---

## Disk Groups

A disk group is the fundamental storage unit in vSAN. Each disk group has one cache SSD (handles writes and accelerates reads) and one or more capacity disks (where data actually lives). Each ESXi host can have up to five disk groups.

### List Disk Groups and Devices

```bash
# All vSAN storage devices — shows SSD (cache tier) and capacity disks
esxcli vsan storage list

# Summary: which SSD is the group leader for each group
esxcli vsan storage list | grep -E "Is SSD|Disk Group UUID|VSAN UUID"
```

### Disk and Group Statistics

```bash
# I/O stats per disk (reads, writes, errors, latency)
esxcli vsan storage stats get

# Per-disk detail (include health state)
esxcli vsan storage list | grep -E "naa\.|Health|State"
```

### Add Disks / Create Disk Group

```bash
# Add a cache SSD and one or more capacity disks (creates new disk group)
esxcli vsan storage add -s <ssd_naa> -d <capacity_naa1> -d <capacity_naa2>

# Add capacity disk to existing disk group
esxcli vsan storage add -s <existing_ssd_naa> -d <new_capacity_naa>
```

### Evacuate Before Removal

Always evacuate data before removing a disk — otherwise object components go absent:

```bash
# Evacuate a disk (moves data to other hosts — waits for completion)
esxcli vsan storage evacuate -d <device_naa>

# Check resync progress during evacuation
esxcli vsan debug resync list

# Confirm no remaining data on disk
esxcli vsan storage list | grep <device_naa>
```

### Remove a Disk Group

```bash
# Remove a cache SSD (removes entire disk group — evacuate first)
esxcli vsan storage remove -s <ssd_naa>

# Remove a single capacity disk from a group
esxcli vsan storage remove -d <capacity_naa>
```

### Disk Group Health

```bash
# Check for degraded or absent components
esxcli vsan debug object list | grep -v healthy

# vSAN health check — disk layer
esxcli vsan health cluster get | grep -i disk

# Overall health summary
esxcli vsan health summary get
```

### Disk Group Best Practices

| Guideline | Reason |
|---|---|
| 1 SSD : 7 capacity disks max | Beyond 7, cache hit rate drops significantly |
| Evacuate before any disk removal | Prevents component loss |
| Match capacity disk sizes within a group | Avoids uneven wear and wasted space |
| Check `esxcli vsan debug resync list` before maintenance | Ensure no active rebuild before removing another disk |
| Replace failed disk within 24h | vSAN has single-failure tolerance — second failure = data loss |

---

## Networking (vSAN VMkernel)

vSAN requires a dedicated VMkernel adapter tagged for vSAN traffic. All hosts in the cluster communicate via this interface using unicast (since vSAN 6.6). MTU should be 9000 (jumbo frames) end-to-end for best performance.

### vSAN VMkernel Adapters

```bash
# List VMkernel adapters tagged for vSAN traffic
esxcli vsan network list

# Unicast agent config — shows peer IPs for each vSAN VMkernel
esxcli vsan network ipconfig list
```

### Connectivity Test

```bash
# Test vSAN network connectivity to all cluster peers
esxcli vsan debug network test
# Sends UDP probes to all known unicast agents and reports latency / loss
```

### Verifying VMkernel Tagging

```bash
# Confirm vmk is tagged for vSAN
esxcli network ip interface tag get -i vmk2

# Expected output includes: VSAN

# Add vSAN tag to a VMkernel (if missing)
esxcli network ip interface tag add -i vmk2 -t VSAN
```

### MTU Verification

vSAN performs best with jumbo frames (MTU 9000) end-to-end:

```bash
# Check VMkernel MTU
esxcli network ip interface list | grep -A5 vmk2

# Test large packet through physical switches (ping with don't-fragment)
vmkping -I vmk2 -d -s 8972 <peer_vmk_ip>
# Expected: no packet loss. If loss occurs — switch or NIC MTU mismatch
```

### Network Configuration Commands

```bash
# Add a vSAN VMkernel
esxcli vsan network ip add -i vmk2

# Remove a VMkernel from vSAN network config
esxcli vsan network ip remove -i vmk2
```

### Network Troubleshooting

| Symptom | Check |
|---|---|
| Cluster health: Network issues | `esxcli vsan debug network test` — look for packet loss |
| High vSAN latency | `vmkping -d -s 8972` — check MTU along path |
| Host isolated from cluster | `esxcli vsan network ipconfig list` — unicast agents populated? |
| vSAN VMkernel missing | `esxcli network ip interface tag get` — VSAN tag present? |

---

## PowerCLI — vSAN

PowerCLI provides a scripting interface to vSAN via vCenter. Use this for automation, scheduled health checks, and capacity reporting across multiple clusters.

```powershell
# Connect to vCenter
Connect-VIServer <vcenter>

# Cluster configuration
Get-VsanClusterConfiguration -Cluster <cluster>

# Health check (equivalent of Skyline Health UI)
Test-VsanClusterHealth -Cluster <cluster>

# Disk groups for a specific host
Get-VsanDiskGroup -VMHost <host>

# Disk inventory for a host
Get-VsanDisk -VMHost <host>

# Resync status — active rebuilds and rebalances
Get-VsanResyncStatus -Cluster <cluster>

# Capacity usage
Get-VsanSpaceUsage -Cluster <cluster>

# Fault domain / witness configuration
Get-VsanFaultDomainConfiguration -Cluster <cluster>

# Full vSAN health check via API (detailed)
$vhs = Get-VsanView -Id VsanVcClusterHealthSystem-vsan-cluster-health-system
$vhs.VsanQueryVcClusterHealthSummary(
    (Get-Cluster <cluster>).ExtensionData.MoRef,
    $null, $null, $true, $null, $null, 'defaultView'
)
```

---

## RVC Commands (Legacy)

RVC (Ruby vSphere Console) was the primary vSAN diagnostic tool before vSAN 6.7. It remains available on vCenter appliances for backwards-compatible diagnostics. Most workflows have moved to `esxcli vsan` and the Skyline Health UI.

### Connecting to RVC

```bash
# SSH to vCenter appliance, then launch RVC
rvc <user>@<vcenter_fqdn>

# Navigate the object tree
ls
cd localhost/
cd localhost/<datacenter>/computers/<cluster>/
```

### Health Checks

```bash
# Full vSAN health check against a cluster
vsan.health.health_check <cluster_path>

# Quiet mode — only failed checks
vsan.health.health_check <cluster_path> --quiet
```

### Disk and Object Status

```bash
# Disk stats per host in the cluster
vsan.disks_stats <cluster_path>

# Object inventory and compliance state
vsan.obj_status_report <cluster_path>

# Detail for a specific object UUID
vsan.object_info <cluster_path> <object_uuid>
```

### Resync Dashboard

```bash
# Active resync operations (rebuilds, migrations)
vsan.resync_dashboard <cluster_path>

# Refresh every 10 seconds
vsan.resync_dashboard <cluster_path> --refresh-rate 10
```

### RVC vs Modern Alternatives

| RVC Command | Modern Equivalent |
|---|---|
| `vsan.health.health_check` | vSAN Health UI / `esxcli vsan health summary get` |
| `vsan.disks_stats` | `esxcli vsan storage stats get` |
| `vsan.resync_dashboard` | `esxcli vsan debug resync list` |
| `vsan.obj_status_report` | `esxcli vsan debug object list` |

RVC is still useful for scripted checks against older vSAN clusters (6.0–6.5) where `esxcli vsan` commands are limited.

---

## Performance Commands

Use these when investigating latency, IOPS, or throughput issues. Run from the ESXi host shell.

### Performance Service Status

```bash
# Confirm performance service is collecting data
esxcli vsan perf get
```

### Per-VMDK Stats

```bash
# IOPS, latency, and throughput per virtual disk
esxcli vsan debug vmdk list
```

Look for high `ReadLatency` or `WriteLatency` values (milliseconds). Sustained values above 10 ms read / 20 ms write indicate a problem.

### Disk-Level Stats

```bash
# Per-physical-disk IOPS, latency, and error counters
esxcli vsan storage stats get
```

### Cache Buffer Utilisation (OSA only)

```bash
# Write buffer usage per disk group — high value = cache SSD bottleneck
esxcli vsan debug disk list | grep -i "cache\|write buffer\|congestion"
```

Cache write buffer > 95% sustained = cache SSD is a bottleneck. Options: reduce write IOPS, add capacity disks to the group, or upgrade the cache SSD.

### Congestion

```bash
# Congestion count per disk group — must be 0 in healthy operation
esxcli vsan debug disk list | grep -i congestion
```

### Historical Performance (PowerCLI)

```powershell
# Query cluster-level performance data (requires Performance Service enabled)
$cluster = Get-Cluster "VSAN-LON-01"
$end = Get-Date
$start = $end.AddHours(-1)

Get-VM -Location $cluster | ForEach-Object {
    $stats = Get-Stat -Entity $_ -Stat "disk.read.latency.average","disk.write.latency.average" `
        -Start $start -Finish $end -IntervalMins 5 -ErrorAction SilentlyContinue
    if ($stats) {
        [PSCustomObject]@{
            VM         = $_.Name
            AvgReadMs  = [Math]::Round(($stats | Where-Object Stat -eq "disk.read.latency.average"  | Measure-Object Value -Average).Average, 2)
            AvgWriteMs = [Math]::Round(($stats | Where-Object Stat -eq "disk.write.latency.average" | Measure-Object Value -Average).Average, 2)
        }
    }
} | Sort-Object AvgWriteMs -Descending | Select -First 20
```

### Latency Alert Thresholds

| Metric | Normal | Investigate | Escalate |
|---|---|---|---|
| Read latency (all-flash OSA) | < 1 ms | > 5 ms sustained | > 10 ms |
| Write latency (all-flash OSA) | < 2 ms | > 10 ms sustained | > 20 ms |
| Read latency (ESA) | < 0.5 ms | > 2 ms sustained | > 5 ms |
| Write latency (ESA) | < 1 ms | > 5 ms sustained | > 10 ms |
| Congestion | 0 | Any non-zero | Sustained > 0 |
