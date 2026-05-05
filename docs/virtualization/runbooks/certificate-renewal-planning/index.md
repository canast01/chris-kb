# Virtualization Certificate Renewal Planning

## Overview

Use this before vCenter, NSX, VxRail, Aria, or related certificate renewals.

## Pre-Checks

- Identify certificate owner.
- Confirm expiration date.
- Confirm certificate type.
- Confirm replacement process.
- Confirm dependency impact.
- Confirm backup or snapshot position.
- Confirm maintenance window.

## Steps

1. Inventory certificates.
2. Confirm renewal method.
3. Confirm trust chain.
4. Create or request replacement certificate.
5. Apply during approved window.
6. Restart services only if required.
7. Validate login, API access, and integrations.

## Validation

- Certificate shows expected expiration.
- UI and API access work.
- Integrations still connect.
- Monitoring is green.
- No new certificate alarms.

## Rollback

- Stop the change if impact increases.
- Return settings to the last known good state where possible.
- Reconnect affected systems if disconnected.
- Escalate with logs, timestamps, screenshots, and task IDs.

## Notes

Keep this page updated with local commands, screenshots, system names, and known environment quirks.
