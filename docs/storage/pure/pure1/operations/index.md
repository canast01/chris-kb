---
tags:
  - operations
  - pure
---
# Pure1 Operations


<div class="kb-summary">
Pure1 operations: fleet health dashboard review, predictive analytics alert configuration, capacity and performance trending, and support case creation from Pure1.

*Applies to: Pure1*
</div>

```text
┌───────────────────────────────────────── Pure1 — Operations ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Daily            │  │            Weekly           │  │           Monthly           │   │
│   │      Check fleet health     │  │      Review open alerts     │  │      Capacity planning      │   │
│   │       Phonehome status      │  │       Review forecasts      │  │       Purity versions       │   │
│   │        Active alerts        │  │         Update ITSM         │  │        Access review        │   │
│   │       TAC case status       │  │      Performance check      │  │        Report to mgmt       │   │
│   │       Degraded arrays       │  │      Dismiss false pos      │  │        Evergreen plan       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Operations entirely via pure1.purestorage.com browser UI · REST API for automation                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Fleet health = Overview showing all arrays with OK/Degraded/Unhealthy status                         │
│  Phonehome status = Confirming Connected for all arrays; data age < 2 minutes                         │
│  Active alerts = Open proactive alerts requiring acknowledgement or ITSM action                       │
│  TAC case status = Checking open Pure Storage support cases in Pure1                                  │
│  Degraded array = Array with non-critical fault; plan remediation within SLA                          │
│  Forecast review = Weekly check of capacity projections; flag < 90 day arrays                         │
│  Performance check = Weekly review of latency/IOPS trends for workload health                         │
│  Purity versions = Monthly audit; arrays running EOS Purity should be scheduled for upgrade           │
│  Evergreen plan = Monthly review of subscription expiry dates for renewal planning                    │
│  Access review = Monthly audit of Pure1 user list; remove stale accounts                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Daily operations begin with logging into the Pure1 dashboard and checking all arrays for health status (green/yellow/red), reviewing active alerts by severity, and checking the capacity trend line for any array approaching 80% used. Stale or missing array data should be investigated immediately by checking the last-seen timestamp and array outbound connectivity. Weekly tasks include exporting the capacity forecast report and distributing it to the storage and capacity planning teams.

**Daily checklist:**

- Log into Pure1 dashboard — confirm all arrays show green health status
- Review active alerts by severity (CRITICAL first, then WARNING)
- Check capacity trend for any array approaching or above 80% used
- Verify last-seen timestamp for all arrays (stale = connectivity issue)

**Weekly tasks:**

- Export capacity forecast report from Pure1 and distribute to team
- Review Pure1 Meta anomaly and workload recommendations

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Alerts](../alerts/)
- [Architecture](../architecture/)
- [Capacity](../capacity/)
- [Cli Reference](../cli-reference/)
- [Deploy](../deploy/)
- [Design Standards](../design-standards/)
- [Health](../health/)
- [Integration](../integration/)
- [Learning Path](../learning-path/)
- [Lifecycle](../lifecycle/)
- [Performance](../performance/)
- [Scripts](../scripts/)
- [Security](../security/)
- [Support](../support/)
- [Troubleshooting](../troubleshooting/)
- [Vendor Support](../vendor-support/)
- [Pure1 — Overview](../)
