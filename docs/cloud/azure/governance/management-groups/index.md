# Management Groups

```mermaid
flowchart LR
    Management_Groups["Management Groups"]
    Management_Groups --> S0["Purpose"]
    Management_Groups --> S1["Common checks"]
    Management_Groups --> S2["Incident notes"]
    Management_Groups --> S3["Change notes"]
    Management_Groups --> S4["Useful commands"]
    Management_Groups --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure Governance Management Groups notes, checks, troubleshooting, commands, change notes, and field references.

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
