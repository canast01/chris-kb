# Virtualization Maintenance Window Runbook

## Overview

Use this for planned work across VMware, VxRail, NSX, Aria, hosts, clusters, or related services.

## Pre-Checks

- Confirm approved change.
- Confirm scope.
- Confirm maintenance window.
- Confirm rollback plan.
- Confirm backups or recovery points.
- Confirm stakeholders and support contacts.
- Confirm no active high-risk alerts.

## Steps

1. Announce start of work.
2. Capture current health.
3. Place affected systems into maintenance state if needed.
4. Complete planned work.
5. Monitor tasks and alerts.
6. Validate services.
7. Announce completion.
8. Update the change record.

## Validation

- No new critical alerts.
- Hosts are connected.
- VMs are running.
- Datastores are accessible.
- Network connectivity is healthy.
- Monitoring is current.
- Change record is updated.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
