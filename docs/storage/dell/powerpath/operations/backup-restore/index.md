# PowerPath — Backup & Restore

> Backup and restore procedures for PowerPath configuration will be documented here.

## Overview

PowerPath configuration backup involves persisting the path policy, device settings, and registration state. Use `powermt save` to write the current configuration to disk before any change.

## Configuration Backup

```bash
# Save current PowerPath configuration to disk
powermt save

# Save with force (overwrites existing saved config)
powermt save force

# Capture path state and policy as a dated baseline file
powermt display dev=all > <hostname>-powermt-baseline-$(date +%Y-%m-%d).txt
powermt display options >> <hostname>-powermt-baseline-$(date +%Y-%m-%d).txt
```

## Configuration Restore

```bash
# Restore PowerPath configuration from saved state
powermt restore

# After restore, verify path state
powermt display dev=all

# Verify policy is intact
powermt display options
```

## Backup Checklist

- [ ] Run `powermt save` before every maintenance window or configuration change
- [ ] Store dated baseline files (`powermt display dev=all` output) in the runbook or change record
- [ ] Include `powermt check_registration` output in the baseline to capture license state
- [ ] Verify configuration persists across reboots: reboot the host and confirm path count and policy match the pre-reboot state
