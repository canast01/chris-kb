---
tags:
  - dell
  - operations
---
# Dell AIOps Operations

<div class="kb-summary">
Dell AIOps Operations reference covering Daily Checklist, Alert Triage Workflow, Health Score Decline Investigation.

*Applies to: Dell AIOps*
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

```text
┌─────────────────────────────────────── Dell AIOps — Operations ───────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Daily            │  │            Weekly           │  │           Monthly           │   │
│   │     Review alert console    │  │    Action recommendations   │  │       Capacity review       │   │
│   │       Check anomalies       │  │       Review insights       │  │       Threshold audit       │   │
│   │      Verify adapters OK     │  │     Update ITSM tickets     │  │        Access review        │   │
│   │      Triage new alerts      │  │       Check forecasts       │  │        Report to mgmt       │   │
│   │    Check platform health    │  │      Dismiss false pos      │  │       Procurement plan      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Operations via AIOps web UI and REST API · admin CLI for platform-level checks                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Alert console = AIOps UI showing all active alerts sorted by severity and age                        │
│  Adapter status = Health check confirming each data source adapter is collecting normally             │
│  Platform health = AIOps self-monitoring; check /api/v1/health endpoint                               │
│  Triage = Classifying new alert: actionable, false positive, or informational                         │
│  Recommendation = AI action item; review weekly and track in ITSM                                     │
│  Insight review = Weekly check of AI-generated fleet-wide patterns                                    │
│  Forecast check = Reviewing capacity projections per system for procurement planning                  │
│  Threshold audit = Monthly validation that alert thresholds match current operational norms           │
│  Access review = Monthly check of AIOps user list for stale or inappropriate access                   │
│  Procurement plan = Capacity expansion request based on AIOps forecast data                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
