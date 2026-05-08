# PowerPath — Common Issues

## Incident Triage

When a host reports I/O errors, elevated latency, or a block device is inaccessible, work through this sequence first.

- [ ] Run `powermt display dev=all` on the affected host immediately — identify which pseudo devices have dead paths and how many paths remain alive for each
- [ ] Check the PowerPath policy: `powermt display options` — if policy shows `BasicFailover` instead of `CLAROpt`, load balancing is degraded; investigate license and run `powermt config`
- [ ] Run `powermt restore` to instruct PowerPath to retry all paths currently marked dead — this alone resolves transient path losses caused by brief fabric events
- [ ] Check HBA port states: `powermt display ports class=all` — a port in `dead` state indicates the HBA itself has lost fabric connectivity, not just individual paths
- [ ] Review host OS logs for the path failure timestamp: `grep -i "powermt\|path\|dead" /var/log/messages` — correlate with fabric switch events
- [ ] Check the SAN fabric switch: confirm the affected HBA WWN and storage array port are still zoned and active; look for CRC errors or port login/logout events on the switch
- [ ] If paths are dead and `powermt restore` does not recover them, confirm the array-side LUN masking is intact — check the masking view or storage view on the array
- [ ] Run `powermt check_registration` if paths show `unlic` state — a license issue will cause PowerPath to drop management of devices after a license check failure

| Question | Answer |
|---|---|
| Which pseudo devices have dead paths? | |
| How many paths remain alive per device? | |
| What is the current load balancing policy? | |
| Are any HBA ports in dead state? | |
| Did powermt restore recover any dead paths? | |

---

## Dead Paths After Reboot

**Symptom:** One or more paths show `dead` immediately after a host reboots, even though the SAN fabric was not changed.

**Cause:** On some Linux kernels and HBA driver combinations, the HBA ports finish logging into the fabric after the PowerPath daemon has already performed its initial path check. PowerPath marks paths dead if the LIP (Loop Initialization Protocol) or PLOGI has not yet completed at scan time.

**Resolution:**

```bash
# 1. Confirm how many dead paths exist
powermt display dev=all | grep -c dead

# 2. Attempt path restore — usually resolves this immediately
powermt restore

# 3. Verify dead path count drops to zero
powermt display dev=all | grep -c dead

# 4. If paths remain dead, check HBA port login state
systool -c fc_host -v | grep -E "port_name|port_state|speed"

# 5. If HBA ports show 'Online', check fabric zoning is still intact
# (Brocade)
switchshow

# 6. Once resolved, save to persist state
powermt save
```

**Prevention:** Add a post-boot `powermt restore` to the startup sequence via a systemd oneshot service or rc.local equivalent, executed after the PowerPath service is confirmed running.

---

## Paths Not Recovering After SAN Maintenance

**Symptom:** SAN maintenance (switch port replacement, cable swap, or array port maintenance) is complete but paths remain in `dead` state on affected hosts.

**Cause:** PowerPath marks a path `dead` when it fails I/O tests. Once marked dead, PowerPath retries dead paths on a timer, but this timer may not have fired yet. `powermt restore` forces an immediate retry.

**Resolution:**

```bash
# 1. Run powermt restore to force immediate path retry
powermt restore

# 2. Wait 30 seconds and check
powermt display dev=all | grep dead

# 3. If paths still dead, trigger a SAN HBA rescan to refresh fabric login
echo "1" > /sys/class/fc_host/host0/issue_lip
echo "1" > /sys/class/fc_host/host1/issue_lip

# 4. Run powermt config to pick up any newly visible paths
powermt config

# 5. Run powermt restore again
powermt restore

# 6. Verify path count per device
powermt display dev=all
```

If paths still do not recover after the above steps, escalate to the SAN team to confirm the switch port and array FA port are fully online and zoned correctly.

---

## Device Not Visible After LUN Provisioning

**Symptom:** A new LUN has been provisioned and masked to the host on the array, but it does not appear in `powermt display dev=all`.

**Cause:** PowerPath only discovers devices that are visible to the OS HBA layer. If the OS has not rescanned for new devices, PowerPath cannot discover them.

**Resolution:**

