---
tags:
  - dell
  - operations
---
# PowerPath — CLI Reference

<div class="kb-summary">
Commonly used `powermt` commands for managing Dell PowerPath multipathing on Linux and Windows hosts. PowerPath is a multipathing driver — it sits between the OS and the storage array, managing multiple physical paths to each disk to ensure high availability and load balancing.

*Applies to: PowerPath*
</div>
![PowerPath — CLI Reference](../../../../assets/storage-dell-powerpath-operations-cli-reference.svg)

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Status & Devices

```d2
direction: right

host: "Host OS" {shape: rectangle}
ppDriver: "PowerPath Driver\npseudo device /dev/emcpowerX" {shape: rectangle}
hba0: "HBA0\nFabric A" {shape: rectangle}
hba1: "HBA1\nFabric B" {shape: rectangle}
spA: "Array SP-A\n(active-optimised paths" {shape: rectangle}
spB: "Array SP-B\n(non-optimised paths" {shape: rectangle}

host -> ppDriver
ppDriver -> hba0
ppDriver -> hba1
hba0 -> spA
hba0 -> spB
hba1 -> spA
hba1 -> spB
```

The first commands to run when checking on PowerPath. `powermt display` shows you all the storage devices and whether their paths are healthy. Dead paths mean some redundancy is lost — you need to investigate.

```bash
# Overall summary — all devices and path states
powermt display

# Path summary per device (compact view)
powermt display options

# Display dead paths only (should be empty in a healthy system)
powermt display dead

# Display PowerPath version
powermt version

# Display license registration
powermt display reg

# Show all devices with full path detail
powermt display dev=all

# Single device detail
powermt display dev=emcpower<n>
powermt display dev=emcpower<n>a

# Logical device info
powermt display ldev

# Filter by storage class
powermt display class=clariion
powermt display class=symmetrix
powermt display class=vplex
```


```text title="Expected output"
PowerPath for Linux Version 6.2.0.0 (build 247)
Symmetrix ID: 000297900123  Logical Device Count: 24
Host: prod-storage-01  OS: Linux 5.10.0-8-generic #1 SMP Debian 5.10.60-1
Fibre Channel: 4 Initiators, 8 Targets, 32 Paths
Disk Devices: 24
  Enabled: 24  Dead: 0  Standby: 0  Failed: 0

Name           Attr  Paths  Prio  Owner               Algo  State
emcpower0      -     4/4    0     prod-storage-01    LB    Alive
emcpower1      -     4/4    0     prod-storage-01    LB    Alive
emcpower2      -     4/4    0     prod-storage-01    LB    Alive
emcpower3      -     2/4    0     prod-storage-01    LB    Alive
...

PowerPath Version: 6.2.0.0 (build 247)
License Status: Valid (expires 2025-12-31)

Symmetrix ID: 000297900123
  Device: emcpower0  Paths: 4  State: Alive  Class: CLARIION
  Device: emcpower1  Paths: 4  State: Alive  Class: SYMMETRIX
  Device: emcpower2  Paths: 4  State: Alive  Class: VPLEX
```

!!! warning "Common errors"
    **`powermt: command not found`** — Install PowerPath package with `apt-get install powerpath` or equivalent for your distribution.
    **`powermt: permission denied`** — Run the command with `sudo` or ensure your user is in the powerpath group with `sudo usermod -aG powerpath $USER`.
    **`powermt display: No devices found`** — Verify PowerPath daemon is running with `sudo systemctl status powerpath` and rescan paths using `powermt config`.
---

## Paths

A path is one physical route from the server's HBA port to a storage array port. PowerPath manages multiple paths per device — if one path fails, I/O automatically continues on surviving paths. These commands let you check, restore, and test paths.

### Path Status

```bash
# All devices with all path states
powermt display dev=all

# Count alive paths (healthy multipath state)
powermt display dev=all | grep -c "alive"

# Count dead paths (should be zero)
powermt display dev=all | grep -c "dead"

# Show only dead paths
powermt display dead
```

### Path State Values

