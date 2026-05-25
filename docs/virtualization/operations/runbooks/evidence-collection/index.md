# Virtualization Evidence Collection

```text
┌─────────────────────────────────────────────────────────────────┐
│                  EVIDENCE COLLECTION WORKFLOW                   │
└──────────────────────────┬──────────────────────────────────────┘
                           │
   ┌───────────────────────▼───────────────────────┐
   │  COLLECT                                      │
   │  ┌─────────┐ ┌────────────┐ ┌──────────────┐ │
   │  │  Logs   │ │Screenshots │ │ Support      │ │
   │  │ hostd   │ │  alarms    │ │ Bundles      │ │
   │  │ vpxa    │ │  tasks     │ │ vm-support   │ │
   │  │ vmkernel│ │  events    │ │ vCenter logs │ │
   │  └────┬────┘ └─────┬──────┘ └──────┬───────┘ │
   └───────┼────────────┼───────────────┼──────────┘
           └────────────┴───────┬────────┘
                                ▼
              ┌─────────────────────────────┐
              │  Build Timeline             │
              │  Affected objects, tz, IDs  │
              └──────────────┬──────────────┘
                             │
              ┌──────────────▼──────────────┐
              │  Bundle & Upload             │
              │  Vendor portal / ticket      │
              └─────────────────────────────┘
```

## Overview

Use this before vendor escalation, RCA work, or major incident review.

## Pre-Checks

- Confirm issue scope.
- Confirm affected objects.
- Confirm timestamps.
- Confirm recent changes.
- Confirm ticket or case number if available.

## Steps

1. Capture screenshots of alarms.
2. Export recent tasks and events.
3. Capture affected object names.
4. Capture timestamps and timezone.
5. Collect support bundles if needed.
6. Record commands already run.
7. Record impact and current status.

## Validation

- Evidence is complete enough for handoff.
- Timeline is clear.
- Affected systems are listed.
- Next owner has what they need.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
