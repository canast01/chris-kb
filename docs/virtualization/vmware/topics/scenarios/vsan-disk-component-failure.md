---
tags:
  - scenarios
  - vmware
  - vsan
  - vsphere-8
---
# vSAN Disk or Component Failure

<div class="kb-summary">
A vSAN disk fails or a component becomes absent, leaving one or more VMs with reduced fault tolerance.
This scenario covers how to identify the failed component, assess the risk window based on FTT policy,
initiate or monitor rebuild after disk replacement, and use VxRail Manager for hardware-assisted workflows
on HCI deployments.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_identify_the_alarm_skyline_health: "1. Identify the Alarm — Skyline Health" {shape: rectangle}
2_identify_the_failed_component: "2. Identify the Failed Component" {shape: rectangle}
3_assess_the_risk_window: "3. Assess the Risk Window" {shape: rectangle}
4_check_physical_disk_health: "4. Check Physical Disk Health" {shape: rectangle}
5_initiate_or_monitor_rebuild: "5. Initiate or Monitor Rebuild" {shape: rectangle}

products_involved -> 1_identify_the_alarm_skyline_health: uses
1_identify_the_alarm_skyline_health -> 2_identify_the_failed_component: uses
2_identify_the_failed_component -> 3_assess_the_risk_window: uses
3_assess_the_risk_window -> 4_check_physical_disk_health: uses
4_check_physical_disk_health -> 5_initiate_or_monitor_rebuild: uses
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

Navigate to **vCenter → Cluster → Monitor → vSAN → Skyline Health** to find the specific failing check before touching any disk.

```text
Common red health checks and their meaning:
  Disk capacity utilisation  — overall capacity above threshold (>70% warn, >80% crit)
  vSAN disk balance          — uneven data distribution across disk groups
  Component health           — one or more components in Absent or Degraded state
  Disk group health          — disk group error; possible disk failure on cache or capacity tier
  Physical disk health       — SMART errors or disk returned hardware error
```

Look for: the **Virtual Objects** view (**vSAN → Monitor → Virtual Objects**) filtered by "Non-compliant" shows exactly which VMs have a live protection gap.

---

## 2. Identify the Failed Component

Expand a non-compliant VM in Virtual Objects to see its component map, then correlate with CLI output to confirm which disk.

```bash
# List all vSAN objects and their health on the host
esxcli vsan debug object list | grep -E "UUID|Health|Host|Disk"

# List vSAN storage devices and disk group membership on the affected host
esxcli vsan storage list

# Identify which disk group is affected
esxcli vsan storage list | grep -E "DiskGroupUUID|SSD|Capacity|State"
```


```text title="Expected output"
UUID: 52e3f4a1-8c2d-4f9e-b1a2-7d6c9e3f2a1b
Health: Healthy
Host: esx-prod-01.lab.local
Disk: naa.6001405a1b2c3d4e5f6a7b8c9d0e1f2a

UUID: 62f4g5b2-9d3e-5g0f-c2b3-8e7d0f4g3b2c
Health: Degraded
Host: esx-prod-01.lab.local
Disk: naa.6001405a1b2c3d4e5f6a7b8c9d0e1f2b

UUID: 73g5h6c3-0e4f-6h1g-d3c4-9f8e1g5h4c3d
Health: Healthy
Host: esx-prod-01.lab.local
Disk: naa.6001405a1b2c3d4e5f6a7b8c9d0e1f2c

DiskGroupUUID: 84h6i7d4-1f5g-7i2h-e4d5-0g9f2h6i5d4e
SSD: naa.6001405a1b2c3d4e5f6a7b8c9d0e1f2d
Capacity: 1.7 TB
State: Healthy

DiskGroupUUID: 95i7j8e5-2g6h-8j3i-f5e6-1h0g3i7j6e5f
SSD: naa.6001405a1b2c3d4e5f6a7b8c9d0e1f2e
Capacity: 1.7 TB
State: Degraded
```

!!! warning "Common errors"
    **`esxcli: Unknown command or namespace vsan`** — Verify vSAN is licensed and enabled on the host by running `esxcli vsan cluster get`.
    **`grep: (standard input) is empty`** — Confirm the host is part of a vSAN cluster and has vSAN enabled with `esxcli vsan cluster get`.
