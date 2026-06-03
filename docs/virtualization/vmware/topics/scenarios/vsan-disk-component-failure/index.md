# vSAN Disk or Component Failure

<div class="kb-summary">
A vSAN disk fails or a component becomes absent, leaving one or more VMs with reduced fault tolerance.
This scenario covers how to identify the failed component, assess the risk window based on FTT policy,
initiate or monitor rebuild after disk replacement, and use VxRail Manager for hardware-assisted workflows
on HCI deployments.
</div>

```text
┌───────────────────────────────── vSAN Disk / Component Failure — Investigation Flow ──────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: vCenter alarm — vSAN health degraded / component absent / capacity critical               ││
│   └──────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                              │                                                        │
│                           ┌──────────────────┴──────────────────┐                                     │
│                           ▼                                     ▼                                     │
│              ┌─────────────────────────┐           ┌─────────────────────────┐                        │
│              │ Skyline Health red      │           │ Virtual Objects view:   │                        │
│              │ check — which category? │           │ find VMs with degraded  │                        │
│              │ Disk / capacity /       │           │ or absent components    │                        │
│              │ network partition?      │           │                         │                        │
│              └────────────┬────────────┘           └────────────┬────────────┘                        │
│                           │                                     │                                     │
│                           ▼                                     ▼                                     │
│              ┌─────────────────────────┐           ┌─────────────────────────┐                        │
│              │ Identify host + disk    │           │ Assess FTT for affected │                        │
│              │ group with absent       │           │ VMs — are they still    │                        │
│              │ component               │           │ compliant?              │                        │
│              └────────────┬────────────┘           └────────────┬────────────┘                        │
│                           │                                     │                                     │
│                           └──────────────────┬──────────────────┘                                     │
│                                              ▼                                                        │
│              ┌───────────────────────────────────────────────────────────────────────────┐            │
│              │  Check physical disk health via ESXi · iDRAC (VxRail) · OMIVV alerts      │            │
│              └───────────────────────────────┬───────────────────────────────────────────┘            │
│                                              │                                                        │
│                           ┌──────────────────┴──────────────────┐                                     │
│                           ▼                                     ▼                                     │
│              ┌─────────────────────────┐           ┌─────────────────────────┐                        │
│              │  Disk truly failed:     │           │  Disk present but       │                        │
│              │  replace hardware;      │           │  disconnected: reseat / │                        │
│              │  vSAN auto-reclaims +   │           │  check HBA; no replace  │                        │
│              │  rebuilds               │           │  needed                 │                        │
│              └────────────┬────────────┘           └────────────┬────────────┘                        │
│                           └──────────────────┬──────────────────┘                                     │
│                                              ▼                                                        │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  CLOSE: Monitor resync ETA · Confirm all VMs compliant · Skyline Health green                     ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | vSAN health alarms; Virtual Objects view; cluster monitoring |
| vSAN | Component health; disk group management; resync queue |
| ESXi | Disk health via esxcli; disk group operations |
| VxRail Manager | Disk replacement wizard; iDRAC hardware event correlation |
| OMIVV (Dell) | Surfaces iDRAC hardware alerts as vCenter alarms |

---

## 1. Identify the Alarm — Skyline Health

Navigate to **vCenter → Cluster → Monitor → vSAN → Skyline Health**. A failing disk or absent component produces one or more red checks:

```text
Common red health checks and their meaning:
  Disk capacity utilisation  — overall capacity above threshold (>70% warn, >80% crit)
  vSAN disk balance          — uneven data distribution across disk groups
  Component health           — one or more components in Absent or Degraded state
  Disk group health          — disk group error; possible disk failure on cache or capacity tier
  Physical disk health       — SMART errors or disk returned hardware error
```

The **Virtual Objects** view (**vSAN → Monitor → Virtual Objects**) shows the per-VM impact. Filter by "Non-compliant" to see which VMs have a protection gap.

---

## 2. Identify the Failed Component

From Virtual Objects, expand a non-compliant VM to see its component map. Note:

- Which **host** the absent component lives on
- Which **disk group** (cache or capacity disk)
- Whether the component is **Absent** (disk gone) or **Degraded** (component needs rebuild but disk is present)

```bash
# List all vSAN objects and their health on the host
esxcli vsan debug object list | grep -E "UUID|Health|Host|Disk"

# List vSAN storage devices and disk group membership on the affected host
esxcli vsan storage list

