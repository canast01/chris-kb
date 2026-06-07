# CloudIQ Operations


<div class="kb-summary">
CloudIQ Operations reference.
</div>

```text
┌──────────────────────────────────────── CloudIQ — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Daily Checks        │  │         Weekly Tasks        │  │        Monthly Tasks        │   │
│   │     Review fleet health     │  │      Action open alerts     │  │      Capacity planning      │   │
│   │       Check red arrays      │  │         Review recs         │  │      Review thresholds      │   │
│   │       Verify telemetry      │  │       Check forecasts       │  │        Report to mgmt       │   │
│   │      Triage new alerts      │  │         Update ITSM         │  │        Access review        │   │
│   │       Check anomalies       │  │        Snooze/dismiss       │  │       Procurement plan      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Operations entirely via cloudiq.dell.com browser UI · no on-prem tooling required                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Fleet health = Overview of all registered arrays and their current health scores                     │
│  Telemetry verification = Confirming each array shows Connected and data age < 15 minutes             │
│  Triage = Classifying new alert as actionable, false positive, or informational                       │
│  Recommendation = AI-suggested action; should be reviewed and acted on within SLA                     │
│  Forecast review = Checking projected capacity exhaustion dates for all arrays                        │
│  Snooze = Temporarily muting a known-benign alert for a defined period                                │
│  Dismiss = Closing a confirmed false-positive alert permanently                                       │
│  Procurement plan = Capacity expansion request based on CloudIQ forecast horizon                      │
│  Access review = Monthly check of CloudIQ user list for stale or inappropriate access                 │
│  ITSM update = Recording CloudIQ alert actions in ServiceNow incident or problem ticket               │
│  Threshold review = Adjusting alert trigger values based on operational experience                    │
│  Management report = Monthly summary of health trends and capacity outlook for leadership             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Daily operations include reviewing the CloudIQ dashboard health summary page, triaging active alerts sorted by severity, checking capacity forecasts for any system with fewer than 30 days to full, and confirming all expected systems are reporting (a missing system indicates an SCG connectivity issue). Weekly tasks include exporting a capacity report for the infrastructure review meeting.

**Daily checklist:**

- Review CloudIQ health summary — confirm all systems have acceptable health scores
- Triage active alerts by severity (CRITICAL first)
- Check capacity forecast — flag any system with less than 30 days to full
- Confirm all expected systems are reporting (missing = SCG connectivity issue)

**Weekly tasks:**

- Export capacity report from CloudIQ and distribute to team
- Review anomaly and recommendation queue — action any HIGH priority items
