# Diagnostic Settings

```mermaid
flowchart LR
    Diagnostic_Settings["Diagnostic Settings"]
    Diagnostic_Settings --> S0["Purpose"]
    Diagnostic_Settings --> S1["Common checks"]
    Diagnostic_Settings --> S2["Incident notes"]
    Diagnostic_Settings --> S3["Change notes"]
    Diagnostic_Settings --> S4["Useful commands"]
    Diagnostic_Settings --> S5["Known issues"]
```

## Purpose

Use this page for practical Azure Monitoring Diagnostic Settings notes, checks, troubleshooting, commands, change notes, and field references.

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
