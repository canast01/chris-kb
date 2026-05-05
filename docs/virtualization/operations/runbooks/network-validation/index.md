# Virtualization Network Validation

## Overview

Use this after network changes, VLAN changes, host work, NSX changes, or VM connectivity issues.

## Pre-Checks

- Confirm affected VLANs or segments.
- Confirm port groups or NSX segments.
- Confirm uplink status.
- Confirm recent switch or firewall changes.
- Confirm affected VM scope.

## Steps

1. Check VM network assignment.
2. Check port group or segment configuration.
3. Check host uplinks.
4. Check VLAN or overlay configuration.
5. Check gateway reachability.
6. Check NSX edge and routing if used.
7. Test from affected and unaffected VMs.

## Validation

- VM connectivity works.
- Uplinks are healthy.
- VLAN or segment config is correct.
- Routing is working.
- No new network alarms.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
