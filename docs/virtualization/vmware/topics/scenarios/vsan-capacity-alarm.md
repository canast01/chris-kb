---
tags:
  - scenarios
  - vmware
  - vsan
  - vsphere-8
---
# vSAN Capacity Alarm

<div class="kb-summary">
vSAN capacity reaches a warning or critical threshold — typically 75% or 80% full —
triggering a Skyline Health alarm and blocking snapshot creation for all VMs on the
affected datastore. This scenario covers how to confirm the alarm, identify the largest
capacity consumers, and recover headroom through snapshot cleanup, storage vMotion, or
capacity additions.

*Applies to: vSphere 7.x / 8.x*
</div>

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | Capacity alarms; vSAN Monitor; Virtual Objects view |
| vSAN | Capacity tracking; object placement; snapshot write reservation |
| ESXi | Disk group management; disk add operations |
| Aria Operations | Capacity trend analysis; projected depletion date |

---

## 1. Confirm the Alarm and Headroom

Navigate to **vCenter → Cluster → Monitor → vSAN → Skyline Health → Capacity** to see the exact percentage and which thresholds are breached.

```text
vSAN capacity thresholds (default):
  75%  Warning — new snapshot creation may be throttled
  80%  Error   — new object writes may be refused; VMs at risk
  95%  Critical — cluster may go read-only; VM crashes possible
```

Confirm via the vSAN Capacity view exactly how much free space remains. The numbers include dedup and compression savings — always use the **physical capacity** figure when calculating headroom, not the effective capacity.

```bash
# SSH to any ESXi host in the cluster to query raw capacity
esxcli vsan storage list | grep -E "SSD|Capacity|Size"

# Or use the vCenter API — PowerCLI query below (see Section 6)
```

Look for: note the projected depletion date shown in Aria Operations (if deployed) — this determines urgency. Immediate action needed if < 20% free and depletion < 7 days.

---

## 2. Break Down Capacity Usage

Navigate to **vCenter → Cluster → Monitor → vSAN → Capacity → Usage Breakdown** to identify what is consuming space.

```text
Typical usage breakdown components:
  VM home objects      — VM config files, swap, log files
  VM disk objects      — VMDK data (largest share)
  Snapshot deltas      — snapshot chain growth; can balloon rapidly
  vSAN system objects  — witness components, checksum objects
  Overhead             — RAID copies and parity (not reclaimed by cleanup)
```

Sort the **vSAN → Virtual Objects** view by "Used Space" (descending) to identify the top 10 largest objects. Export or note the owners (VM names and VMDK labels) before taking action.

Look for: any VM with snapshot chain depth > 3 or snapshots older than 7 days. These are the fastest wins — a single unconsolidated snapshot can consume as much space as the VMDK itself.

---

## 3. Remove Snapshot Waste

Snapshots are the most common cause of unexpected vSAN capacity consumption.

```powershell
# Find all VMs with snapshots older than 72 hours
Get-VM | Get-Snapshot | Where-Object {
    $_.Created -lt (Get-Date).AddHours(-72)
} | Select-Object VM, Name, Description, Created, @{
    N="SizeGB"; E={[math]::Round($_.SizeGB, 1)}
} | Sort-Object SizeGB -Descending | Format-Table -AutoSize
```

Before removing a snapshot, confirm with the application or backup team that it is safe to do so (the snapshot may be held by a backup job).

```powershell
# Consolidate snapshots for a specific VM (removes all snapshots cleanly)
Get-VM -Name "vm-name" | Get-Snapshot | Remove-Snapshot -RunAsync -Confirm:$false
```

After snapshot removal, monitor the virtual objects view — delta disks should shrink within minutes and the capacity alarm should clear once usage drops below the threshold.

Look for: if snapshot removal does not free space immediately, the VM may have a **snapshot consolidation required** alarm — see [VM Snapshot Consolidation Required](vm-snapshot-consolidation-required/index.md) for that sub-flow.

---

## 4. Move or Reclaim Data

If snapshot cleanup is insufficient, consider moving large VMDKs to another datastore.

```powershell
# Storage vMotion a VM to a different datastore
$vm = Get-VM -Name "large-vm"
$targetDS = Get-Datastore -Name "alternate-datastore"
Move-VM -VM $vm -Datastore $targetDS -RunAsync
```

If no alternative datastore is available, add capacity to the vSAN cluster:

