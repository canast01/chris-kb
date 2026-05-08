# PowerPath — Common Issues

## Dead Paths

```bash
# Identify dead paths
powermt display dev=all | grep -A5 dead

# Attempt automatic path restore
powermt restore

# Force re-check of all paths
powermt check_registration
```

If paths remain dead after `powermt restore`:
1. Check HBA port state on the host (`systool -c fc_host -v` on Linux)
2. Check SAN switch port state (Cisco: `show interface fc x/x`, Brocade: `portshow x`)
3. Check array port state on the storage array console

## All Paths Dead to a Device

If all paths to a device are dead:

1. Confirm LUN masking is still in place on the array
2. Confirm host HBA WWNs still match the masking configuration
3. Check SAN fabric for zoning changes
4. Reboot HBA driver if needed: `echo 1 > /sys/class/fc_host/hostX/issue_lip`

## Device Not Visible

```bash
# Rescan after new LUN provisioned
powermt config

# If still missing, rescan HBA
echo "- - -" > /sys/class/scsi_host/hostX/scan

# Confirm array has presented the LUN to this host
```

## Incorrect Path Count

Expected 4 paths, seeing 2:
- Check both SAN fabrics are connected (dual-fabric design)
- Verify both HBA ports are online
- Verify zoning includes both initiator ports on both fabrics

## Wrong Load Balance Policy

```bash
# Reset policy to CLAROpt (Active/Optimized)
powermt set policy=co dev=all

# Verify
powermt display dev=all | grep policy
```

## PowerPath Not Starting After Reboot

```bash
# Check service status
systemctl status PowerPath

# Check kernel module loaded
lsmod | grep emcp

# Re-load module manually
modprobe emcp
```

## Common Issues Reference

| Symptom | Likely Cause | Action |
|---|---|---|
| Dead paths after reboot | HBA driver load order | Run `powermt restore` after boot |
| Device missing | LUN not presented or rescan needed | `powermt config` |
| Performance issues | Suboptimal path policy | `powermt set policy=co dev=all` |
| Path flapping | SAN fabric instability | Check switch and cable |
| multipathd conflict | Both multipath stacks active | Disable `multipathd` |
| `unlic` paths | License expired or not applied | Run `powermt check_registration` |
| Unbalanced path I/O | Wrong policy | `powermt set policy=co dev=all` |
