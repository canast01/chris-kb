# VxRail Pre-Upgrade Checks

## Overview

Use this page before VxRail lifecycle upgrades or firmware updates.

```text
  ┌──────────────────────────────────────────────────────┐
  │             Pre-Upgrade Check Gate                   │
  │                                                      │
  │  Compatibility                                       │
  │  Dell IMT ──► target version ──► vSphere/vSAN/NSX   │
  │                 │                                    │
  │                 ▼                                    │
  │  Cluster health                                      │
  │  VxRail Mgr ──► all green │ no active faults        │
  │  vSAN ──► no degraded disk groups                   │
  │                 │                                    │
  │                 ▼                                    │
  │  Free capacity                                       │
  │  vSAN slack > 30% ──► sufficient for remediation    │
  │  Datastore not full ──► ISOs / bundles fit           │
  │                 │                                    │
  │                 ▼                                    │
  │  Snapshots                                           │
  │  No old/large snapshots on cluster VMs              │
  │  Consolidate before LCM                             │
  │                 │                                    │
  │                 ▼                                    │
  │  All checks pass ──► proceed with LCM upgrade       │
  │  Any fail ──► resolve before starting               │
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
