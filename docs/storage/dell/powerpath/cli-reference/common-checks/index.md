# Common Check Sequences

> Part of the Dell PowerPath CLI Reference.
## Quick Health Check

Run this sequence to assess PowerPath state on a Linux host:

```bash
# 1. Count alive paths (healthy multipath state)
powermt display dev=all | grep -c "alive"

# 2. Count dead paths (should be zero)
powermt display dev=all | grep -c "dead"

# 3. Show dead paths directly
powermt display dead

# 4. PowerPath self-check
powermt check

# 5. Attempt to restore dead paths
powermt restore
```

## Path Count Per Device

```bash
# Summary per device (alive vs dead)
powermt display dev=all | awk '
    /emcpower/ { dev=$1; alive=0; dead=0 }
    /alive/    { alive++ }
    /dead/     { dead++ }
    /^$/       { if (dev) printf "%s  alive: %d  dead: %d\n", dev, alive, dead; dev="" }
'

# Simpler per-device path count
powermt display dev=all | grep -E "emcpower|State"
```

## Configuration Verification

```bash
# Save current PowerPath configuration (persist after reboot)
powermt save

# Load saved configuration
powermt restore

# Check PowerPath version
powermt version

# Check license
powermt lic
```

## Service and Driver Status

```bash
# Linux — PowerPath daemon status
systemctl status PowerPath
service PowerPath status

# Check loaded driver
lsmod | grep emcpower

# Kernel module version
modinfo emcpower | grep version
```

## Per-Device Detail

```bash
# Full detail for one device
powermt display dev=emcpower0

# Device identifier (NAA/disk ID)
powermt display dev=emcpower0 | grep -E "Pseudo|WWN|ID"
```

## Post-Maintenance Validation

After any SAN maintenance (zoning changes, LUN remapping, path reconfiguration):

```bash
# 1. Rescan for new devices
powermt config

# 2. Verify all paths recovered
powermt display dead

# 3. Confirm path balance
powermt display dev=all | grep -E "emcpower|alive|dead"

# 4. Save new configuration
powermt save
```
