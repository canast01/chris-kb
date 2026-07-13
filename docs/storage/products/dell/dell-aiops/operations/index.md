---
tags:
  - dell
  - operations
description: "Dell AIOps Operations reference covering Daily Checklist, Alert Triage Workflow, Health Score Decline Investigation. FAQFrequently asked questions, common..."
---
# Dell AIOps Operations

<div class="kb-summary">
Dell AIOps Operations reference covering Daily Checklist, Alert Triage Workflow, Health Score Decline Investigation.

*Applies to: Dell AIOps*
  <a class="kb-card" href="faq/"><strong>FAQ</strong><span>Frequently asked questions, common issues, and quick answers for day-to-day operations.</span></a>
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Daily Checklist

| Check | Location | Pass Criteria |
|---|---|---|
| New Critical recommendations | CloudIQ > AIOps > Recommendations | No unacknowledged Critical recommendations |
| Active anomaly alerts | CloudIQ > AIOps > Anomalies | Review any new anomalies; no unacknowledged Critical anomalies |
| Infrastructure health scores | CloudIQ > Assets | No systems below 60 health score |
| SCG collection status | SCG admin UI > Systems | All systems show last-seen within 30 minutes |
| Notification delivery | CloudIQ > Settings > Notifications > Delivery Log | No failed notification deliveries |

## Alert Triage Workflow

### Critical or High Recommendation

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Alerts](../alerts/)
- [Architecture](../architecture/)
- [Cli Reference](../cli-reference/)
- [Deploy](../deploy/)
- [Design Standards](../design-standards/)
- [Insights](../insights/)
- [Integration](../integration/)
- [Learning Path](../learning-path/)
- [Lifecycle](../lifecycle/)
- [Recommendations](../recommendations/)
- [Reporting](../reporting/)
- [Scripts](../scripts/)
- [Security](../security/)
- [Troubleshooting](../troubleshooting/)
- [Vendor Support](../vendor-support/)
- [Dell AIOps — Overview](../)
