# PowerPath Host Validation

Validate PowerPath installation and path configuration after host provisioning or changes.
## Check PowerPath Version

```bash
# Linux
powermt version

# Windows (PowerShell or cmd)
powermt version
```

## Verify PowerPath is Running

```bash
# Linux — check PowerPath daemon
/etc/init.d/PowerPath status
# or
systemctl status PowerPath

# Windows
sc query EMCPower
```

## Device Discovery

```bash
# Rescan for new devices
powermt config

# Check device list
powermt display dev=all
```

## Path Count Validation

For each device, confirm expected path count (typically 2 or 4 per LUN):

```bash
powermt display dev=all
```

Count `alive` paths per pseudo device. Compare against expected path count from the storage array zoning design.

## Host Registration on Array

Ensure the host is registered on the array (PowerMax/VNX/Unity) with the correct initiators:

- Check via array management console that all HBA WWNs/iSCSI IQNs are registered
- Confirm LUN masking to the correct host or host group

## After OS Reboot Validation

```bash
# Confirm PowerPath loaded and devices are present
powermt display dev=all

# Confirm no dead paths after reboot
powermt display dev=all | grep -i dead

# Restore paths if needed
powermt restore
```

## Multipath Conflict Check (Linux)

Ensure `multipathd` is disabled when using PowerPath — running both simultaneously causes conflicts:

```bash
systemctl status multipathd
# Should be inactive/disabled when PowerPath is in use
```

## Validation Checklist

| Check | Command | Expected |
|---|---|---|
| PowerPath running | `systemctl status PowerPath` | Active |
| All devices visible | `powermt display dev=all` | All LUNs listed |
| No dead paths | `grep dead` output | 0 dead paths |
| Path count correct | Count `alive` per device | Matches design |
| multipathd disabled | `systemctl status multipathd` | Inactive |