Look for: note which host the absent component lives on, which disk group it belongs to, and whether the state is `Absent` (disk gone) or `Degraded` (disk present but component needs rebuild).

---

## 3. Assess the Risk Window

Before touching anything, determine whether the cluster can survive another failure during the rebuild.

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

SSH to the affected ESXi host to confirm whether the disk has truly failed or is merely disconnected before ordering a replacement.

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


```text title="Expected output"
Display Name: Local ATA Disk mpx.vmhba0:C0:T0:L0
State: Online
Device: naa.5001b1a9b3c4d5e6

Display Name: SAS Disk mpx.vmhba1:C0:T1:L0
State: Online
Device: naa.6002ac0000a1b2c3d4e5f6g7

Display Name: NVMe Device mpx.vmhba2:C0:T2:L0
State: Online
Device: naa.55cd2e404bd2e11e

SMART Health Data for Device naa.5001b1a9b3c4d5e6:
Parameter: Reallocated Sector Count
Value: 8
Threshold: 36
Status: OK

Parameter: Uncorrectable Sector Count
Value: 0
Threshold: 0
Status: OK

Parameter: SSD Wear Indicator
Value: 78
Threshold: 10
Status: OK

Parameter: Drive Temperature
Value: 42
Threshold: 60
Status: OK
```

!!! warning "Common errors"
    **`Error: Could not retrieve SMART data for device naa.<device-id>`** — Verify the NAA identifier is correct by copying it directly from the device list output and ensure the device supports SMART queries.
    **`Error: Unknown option or syntax error in esxcli command`** — Check your ESXi version supports the `esxcli storage core device smart` command (requires ESXi 6.5+); use `esxcli storage core device list` alone if unavailable.
For VxRail deployments, check iDRAC before acting — OMIVV surfaces hardware events as vCenter alarms:

```bash
# SSH to iDRAC (or use web UI at https://<idrac-ip>)
racadm getsel | grep -i "storage\|disk\|drive"
```


```text title="Expected output"
SEL Records:
   1 | 01/15/2024 | 14:32:45 | Storage | Physical Disk 0 in Slot 1 | Predictive Failure
   2 | 01/15/2024 | 14:35:12 | Storage | RAID Controller 0 | Battery Learn Cycle Started
   3 | 01/16/2024 | 09:18:33 | Disk | Physical Disk 2 in Slot 3 | Drive Online
   4 | 01/16/2024 | 11:45:22 | Storage | Virtual Disk 1 | Rebuild in Progress
   5 | 01/17/2024 | 16:22:10 | Drive | Hot Spare Activated | Slot 4
```

!!! warning "Common errors"
    **`racadm: command not found`** — Install Dell OMECLI tools or use the iDRAC web UI at https://<idrac-ip> instead.
    **`DRAC001: Authentication failed`** — Verify iDRAC credentials and ensure your user account has sufficient permissions to query system event logs.
Look for: cross-reference **vCenter → Alarms → Triggered Alarms** for any Dell OMIVV alarm correlated with the vSAN alert to confirm the physical disk identity.

---

## 5. Initiate or Monitor Rebuild

Replace the failed disk — vSAN automatically detects the new disk and begins rebuilding absent components; do not manually re-add it.

```bash
# Monitor resync progress from ESXi CLI
esxcli vsan debug resync summary get

# Output fields:
#   BytesToResync     — remaining data to rebuild
#   ResyncType        — REPAIR (failed component) / REBALANCE / POLICY_CHANGE
#   ObjectsToResync   — number of VM disk objects still rebuilding
#   ActiveResyncETA   — estimated completion time
```


