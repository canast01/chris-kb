# Alert Tuning

Alert tuning is important because too many low-value alerts create noise.

```mermaid
flowchart LR
    Alert_Tuning["Alert Tuning"]
    Alert_Tuning --> S0["Good Alert Tuning Should Include"]
    Alert_Tuning --> S1["Common checks"]
    Alert_Tuning --> S2["Incident notes"]
    Alert_Tuning --> S3["Change notes"]
    Alert_Tuning --> S4["Useful commands"]
    Alert_Tuning --> S5["Known issues"]
```

## Good Alert Tuning Should Include

- Clear severity levels
- Actionable descriptions
- Ownership or assignment
- Escalation path
- Suppression rules for known maintenance windows
- Review of repeat alerts
- Removal of stale or low-value alerts

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
