# Venafi — Diagnostics


<div class="kb-summary">
Use this page for practical Venafi troubleshooting notes, checks, commands, change notes, and field references.
</div>

## Venafi Diagnostic Flow

```mermaid
flowchart TD
    issue["Venafi issue reported\n(cert not issuing / renewal failed / UI unavailable)"]
    issue --> svcCheck["Check Venafi services:\nGet-Service -Name 'Venafi*'"]
    svcCheck --> svcRunning{"All services\nrunning?"}
    svcRunning -->|"no"| startSvc["Start-Service Venafi*\nCheck Windows Event Log"]
    svcRunning -->|"yes"| sqlCheck["Test SQL connectivity:\nNew-Object SqlConnection + Open()"]
    startSvc --> sqlCheck
    sqlCheck --> sqlOK{"SQL connection\nok?"}
    sqlOK -->|"no"| fixSQL["Fix SQL connectivity:\nFirewall / credentials / AG failover"]
    sqlOK -->|"yes"| caCheck["Test CA connector:\nTPP UI → Config → CAs → Test Connection"]
    fixSQL --> caCheck
    caCheck --> caOK{"CA connector\nhealthy?"}
    caOK -->|"no"| caFix["Fix CA connectivity:\nADCS CES URL / DigiCert API key / network"]
    caOK -->|"yes"| logReview["Collect TPP logs:\nVdcLogFile*.log in ProgramData\\Venafi\\log"]
```

## Common Checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident Notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
- Error message
- What changed
- What was checked
- Next action

## Change Notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Useful Commands

```powershell
# Quick health check: verify core Venafi services are running
Get-Service -Name "Venafi*" | Select-Object Name, Status, StartType

# Verify SQL connectivity
$sql = New-Object System.Data.SqlClient.SqlConnection
$sql.ConnectionString = "Server=sql01.corp.example.com;Database=VenafiDB;Integrated Security=True"
$sql.Open()
Write-Host "SQL connection: $($sql.State)"
$sql.Close()
```
