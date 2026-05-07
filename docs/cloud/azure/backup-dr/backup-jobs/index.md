# Backup Jobs

```mermaid
flowchart LR
    Backup_Jobs["Backup Jobs"]
    Backup_Jobs --> S0["Purpose"]
    Backup_Jobs --> S1["Common checks"]
    Backup_Jobs --> S2["Incident notes"]
    Backup_Jobs --> S3["Change notes"]
    Backup_Jobs --> S4["Useful commands"]
    Backup_Jobs --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure Backup and DR Backup Jobs notes, checks, troubleshooting, commands, change notes, and field references.

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
