# ESXi Host Evacuation Runbook

## Overview

Use this before host maintenance, patching, hardware work, or lifecycle activity.

## Pre-Checks

- Confirm cluster capacity.
- Confirm DRS status.
- Confirm no pinned or special workload constraints.
- Check datastore access.
- Check vSAN resync activity if used.
- Confirm host hardware health.
- Confirm maintenance window.

## Steps

1. Review running VMs on the host.
2. Check cluster capacity.
3. Check vSAN health if used.
4. Enter maintenance mode using the correct evacuation option.
5. Monitor VM migrations.
6. Resolve stuck migrations if needed.
7. Complete maintenance.
8. Exit maintenance mode.
9. Confirm host health.

## Validation

- Host exits maintenance mode cleanly.
- VMs are running.
- Cluster capacity is normal.
- No new vSAN issues.
- No new host alarms.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