```text
Adding a disk group (no host required):
  vCenter → Cluster → Configure → vSAN → Disk Management
  Select host → Add Disk Group
  Assign one cache SSD + 1–7 capacity disks
  vSAN redistributes data automatically (rebalance takes minutes to hours)

Adding a new ESXi host:
  Add host to cluster first, claim disks in Disk Management
  vSAN automatically begins a rebalance to distribute data
  Monitor via: Monitor → vSAN → Rebalance
```

Look for: after adding disks or a host, confirm the capacity alarm clears and the Skyline Health capacity check returns green. Rebalance progress is visible in **Monitor → vSAN → Rebalance**.

---

## 5. Prevent Recurrence

After resolving the immediate issue, address the root cause to prevent recurrence.

```text
Preventive actions:
  Set vSAN capacity alarm threshold to 70% (gives earlier warning)
  Enable Aria Operations capacity projections with 30-day look-ahead
  Set a backup retention policy that limits snapshot age to 24 hours
  Review SPBM policies — FTT=2 (RAID-6) uses less overhead than FTT=2 (RAID-1)
  Enable vSAN dedup and compression if workload is compressible (all-flash only)
```

```bash
# Check dedup/compression ratio on the cluster
esxcli vsan datastore namespaceobjectlist get | grep -E "Ratio|Dedup|Compress"
```

---

## 6. PowerCLI — Capacity and Usage Queries

```powershell
# Get overall vSAN datastore capacity and free space
Get-Datastore -Name "vsanDatastore" | Select-Object Name, CapacityGB, FreeSpaceGB, @{
    N="UsedPct"; E={[math]::Round((1 - ($_.FreeSpaceGB / $_.CapacityGB)) * 100, 1)}
}

# Get all snapshots on the cluster with size
Get-VM | Get-Snapshot | Select-Object VM, Name, Created, SizeGB |
    Sort-Object SizeGB -Descending | Select-Object -First 20

# Get vSAN cluster capacity via vSAN API
$vsanCapacity = Get-VsanView -Id "VsanVcClusterSpaceReportSystem-vsan-cluster-space-report-system"
$report = $vsanCapacity.VsanQuerySpaceUsage($cluster.ExtensionData.MoRef)
$report.FreeCapacityB / 1GB
```

---

## Key Terms

| Term | Definition |
|---|---|
| vSAN | VMware's hyperconverged storage layer; pools local ESXi disks into a shared distributed datastore |
| Capacity threshold | Configurable percentage at which vSAN raises a warning or error alarm; default warning=75%, error=80% |
| Snapshot delta | VMDK delta disk created when a snapshot is taken; grows with every write to the original VMDK |
| Dedup/compression | vSAN data reduction features; dedup removes identical blocks, compression reduces block size; all-flash only |
| SPBM | Storage Policy-Based Management — defines FTT, RAID level, encryption per VM; FTT level directly affects capacity overhead |
| FTT | Failures to Tolerate; FTT=1 RAID-1 doubles capacity usage, FTT=1 RAID-5 uses 1.33x, FTT=2 RAID-6 uses 1.5x |
| Rebalance | vSAN background process that redistributes data evenly across disk groups after a disk or host is added |
| Object | The unit of vSAN storage — each VMDK, snapshot delta, VM home, and swap file is a separate object |
| Skyline Health | vSAN health monitoring dashboard in vCenter; includes capacity, disk, network, and cluster configuration checks |

---

## Common Mistakes

- **Treating dedup/compression savings as guaranteed free space.** Dedup ratios vary by workload. If you size based on effective capacity, a sudden reduction in compressibility (e.g. encrypted VMs) can exhaust physical capacity without warning.
- **Allowing backup snapshots to accumulate.** Backup software creates and removes snapshots; if backup jobs fail silently, snapshot deltas grow until the alarm fires.
- **Adding disks to an already-full cluster.** If the cluster is above 90%, adding a disk group triggers a rebalance that briefly increases I/O load. Schedule disk additions during off-peak hours.
- **Not checking snapshot consolidation required.** After deleting a snapshot via vCenter, a consolidation error may leave delta disks on disk. Always check for the consolidation required alarm post-deletion.

---

## Related Scenarios

- [VM Snapshot Consolidation Required](vm-snapshot-consolidation-required/index.md) — snapshot delta files not removed after deletion; separate consolidation workflow.
- [Storage vMotion / Datastore Migration](storage-vmotion-datastore-migration/index.md) — moving VMs between datastores as a capacity management action.
- [vSAN Disk or Component Failure](vsan-disk-component-failure/index.md) — disk failure reduces vSAN capacity and triggers a related set of alarms.
