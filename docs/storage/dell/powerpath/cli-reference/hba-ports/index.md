# PowerPath HBA Ports Reference

Commands for viewing HBA port information and path status in Dell PowerPath/VE.

## List All HBA Ports

```bash
# Show all HBA ports and their status
powermt display hba

# Sample output:
# HBA              Vendor         Port  Status  PWWN
# hba-1            Emulex         0     active  10:00:00:00:c9:xx:xx:xx
# hba-2            Emulex         0     active  10:00:00:00:c9:xx:xx:xx

# Show detailed per-port info
powermt display hba=<hba_id>
```

## Show Path Information

```bash
# Show all paths (initiator → target → device)
powermt display port

# Sample output shows:
# - Port ID
# - HBA binding
# - Target WWPN
# - Array and port name
# - Path state (alive/dead)
# - I/O statistics

# Show paths for a specific device
powermt display dev=<device_id> port

# Show only failed/dead paths
powermt display hba | grep -i dead
powermt display port | grep -i dead
```

## Check Path State

```bash
# Full device and path display
powermt display dev=all

# Compact display — useful for quick health check
powermt display dev=all format=c

# Check active vs standby paths (for PowerMax/VMAX)
powermt display dev=all | grep -E "Alive|Dead|Standby"
```

## Path Statistics

```bash
# Show I/O load per path
powermt display dev=all stats

# Reset path statistics (after troubleshooting)
powermt reset dev=<device_id>
```

## HBA Port to WWPN Mapping

```bash
# On Linux — map HBA port to WWPN via /sys
cat /sys/class/fc_host/host*/port_name
# Output: 0x10000000c9xxxxxx (one line per port)

# On Windows — list HBA WWPNs via WMI
Get-WmiObject -Namespace "root\WMI" -Class "MSFC_FCAdapterHBAAttributes" |
    Select-Object NodeWWN, PortWWN

# Via hbanyware (Emulex/Broadcom HBA utility)
hbacmd listhbas
hbacmd hbaattrib <HBA_WWN>
```

## Common PowerPath CLI Quick Reference

| Task | Command |
|---|---|
| Show all devices | `powermt display dev=all` |
| Show HBA ports | `powermt display hba` |
| Show port details | `powermt display port` |
| Check path load | `powermt display dev=all stats` |
| Save configuration | `powermt save` |
| Restore configuration | `powermt restore` |
| Check PowerPath version | `powermt version` |
| Check PowerPath service | `systemctl status PowerPath` (Linux) |

## Troubleshooting Dead Paths

```bash
# Identify dead paths
powermt display dev=all | grep -B 2 dead

# Manually attempt path recovery
powermt check dev=<device_id>

# Restore all paths
powermt restore dev=<device_id>

# If path stays dead: check HBA driver, zoning, and array target port status
# Array-side: use Unisphere or `symcfg list -fa` to check port state
```