| State | Meaning |
|---|---|
| `alive` | Path healthy and in use |
| `dead` | Path failed — I/O not sent on this path |
| `failed` | Path HBA or connection failure |
| `unlic` | Path exists but PowerPath license does not cover it |
| `sdsf` | Standby path (used when primary paths fail) |

### Restore and Recover Paths

```bash
# Attempt to restore all dead paths
powermt restore

# Rescan for new devices or newly presented LUNs
powermt config

# Remove dead path records
powermt remove dead

# After SAN maintenance — full recovery sequence
powermt config
powermt restore
powermt display dead   # confirm zero dead paths
powermt save
```

### Manual Path Failover and Unblock

```bash
# Fail a specific path (force I/O off a port — testing/maintenance)
powermt fail dev=emcpower0 path=<hba_port_id>

# Unblock a path (re-enable after manual fail)
powermt unblock dev=emcpower0 path=<hba_port_id>
```

### Path Detail

```bash
# Full detail for one device including each path's I/O stats
powermt display dev=emcpower0

# With port info
powermt display dev=emcpower0 port

# Confirm ALUA active-optimized paths
powermt display dev=emcpower0 | grep -E "State|ALUA"

# Verify expected number of paths per device
powermt display dev=all | awk '/emcpower/{d=$1;c=0} /alive/{c++} /^$/{if(d) print d" "c; d=""}'
```

### Common Path Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Dead paths on all HBAs | SAN switch or array port issue | Check zoning and array port health |
| Dead paths on one HBA | HBA failure or cable/SFP | Replace HBA or cable |
| Paths not auto-recovering | `powermt restore` needed | Run `powermt restore` after SAN fix |
| New LUNs not visible | No rescan | Run `powermt config` |
| Unbalanced path I/O | Wrong policy | `powermt set policy=co dev=all` |

---

## HBA Ports

HBA (Host Bus Adapter) ports are the server-side physical connections into the SAN fabric. Each HBA port has a WWN (World Wide Name) — a unique address used for SAN zoning. These commands show which HBA ports are in use and their connection state.

```bash
# Show all HBA ports and their status
powermt display hba

# Detailed per-port info
powermt display hba=<hba_id>

# Show all paths (initiator → target → device)
powermt display port

# Show paths for a specific device
powermt display dev=<device_id> port

# Show only failed/dead paths
powermt display hba | grep -i dead
powermt display port | grep -i dead
```

### Path Statistics

```bash
# Show I/O load per path
powermt display dev=all stats

# Reset path statistics (after troubleshooting)
powermt reset dev=<device_id>
```

### HBA Port to WWPN Mapping

```bash
# On Linux — map HBA port to WWPN via /sys
cat /sys/class/fc_host/host*/port_name

# On Windows — list HBA WWPNs via WMI
Get-WmiObject -Namespace "root\WMI" -Class "MSFC_FCAdapterHBAAttributes" |
    Select-Object NodeWWN, PortWWN

# Via hbanyware (Emulex/Broadcom HBA utility)
hbacmd listhbas
hbacmd hbaattrib <HBA_WWN>
```

### PowerPath Quick Reference

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

### Troubleshooting Dead Paths

```bash
# Identify dead paths
powermt display dev=all | grep -B 2 dead

# Manually attempt path recovery
powermt check dev=<device_id>

# Restore all paths
powermt restore dev=<device_id>
```

---

## Load Balancing & Policies

PowerPath distributes I/O across available paths using a configurable load balancing policy. The right policy depends on the storage array type. For Dell EMC arrays, `co` (CLARiiON Optimized) is the default and recommended setting — it uses ALUA to prefer the owning storage processor's paths.

### Available Policies

| Policy | Code | Description |
|---|---|---|
| CLARiiON Optimized | `co` | Default for Dell EMC arrays — uses active-optimized paths first |
| Round Robin | `rr` | Distributes I/O evenly across all active paths |
| Adaptive | `ad` | Load-based selection — switches to least-loaded path |
| No Redirect | `nr` | Uses first active path only (no load balancing) |
| Single Initiator | `si` | Pins I/O to a single HBA port |

### View Current Policy