```text title="Expected output"
BytesToResync: 2147483648
ResyncType: REPAIR
ObjectsToResync: 42
ActiveResyncETA: 2h 15m
ResyncStartTime: 2024-01-15T09:32:14Z
ResyncEndTime: 2024-01-15T11:47:14Z
CurrentResyncRate: 16.8 MB/s
PendingResyncObjects: 12
CompletedResyncObjects: 30
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace path vsan/debug/resync/summary.`** — Verify VSAN is licensed and enabled on the cluster; run `esxcli vsan cluster get` to confirm VSAN status first.
    **`Error: Permission denied.`** — Ensure you are logged in with root or an account with VSAN administration privileges; use `esxcli system permission list` to verify your role.
Look for: `ResyncType = REPAIR` with decreasing `BytesToResync` confirms rebuild is in progress. For VxRail, use **VxRail Manager → Maintenance → Disk Replacement** wizard — it verifies cluster capacity before removal and monitors rebuild post-replacement.

---

## 6. PowerCLI — Disk Group and Health Queries

Pull disk group and cluster health state programmatically for post-replacement validation.

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

## Key Terms

| Term | Definition |
|---|---|
| vSAN | VMware's hyperconverged storage layer that pools local disks across cluster hosts into a shared datastore; data is distributed as objects and components across hosts |
| OSA | Original Storage Architecture — the vSAN disk group model using a dedicated cache disk (SSD) plus capacity disks; used in vSAN 7 and earlier by default |
| ESA | Express Storage Architecture — vSAN 8+ all-NVMe model that eliminates the cache tier; each disk contributes directly to both capacity and performance |
| FTT | Failures to Tolerate — the SPBM policy attribute that defines how many simultaneous host or disk failures a VM's data can survive; determines the minimum host count required |
| RAID-1 | vSAN mirroring protection; writes N+1 full copies of each object across different fault domains; FTT=1 RAID-1 requires 3 hosts and uses 2x capacity overhead |
| RAID-5 | vSAN erasure coding for FTT=1; distributes data + parity across 4 hosts; uses 1.33x capacity overhead compared to RAID-1's 2x |
| Disk group | OSA grouping of one cache SSD plus 1–7 capacity disks on a single ESXi host; all capacity disks in the group share the cache tier |
| Component | The smallest unit of a vSAN object; a single VM disk (VMDK) is split into one or more components distributed across different hosts according to the FTT policy |
| Resync | The rebuild process vSAN runs after a disk or host failure to recreate absent components on surviving hosts and restore the configured FTT level |
| SPBM | Storage Policy-Based Management — vSphere framework where VM storage rules (FTT, RAID level, encryption) are defined as policies and applied per VM or VMDK |
| Skyline Health | The vSAN health monitoring dashboard in vCenter; runs continuous health checks across disk, capacity, network, and cluster configuration categories |
| OMIVV | OpenManage Integration for VMware vCenter — Dell plugin that forwards iDRAC hardware alerts (disk failures, SMART errors) into vCenter as native alarms |
| iDRAC | Integrated Dell Remote Access Controller — out-of-band management interface on Dell servers; provides hardware-level disk and controller event logs independent of the OS |

---

## Common Mistakes

- **Replacing a disk before checking whether another component is already absent.** If the cluster already has one absent component and you place the affected host in maintenance mode to replace the disk, you may create a second absent component — making some VMs non-compliant or causing data loss.
- **Not monitoring resync ETA before other maintenance.** Any host maintenance during an active resync reduces the protection level further. Always check resync queue first.
- **Confusing "Absent" with "Degraded."** Absent means the physical disk or host is gone — the component cannot serve reads or writes. Degraded means the component is present but needs to be rebuilt. The urgency is different.
- **Skipping iDRAC/OMIVV for VxRail.** vSAN may show a component absent before the iDRAC alarm fires. Checking both sources prevents misidentifying which physical disk to replace.

---

## Related Scenarios

- [VM Inaccessible / HA Failover](vm-inaccessible-ha-failover.md) — Host failure produces the same vSAN resync queue as a disk failure; HA adds VM restart complexity.
- [VM Performance Degraded](vm-performance-degraded.md) — Active vSAN resync increases disk latency for all VMs sharing the disk group, causing performance complaints.
- [vMotion Failing](vmotion-failing.md) — DRS may attempt to evacuate VMs from a host with a degraded disk group; Storage vMotion failures can occur if vSAN components are non-compliant.
