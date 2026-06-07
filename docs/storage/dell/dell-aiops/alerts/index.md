# Dell AIOps: AI-Generated Alerts, Anomaly Detection, and Correlation


<div class="kb-summary">
Dell AIOps: AI-Generated Alerts, Anomaly Detection, and Correlation reference covering Alert Correlation, Predicted Failure Alerts, Acknowledging and Dismissing AI Alerts, Common AI Alert Issues.
</div>

```text
┌───────────────────────────────────────── Dell AIOps — Alerts ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 Alert Types                  │                Alert Lifecycle                 │   │
│   │        Threshold: static metric limit        │              Open: condition met               │   │
│   │        Anomaly: ML baseline deviation        │          Acknowledged: engineer seen           │   │
│   │         Predictive: failure forecast         │           In Progress: being worked            │   │
│   │           Capacity: fill date near           │          Resolved: condition cleared           │   │
│   │          Hardware: component fault           │           Dismissed: false positive            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Alerts generated in AIOps engine · delivered via console, email, webhook, and ITSM                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Threshold alert = Fires when metric exceeds static limit (e.g., utilisation > 85%)                   │
│  Anomaly alert = Fires when ML model detects unusual pattern outside learned baseline                 │
│  Predictive alert = Fires when model forecasts failure or capacity exhaustion within horizon          │
│  Capacity alert = Fires when forecast horizon drops below threshold (e.g., 90 days)                   │
│  Hardware alert = Propagated from array firmware; component failure detected                          │
│  Acknowledge = Engineer marks alert as seen; stops re-notification                                    │
│  In Progress = Status indicating active remediation in progress                                       │
│  Resolved = Alert auto-closes when triggering condition no longer detected                            │
│  Dismissed = Alert closed as false-positive; reason required                                          │
│  Severity = Critical / Warning / Informational; routes to different notification targets              │
│  Alert context = Related metrics, affected objects, and recommendation attached to alert              │
│  Noise reduction = Correlation grouping related alerts into single actionable incident                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Acknowledging and Dismissing AI Alerts

```bash
# Acknowledge an AI alert
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/alerts/<alertId>/acknowledge" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"comment": "Under investigation - ticket INC0099123"}'

# Dismiss a false positive
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/alerts/<alertId>/dismiss" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"reason": "FALSE_POSITIVE", "comment": "Caused by planned backup job"}'
```

## Common AI Alert Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Alert fires during known maintenance | Model not aware of maintenance window | Mark windows in CloudIQ; dismiss and provide feedback |
| Low confidence anomaly alerts | Insufficient training data | Wait for 14+ days of baseline data |
| Correlated group missing events | Events on different systems not linked | Ensure all systems in same tenant/site group |
| Predicted failure does not materialise | Model false positive | Dismiss with feedback to improve future accuracy |
| Anomaly fires every day at same time | Recurring scheduled job creating pattern | Model should learn after 2–3 weeks; dismiss until then |
