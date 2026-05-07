# Service Health

```mermaid
flowchart LR
    Service_Health["Service Health"]
    Service_Health --> S0["Purpose"]
    Service_Health --> S1["Common checks"]
    Service_Health --> S2["Incident notes"]
    Service_Health --> S3["Change notes"]
    Service_Health --> S4["Useful commands"]
    Service_Health --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure Monitoring Service Health notes, checks, troubleshooting, commands, change notes, and field references.

## Common checks

- Confirm subscription
- Confirm resource group
- Confirm region
- Review active alerts
- Review recent changes
- Check activity logs
- Check permissions
- Capture current state before changes

## Incident notes

Capture:

- Symptom
- Start time
- Impact
- Subscription
- Resource group
- Resource name
- Error message
- What changed
- What was checked
- Next action

## Change notes

- Confirm change approval
- Confirm maintenance window
- Confirm rollback plan
- Capture current state
- Make one change at a time
- Validate after the change

## Useful commands

Add tested Azure CLI or PowerShell commands here.

## Known issues

Add known issues here as they come up.
