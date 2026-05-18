# VxRail Node Health Review

## Overview

Use this page to review host, hardware, vSAN, and cluster health by node.

```
  ┌──────────────────────────────────────────────────────┐
  │            Node Health Review Workflow               │
  │                                                      │
  │  Hardware alerts                                     │
  │  iDRAC ──► VxRail Mgr ──► vCenter host alarms       │
  │                 │                                    │
  │                 ▼                                    │
  │  ┌──────────────────────────────────────────────┐    │
  │  │  Disk groups (per node)                      │    │
  │  │  vSAN ──► Disk Management ──► disk group OK? │    │
  │  │  Cache tier healthy │ Capacity tier healthy  │    │
  │  └──────────────────────┬───────────────────────┘    │
  │                         ▼                            │
  │  ┌──────────────────────────────────────────────┐    │
  │  │  Network state                               │    │
  │  │  vmnic link │ vmkernel IP │ vSAN vmk reachable│   │
  │  └──────────────────────┬───────────────────────┘    │
  │                         ▼                            │
  │  ┌──────────────────────────────────────────────┐    │
  │  │  iDRAC status                                │    │
  │  │  SEL: no critical events                     │    │
  │  │  Sensors: temp / PSU / fan all nominal       │    │
  │  └──────────────────────────────────────────────┘    │
  │                         │                            │
  │                         ▼                            │
  │  All green ──► node healthy ──► document result     │
  └──────────────────────────────────────────────────────┘
```

## Pre-Checks

- Confirm scope.
- Confirm maintenance window if changes are planned.
- Confirm current health.
- Check recent alerts and tasks.
- Confirm access to management tools.
- Confirm rollback path if configuration changes are made.

## Steps

1. Identify the affected object.
2. Capture current state.
3. Review alarms, logs, and recent changes.
4. Apply the planned action.
5. Validate service health.
6. Record notes and follow-up items.

## Validation

- Confirm the object is healthy.
- Confirm no new critical alarms.
- Confirm monitoring reflects the expected state.
- Confirm related systems still have access.
- Document the result.

## Rollback

- Revert the changed setting if possible.
- Restore prior configuration from documented state.
- Escalate if rollback requires vendor support.

## Notes

Keep screenshots, task IDs, error messages, and timestamps with the change or incident record.
