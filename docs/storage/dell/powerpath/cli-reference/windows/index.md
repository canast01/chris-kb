# Windows PowerPath

> Part of the Dell PowerPath CLI Reference.

PowerPath for Windows (PowerPath/VE for Windows in virtual environments) installs as a Windows service and driver, manageable via `powermt` in PowerShell or CMD.

## Basic Status

```powershell
# Display all PowerPath devices and paths
powermt display

# Display all devices with path detail
powermt display dev=all

# Filter by storage class (symmetrix = PowerMax/VMAX)
powermt display class=symmetrix

# Count alive paths
powermt display dev=all | Select-String "alive" | Measure-Object | Select-Object Count
```

## Health and Recovery

```powershell
# PowerPath self-check
powermt check

# Restore dead paths
powermt restore

# Dead paths
powermt display dead
```

## Save Configuration

```powershell
# Save current configuration (persists policy settings across reboots)
powermt save
```

## Service Management

```powershell
# PowerPath service status
Get-Service -Name "EMCPower*"
Get-Service -Name "PowerPath*"

# Restart PowerPath (use only during maintenance)
Restart-Service -Name "EMCPowerPath" -Force

# Check if PowerPath driver is loaded
Get-WmiObject Win32_SystemDriver | Where-Object { $_.Name -match "emcpower" }
```

## Device Management

```powershell
# Full detail for a specific device
powermt display dev=harddisk2

# Mapping between Windows disk numbers and PowerPath pseudo-devices
powermt display dev=all | Select-String "harddisk"

# PowerPath version
powermt version

# License status
powermt lic
```

## Policy Configuration

```powershell
# View current policy per device
powermt display dev=all | Select-String "policy"

# Set policy (CLARiiON Optimized for Dell EMC arrays)
powermt set policy=co dev=all class=clariion

# Save after policy change
powermt save
```

## Event Log Integration

```powershell
# PowerPath logs to Windows Event Log
Get-WinEvent -LogName "Application" -MaxEvents 50 | Where-Object { $_.ProviderName -match "PowerPath" }
Get-WinEvent -LogName "System" | Where-Object { $_.ProviderName -match "EMC" } | Select-Object TimeCreated, Message
```

## Disk Management Integration

```powershell
# PowerPath devices appear as disks in Windows
# List disks via WMI
Get-Disk | Where-Object { $_.FriendlyName -match "DGC\|EMC" } | Select-Object Number, FriendlyName, OperationalStatus, Size
```

## Common Issues

| Symptom | Check | Command |
|---|---|---|
| PowerPath not loading | Service running? | `Get-Service EMCPower*` |
| Dead paths | SAN connectivity issue | `powermt display dead` |
| Wrong policy applied | Check and reset | `powermt display dev=all | Select-String policy` |
| Disks not visible | Rescan and config | `powermt config` |
