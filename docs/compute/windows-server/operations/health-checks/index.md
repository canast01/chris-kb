# Windows Server — Health Checks


<div class="kb-summary">
Routine checks, service validation, and status verification.
</div>

## Daily Health Check Flow

```mermaid
flowchart TD
    start["Start Daily Checks"]
    svcCheck{"Auto-start services\nall Running?"}
    diskCheck{"Disk free\n> 20%?"}
    evtCheck{"System event log\n0 errors (24h)?"}
    defCheck{"Defender\nup to date?"}
    rebootCheck{"Pending\nreboot?"}
    allGood["All checks passed\nLog result"]
    investigate["Investigate\nand action"]

    start --> svcCheck
    svcCheck -- Yes --> diskCheck
    svcCheck -- No --> investigate
    diskCheck -- Yes --> evtCheck
    diskCheck -- No --> investigate
    evtCheck -- Yes --> defCheck
    evtCheck -- No --> investigate
    defCheck -- Yes --> rebootCheck
    defCheck -- No --> investigate
    rebootCheck -- No --> allGood
    rebootCheck -- Yes --> investigate
```
```
┌─────────────────────────────────── Windows Server — Health Checks ────────────────────────────────────┐
│                                                                                                       │
│  Regular health checks: disk, AD replication, services, and event log review.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                System Health                 │  │                  AD Health                  │   │
│   │          Disk: > 20 % free required          │  │            repadmin /replsummary            │   │
│   │            CPU: < 80 % sustained             │  │               dcdiag /test:all              │   │
│   │          Memory: paging < 100 MB/s           │  │         netlogon: running on all DCs        │   │
│   │        Event log: filter 1xxx errors         │  │       SYSVOL: replicated + accessible       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    System + AD checks should run daily; cluster and security checks weekly                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Cluster Health (WSFC)             │  │               Security Posture              │   │
│   │           Get-ClusterNode: all up            │  │         Missing patches: age < 30 d         │   │
│   │            Cluster log: no errors            │  │         Defender: signatures current        │   │
│   │          Quorum: witness reachable           │  │         Local admins: minimum count         │   │
│   │           CSV: available + healthy           │  │              Audit log: no gaps             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Physical or virtual server · Domain Controllers · cluster shared storage · SIEM                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  repadmin      = AD replication admin tool; /replsummary shows lag and errors                         │
│  dcdiag        = DC diagnostic tool; runs test battery against all DCs                                │
│  netlogon      = Windows service; required for domain auth and GPO application                        │
│  SYSVOL        = shared folder on all DCs; must be replicated and accessible                          │
│  Get-ClusterNode= PowerShell command; shows all cluster nodes and their state                         │
│  Quorum        = cluster voting mechanism; requires majority to stay online                           │
│  Witness       = quorum tie-breaker; disk witness or cloud witness                                    │
│  CSV           = Cluster Shared Volume; shared storage for Hyper-V VMs                                │
│  Paging        = excessive page file activity indicates RAM shortage                                  │
│  Event 1xxx    = common error range in Windows event logs; filter by level                            │
│  Audit log gap = gap in security event log sequence; may indicate tampering                           │
│  LAPS          = auto-rotated local admin password; check rotation age                                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

### Disk Space

```powershell
# All drives with free space
Get-PSDrive -PSProvider FileSystem |
  Select-Object Name,
    @{N="Used(GB)"; E={[math]::Round($_.Used/1GB,2)}},
    @{N="Free(GB)"; E={[math]::Round($_.Free/1GB,2)}},
    @{N="Total(GB)"; E={[math]::Round(($_.Used+$_.Free)/1GB,2)}},
    @{N="Free%"; E={[math]::Round($_.Free/($_.Used+$_.Free)*100,1)}} |
  Where-Object {$_."Total(GB)" -gt 0}
```

Alert threshold: warn at < 20% free, critical at < 10% free.

### CPU and Memory

```powershell
# CPU utilisation (5-second average)
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 5 -MaxSamples 3 |
  Select-Object -ExpandProperty CounterSamples |
  Select-Object CookedValue

# Memory usage
$os = Get-CimInstance Win32_OperatingSystem
[PSCustomObject]@{
  TotalGB   = [math]::Round($os.TotalVisibleMemorySize/1MB, 2)
  FreeGB    = [math]::Round($os.FreePhysicalMemory/1MB, 2)
  UsedPct   = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / $os.TotalVisibleMemorySize * 100, 1)
}

# Top 10 processes by CPU
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, WorkingSet, Id
```

### Windows Defender Status

```powershell
# Defender status
Get-MpComputerStatus | Select-Object `
  AMServiceEnabled, AntispywareEnabled, AntivirusEnabled,
  RealTimeProtectionEnabled, AntivirusSignatureLastUpdated,
  QuickScanStartTime, FullScanStartTime

# Check for threats
Get-MpThreatDetection | Select-Object ThreatID, ProcessName, ActionSuccess, InitialDetectionTime
```

### Scheduled Tasks

```powershell
# Tasks that failed in last 24 hours
Get-ScheduledTask | Where-Object State -ne Disabled |
  ForEach-Object {
    $info = $_ | Get-ScheduledTaskInfo
    [PSCustomObject]@{
      TaskName   = $_.TaskName
      TaskPath   = $_.TaskPath
      LastResult = $info.LastTaskResult
      LastRun    = $info.LastRunTime
    }
  } |
  Where-Object LastResult -ne 0 |
  Sort-Object LastRun -Descending
```

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

## Performance Counter Hierarchy

