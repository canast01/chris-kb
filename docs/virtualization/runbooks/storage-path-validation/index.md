# Virtualization Storage Path Validation

## Overview

Use this after SAN changes, storage maintenance, host work, or datastore alerts.

## Pre-Checks

- Confirm affected hosts and datastores.
- Confirm storage array status.
- Confirm SAN zoning or masking changes.
- Confirm no active datastore outage.
- Confirm maintenance window if changes are planned.

## Steps

1. Check datastore visibility.
2. Check host storage adapters.
3. Check path count and path state.
4. Check multipathing policy.
5. Review storage latency.
6. Confirm VMs can access datastores.
7. Compare against expected path design.

## Validation

- Expected paths are visible.
- No dead paths remain unless expected.
- Datastores are mounted.
- Latency is normal.
- No new storage alarms.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