```bash
# 1. Force an HBA-level rescan on Linux (Fibre Channel)
# Repeat for each HBA host adapter index (host0, host1, host2, etc.)
echo "- - -" > /sys/class/scsi_host/host0/scan
echo "- - -" > /sys/class/scsi_host/host1/scan

# On RHEL/OEL systems, use the rescan-scsi-bus utility if available
/usr/bin/rescan-scsi-bus.sh

# 2. Run powermt config to discover newly visible devices
powermt config

# 3. Confirm the new device appears
powermt display dev=all

# 4. Set the correct policy on newly discovered devices
powermt set policy=CLAROpt class=all

# 5. Persist configuration
powermt save
```

If the device still does not appear after the above, verify at the array that:
- The LUN is fully created and not in a provisioning or error state
- The host initiator (HBA WWN or iSCSI IQN) is correctly registered in the host group
- The LUN masking view includes the newly provisioned LUN

---

## Unlicensed Paths (unlic State)

**Symptom:** `powermt display dev=all` shows paths in `unlic` state. I/O is not sent over these paths.

**Cause:** The PowerPath license has expired, is not applied to this host, or the license check failed after an OS upgrade or kernel update.

**Resolution:**

```bash
# 1. Check license state
powermt check_registration

# Expected output when valid:
# PowerPath Registration: Licensed
# Expiration date: 2026-12-31

# 2. If expired or not licensed, apply the license key
# (Obtain the registration key from the Dell support portal
#  or your Dell account team)
powermt register <registration_key>

# 3. Re-run powermt config to re-evaluate all paths under the new license
powermt config

# 4. Confirm paths are no longer in unlic state
powermt display dev=all | grep unlic

# 5. Set policy and save
powermt set policy=CLAROpt class=all
powermt save
```

**Note:** Paths in `unlic` state are not managed by PowerPath — I/O may still flow over them via native OS multipath if DM-Multipath is active, but PowerPath provides no failover or load balancing for these paths.

---

## Wrong Load Balancing Policy

**Symptom:** `powermt display options` or `powermt display dev=all` shows a policy other than `CLAROpt` (e.g., `RoundRobin`, `BasicFailover`) on Dell/EMC arrays.

**Cause:** The policy was not set or persisted after installation; or `powermt restore` was run without a saved CLAROpt configuration; or a default policy was applied after a PowerPath upgrade.

**Resolution:**

```bash
# 1. Check current policy
powermt display options

# 2. Check per-device policy
powermt display dev=all | grep -i policy

# 3. Apply CLAROpt to all devices
powermt set policy=CLAROpt class=all

# For symmetrix/PowerMax class specifically
powermt set policy=CLAROpt class=symmetrix

# 4. Confirm the change
powermt display options

# 5. Persist — critical step
powermt save
```

**Impact of wrong policy:** `RoundRobin` sends I/O over all paths regardless of ALUA state. On active/passive arrays, this causes I/O to be sent over non-optimised paths (the standby storage processor), which the array then re-routes internally — causing latency and additional array-side CPU overhead.

---

## Path Flapping (Intermittent Dead/Alive Cycling)

**Symptom:** Paths alternate between `alive` and `dead` repeatedly. Host OS logs show frequent path error and restore events. Application sees intermittent latency spikes.

**Cause:** Physical layer issue — marginal SFP, damaged FC cable, dirty connector, or an oversubscribed or error-prone switch port. The path passes enough tests to be marked `alive`, then fails again.

**Diagnosis:**

```bash
# 1. Identify which specific paths are flapping — check for repeated events in syslog
grep -i "emcp\|path\|dead\|restored" /var/log/messages | tail -100

# 2. Identify the HBA and switch port for the affected path
powermt display dev=all
# Note the HBA port ID and the target (array) port for the flapping path

# 3. Check the FC switch for error counters on the suspected port
# Brocade:
portshow <port_number>
# Look for: LIP, Loss of Signal, Loss of Sync, CRC errors

# Cisco MDS:
show interface fc1/1
# Look for: link_failures, sync_loss, signal_loss, credit_loss

# 4. On the host, check HBA error counters
cat /sys/class/fc_host/host0/statistics/error_frames
cat /sys/class/fc_host/host0/statistics/link_failure_count
cat /sys/class/fc_host/host0/statistics/loss_of_signal_count
```

