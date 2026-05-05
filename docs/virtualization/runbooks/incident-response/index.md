# Virtualization Incident Response

## Overview

Use this during virtualization incidents where VMs, hosts, clusters, datastores, networking, or management tools are impacted.

## Pre-Checks

- Confirm impact and scope.
- Identify affected applications or business services.
- Check recent changes.
- Confirm management access.
- Review vCenter, ESXi, vSAN, NSX, VxRail, and Aria alerts.
- Start a timeline.

## Steps

1. Confirm whether impact is VM, host, cluster, storage, network, or management-plane related.
2. Check vCenter alarms and recent tasks.
3. Check host connection state.
4. Check datastore and vSAN health.
5. Check network connectivity and NSX health if used.
6. Check VxRail Manager if the environment is VxRail.
7. Capture screenshots and timestamps.
8. Escalate with clear scope and evidence.

## Validation

- Impact is understood.
- Affected objects are identified.
- Current health is documented.
- Next action owner is clear.
- Timeline has been started.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
