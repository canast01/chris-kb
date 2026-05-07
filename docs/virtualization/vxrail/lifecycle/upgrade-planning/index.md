# VxRail Upgrade Procedure

VxRail upgrades include VMware software, Dell firmware, drivers, and VxRail-specific lifecycle validation. Use VxRail Manager and the approved upgrade bundle — do not treat a VxRail upgrade like a standard ESXi upgrade.

---
## Phase 1: Planning

### Capture Current State

Document:

- VxRail cluster name and version
- VxRail Manager version
- vCenter version
- ESXi version and vSAN version
- Node models and serial numbers
- Firmware bundle and driver versions
- Current alarms and open support cases

### Confirm Target Version

- Target VxRail version and upgrade path
- Internet-connected or offline upgrade method
- Expected upgrade duration
- Known issues for the target version
- Required Dell support engagement if any

### Review Release Notes

Check:

- Fixed and known issues
- Firmware and driver changes
- vCenter compatibility
- Required pre-checks
- Upgrade limitations

---

## Phase 2: Pre-Upgrade Health Checks

### VxRail Manager

- UI loads and communicates with vCenter
- Services healthy, certificate valid
- Enough disk space
- No failed prior upgrade tasks

### vCenter

- Login works, services healthy
- All hosts Connected, no unexpected maintenance mode
- HA and DRS healthy, no critical alarms

### vSAN Skyline Health

- Green — no failed disks, no inaccessible or degraded objects
- No unexpected resync, capacity within safe limits

### Hardware (Each Node)

- iDRAC reachable
- PSU, memory, CPU, fans, NICs, and disks healthy
- No predictive failures
- Firmware inventory available

### DNS, NTP, and Backup

- Forward and reverse DNS working for all nodes and vCenter
- NTP synchronized across all nodes
- vCenter backup completed
- Critical VM backups completed
- Backup team aware of maintenance

---

## Phase 3: Pre-Upgrade Support Bundle

Collect before starting:

- VxRail Manager support bundle
- vCenter, ESXi, vSAN, and iDRAC logs if issues exist

Save with standard name:

```
vxrail-support-bundle-CLUSTERNAME-YYYY-MM-DD.zip
```

---

## Phase 4: Upgrade Pre-Check

Run VxRail Manager pre-check.

If pre-check fails:

1. Capture failure message and detailed output
2. Do not start upgrade
3. Fix the known issue and re-run pre-check
4. Open a Dell support case if unclear
5. Attach support bundle if needed

---

## Phase 5: Upgrade Execution

### Start Upgrade

1. Upload or select upgrade bundle in VxRail Manager
2. Confirm target version and run validation
3. Accept upgrade plan and start upgrade
4. Monitor each stage

### Monitor Upgrade

Watch:

- VxRail Manager status and upgrade percentage
- vCenter tasks
- Host maintenance mode, firmware updates, and reboots
- vSAN resync activity
- Hardware alerts

### Node-by-Node Behavior

For each node:

1. Workloads migrate off node
2. Host enters maintenance mode
3. Firmware and software updated
4. Host reboots and reconnects
5. Host exits maintenance mode
6. Health validated
7. Upgrade moves to next node

### Do Not Interrupt

Do not reboot VxRail Manager, reboot hosts manually, cancel upgrade, restart services, make unrelated vCenter changes, or force remove hosts from maintenance mode — unless instructed by Dell support.

---

## Phase 6: Failed Upgrade Handling

If upgrade fails or gets stuck:

1. Capture exact error and screenshots
2. Review VxRail Manager status and vCenter tasks
3. Identify affected node
4. Check host maintenance mode state, vSAN health, and hardware alerts
5. Collect support bundle
6. Open Dell support case
7. Follow Dell recovery steps

> Do not guess on failed VxRail upgrades. The wrong action makes recovery harder.

---

## Phase 7: Post-Upgrade Validation

- VxRail Manager UI shows target version
- All hosts Connected
- vSAN Skyline Health green, no unexpected resyncs
- Hardware health clean, firmware matches baseline
- VMs running, DRS and HA healthy
- Backups working
- Monitoring tools receiving data

## Phase 8: Documentation

Update:

- Change ticket with upgrade start/end time and results
- VxRail, vCenter, ESXi, firmware, and driver versions
- Pre-check and post-check results
- Issues found and Dell case number if used
- Lessons learned
