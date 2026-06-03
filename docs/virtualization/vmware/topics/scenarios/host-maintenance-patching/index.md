# Host Maintenance and Patching

<div class="kb-summary">
Host maintenance and patching is the most common planned task in VMware operations. Done correctly
it produces zero VM downtime — DRS vMotions all VMs off the host before any disruption occurs.
Done incorrectly it causes vSAN data unavailability, stuck resync queues, or VM outages. This
scenario covers the full procedure from pre-flight checks through post-patch validation.
</div>

```text
┌──────────────────────────────── Host Maintenance and Patching — Procedure Flow ─────────────────────────────────┐
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
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Before touching any host, confirm the cluster is in a healthy baseline state. Starting maintenance
on a degraded cluster can cause vSAN data unavailability or stacked failures.

```powershell
# Check cluster DRS and HA state
Get-Cluster "cluster-name" | Select Name, DrsEnabled, DrsAutomationLevel, HAEnabled

# Check vSAN cluster configuration (must show health: green before proceeding)
Get-VsanClusterConfiguration -Cluster (Get-Cluster "cluster-name")
```

```bash
# Check current vSAN resync queue — must be 0 bytes before entering maintenance
# Run from ESXi shell on any host in the cluster
esxcli vsan debug resync summary get
```

Check Aria Operations for any active critical or warning alerts on this host or its VMs before
proceeding. Any existing vSAN degradation, storage latency, or HA fault must be resolved first.

Minimum requirements to proceed:

| Check | Requirement |
|---|---|
| DRS mode | At least Partially Automated |
| HA state | Enabled and configured |
| vSAN health | All green in Skyline Health |
| vSAN resync queue | 0 bytes remaining |
| Aria Ops alerts | No critical alerts on the target host |

---

## 2. Evacuate VMs

Put the host into maintenance mode with full VM evacuation. DRS will vMotion all running VMs to
other hosts in the cluster automatically if DRS is at least Partially Automated.

```powershell
# PowerCLI — evacuate all VMs and enter maintenance mode
Get-VMHost "esxi-host.domain.local" | Set-VMHost -State Maintenance
```

From the vCenter UI: right-click the host → **Maintenance Mode** → **Enter Maintenance Mode** →
select **Move powered-off and suspended VMs to other hosts in the cluster** if applicable.

If DRS is Manual: vMotion each running VM individually before entering maintenance mode. Check
vCenter → Host → VMs tab to confirm zero powered-on VMs remain on the host before proceeding.

---

## 3. vSAN Maintenance Mode — Choose the Right Data Migration Option

When a host enters maintenance mode on a vSAN cluster, you must choose how vSAN handles the data
stored on that host's disk groups. The choice has a direct impact on data safety and how long
the maintenance mode transition takes.

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

In vCenter: **Lifecycle Manager** → select the host → **Remediate**. LCM places the host into
maintenance mode automatically (if not already there), applies the patch baseline, reboots, and
exits maintenance mode.

For VxRail nodes: use **VxRail Manager LCM**, not vCenter LCM directly. VxRail Manager ensures
the new ESXi version matches the VxRail bundle and that firmware, drivers, and vSAN configuration
are applied in the correct order. Using vCenter LCM directly on VxRail breaks the support matrix.

---

## 5. Manual Patch via esxcli (When LCM Is Not Available)

Upload the patch ZIP to a datastore first (via SFTP or vCenter datastore browser), then run from
the ESXi shell:

```bash
# Apply patch from a datastore path
esxcli software vib update -d /vmfs/volumes/<datastore>/patch.zip

# Confirm what was installed
esxcli software vib list | grep -i <patch-name>

# Ensure maintenance mode is active, then reboot
esxcli system maintenanceMode set --enable true
reboot
```

After reboot, the host will reconnect to vCenter. Confirm the host shows **Connected** and no
maintenance mode banner before proceeding.

---

## 6. Exit Maintenance Mode

After the reboot completes and the host reconnects to vCenter:

```powershell
# Exit maintenance mode via PowerCLI
Get-VMHost "esxi-host.domain.local" | Set-VMHost -State Connected
```

Or from the vCenter UI: right-click the host → **Maintenance Mode** → **Exit Maintenance Mode**.

DRS will rebalance VMs back to the host automatically if the cluster is Fully Automated. If DRS is
Partially Automated or Manual, review the DRS recommendations and apply them manually.

---

## 7. Post-Patch Validation

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

## Common Mistakes

- **Entering maintenance mode with No Data Migration before a reboot.** This leaves vSAN with zero
  redundancy on affected objects for the duration of the reboot. A second concurrent host failure
  causes data unavailability. Always use Ensure Accessibility for patching.
- **Starting maintenance with an active vSAN resync queue.** If the cluster is already resyncing
  when you enter maintenance, the resync will slow further or stall. Resolve any existing
  degradation before adding another host to maintenance.
- **Using vCenter LCM on VxRail nodes.** VxRail nodes must be patched through VxRail Manager to
  keep firmware, drivers, and ESXi in the validated bundle. LCM outside VxRail Manager breaks
  the support configuration.
- **Forgetting to check DRS mode.** If DRS is Manual, no automatic vMotion occurs. The host enters
  maintenance mode with VMs still running on it, which triggers HA failovers unnecessarily.

---

## Related Scenarios

- Capacity Planning
- vSAN Disk or Component Failure
- VxRail LCM Upgrade Failure
