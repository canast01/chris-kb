---
tags:
  - dell
  - operations
---
# CloudIQ: Proactive Recommendations and Implementation Tracking


<div class="kb-summary">
CloudIQ: Proactive Recommendations and Implementation Tracking reference covering Implementing a Recommendation, Energy Savings Recommendations, Tracking Recommendation History, Common Recommendation Issues.
</div>

```text
┌──────────────────────────────────── CloudIQ — AI Recommendations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           CloudIQ AI generates recommendations based on health issues and anomalies           │   │
│   │            Categories: Performance, Capacity, Availability, Security, Best Practice           │   │
│   │          Priority: Critical (act now), High (act soon), Medium (plan), Low (optional)         │   │
│   │          Each recommendation: problem description, impact, suggested action, KB link          │   │
│   │                    Track status: Open → In Progress → Resolved → Dismissed                    │   │
│   │         Resolution improves health score once Dell cloud receives confirming telemetry        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Recommendations computed in Dell cloud from fleet-wide ML · no on-prem component                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Recommendation = AI action item linking a detected issue to a corrective step                        │
│  Priority = Urgency classification: Critical/High/Medium/Low                                          │
│  KB link = Dell Knowledge Base article linked from recommendation for detailed steps                  │
│  Impact = Estimated health score improvement if recommendation is implemented                         │
│  In Progress = Status indicating team has started working on the recommendation                       │
│  Resolved = Recommendation marked done; CloudIQ validates via subsequent telemetry                    │
│  Dismissed = Recommendation closed without action; should include a reason comment                    │
│  Fleet-wide ML = Models trained on all registered Dell arrays globally for pattern matching           │
│  Best practice = Recommendation to align configuration with Dell recommended settings                 │
│  Security recommendation = Flagging insecure configuration (weak auth, unencrypted replication)       │
│  Confirming telemetry = Subsequent metric push showing issue condition no longer present              │
│  SLA = Internal target for acting on Critical/High recommendations (e.g., within 3 business days)     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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
