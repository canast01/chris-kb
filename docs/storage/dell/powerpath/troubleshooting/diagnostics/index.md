# PowerPath — Diagnostics

> Diagnostic procedures and log analysis for PowerPath will be documented here.

## Diagnostic Data Collection

Before escalating a PowerPath issue to Dell Support, collect the following diagnostic information:

```bash
# PowerPath version
powermt version

# License registration status
powermt check_registration

# All device and path state (save full output)
powermt display dev=all

# All HBA port states
powermt display ports class=all

# Load balancing policy and options
powermt display options

# OS and kernel version (Linux)
uname -r
cat /etc/os-release

# HBA driver version (Linux Fibre Channel)
systool -c fc_host -v 2>/dev/null | grep -E "driver_version|firmware_version|port_name"

# Recent PowerPath-related kernel messages (Linux)
dmesg | grep -i "emcp\|PowerPath" | tail -50
journalctl -k --since "1 hour ago" | grep -i "emcp\|powerpath"

# System logs for I/O errors around the time of the issue (Linux)
grep -i "emcp\|scsi\|hba" /var/log/messages | tail -100
```

## Log Locations

| Platform | Log Location | Keywords |
|---|---|---|
| Linux | `/var/log/messages` or `journalctl` | `emcp`, `PowerPath`, `dead path`, `path restored` |
| Windows | Windows Event Log (Application + System) | `PowerPath`, `EMC` |
| AIX | `/var/adm/ras/errlog` (use `errpt`) | PowerPath entries |

## Common Diagnostic Sequences

### Check Path State Immediately

```bash
powermt display dev=all
powermt display ports class=all
powermt display options
```

### Check for Kernel-Level Errors

```bash
dmesg | grep -iE "scsi|multipath|emcpower|powerpath" | tail -50
journalctl -k --since "1 hour ago" | grep -iE "emcp|powerpath"
```

### Verify License

```bash
powermt check_registration
```

### Check Daemon Status

```bash
systemctl status PowerPath
lsmod | grep emcp
```
