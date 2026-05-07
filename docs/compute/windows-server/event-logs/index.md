# Windows Server Event Logs

Querying, filtering, and forwarding Windows event logs via PowerShell.
## Key Event Logs

| Log | Path | Content |
|---|---|---|
| System | `System` | OS events, driver failures, service stops, hardware |
| Application | `Application` | App errors, .NET exceptions, SQL, IIS |
| Security | `Security` | Authentication, account management, privilege use |
| Setup | `Setup` | Windows Update, component installs |
| Windows PowerShell | `Windows PowerShell` | PS script execution |
| Sysmon | `Microsoft-Windows-Sysmon/Operational` | Process creation, network, file events (if deployed) |

## Get-WinEvent — Common Queries

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
    LogName = 'Security'
    Id      = 4625
    StartTime = (Get-Date).AddHours(-24)
} | Select-Object TimeCreated, Message | Select-Object -First 20

# Successful logons (Event ID 4624)
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id      = 4624
} -MaxEvents 20 | Select-Object TimeCreated, Message
```

## Key Security Event IDs

| Event ID | Description |
|---|---|
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4634 | Logoff |
| 4648 | Logon with explicit credentials (RunAs) |
| 4663 | Object access attempt |
| 4688 | Process creation |
| 4698 | Scheduled task created |
| 4719 | Audit policy changed |
| 4720 | User account created |
| 4732 | Member added to a local security group |
| 4740 | Account locked out |
| 4756 | Member added to a universal security group |
| 7036 | Service started or stopped |
| 41 | Kernel power — unexpected reboot |
| 6008 | Unexpected shutdown |

## Searching by Event ID

```powershell
# Account lockouts in last hour
Get-WinEvent -FilterHashtable @{ LogName='Security'; Id=4740; StartTime=(Get-Date).AddHours(-1) } |
    ForEach-Object {
        $xml = [xml]$_.ToXml()
        [PSCustomObject]@{
            Time     = $_.TimeCreated
            Account  = $xml.Event.EventData.Data | Where-Object Name -eq 'TargetUserName' | Select-Object -ExpandProperty '#text'
            CallerDC = $xml.Event.EventData.Data | Where-Object Name -eq 'SubjectDomainName' | Select-Object -ExpandProperty '#text'
        }
    }

# Service stops (7034 = unexpected, 7036 = started/stopped)
Get-WinEvent -FilterHashtable @{ LogName='System'; Id=7034,7036; StartTime=(Get-Date).AddHours(-24) } |
    Select-Object TimeCreated, Message | Format-List
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
