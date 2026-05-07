# Managed Disks

```mermaid
flowchart LR
    Managed_Disks["Managed Disks"]
    Managed_Disks --> S0["Purpose"]
    Managed_Disks --> S1["Common checks"]
    Managed_Disks --> S2["Incident notes"]
    Managed_Disks --> S3["Change notes"]
    Managed_Disks --> S4["Useful commands"]
    Managed_Disks --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure Storage Managed Disks notes, checks, troubleshooting, commands, change notes, and field references.

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