**Resolution:** Replace the suspect SFP or cable. Clean dirty connectors. If the switch port is oversubscribed or showing persistent CRC errors, relocate the connection to a clean port. After physical repair, run `powermt restore` and monitor for 30 minutes to confirm the path has stabilised.

---

## DM-Multipath Conflict

**Symptom:** PowerPath pseudo devices (`/dev/emcpower*`) appear but also show as `dm-*` devices. I/O errors may occur. `multipathd` is running alongside PowerPath.

**Cause:** Both PowerPath and DM-Multipath (`multipathd`) are claiming the same underlying SCSI devices. This causes conflicting I/O routing and can result in I/O errors or data inconsistency.

**Resolution:**

```bash
# 1. Confirm multipathd is running
systemctl status multipathd

# 2. Check if Dell/EMC devices are being claimed by DM-Multipath
multipath -ll | grep -iE "DGC|EMC|SYMMETRIX"

# 3. Add a blacklist entry in /etc/multipath.conf for Dell/EMC devices
# Edit /etc/multipath.conf and add:
#
# blacklist {
#     device {
#         vendor "DGC"
#         product ".*"
#     }
#     device {
#         vendor "EMC"
#         product "SYMMETRIX"
#     }
# }

# 4. Reload multipathd to apply the blacklist
systemctl reload multipathd

# 5. Confirm Dell/EMC devices no longer appear in multipath -ll output
multipath -ll | grep -iE "DGC|EMC|SYMMETRIX"

# 6. If multipathd is not needed on this host at all, disable it
systemctl disable --now multipathd

# 7. Validate PowerPath devices are clean
powermt display dev=all
```

---

## PowerPath Service Not Starting After Reboot

**Symptom:** After a host reboot, `powermt display dev=all` returns an error or shows no devices. The PowerPath pseudo devices (`/dev/emcpower*`) are not present.

**Resolution:**

```bash
# 1. Check if the PowerPath service is running
systemctl status PowerPath

# 2. Check if the kernel module is loaded
lsmod | grep emcp
# If no output, the module is not loaded

# 3. Attempt to load the module manually
modprobe emcp

# 4. Start the PowerPath service
systemctl start PowerPath

# 5. Check service logs for startup errors
journalctl -u PowerPath --since "1 hour ago"

# 6. Verify kernel module version matches installed PowerPath
modinfo emcp | grep -E "version|filename"
powermt version

# If versions do not match, a kernel update may have invalidated the module
# Run the PowerPath installer again (--repair or reinstall) to rebuild the module
# for the current kernel
```

**Common cause after OS/kernel update:** A kernel update replaces the running kernel but does not rebuild the PowerPath kernel module for the new kernel. The PowerPath DKMS package should rebuild automatically, but if DKMS is not configured or fails, the module will be missing after reboot. Check `dmesg` for module load errors.

---

## Common Issues Reference

| Symptom | Likely Cause | Action |
|---|---|---|
| Dead paths after reboot | HBA login timing; module not rebuilt | `powermt restore`; check HBA port state |
| Paths not recovering after SAN maintenance | Dead paths not retried | `powermt restore`; trigger HBA LIP if needed |
| New LUN not visible | HBA not rescanned | Rescan SCSI bus; `powermt config` |
| `unlic` paths | License expired or not applied | `powermt check_registration`; re-register |
| Wrong policy (RoundRobin, BasicFailover) | Not set or not persisted | `powermt set policy=CLAROpt class=all`; `powermt save` |
| Path flapping | Marginal SFP, cable, or switch port | Check switch port error counters; replace hardware |
| DM-Multipath conflict | `multipathd` claiming PowerPath devices | Blacklist Dell/EMC devices in `multipath.conf` |
| PowerPath service not starting | Module not loaded; kernel update | `modprobe emcp`; rebuild DKMS module |
| Configuration not persisted after reboot | `powermt save` not run | Run `powermt save` after every change |
| All paths dead to a device | Array-side masking change; fabric failure | Verify LUN masking at array; check fabric |
