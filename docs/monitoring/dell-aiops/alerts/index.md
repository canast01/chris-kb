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

Anomaly alert fields:

| Field | Meaning |
|---|---|
| `deviation_percent` | How far above/below the expected band the metric is |
| `confidence` | Model confidence (0–1); values < 0.7 indicate early learning |
| `baseline_window_days` | How many days the model was trained on |
| `contributing_metrics` | Other metrics correlated with the anomaly |

## Alert Correlation

AIOps groups related alerts that likely share a common cause. For example, high latency on a volume, increased queue depth on the controller, and a degraded disk can be grouped as a single correlated alert for a failing drive.

```bash
# List correlated alert groups
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/alert_groups?filter=state%20eq%20%27ACTIVE%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {id, root_cause_summary, alert_count, started_at}'
```

Correlation benefits:

| Without Correlation | With Correlation |
|---|---|
| 15 individual alerts for a failing node | 1 grouped alert: "Node degradation detected" |
| Separate notifications per symptom | Single notification with full context |
| Manual investigation to find root cause | Suggested root cause included |

## Predicted Failure Alerts

Predictive alerts are generated when component health indicators (SMART data for drives, thermal trends, error counters) match patterns associated with historical failures in the Dell telemetry dataset.

```bash
# Query predicted failure alerts
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/alerts?filter=type%20eq%20%27PREDICTED_FAILURE%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {system_name, component, predicted_failure_within_days}'
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
