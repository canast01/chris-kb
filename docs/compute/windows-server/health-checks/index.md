# Windows Server Health Checks

Quick checks to confirm a Windows Server is healthy before and after changes, and during incident triage.

## System Overview

```powershell
# Uptime
(Get-Date) - (gcim Win32_OperatingSystem).LastBootUpTime

# OS version, build, and hostname
Get-ComputerInfo | Select-Object CsName, OsName, OsVersion, OsBuildNumber, WindowsVersion

# Last 5 system events (errors/warnings)
Get-WinEvent -LogName System -MaxEvents 100 |
    Where-Object { $_.LevelDisplayName -in "Error","Warning" } |
    Select-Object -First 5 TimeCreated, LevelDisplayName, Message
```

## CPU and Memory

```powershell
# CPU usage (10-second sample)
$cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 5
$cpu.CounterSamples.CookedValue | Measure-Object -Average | Select-Object Average

# Memory
$os = Get-CimInstance Win32_OperatingSystem
[PSCustomObject]@{
    TotalGB     = [math]::Round($os.TotalVisibleMemorySize/1MB, 1)
    FreeGB      = [math]::Round($os.FreePhysicalMemory/1MB, 1)
    UsedPct     = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize * 100, 1)
}

# Top CPU-consuming processes
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, Id, CPU, WorkingSet
```

## Disk

```powershell
# Disk free space — flag below 20%
Get-PSDrive -PSProvider FileSystem | Select-Object Name,
    @{N="FreeGB";   E={ [math]::Round($_.Free/1GB, 1) }},
    @{N="TotalGB";  E={ [math]::Round(($_.Used + $_.Free)/1GB, 1) }},
    @{N="UsedPct";  E={ [math]::Round($_.Used/($_.Used + $_.Free)*100, 1) }} |
    Where-Object { $_.UsedPct -gt 80 }

# Disk performance counters
Get-Counter '\PhysicalDisk(*)\Avg. Disk sec/Transfer' -SampleInterval 2 -MaxSamples 3 |
    ForEach-Object { $_.CounterSamples | Select-Object Path, CookedValue }
```

## Services

```powershell
# Services in a stopped state that should be running (auto start)
Get-Service | Where-Object { $_.StartType -eq "Automatic" -and $_.Status -ne "Running" } |
    Select-Object Name, DisplayName, Status

# Check a specific service
Get-Service -Name <ServiceName> | Select-Object Name, Status, StartType
```

## Event Log Quick Review

```powershell
# System errors in last 24 hours
Get-WinEvent -FilterHashtable @{ LogName='System'; Level=2; StartTime=(Get-Date).AddHours(-24) } |
    Select-Object TimeCreated, Id, Message | Select-Object -First 10

# Application errors in last 24 hours
Get-WinEvent -FilterHashtable @{ LogName='Application'; Level=2; StartTime=(Get-Date).AddHours(-24) } |
    Select-Object TimeCreated, Id, Message | Select-Object -First 10
```

## Network

```powershell
# Interface status
Get-NetAdapter | Select-Object Name, Status, LinkSpeed, MacAddress

# IP addresses
Get-NetIPAddress | Where-Object { $_.AddressFamily -eq "IPv4" } |
    Select-Object InterfaceAlias, IPAddress, PrefixLength

# Active TCP connections
Get-NetTCPConnection -State Established |
    Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, OwningProcess |
    Sort-Object RemoteAddress | Select-Object -First 20

# Test DNS resolution
Resolve-DnsName corp.local
```

## Pending Reboots

```powershell
# Check for pending reboot from Windows Update or software installs
$rebootPending = $false
if (Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired" -EA SilentlyContinue) { $rebootPending = $true }
if (Get-ItemProperty "HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager" -Name PendingFileRenameOperations -EA SilentlyContinue) { $rebootPending = $true }
"Reboot Pending: $rebootPending"
```

## Health Check Summary

| Check | Command | Healthy |
|---|---|---|
| Uptime reasonable | `(Get-Date) - LastBootUpTime` | No unexpected recent reboot |
| CPU usage | `Get-Counter` | < 80% sustained |
| Memory available | `Get-CimInstance Win32_OperatingSystem` | > 20% free |
| No disk > 80% | `Get-PSDrive` | All < 80% used |
| No stopped auto services | `Get-Service` | 0 stopped auto-start |
| No System errors (24h) | `Get-WinEvent` | 0 critical errors |
| Network adapters up | `Get-NetAdapter` | All status = Up |
| Pending reboot | Registry check | $false |
