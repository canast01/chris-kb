# Host Maintenance and Patching

<div class="kb-summary">
Host maintenance and patching is the most common planned task in VMware operations. Done correctly
it produces zero VM downtime — DRS vMotions all VMs off the host before any disruption occurs.
Done incorrectly it causes vSAN data unavailability, stuck resync queues, or VM outages. This
scenario covers the full procedure from pre-flight checks through post-patch validation.
</div>

```text
┌──────────────────────────────── Host Maintenance and Patching — Procedure Flow ───────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: Host requires patching — ESXi update, firmware, driver, or hardware maintenance                  ││
│   └────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                                                ▼                                                      │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Step 1 — Pre-maintenance checks: DRS enabled, HA enabled, vSAN health green, resync queue = 0          ││
│   └────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                                                ▼                                                      │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Step 2 — Evacuate VMs: Enter maintenance mode → DRS vMotions all running VMs off host automatically    ││
│   └────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                                                ▼                                                      │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Step 3 — vSAN maintenance mode: choose data migration option (Ensure Accessibility recommended)        ││
│   └────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                          ┌─────────────────────┼─────────────────────┐                                │
│                          ▼                     ▼                     ▼                                │
│            ┌─────────────────────┐  ┌──────────────────────┐  ┌─────────────────────┐                 │
│            │  LCM / VUM patch    │  │  esxcli manual patch │  │  Firmware / hardware│                 │
│            │  via vCenter LCM    │  │  (no LCM available)  │  │  — short outage only│                 │
│            └──────────┬──────────┘  └──────────┬───────────┘  └──────────┬──────────┘                 │
│                       └─────────────────────────┼──────────────────────────┘                          │
│                                                 ▼                                                     │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Step 4 — Reboot host → exits maintenance mode → DRS rebalances VMs back                                 ││
│   └────────────────────────────────────────────┬─────────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                                                ▼                                                      │
│   ┌──────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Step 5 — Post-patch validation: version confirmed, vSAN resync = 0, HA agent running                   ││
│   └──────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

```bash
# Confirm vSAN resync queue has drained back to 0 after maintenance
esxcli vsan debug resync summary get
```

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
