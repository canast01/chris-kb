# Azure Backup

```mermaid
flowchart LR
    Azure_Backup["Azure Backup"]
    Azure_Backup --> S0["Purpose"]
    Azure_Backup --> S1["Common checks"]
    Azure_Backup --> S2["Incident notes"]
    Azure_Backup --> S3["Change notes"]
    Azure_Backup --> S4["Useful commands"]
    Azure_Backup --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure Backup and DR Azure Backup notes, checks, troubleshooting, commands, change notes, and field references.

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