# Identify which disk group is affected
esxcli vsan storage list | grep -E "DiskGroupUUID|SSD|Capacity|State"
```

---

## 3. Assess the Risk Window

Before touching anything, determine whether the cluster can tolerate another failure.

| FTT | Policy | Failures Tolerated | VM State with 1 Absent Component | Action |
|---|---|---|---|---|
| 1 | RAID-1 (mirroring) | 1 | Still compliant — 1 replica remains | Monitor; replace within maintenance window |
| 1 | RAID-5 (erasure coding) | 1 | Still compliant — parity intact | Monitor; do not remove another host |
| 2 | RAID-6 (erasure coding) | 2 | Still compliant after first failure | Monitor; urgent if second failure occurs |
| 1 | RAID-1 | 1 | Second component absent | Non-compliant — data risk; act immediately |

```text
Risk window = time between first failure and rebuild completion.
During this window, a second disk or host failure may cause data loss.
Do NOT put other hosts into maintenance mode during an active risk window.
```

---

## 4. Check Physical Disk Health

SSH to the affected ESXi host and interrogate the disk.

```bash
# List all storage devices visible to ESXi
esxcli storage core device list | grep -E "Display|State|Device"

# Check SMART health data for the specific device
# Replace naa.<device-id> with the actual NAA identifier from the list above
esxcli storage core device smart get -d naa.<device-id>

# Key SMART attributes to check:
# Reallocated Sector Count > 0    — sectors remapped; disk degrading
# Uncorrectable Sector Count > 0  — data loss risk
# SSD Wear Indicator < 5%         — flash near end of life
# Drive Temperature > 55°C        — thermal issue
```

For **VxRail** deployments, check iDRAC for hardware events before acting:

```bash
# SSH to iDRAC (or use web UI at https://<idrac-ip>)
# Check storage controller and physical disk alerts
racadm getsel | grep -i "storage\|disk\|drive"
```

OMIVV (OpenManage Integration for VMware vCenter) surfaces these as vCenter alarms. Check **vCenter → Alarms → Triggered Alarms** for any Dell hardware events correlated with the vSAN alert.

---

## 5. Initiate or Monitor Rebuild

**If the disk is physically failed:** replace it. vSAN automatically detects the new disk, adds it to the disk group, and begins rebuilding absent components.

**Do not manually re-add the disk** unless vSAN fails to claim it automatically (rare). Let vSAN handle discovery.

```bash
# Monitor resync progress from ESXi CLI
esxcli vsan debug resync summary get

# Output fields:
#   BytesToResync     — remaining data to rebuild
#   ResyncType        — REPAIR (failed component) / REBALANCE / POLICY_CHANGE
#   ObjectsToResync   — number of VM disk objects still rebuilding
#   ActiveResyncETA   — estimated completion time
```

In vCenter, go to **vSAN → Monitor → Resyncing Objects** for a visual view of the queue.

For VxRail, use **VxRail Manager → Maintenance → Disk Replacement** wizard. It:

1. Verifies the cluster has sufficient capacity before replacement
2. Guides through safe removal without triggering a second failure
3. Monitors rebuild progress post-replacement

---

## 6. PowerCLI — Disk Group and Health Queries

```powershell
# Get all disk groups for a specific ESXi host
Get-VsanDiskGroup -VMHost (Get-VMHost "esxi-host.domain.local") `
  | Format-List

# List all disks in each disk group with health status
Get-VsanDiskGroup -VMHost (Get-VMHost "esxi-host.domain.local") `
  | Get-VsanDisk | Select-Object DisplayName, State, Vendor, IsSsd

# Query cluster-level vSAN health summary via API
$vsanHealth = Get-VsanView -Id "VsanVcClusterHealthSystem-vsan-cluster-health-system"
$spec = New-Object VMware.Vimautomation.Storage.Impl.V1.VsanQueryVcClusterHealthSummarySpec
$vsanHealth.VsanQueryVcClusterHealthSummary($cluster.ExtensionData.MoRef, $null, $null, $true, $null, $null, "defaultView")
```

---

## Common Mistakes

- **Replacing a disk before checking whether another component is already absent.** If the cluster already has one absent component and you place the affected host in maintenance mode to replace the disk, you may create a second absent component — making some VMs non-compliant or causing data loss.
- **Not monitoring resync ETA before other maintenance.** Any host maintenance during an active resync reduces the protection level further. Always check resync queue first.
- **Confusing "Absent" with "Degraded."** Absent means the physical disk or host is gone — the component cannot serve reads or writes. Degraded means the component is present but needs to be rebuilt. The urgency is different.
- **Skipping iDRAC/OMIVV for VxRail.** vSAN may show a component absent before the iDRAC alarm fires. Checking both sources prevents misidentifying which physical disk to replace.

---

## Related Scenarios

- [VM Inaccessible / HA Failover](../vm-inaccessible-ha-failover/index.md) — Host failure produces the same vSAN resync queue as a disk failure; HA adds VM restart complexity.
- [VM Performance Degraded](../vm-performance-degraded/index.md) — Active vSAN resync increases disk latency for all VMs sharing the disk group, causing performance complaints.
- [vMotion Failing](../vmotion-failing/index.md) — DRS may attempt to evacuate VMs from a host with a degraded disk group; Storage vMotion failures can occur if vSAN components are non-compliant.
