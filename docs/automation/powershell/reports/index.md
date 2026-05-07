# PowerShell Reports

## Export-CSV and ConvertTo-Csv

CSV exports are the simplest way to produce shareable tabular data.

```powershell
# Export service status to CSV
Get-Service | Select-Object Name, DisplayName, Status |
    Export-Csv -Path C:\Reports\services.csv -NoTypeInformation -Encoding UTF8

# Append rows to an existing CSV
Get-Process | Select-Object Name, Id, CPU |
    Export-Csv -Path C:\Reports\processes.csv -Append -NoTypeInformation

# Convert to CSV string (no file)
$data = Get-Process | Select-Object Name, CPU | ConvertTo-Csv -NoTypeInformation
```

## HTML Reports with ConvertTo-Html

```powershell
# Basic HTML report
$header = "<style>body{font-family:Arial} table{border-collapse:collapse} td,th{border:1px solid #ccc;padding:6px}</style>"

Get-Service |
    Where-Object { $_.Status -eq 'Stopped' } |
    Select-Object Name, DisplayName, StartType |
    ConvertTo-Html -Title "Stopped Services" -Head $header |
    Out-File C:\Reports\stopped-services.html

# Multi-section HTML report
$htmlBody = ""
$htmlBody += "<h2>Disk Usage</h2>"
$htmlBody += Get-PSDrive -PSProvider FileSystem |
    Select-Object Name, @{N='Used(GB)';E={[math]::Round($_.Used/1GB,2)}}, @{N='Free(GB)';E={[math]::Round($_.Free/1GB,2)}} |
    ConvertTo-Html -Fragment

$htmlBody += "<h2>Top Processes by CPU</h2>"
$htmlBody += Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, CPU, WorkingSet |
    ConvertTo-Html -Fragment

ConvertTo-Html -Title "Server Report" -Head $header -Body $htmlBody |
    Out-File C:\Reports\server-report.html
```

## Send-MailMessage and Email Reports

```powershell
# Send a report by email (PowerShell 5.1 — deprecated but still functional)
$mailParams = @{
    To         = 'ops-team@example.com'
    From       = 'automation@example.com'
    Subject    = "Daily Server Report - $(Get-Date -Format 'yyyy-MM-dd')"
    Body       = (Get-Content C:\Reports\server-report.html -Raw)
    BodyAsHtml = $true
    SmtpServer = 'smtp.example.com'
    Port       = 587
    Credential = (Get-Credential)
    UseSsl     = $true
    Attachments = 'C:\Reports\services.csv'
}
Send-MailMessage @mailParams
```

## Scheduled Tasks for Automated Reports

```powershell
# Create a scheduled task to run a report script daily
$action  = New-ScheduledTaskAction -Execute 'powershell.exe' `
               -Argument '-NonInteractive -File C:\Scripts\daily-report.ps1'
$trigger = New-ScheduledTaskTrigger -Daily -At '06:00AM'
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -RunOnlyIfNetworkAvailable

Register-ScheduledTask `
    -TaskName   'DailyServerReport' `
    -TaskPath   '\Automation\' `
    -Action     $action `
    -Trigger    $trigger `
    -Settings   $settings `
    -RunLevel   Highest `
    -Description 'Generate and email daily server report'

# Run the task immediately for testing
Start-ScheduledTask -TaskPath '\Automation\' -TaskName 'DailyServerReport'

# Check last run result
Get-ScheduledTaskInfo -TaskPath '\Automation\' -TaskName 'DailyServerReport' |
    Select-Object LastRunTime, LastTaskResult
```

## Report Format Reference

| Format | Cmdlet | Best for |
|---|---|---|
| CSV | `Export-Csv` | Excel, data import, simple tables |
| HTML | `ConvertTo-Html` | Emailed reports, dashboards |
| JSON | `ConvertTo-Json` | API output, structured data exchange |
| Excel | `ImportExcel` module | Rich formatting, charts |
| XML | `Export-Clixml` | PowerShell object serialisation |
| Text | `Out-File` | Logs, plain-text summaries |

```powershell
# JSON export example
Get-Process | Select-Object Name, Id, CPU |
    ConvertTo-Json -Depth 3 |
    Out-File C:\Reports\processes.json -Encoding UTF8
```
