# Windows Server Performance

Performance monitoring, baseline capture, and bottleneck identification on Windows Server.

## Quick Performance Snapshot

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

## Performance Counters

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

# Context switches — above 10,000/s per CPU = possible bottleneck
Get-Counter '\System\Context Switches/sec'
```

## Performance Thresholds

| Counter | Warning | Critical |
|---|---|---|
| CPU % Processor Time | > 70% sustained | > 90% sustained |
| Memory Available MB | < 20% of total | < 10% of total |
| Pages/sec | > 100/sec | > 1,000/sec |
| Disk Avg. sec/Transfer | > 15 ms | > 25 ms |
| Disk % Disk Time | > 80% | > 95% |
| Network % Bandwidth | > 70% | > 90% |

## Data Collector Sets (PerfMon)

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

## Resource Monitor (resmon.exe)

Run `resmon.exe` for a real-time graphical view of CPU, memory, disk, and network broken down per-process. Useful for identifying which process is consuming resources during an incident.

## Memory Analysis

```powershell
# Memory allocation by process
Get-Process | Sort-Object WorkingSet -Descending | Select-Object -First 15 Name, Id,
    @{N="WS_MB";    E={ [math]::Round($_.WorkingSet/1MB,1) }},
    @{N="Priv_MB";  E={ [math]::Round($_.PrivateMemorySize64/1MB,1) }},
    @{N="VM_GB";    E={ [math]::Round($_.VirtualMemorySize64/1GB,2) }}

# Non-paged pool exhaustion (Event ID 2019 in System log)
Get-WinEvent -FilterHashtable @{ LogName='System'; Id=2019 } -MaxEvents 5

# Check for memory leaks — watch a process over time
$proc = Get-Process -Name "w3wp"
for ($i=0; $i -lt 6; $i++) {
    [PSCustomObject]@{
        Time   = Get-Date -Format HH:mm:ss
        WS_MB  = [math]::Round($proc.WorkingSet/1MB, 1)
    }
    Start-Sleep 10
}
```

## CPU Analysis

```powershell
# Per-core CPU usage
1..4 | ForEach-Object {
    Get-Counter "\Processor($_)\% Processor Time" -SampleInterval 2 -MaxSamples 3 |
        ForEach-Object { $_.CounterSamples | Select-Object Path, CookedValue }
}

# Process with high CPU — get thread-level detail
$proc = Get-Process -Name "sqlservr"
$proc.Threads | Sort-Object TotalProcessorTime -Descending | Select-Object -First 5 Id, TotalProcessorTime

# Check for CPU throttling or power plan
powercfg /getactivescheme
# Should be: High Performance for servers
```

## Disk Performance

```powershell
# Disk latency per physical disk
Get-Counter '\PhysicalDisk(*)\Avg. Disk sec/Read',
            '\PhysicalDisk(*)\Avg. Disk sec/Write',
            '\PhysicalDisk(*)\Disk Reads/sec',
            '\PhysicalDisk(*)\Disk Writes/sec' -SampleInterval 2 -MaxSamples 5 |
    ForEach-Object { $_.CounterSamples | Select-Object Path, CookedValue }

# Identify busy volume
Get-Counter '\LogicalDisk(*)\% Disk Time' -SampleInterval 2 -MaxSamples 3 |
    ForEach-Object { $_.CounterSamples | Sort-Object CookedValue -Descending | Select-Object -First 5 Path, CookedValue }
```

## Network Performance

```powershell
# Throughput per adapter
Get-Counter '\Network Interface(*)\Bytes Total/sec' -SampleInterval 2 -MaxSamples 3

# Errors and discards
Get-Counter '\Network Interface(*)\Packets Received Errors',
            '\Network Interface(*)\Packets Outbound Errors'

# Adapter details
Get-NetAdapterStatistics | Select-Object Name, ReceivedBytes, SentBytes, ReceivedDiscardedPackets, OutboundDiscardedPackets
```

## Windows Performance Analyzer (WPA)

For deep-dive analysis, collect a Windows Performance Recorder (WPR) trace:

```cmd
:: Start trace
wpr -start CPU -start DiskIO -start Network -filemode

:: Stop and save
wpr -stop C:\Logs\trace-$(date /t).etl

:: Open in WPA (Windows Performance Analyzer) for flame graphs and timeline analysis
```