```bash
# Policy for a specific device
powermt display dev=emcpower0 | grep -i policy

# Policy for all devices
powermt display dev=all | grep -i policy
```

### Set Policy

```bash
# Set policy on a specific device
powermt set policy=co dev=emcpower0

# Set policy across all devices of a specific class
powermt set policy=co dev=all class=clariion
powermt set policy=rr dev=all class=symmetrix

# Set policy globally
powermt set policy=co dev=all

# Save after changing policy (persists across reboots)
powermt save
```

### Recommended Policies by Array

| Array | Recommended Policy |
|---|---|
| PowerMax / VMAX | `co` (CLARiiON Optimized) |
| PowerStore | `co` |
| Unity | `co` |
| Non-Dell arrays | `rr` (Round Robin) |

### Verifying Load Distribution

```bash
# Check path I/O statistics
powermt display dev=emcpower0 | grep -E "Bytes|I/Os"

# Full device detail with path stats
powermt display dev=emcpower0 port
```

### Troubleshooting Uneven Load

```bash
powermt display dev=all | grep policy
powermt restore
powermt save
```

---

## Configuration & Checks

These commands manage the PowerPath configuration file, validate the current setup, and let you add or remove devices after SAN changes. Always save after making changes so they persist across reboots.

```bash
# Check all paths
powermt check

# Check specific device
powermt check dev=emcpower<n>

# Verify consistency
powermt display options

# Show configuration file
cat /etc/powermt.custom

# Save current configuration
powermt save
powermt save force

# Load / restore config
powermt restore

# Reconfig (after new device attachment)
powermt config

# Remove stale devices
powermt remove dev=emcpower<n>
powermt remove dead
```

---

## Windows PowerPath

On Windows, `powermt` runs from PowerShell or CMD after the PowerPath service and driver are installed. The commands are largely the same as Linux with some Windows-specific additions.

```powershell
# Display all PowerPath devices and paths
powermt display

# Display all devices with path detail
powermt display dev=all

# Filter by storage class
powermt display class=symmetrix

# Count alive paths
powermt display dev=all | Select-String "alive" | Measure-Object | Select-Object Count

# PowerPath self-check
powermt check

# Restore dead paths
powermt restore

# Dead paths
powermt display dead

# Save configuration
powermt save

# PowerPath service status
Get-Service -Name "EMCPower*"
Get-Service -Name "PowerPath*"

# Restart PowerPath (use only during maintenance)
Restart-Service -Name "EMCPowerPath" -Force

# Check if PowerPath driver is loaded
Get-WmiObject Win32_SystemDriver | Where-Object { $_.Name -match "emcpower" }

# View current policy per device
powermt display dev=all | Select-String "policy"

# Set policy (CLARiiON Optimized for Dell EMC arrays)
powermt set policy=co dev=all class=clariion

# PowerPath logs in Windows Event Log
Get-WinEvent -LogName "Application" -MaxEvents 50 | Where-Object { $_.ProviderName -match "PowerPath" }

# PowerPath devices — list disks via WMI
Get-Disk | Where-Object { $_.FriendlyName -match "DGC\|EMC" } | Select-Object Number, FriendlyName, OperationalStatus, Size
```

---

## Common Check Sequences

Runbooks for the most common PowerPath tasks. Use these as a checklist during troubleshooting or after SAN maintenance.

### Quick Health Check

```bash
# 1. Count alive paths
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

### Path Count Per Device

```bash
# Summary per device (alive vs dead)
powermt display dev=all | awk '
    /emcpower/ { dev=$1; alive=0; dead=0 }
    /alive/    { alive++ }
    /dead/     { dead++ }
    /^$/       { if (dev) printf "%s  alive: %d  dead: %d\n", dev, alive, dead; dev="" }
'
```

### Service and Driver Status (Linux)

```bash
# PowerPath daemon status
systemctl status PowerPath
service PowerPath status

# Check loaded driver
lsmod | grep emcpower

# Kernel module version
modinfo emcpower | grep version
```

### Post-Maintenance Validation

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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powerpath — Procedures](../procedures/)
- [Powerpath — Scripts](../scripts/)
- [Powerpath — Health Checks](../health-checks/)
