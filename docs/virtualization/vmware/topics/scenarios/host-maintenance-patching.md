---
tags:
  - scenarios
  - vmware
description: "Host maintenance and patching is the most common planned task in VMware operations. Done correctly it produces zero VM downtime — DRS vMotions all VMs off..."
---
# Host Maintenance and Patching

<div class="kb-summary">
Host maintenance and patching is the most common planned task in VMware operations. Done correctly
it produces zero VM downtime — DRS vMotions all VMs off the host before any disruption occurs.
Done incorrectly it causes vSAN data unavailability, stuck resync queues, or VM outages. This
scenario covers the full procedure from pre-flight checks through post-patch validation.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_premaintenance_checks: "1. Pre-Maintenance Checks" {shape: rectangle}
2_evacuate_vms: "2. Evacuate VMs" {shape: rectangle}
3_vsan_maintenance_mode_choose_the_r: "3. vSAN Maintenance Mode — Choose the Right Data\nMigration O" {shape: rectangle}
4_apply_patches_via_lifecycle_manage: "4. Apply Patches via Lifecycle Manager" {shape: rectangle}
5_manual_patch_via_esxcli_when_lcm_i: "5. Manual Patch via esxcli (When LCM Is Not Available)" {shape: rectangle}

products_involved -> 1_premaintenance_checks: uses
1_premaintenance_checks -> 2_evacuate_vms: uses
2_evacuate_vms -> 3_vsan_maintenance_mode_choose_the_r: uses
3_vsan_maintenance_mode_choose_the_r -> 4_apply_patches_via_lifecycle_manage: uses
4_apply_patches_via_lifecycle_manage -> 5_manual_patch_via_esxcli_when_lcm_i: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter Server | Maintenance mode entry, DRS automation, inventory visibility during patching |
| ESXi | The host being patched; receives updates and reboots |
| vSAN | Data migration during maintenance mode; resync monitoring before and after |
| Lifecycle Manager (LCM) / VUM | Patch baseline management and remediation orchestration |
| Aria Operations | Pre-maintenance alert check; post-patch health validation |

---

## 1. Pre-Maintenance Checks

Confirm the cluster is in a healthy baseline state before touching any host.

```powershell
# Check cluster DRS and HA state
Get-Cluster "cluster-name" | Select Name, DrsEnabled, DrsAutomationLevel, HAEnabled

# Check vSAN cluster configuration (must show health: green before proceeding)
Get-VsanClusterConfiguration -Cluster (Get-Cluster "cluster-name")
```

```bash
# Check current vSAN resync queue — must be 0 bytes before entering maintenance
esxcli vsan debug resync summary get
```


```text title="Expected output"
Cluster UUID: 52d4a8f1-2e3c-4d5a-9c1b-7f8e9a0b1c2d
Resync Queue Size: 0 B
Resync Queue Objects: 0
Resync Queue Congestion: 0%
Last Updated: 2024-01-15 14:32:18 UTC
Node: esx-host-04.lab.local
```

!!! warning "Common errors"
    **`Unknown command or namespace vsan debug resync summary get`** — Verify vSAN is licensed and enabled on the cluster; run `esxcli vsan cluster get` first to confirm vSAN status.
    **`Error: Unable to connect to Management Agent on localhost`** — Restart the hostd service with `systemctl restart hostd` and wait 30 seconds before retrying.
Expected: resync queue output shows 0 bytes remaining on all components.

| Check | Requirement |
|---|---|
| DRS mode | At least Partially Automated |
| HA state | Enabled and configured |
| vSAN health | All green in Skyline Health |
| vSAN resync queue | 0 bytes remaining |
| Aria Ops alerts | No critical alerts on the target host |

---

## 2. Evacuate VMs

Put the host into maintenance mode — DRS will vMotion all running VMs off automatically.

```powershell
# PowerCLI — evacuate all VMs and enter maintenance mode
Get-VMHost "esxi-host.domain.local" | Set-VMHost -State Maintenance
```

Expected: host transitions to Maintenance state with zero powered-on VMs remaining.

If DRS is Manual: vMotion each running VM individually before entering maintenance mode. Check
vCenter → Host → VMs tab to confirm zero powered-on VMs remain on the host before proceeding.

---

## 3. vSAN Maintenance Mode — Choose the Right Data Migration Option

