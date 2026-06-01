# CyberArk — Diagnostics


<div class="kb-summary">
Use this page for practical CyberArk troubleshooting notes, checks, commands, change notes, and field references.
</div>

## CyberArk Diagnostic Flow

```mermaid
flowchart TD
    issue["CyberArk issue reported\n(login failure / rotation failed / session error)"]
    issue --> component{"Which component?"}
    component -->|"can't log in to PVWA"| pvwaCheck["Check PVWA IIS app pool\nGet-WebApplication PasswordVault\nVerify PVWA → Vault :1858"]
    component -->|"password rotation failed"| cpmCheck["Check CPM service\nGet-Service 'CyberArk Central Policy Manager'\nReview pm.log for error code"]
    component -->|"PSM session fails"| psmCheck["Check PSM service\nGet-Service 'Cyber-Ark Privileged Session Manager'\nReview PSMConsole.log"]
    component -->|"LDAP / MFA issues"| authCheck["Test LDAPS :636 from PVWA\nTest RADIUS :1812 to Duo Proxy\nCheck PVWA auth configuration"]
    pvwaCheck --> vaultConn["Test-NetConnection vault01 -Port 1858"]
    cpmCheck --> vaultConn
    psmCheck --> vaultConn
    vaultConn --> vaultOK{"Vault reachable?"}
    vaultOK -->|"no"| networkFix["Check firewall rules\nbetween component and Vault"]
    vaultOK -->|"yes"| logsReview["Review component logs\nCheck SIEM for audit events"]
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

Add tested commands here.
