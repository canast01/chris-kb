---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
---
# Host Disconnected / Not Responding

<div class="kb-summary">
Diagnosing ESXi hosts showing disconnected or not responding in vCenter — management network failures, HA isolation, hostd/vpxa agent issues, and reconnect procedures.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
quick_triage: "Quick Triage" {shape: rectangle}
host_disconnected_in_vcenter: "Host Disconnected in vCenter" {shape: rectangle}
management_agent_reset: "Management Agent Reset" {shape: rectangle}
management_network_down: "Management Network Down" {shape: rectangle}
host_not_responding_psod_or_hung_ker: "Host Not Responding (PSOD or Hung Kernel)" {shape: rectangle}
host_cannot_enter_maintenance_mode: "Host Cannot Enter Maintenance Mode" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> quick_triage: investigate
symptom -> host_disconnected_in_vcenter: investigate
symptom -> management_agent_reset: investigate
symptom -> management_network_down: investigate
symptom -> host_not_responding_psod_or_hung_ker: investigate
symptom -> host_cannot_enter_maintenance_mode: investigate
quick_triage -> resolution
host_disconnected_in_vcenter -> resolution
management_agent_reset -> resolution
management_network_down -> resolution
host_not_responding_psod_or_hung_ker -> resolution
host_cannot_enter_maintenance_mode -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Quick Triage

First, establish whether the host is truly unreachable or just disconnected in vCenter.

```bash
# Ping the host management IP from your workstation or jump host
ping <esxi-mgmt-ip>

# Try SSH directly — if this works, the host is up and it's a vCenter-to-host agent issue
ssh root@<esxi-mgmt-ip>

# Check DNS resolution for the host FQDN
nslookup <esxi-fqdn>
```

If ping works but vCenter shows "Not Responding", skip to [Management Agent Reset](#management-agent-reset).

If ping fails entirely, skip to [Management Network Down](#management-network-down).

---

## Host Disconnected in vCenter

The host is reachable but vCenter has lost its agent connection (vpxa). Common causes: vpxa crash, certificate mismatch, or a vCenter restart while the host was isolated.

**Step 1 — Right-click the host in vCenter → Connect.** If this resolves it immediately, the connection was dropped by a transient event.

**Step 2 — If reconnect fails**, SSH to the host and check services:

```bash
# Check vpxa and hostd status
/etc/init.d/vpxa status
/etc/init.d/hostd status

# Restart vpxa (the vCenter agent — safe to restart, no VM impact)
/etc/init.d/vpxa restart

# If vpxa alone does not fix it, restart hostd too
/etc/init.d/hostd restart

# Check for errors in logs
tail -100 /var/log/vpxa.log
tail -100 /var/log/hostd.log
```

**Step 3 — Re-add the host in vCenter** if the agent restart does not help. In vCenter, right-click the host → Disconnect → Remove from Inventory → Re-add with Add Host wizard.

---

## Management Agent Reset

Use this when the host is reachable over the network but management services are unresponsive or looping.

```bash
# Full management agent restart (safe — does not affect running VMs)
services.sh restart

# Or restart individual services
/etc/init.d/hostd restart
/etc/init.d/vpxa restart
/etc/init.d/ntpd restart

# Verify services are running
services.sh status | grep -E "hostd|vpxa|ntpd"

# Check for stuck or looping processes
ps -c | grep hostd
ps -c | grep vpxa
```

If hostd is repeatedly crashing, check disk space — a full `/` or `/scratch` partition prevents hostd from writing its state file:

```bash
df -h
vdf -h
```

---

## Management Network Down

The host is not reachable at all. Check in this order:

1. **Physical layer** — Is the management NIC connected? Check iDRAC/iLO for NIC link state.
2. **VLAN configuration** — Was a switch or port-group change recently made?
3. **IP configuration** — Verify via iDRAC/iLO console or direct keyboard/monitor:

```bash
# From ESXi direct console (DCUI) — check VMkernel adapter
esxcli network ip interface list
esxcli network ip interface ipv4 get -i vmk0

# Check default gateway
esxcli network ip route list

# Verify basic network reachability
esxcli network diag ping -H <vcenter-ip>
```

4. **Firewall** — Confirm the management VLAN firewall rules allow TCP 443, 902, and 8080 from vCenter to the host.

---

## Host Not Responding (PSOD or Hung Kernel)

A "Not Responding" state that persists after network checks usually means the host kernel has halted (PSOD — Purple Screen of Death) or the host is completely hung.

1. Open **iDRAC/iLO virtual console** — if you see a purple screen with a backtrace, the host has crashed.
2. Capture a photo of the PSOD (contains crash address and module name — needed for VMware GSS).
3. If the PSOD does not auto-reboot: trigger a hard reset via iDRAC/iLO.
4. After reboot, collect the **vm-support bundle** before further investigation:

```bash
# Generate support bundle from host
vm-support -w /tmp
# SCP the bundle off before it is potentially overwritten by another crash
```

5. Review `/var/log/vmkernel.log` and `/var/log/vobd.log` for hardware errors preceding the crash.

---

## Host Cannot Enter Maintenance Mode

Common blockers and resolutions:

| Blocker | Check | Resolution |
|---|---|---|
| Running VMs cannot be migrated | DRS disabled or VMs pinned | Enable DRS or manually vMotion VMs first |
| vSAN evacuation failing | Insufficient vSAN capacity | Ensure cluster can absorb evacuated objects; check vSAN health |
| Template or ISO locked to host | Storage affinity rules | Move templates to a shared datastore not tied to the host |
| HA reconfiguration pending | HA agent failure | Reconfigure HA on the cluster before placing host in maintenance |
| Witness appliance on host | Cannot evacuate witness | Handle witness in its own maintenance window |

```powershell
# Check which VMs are on the host
Get-VMHost "esxi-host-fqdn" | Get-VM | Select Name, PowerState

# Force maintenance mode without vMotion (only if VMs are confirmed powered off)
Set-VMHost "esxi-host-fqdn" -State Maintenance -Evacuate $false
```

---

## Host Hardware Warning

Hardware alerts surface as vCenter alarms (yellow/red) on the host object. Correlate with the physical hardware management console.

```bash
# Check hardware health from ESXi CLI
esxcli hardware platform get
esxcli hardware memory get
esxcli hardware cpu list

# Check physical disk health
esxcli storage hba list

# Review system event log for hardware errors
vim-cmd hostsvc/firmware/sync_config
```

From iDRAC/iLO, review:
- PSU status
- Memory DIMM errors
- Physical disk and RAID state
- NIC link state
- Thermal / fan status

---

## Host NTP Drift

Certificate validation, HA heartbeats, and vSAN all depend on time sync. A drifting host can cause cascading issues.

```bash
# Check NTP status on ESXi
esxcli system ntp get
ntpq -p

# If NTP is not configured, set it
esxcli system ntp set --server <ntp-server-ip>
esxcli system ntp set --enabled true

# Force time sync immediately
/etc/init.d/ntpd restart

# Verify sync — look for * or + prefix next to a time source
ntpq -p
```

Hosts more than 5 minutes out of sync with vCenter will trigger authentication errors and HA isolation warnings.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificate Issues](certificate-issue.md)
- [Datastore Issues](datastore-inaccessible.md)
- [Known Issues and Fix Patterns](known-issues.md)
- [Virtualization Troubleshooting](index.md)
