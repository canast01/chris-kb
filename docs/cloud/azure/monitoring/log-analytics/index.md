# Log Analytics

```mermaid
flowchart LR
    Log_Analytics["Log Analytics"]
    Log_Analytics --> S0["Purpose"]
    Log_Analytics --> S1["Common checks"]
    Log_Analytics --> S2["Incident notes"]
    Log_Analytics --> S3["Change notes"]
    Log_Analytics --> S4["Useful commands"]
    Log_Analytics --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure Monitoring Log Analytics notes, checks, troubleshooting, commands, change notes, and field references.

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