When entering maintenance mode on a vSAN cluster, select the data migration option that matches the maintenance type.

| Option | Data movement | Time to enter | When to use |
|---|---|---|---|
| Ensure Accessibility | Migrates data so at least 1 accessible copy remains on other hosts | Fast | Standard patching — recommended default |
| Full Data Migration | Moves all data off this host to other hosts | Slow | Extended maintenance, host replacement, suspected disk failure |
| No Data Migration | Leaves data in place — no movement | Instant | BIOS update, NIC swap under 30 minutes maximum |

**Do not use No Data Migration for patching.** Patching requires a reboot. During the reboot,
vSAN has zero redundancy for objects with components on that host. A second host failure during
that window causes data unavailability.

---

## 4. Apply Patches via Lifecycle Manager

Remediate the host through vCenter LCM — it handles maintenance mode entry, patch application, and reboot automatically.

In vCenter: **Lifecycle Manager** → select the host → **Remediate**.

For VxRail nodes: use **VxRail Manager LCM**, not vCenter LCM directly. VxRail Manager ensures
the new ESXi version matches the VxRail bundle and that firmware, drivers, and vSAN configuration
are applied in the correct order. Using vCenter LCM directly on VxRail breaks the support matrix.

---

## 5. Manual Patch via esxcli (When LCM Is Not Available)

Upload the patch ZIP to a datastore first, then apply from the ESXi shell.

```bash
# Apply patch from a datastore path
esxcli software vib update -d /vmfs/volumes/<datastore>/patch.zip

# Confirm what was installed
esxcli software vib list | grep -i <patch-name>

# Ensure maintenance mode is active, then reboot
esxcli system maintenanceMode set --enable true
reboot
```


```text title="Expected output"
Installation Result
   Message: The update completed successfully, but the system needs to be rebooted for the changes to take effect.
   Reboot Required: true
   VIBs Installed: esx-base-6.7.0-20231015.0.0.0.official-patch-ESXi670-202310b1
   VIBs Removed: esx-base-6.7.0-20230915.0.0.0.official-patch-ESXi670-202309b1

Name                                    Version                       Vendor   Status Install Date
esx-base-6.7.0-20231015.0.0.0.official  6.7.0-20231015.0.0.0.official VMware   CommunitySupported 2023-10-15

Entering maintenance mode...
(no output — command completes silently)
Rebooting...
```

!!! warning "Common errors"
    **`VIB Integ Error: (1) Requires: esx-base >= 6.7.0-20230101.0.0.0.official`** — Verify the patch is compatible with your current ESXi version using `esxcli system version get`.
    **`Error: Could not find a local VMFS volume at path /vmfs/volumes/<datastore>/patch.zip`** — Confirm the datastore name and patch filename are correct, and that the file exists using `ls -la /vmfs/volumes/<datastore>/`.
    **`Error: The host is not in maintenance mode. Please enter maintenance mode before installing VIBs.`** — Enable maintenance mode with `esxcli system maintenanceMode set --enable true` before running the update command.
Expected: host reconnects to vCenter after reboot showing **Connected** with no maintenance mode banner.

---

## 6. Exit Maintenance Mode

After reboot and vCenter reconnection, exit maintenance mode to allow DRS to rebalance VMs.

```powershell
# Exit maintenance mode via PowerCLI
Get-VMHost "esxi-host.domain.local" | Set-VMHost -State Connected
```

Expected: host state changes to Connected; DRS begins rebalancing VMs back to the host.

---

## 7. Post-Patch Validation

Confirm version, vSAN disk groups, HA agent, and resync queue after returning the host to service.

```bash
# Verify ESXi version matches the target patch level
esxcli system version get

# Verify vSAN disk groups are present and healthy
esxcli vsan storage list

# Confirm HA agent (fdm) is running — required for HA to protect VMs on this host
/etc/init.d/vmware-fdm status
```


```text title="Expected output"
Product: VMware ESXi
   Version: 7.0.3
   Build: 19482537
   Update: 3
   Patch: ESXi700-202301001

ClusterUUID: 52d4a8f1-7c2e-4a9b-b1e3-9f2c8d1a5b3c
NodeUUID: 7a3c9e2f-1b4d-8c5a-6e9f-2d1a4b8c3e5f
DiskGroupUUID: 4f2e1a9c-3b5d-7e8a-1f4c-6b9d2a5e3c1f
State: healthy
Capacity: 1.8 TB
Used: 847 GB
Reserved: 92 GB

vmware-fdm (pid 2847) is running
```

