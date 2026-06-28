---
tags:
  - dell
  - operations
---
# CloudIQ: Proactive Recommendations and Implementation Tracking

<div class="kb-summary">
CloudIQ: Proactive Recommendations and Implementation Tracking reference covering Implementing a Recommendation, Energy Savings Recommendations, Tracking Recommendation History, Common Recommendation Issues.

*Applies to: CloudIQ*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Common Recommendation Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| No recommendations appearing | New system, insufficient history | Wait 7+ days for telemetry analysis |
| Recommendation keeps reappearing | Not fully implemented | Verify change was applied on system side |
| Incorrect impact estimate | Edge case in analytics model | Dismiss with note, open feedback via support portal |
| Firmware recommendation not applying | System in production, change window needed | Schedule and mark as in-progress with comment |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [CloudIQ: Alert Types, Severity, and Notification Configuration](alerts.md)
- [Dell CloudIQ Backup and Restore](backup-restore.md)
- [CloudIQ: Capacity Forecasting and Pool Utilisation](capacity.md)
- [CloudIQ — Operations](index.md)
- [CloudIQ — Architecture](../architecture/)
- [CloudIQ — Initial Setup](../deploy/)
- [CloudIQ — Security](../security/)
- [CloudIQ — Troubleshooting](../troubleshooting/)
