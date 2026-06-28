---
tags:
  - operations
  - powershell
---
# PowerShell — Health Checks

<div class="kb-summary">
Health Checks reference covering Module Health, Scheduled Tasks, Remoting Connectivity.

*Applies to: PowerShell 7.x*
</div>

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
run_this_routine: "Run This Routine" {shape: rectangle}
scheduled_tasks: "Scheduled Tasks" {shape: rectangle}
remoting_connectivity: "Remoting Connectivity" {shape: rectangle}
powershell_environment_health_check_: "PowerShell Environment Health Check Flow" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> run_this_routine
run_this_routine -> scheduled_tasks
scheduled_tasks -> remoting_connectivity
remoting_connectivity -> powershell_environment_health_check_
powershell_environment_health_check_ -> verify
verify -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

```powershell
# 1. PowerShell version
$PSVersionTable

# 2. Module inventory
Get-Module -ListAvailable | Sort Name | Select Name,Version | Format-Table

# 3. Scheduled task health — running tasks or tasks with non-zero last result
Get-ScheduledTask | Where {$_.State -eq 'Running' -or $_.LastTaskResult -ne 0} | Select TaskName,State,LastTaskResult

# 4. Execution policy — verify no unexpected restrictions
Get-ExecutionPolicy -List

# 5. WinRM connectivity (for remoting)
Test-WSMan -ComputerName <target>

# 6. PowerShell Core availability — verify if cross-platform scripts require PS Core
pwsh -Version
```

**List only installed PSGallery modules**

```powershell
Get-InstalledModule | Sort-Object Name | Select-Object Name, Version, PublishedAt
```

**Check for outdated modules**

```powershell
Get-InstalledModule | ForEach-Object {
    $latest = Find-Module $_.Name -ErrorAction SilentlyContinue
    if ($latest -and $latest.Version -gt $_.Version) {
        [PSCustomObject]@{
            Name           = $_.Name
            Installed      = $_.Version
            Latest         = $latest.Version
        }
    }
}
```

**Update a specific module**

```powershell
Update-Module -Name <ModuleName> -Force
```

**Verify a critical module is importable**

```powershell
Import-Module <ModuleName> -ErrorAction Stop
Get-Command -Module <ModuleName> | Measure-Object
```

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| Critical modules present | All required modules found | Install via `Install-Module` |
| Module versions | Current or pinned release | Update or pin in deployment scripts |
| Import without error | No `CommandNotFoundException` | Resolve missing dependencies |
| Duplicate module versions | Single version per module | Remove stale versions with `Uninstall-Module` |

---

## Scheduled Tasks

PowerShell automation frequently runs as scheduled tasks. Tasks that fail silently or stop running are a common source of undetected automation breakdowns.

**List all scheduled tasks with non-zero last result**

```powershell
Get-ScheduledTask | Where-Object { $_.LastTaskResult -ne 0 } |
    Select-Object TaskName, TaskPath, State, LastTaskResult |
    Sort-Object LastTaskResult
```

**List tasks currently in Running state**

```powershell
Get-ScheduledTask | Where-Object { $_.State -eq 'Running' } |
    Select-Object TaskName, TaskPath, State
```

**Check last run time and result for a specific task**

```powershell
Get-ScheduledTaskInfo -TaskName "<TaskName>" | Select-Object LastRunTime, LastTaskResult, NextRunTime
```

**Common exit codes**

| Exit code | Meaning |
|---|---|
| `0` | Success |
| `1` | General error |
| `0x41301` | Task is currently running |
| `0x80070005` | Access denied — check task account permissions |
| `0x8007010B` | Directory not found — check script path |

**Re-enable a disabled task**

```powershell
Enable-ScheduledTask -TaskName "<TaskName>"
```

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| `LastTaskResult` | `0` for all tasks | Investigate non-zero exit codes |
| Task state | `Ready` or `Running` | Re-enable `Disabled` tasks if unexpected |
| `NextRunTime` | Populated and future-dated | Re-register task if `NextRunTime` is null |
| Task account | Service account with least privilege | Audit tasks running as `SYSTEM` unnecessarily |

---

## Remoting Connectivity

PowerShell Remoting (WinRM) enables remote script execution and is required for Invoke-Command, Enter-PSSession, and many management tools.

**Test WinRM connectivity to a remote host**

```powershell
Test-WSMan -ComputerName <target>
```

A successful response returns an XML object with the WinRM service version. An error indicates WinRM is not running or a firewall is blocking port 5985 (HTTP) or 5986 (HTTPS).

**Test network connectivity to WinRM port**

```powershell
Test-NetConnection -ComputerName <target> -Port 5985
```

**List configured PS session configurations**

```powershell
Get-PSSessionConfiguration | Select-Object Name, Enabled, Permission
```

**Test a remote session end-to-end**

```powershell
$session = New-PSSession -ComputerName <target> -ErrorAction Stop
Invoke-Command -Session $session -ScriptBlock { $env:COMPUTERNAME }
Remove-PSSession $session
```

**Check WinRM service status on the remote host**

```powershell
Invoke-Command -ComputerName <target> -ScriptBlock { Get-Service WinRM | Select-Object Status }
```

**JEA endpoint check**

```powershell
# List JEA endpoints
Get-PSSessionConfiguration | Where-Object { $_.SessionType -eq 'RestrictedRemoteServer' }
```

**Key health indicators**

| Indicator | Healthy | Action Required |
|---|---|---|
| `Test-WSMan` response | Returns WinRM XML object | Enable WinRM: `Enable-PSRemoting -Force` |
| Port 5985/5986 | TCP open | Check Windows Firewall and network ACLs |
| PS session creation | No authentication errors | Verify Kerberos/NTLM and DNS resolution |
| Session configuration | `Enabled = True` | Enable with `Enable-PSSessionConfiguration` |

---

## PowerShell Environment Health Check Flow

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [PowerShell — Procedures](../procedures/)
- [PowerShell — CLI Reference](../cli-reference/)
- [PowerShell — Common Issues](../../troubleshooting/common-issues/)