!!! warning "Common errors"
    **`esxcli: command not found`** — Ensure you are running this command directly on the ESXi host console or via SSH with root privileges, not from a vCenter management station.
    **`State: degraded`** — Run `esxcli vsan storage list` to identify failed disks and replace or re-seat the affected storage device.
    **`vmware-fdm (pid XXXX) is stopped`** — Restart the HA agent with `/etc/init.d/vmware-fdm start` and verify cluster membership in vCenter.
```bash
# Confirm vSAN resync queue has drained back to 0 after maintenance
esxcli vsan debug resync summary get
```


```text title="Expected output"
Resync Queue Summary
====================
Queue Name                          Pending Objects    Bytes Remaining
-----------                         ---------------    ---------------
Data                                0                  0 B
Metadata                            0                  0 B
Total Resync Operations             0                  0 B
Last Updated                        2024-01-15 14:32:18 UTC
Cluster Resync Status               Completed
Average Resync Rate                 125.4 MB/s
```

!!! warning "Common errors"
    **`Unknown command at path esxcli vsan debug resync summary get`** — Verify the ESXi host is vSAN-enabled and the vSAN service is running with `systemctl status vsand`.
    **`Error: Unable to connect to the vSAN cluster`** — Ensure the host is part of an active vSAN cluster and network connectivity exists between cluster nodes.
Expected: version string matches target patch, all disk groups listed, fdm reports running, resync = 0 bytes.

---

## Post-Task Validation

| Check | Command / Location | Expected Result |
|---|---|---|
| Host connected to vCenter | vCenter inventory | Connected, no warnings |
| ESXi version updated | `esxcli system version get` | Target patch version string |
| vSAN resync complete | `esxcli vsan debug resync summary get` | 0 bytes remaining |
| HA agent running | `/etc/init.d/vmware-fdm status` | Running |
| VMs redistributed | vCenter → Cluster → DRS → Faults | No DRS faults |
| Aria Ops alerts | Aria Operations → Alerts | No new alerts since maintenance |

---

## Key Terms

| Term | Definition |
|---|---|
| DRS | Distributed Resource Scheduler — vCenter feature that automatically vMotions VMs across hosts to balance CPU and memory load; required for automated VM evacuation during maintenance mode |
| HA | High Availability — vCenter cluster feature that restarts VMs on surviving hosts after a host failure; must be enabled before entering maintenance to ensure protection during the patching window |
| vSAN maintenance mode | A vSAN-specific state layered on top of ESXi maintenance mode that governs how vSAN handles data stored on the host's disk groups before the host goes offline |
| Ensure Accessibility | vSAN data migration option that moves enough data components off the host so every object retains at least one accessible copy on the remaining hosts — recommended for standard patching |
| Full Data Migration | vSAN data migration option that moves all data off the host to other hosts before entering maintenance; slowest option but safest for extended maintenance or suspected disk faults |
| No Data Migration | vSAN data migration option that leaves all data in place; instant entry but leaves zero redundancy for affected objects during a reboot — unsafe for any patching that requires a reboot |
| FDM | Fault Domain Manager — the HA agent process running on each ESXi host that communicates host liveness to vCenter; must be running post-patch for HA to protect VMs on that host |
| LCM | Lifecycle Manager — vCenter component (formerly vSphere Update Manager/VUM) that manages patch baselines, desired state images, and orchestrates host remediation including maintenance mode entry and reboot |
| VUM | vSphere Update Manager — the legacy name for Lifecycle Manager prior to vSphere 7; functionally equivalent for patch baseline management and remediation |
| VxRail LCM | Dell VxRail-specific lifecycle management workflow embedded in VxRail Manager that validates firmware, driver, and ESXi bundle alignment before applying patches to VxRail nodes |
| resync queue | The backlog of vSAN data components that need to be rebuilt or resynced across hosts after a failure or maintenance event; must be 0 bytes before entering maintenance on any additional host |
| vMotion | Live migration of a running VM from one ESXi host to another with no downtime; the mechanism DRS uses to evacuate VMs from a host entering maintenance mode |
