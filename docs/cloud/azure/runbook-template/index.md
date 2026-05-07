# Azure Runbook Template

```mermaid
flowchart LR
    Runbook_Template["Runbook Template"]
    Runbook_Template --> S0["Purpose"]
    Runbook_Template --> S1["Common checks"]
    Runbook_Template --> S2["Incident notes"]
    Runbook_Template --> S3["Change notes"]
    Runbook_Template --> S4["Useful commands"]
    Runbook_Template --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure runbook template notes, checks, troubleshooting, commands, change notes, and field references.

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