```mermaid
flowchart LR
    subgraph cpu["CPU"]
        cpuTotal["Processor Total %"]
        cpuPerCore["Per-core %"]
        ctxSwitch["Context Switches/sec"]
    end
    subgraph mem["Memory"]
        memAvail["Available MBytes"]
        pagesSec["Pages/sec"]
        nonPagePool["NonPaged Pool"]
    end
    subgraph disk["Disk"]
        diskTime["% Disk Time"]
        diskLatency["Avg Disk sec/Transfer"]
        diskIops["Disk Transfers/sec"]
    end
    subgraph net["Network"]
        bytesTotal["Bytes Total/sec"]
        pktErrors["Packets Errors/sec"]
    end
    perfMon["PerfMon\nData Collector Set"]

    cpu --> perfMon
    mem --> perfMon
    disk --> perfMon
    net --> perfMon
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

## Event Logs

| Log | Path | Content |
|---|---|---|
| System | `System` | OS events, driver failures, service stops, hardware |
| Application | `Application` | App errors, .NET exceptions, SQL, IIS |
| Security | `Security` | Authentication, account management, privilege use |
| Setup | `Setup` | Windows Update, component installs |
| Windows PowerShell | `Windows PowerShell` | PS script execution |
| Sysmon | `Microsoft-Windows-Sysmon/Operational` | Process creation, network, file events (if deployed) |

### Get-WinEvent — Common Queries

```powershell
# Errors in System log — last 24 hours
Get-WinEvent -FilterHashtable @{
    LogName   = 'System'
    Level     = 2
    StartTime = (Get-Date).AddHours(-24)
} | Select-Object TimeCreated, Id, Message | Format-List

# Application errors — last 6 hours
Get-WinEvent -FilterHashtable @{
    LogName   = 'Application'
    Level     = 2
    StartTime = (Get-Date).AddHours(-6)
} | Select-Object -First 20 TimeCreated, Id, Message

# Security log — failed logons (Event ID 4625)
Get-WinEvent -FilterHashtable @{
    LogName   = 'Security'
    Id        = 4625
    StartTime = (Get-Date).AddHours(-24)
} | Select-Object TimeCreated, Message | Select-Object -First 20
```

### Key Security Event IDs

| Event ID | Description |
|---|---|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4634 | Logoff |
| 4688 | Process creation |
| 4720 | User account created |
| 4740 | Account locked out |
| 7036 | Service started or stopped |
| 41 | Kernel power — unexpected reboot |
| 6008 | Unexpected shutdown |

### Log Size and Retention

```powershell
# Check current log sizes and limits
Get-WinEvent -ListLog System, Application, Security |
    Select-Object LogName, MaximumSizeInBytes,
        @{N="CurrentSizeMB"; E={ [math]::Round($_.FileSize/1MB,1) }},
        LogMode

# Set max size (e.g., Security log to 1 GB)
wevtutil sl Security /ms:1073741824
```

## Performance

### Quick Performance Snapshot

```powershell
# CPU usage (5-sample average)
$cpu = Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 2 -MaxSamples 5
[math]::Round(($cpu.CounterSamples.CookedValue | Measure-Object -Average).Average, 1)

# Memory
$os = Get-CimInstance Win32_OperatingSystem
[PSCustomObject]@{
    TotalGB   = [math]::Round($os.TotalVisibleMemorySize/1MB, 1)
    FreeGB    = [math]::Round($os.FreePhysicalMemory/1MB, 1)
    UsedPct   = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory)/$os.TotalVisibleMemorySize*100, 1)
}

# Top processes by CPU
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, Id,
    @{N="CPU%"; E={ [math]::Round($_.CPU, 1) }}, WorkingSet

# Top processes by memory
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 10 Name, Id,
    @{N="MemMB"; E={ [math]::Round($_.WorkingSet/1MB, 1) }}
```

### Performance Thresholds

| Counter | Warning | Critical |
|---|---|---|
| CPU % Processor Time | > 70% sustained | > 90% sustained |
| Memory Available MB | < 20% of total | < 10% of total |
| Pages/sec | > 100/sec | > 1,000/sec |
| Disk Avg. sec/Transfer | > 15 ms | > 25 ms |
| Disk % Disk Time | > 80% | > 95% |
| Network % Bandwidth | > 70% | > 90% |

### Performance Counters

```powershell
# CPU — sustained above 85% = problem
Get-Counter '\Processor(_Total)\% Processor Time' -SampleInterval 5 -MaxSamples 12 |
    ForEach-Object { $_.CounterSamples | Select-Object Path, CookedValue }

# Memory — pages/sec above 1000 sustained = memory pressure
Get-Counter '\Memory\Pages/sec', '\Memory\Available MBytes' -SampleInterval 5 -MaxSamples 6

# Disk — latency above 20ms = problem
Get-Counter '\PhysicalDisk(*)\Avg. Disk sec/Transfer' -SampleInterval 2 -MaxSamples 5

# Network — throughput and errors
Get-Counter '\Network Interface(*)\Bytes Total/sec', '\Network Interface(*)\Packets Received Errors'
```

### Data Collector Sets (PerfMon)

```powershell
# Create a data collector set from command line
logman create counter "PerfBaseline" ^
    -c "\Processor(_Total)\% Processor Time" ^
       "\Memory\Available MBytes" ^
       "\PhysicalDisk(*)\Avg. Disk sec/Transfer" ^
       "\Network Interface(*)\Bytes Total/sec" ^
    -si 00:00:05 ^
    -f bincirc ^
    -max 500 ^
    -o C:\PerfLogs\baseline

logman start PerfBaseline
logman stop PerfBaseline
```
