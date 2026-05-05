# VM Snapshot Cleanup Runbook

## Overview

Use this to find and clean up old or risky VM snapshots.

## Pre-Checks

- Confirm snapshot owner.
- Confirm snapshot age.
- Confirm backup status.
- Confirm datastore free space.
- Confirm no active backup or replication job.
- Confirm application owner approval if needed.

## Steps

1. Identify snapshots older than the approved threshold.
2. Confirm owner and purpose.
3. Check datastore capacity.
4. Remove snapshots during a safe window.
5. Monitor consolidation tasks.
6. Resolve consolidation warnings if needed.
7. Document cleanup results.

## Validation

- Snapshot removed.
- VM has no consolidation warning.
- Datastore capacity is stable.
- Application owner confirms no issue if required.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
