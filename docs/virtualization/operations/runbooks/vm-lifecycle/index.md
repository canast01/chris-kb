# VM Lifecycle Runbook

```
┌─────────────────────────────────────────────────────────────────┐
│                      VM LIFECYCLE FLOW                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  REQUEST  ► Validate owner, purpose, sizing, network    │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  BUILD    ► Deploy from template, apply naming/tags     │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  CONFIGURE ► Backup policy, monitoring, access          │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  HAND-OFF  ► Validate connectivity, document owner      │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  REVIEW    ► Periodic check: owner, purpose, usage      │
   └───────────────────────┬─────────────────────────────────┘
                           │
   ┌───────────────────────▼─────────────────────────────────┐
   │  RETIRE/CLEANUP ► Confirm approval ► Power off ►        │
   │  Remove backup ► Delete VM ► Update CMDB                │
   └─────────────────────────────────────────────────────────┘
```

## Overview

Use this for VM build, change, ownership, review, retirement, and cleanup.

## Pre-Checks

- Confirm VM owner.
- Confirm business purpose.
- Confirm sizing.
- Confirm backup policy.
- Confirm monitoring.
- Confirm network and security requirements.
- Confirm naming standard.

## Steps

1. Validate request details.
2. Build or update VM.
3. Apply naming and tagging standards.
4. Confirm backup and monitoring.
5. Validate access and connectivity.
6. Record owner and lifecycle notes.
7. Review unused VMs regularly.
8. Decommission cleanly when approved.

## Validation

- VM has owner.
- VM follows naming standard.
- Backup is assigned.
- Monitoring is active.
- Tags or inventory notes are current.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
