---
tags:
  - troubleshooting
  - windows
search:
  boost: 1.5
---
# Windows Server — Diagnostics


<div class="kb-summary">
Diagnostics reference covering Windows Event Log Pipeline, Key Security Event IDs, Searching by Event ID, Exporting Logs, Event Log Forwarding (WEF) and 3 more sections.

*Applies to: Windows Server 2019 / 2022*
</div>
![Windows Server — Diagnostics](../../../../assets/compute-windows-server-troubleshooting-diagnostics-index.svg)


Diagnostic procedures and log analysis.

## Before you begin

- **Access:** Local Administrator or Domain Admin on target hosts
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Windows Event Log Pipeline

```mermaid
flowchart LR
    kernel["Kernel / Drivers"]
    apps["Applications\n.NET · SQL · IIS"]
    svcEvents["Services\nstart · stop · crash"]
    security["Security Subsystem\nauth · privilege · object access"]

    sysLog["System Event Log"]
    appLog["Application Event Log"]
    secLog["Security Event Log"]
    psLog["PowerShell Log"]

    siem["SIEM\nEvent Hub · Splunk"]
    wef["WEF Collector\nWindows Event Forwarding"]

    kernel --> sysLog
    svcEvents --> sysLog
    apps --> appLog
    security --> secLog
    sysLog --> wef
    appLog --> wef
    secLog --> wef
    psLog --> wef
    wef --> siem
```


## Exporting Logs

```powershell
# Export Security log to EVTX file
wevtutil epl Security C:\Logs\Security-$(Get-Date -Format 'yyyyMMdd').evtx

# Export filtered events to XML
Get-WinEvent -FilterHashtable @{ LogName='System'; Level=2 } -MaxEvents 500 |
    Export-Clixml C:\Logs\SystemErrors.xml

# Export to CSV for analysis
Get-WinEvent -FilterHashtable @{ LogName='System'; Level=2; StartTime=(Get-Date).AddDays(-7) } |
    Select-Object TimeCreated, Id, LevelDisplayName, Message |
    Export-Csv C:\Logs\SystemErrors.csv -NoTypeInformation
```

## Event Log Forwarding (WEF)

Windows Event Forwarding collects events centrally from multiple servers.

```powershell
# On collector — enable WecSvc
wecutil qc /q

# Create subscription (from XML file)
wecutil cs C:\Subscriptions\security-events.xml

# List subscriptions
wecutil es

# Check subscription status
wecutil gr <SubscriptionName>
```

On source servers, configure via GPO:
- `Computer Configuration → Windows Settings → Security Settings → System Services → Windows Remote Management → Automatic`
- `Computer Configuration → Administrative Templates → Windows Components → Event Forwarding → Configure target Subscription Manager`

## Log Size and Retention

```powershell
# Check current log sizes and limits
Get-WinEvent -ListLog System, Application, Security |
    Select-Object LogName, MaximumSizeInBytes,
        @{N="CurrentSizeMB"; E={ [math]::Round($_.FileSize/1MB,1) }},
        LogMode

# Set max size (e.g., Security log to 1 GB)
wevtutil sl Security /ms:1073741824

# Clear a log (after archiving)
wevtutil cl Application
```

## Sysmon (Extended Logging)

If Sysmon is deployed:

```powershell
# Process creation events (Event ID 1)
Get-WinEvent -LogName 'Microsoft-Windows-Sysmon/Operational' |
    Where-Object { $_.Id -eq 1 } |
    Select-Object -First 20 TimeCreated, Message | Format-List

# Network connections (Event ID 3)
Get-WinEvent -LogName 'Microsoft-Windows-Sysmon/Operational' |
    Where-Object { $_.Id -eq 3 } |
    Select-Object -First 20 TimeCreated, Message | Format-List
```

---

## Performance Analysis

Performance monitoring, baseline capture, and bottleneck identification.

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

### Collecting Diagnostics for Vendor/TAC

```powershell
# System info
msinfo32 /report C:\Logs\msinfo32-$(hostname)-$(Get-Date -Format yyyyMMdd).txt

# Event logs export
wevtutil epl System C:\Logs\System.evtx
wevtutil epl Application C:\Logs\Application.evtx
wevtutil epl Security C:\Logs\Security.evtx

# Network trace (2-minute capture)
netsh trace start capture=yes tracefile=C:\Logs\nettrace.etl
Start-Sleep 120
netsh trace stop
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable

---

## See also

- [Windows Server — Common Issues](../common-issues/)
- [Windows Server — Escalation](../escalation/)
- [Windows Server — Health Checks](../../operations/health-checks/)
