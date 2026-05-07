# Restore Testing

```mermaid
flowchart LR
    Restore_Testing["Restore Testing"]
    Restore_Testing --> S0["Purpose"]
    Restore_Testing --> S1["Common checks"]
    Restore_Testing --> S2["Incident notes"]
    Restore_Testing --> S3["Change notes"]
    Restore_Testing --> S4["Useful commands"]
    Restore_Testing --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure Backup and DR Restore Testing notes, checks, troubleshooting, commands, change notes, and field references.

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
