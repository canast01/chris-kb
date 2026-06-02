# PowerShell — Escalation


<div class="kb-summary">
> Part of the [PowerShell Troubleshooting](../index.md) reference.
</div>

---

## Escalation Matrix

| Severity | Criteria | First Responder | Escalation Target | SLA |
|---|---|---|---|---|
| P1 — Critical | Production automation fully stopped; business impact ongoing | On-call automation engineer | Platform lead + infrastructure manager | Acknowledge in 15 min; update every 30 min |
| P2 — High | Scheduled job failing; degraded automation; workaround available | Automation team (business hours) | Platform lead | Acknowledge in 1 hr; resolve within 4 hr |
| P3 — Medium | Non-critical script failure; dev/test environment affected | Automation team | Senior engineer | Resolve within next business day |
| P4 — Low | Intermittent error; cosmetic; documentation gap | Ticket assigned to automation team | N/A | Resolve within sprint |

---

## Information to Collect Before Escalating

Never escalate without collecting this data first. Incomplete escalations waste time and delay resolution.

### 1. PowerShell Environment

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
(paste $Error[0].Exception.Message here)
```text

**Stack Trace:**
```
(paste $Error[0].ScriptStackTrace here)
```text

**Recent Changes:**

**Transcript Attached:** [Yes / No]
**Workaround in Place:** [Yes — describe / No]

**Business Impact:**
```

---

## Escalation Contacts

| Role | Contact | Channel | Hours |
|---|---|---|---|
| On-Call Automation Engineer | PagerDuty rotation | PagerDuty → "Platform Automation" | 24/7 for P1/P2 |
| Platform Lead | platform-lead@example.com | Slack #platform-automation | Business hours |
| Infrastructure Manager | infra-mgr@example.com | Slack #infra-escalation | Business hours |
| Security (if credential/access issue) | security-ops@example.com | Slack #security-ops | 24/7 for P1 |
| Microsoft Support | Enterprise Agreement portal | CSS case | Per EA SLA |

> Update this table to reflect your organisation's actual contacts.

---

## Production Script Failure Runbook

Follow these steps in order when a production automation script fails.

### Step 1 — Confirm the Failure

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

### Step 2 — Assess Business Impact

- Is the automation blocking a downstream process?
- Is there data loss risk (e.g., a backup or sync job)?
- Is there a manual workaround that operations can perform?

Document the impact in the incident ticket immediately.

### Step 3 — Attempt Immediate Remediation

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

Common quick fixes:

| Symptom | Quick fix |
|---|---|
| `Access is denied` | Credential rotation may have expired the service account password — update scheduled task credential |
| Module not found | Module removed or path changed — reinstall: `Install-Module MyModule -Force` |
| Script not found | Deployment failure — restore script from source control |
| WinRM failure | WinRM service stopped on target — `Invoke-Command { Start-Service WinRM }` (if any remoting still works) |
| Certificate error | Cert expired — renew cert or switch to HTTP (non-prod only) |

### Step 4 — Engage Escalation Path (if Step 3 fails)

1. Post in `#platform-automation` Slack with the incident number and brief description
2. If P1: trigger PagerDuty alert for the platform automation rotation
3. Attach all collected diagnostic data to the ticket
4. Set incident status to "In Progress — Escalated"
5. Provide a status update every 30 minutes until resolved

### Step 5 — Post-Incident

After resolution, within 24 hours:

- [ ] Root cause documented in the ticket
- [ ] Incident timeline recorded
- [ ] Remediation steps validated
- [ ] Monitoring/alerting gap identified and ticket created
- [ ] Script updated if code was root cause — PR raised and merged
- [ ] Post-mortem scheduled if P1 or P2

---

## Recurring Failure Register

Track recurring failures to identify systemic issues.

| Script | Failure Count (last 90d) | Last Failure | Root Cause | Status |
|---|---|---|---|---|
| Backup-VMs.ps1 | 3 | 2026-04-01 | WinRM credential expiry | Monitoring added |
| Sync-ADGroups.ps1 | 1 | 2026-03-15 | Network timeout | Under investigation |
| Deploy-Widget.ps1 | 0 | — | — | Healthy |

> Maintain this table in your team wiki or ITSM system. Scripts with more than 2 failures in 90 days require a reliability review.
