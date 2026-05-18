# RCA Template

```
┌─────────────────────────────────────────────────────────────────┐
│                      RCA STRUCTURE FLOW                         │
└──────────────────────────┬──────────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  TIMELINE                                               │
   │  Detected ► Investigated ► Cause ID'd ► Fix ► Restored  │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  ROOT CAUSE                                             │
   │  Single direct cause of the failure event               │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  CONTRIBUTING FACTORS                                   │
   │  Config drift │ Missing monitoring │ Process gap         │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  CORRECTIVE ACTIONS                                     │
   │  Immediate fix applied to restore service               │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  PREVENTION                                             │
   │  Monitoring │ Runbook │ Change process │ Automation      │
   └─────────────────────────────────────────────────────────┘
```

## Summary

Brief description of what happened.

## Impact

Systems, users, applications, or services affected.

## Timeline

| Time | Event |
|---|---|
| HH:MM | Issue detected |
| HH:MM | Investigation started |
| HH:MM | Cause identified |
| HH:MM | Fix applied |
| HH:MM | Service restored |

## Root Cause

Explain the actual cause of the issue.

## Resolution

Explain what was done to fix it.

## Prevention

List steps to reduce the chance of the issue happening again.

## Evidence

Attach logs, screenshots, events, support case numbers, and validation results.
