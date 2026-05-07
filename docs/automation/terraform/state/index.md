# State

```mermaid
flowchart LR
    State["State"]
    State --> S0["Purpose"]
    State --> S1["Common checks"]
    State --> S2["Incident notes"]
    State --> S3["Change notes"]
    State --> S4["Useful commands"]
    State --> S5["Known issues"]
```

## Purpose

Use this page for practical Terraform State notes, checks, troubleshooting, commands, change notes, and field references.

## Common checks

- Confirm current health
- Review active alerts
- Check recent changes
- Confirm dependencies
- Check logs, events, and monitoring
- Capture current state before changes

## Incident notes

Capture:

- Symptom
- Start time
- Impact
- System or service name
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

Add tested commands here.

## Known issues

Add known issues here as they come up.
