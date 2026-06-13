---
tags:
  - powershell
  - troubleshooting
---
# PowerShell — Escalation

```powershell
# Run on the affected host and attach output to the ticket
$PSVersionTable | ConvertTo-Json
Get-ExecutionPolicy -List
$env:PSModulePath -split [IO.Path]::PathSeparator
Get-Module | Select-Object Name, Version, Path | ConvertTo-Json
[System.Environment]::OSVersion.VersionString
[System.Environment]::Is64BitOperatingSystem
[System.Environment]::Is64BitProcess
```
```text
┌─────────────────────────────────────── PowerShell — Escalation ───────────────────────────────────────┐
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Escalate PowerShell issues to: infra team (remoting), vendor support (module bugs), Microsoft │   │
│   │     PowerShell Core issues: GitHub.com/PowerShell/PowerShell — file issue with repro steps    │   │
│   │Module issues: vendor support portal (VMware, Dell, Microsoft) — include module version + error│   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Triggers              │  │                Info to Gather               │   │
│   │          PS crashes / hangs on host          │  │            $PSVersionTable output           │   │
│   │        Module API returns wrong data         │  │           Get-InstalledModule list          │   │
│   │         WinRM broken after OS update         │  │           winrm get config output           │   │
│   │        JEA endpoint stops responding         │  │          Get-PSSessionConfiguration         │   │
│   │            DSC compilation errors            │  │          Get-DscConfigurationStatus         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   PS GitHub issues = file bugs at github.com/PowerShell/PowerShell with minimal repro script  │   │
│   │      DSC status       = Get-DscConfigurationStatus; shows last enactment result and error     │   │
│   │   WinRM event log  = Event Viewer → Microsoft → Windows → WinRM for connection error details  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

**Stack Trace:**
```
```text

**Recent Changes:**

**Transcript Attached:** [Yes / No]
**Workaround in Place:** [Yes — describe / No]

**Business Impact:**
```
```powershell
# Check scheduled task last run result
Get-ScheduledTaskInfo -TaskName 'MyAutomationTask' |
    Select-Object LastRunTime, LastTaskResult, NextRunTime

# LastTaskResult = 0 means success
# LastTaskResult = 0x1 (1) means incorrect function — generic failure
# LastTaskResult = 0x8007010B = directory not found
```
```powershell
# Check Windows Event Log for the automation source
Get-WinEvent -FilterHashtable @{
    LogName   = 'Application'
    StartTime = (Get-Date).AddHours(-2)
} | Where-Object { $_.ProviderName -like '*Widget*' -or $_.Message -like '*failed*' } |
    Select-Object TimeCreated, Id, LevelDisplayName, Message |
    Format-Table -Wrap
```
```powershell
# Re-run the scheduled task manually (if safe to do so)
Start-ScheduledTask -TaskName 'MyAutomationTask'

# Monitor task state
do {
    $info = Get-ScheduledTaskInfo -TaskName 'MyAutomationTask'
    Write-Host "$(Get-Date -Format HH:mm:ss) — State: $($info.LastRunTime) | Result: $($info.LastTaskResult)"
    Start-Sleep -Seconds 10
} until ((Get-ScheduledTask -TaskName 'MyAutomationTask').State -ne 'Running')
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

