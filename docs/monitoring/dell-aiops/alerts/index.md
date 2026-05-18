# Dell AIOps: AI-Generated Alerts, Anomaly Detection, and Correlation

```
AI Alert Flow — Dell AIOps
┌──────────────────────────────────────┐
│  Telemetry anomaly detected          │
│  metric deviates from learned band   │
└────────────────┬─────────────────────┘
                 ▼
┌──────────────────────────────────────┐
│  ML root cause analysis              │
│  ┌──────────────────────────────┐   │
│  │ deviation_percent: +42%      │   │
│  │ confidence: 0.91             │   │
│  │ contributing: disk SMART,    │   │
│  │   queue depth, write latency │   │
│  └──────────────────────────────┘   │
└────────────────┬─────────────────────┘
                 ▼
┌──────────────────────────────────────┐
│  Alert with recommended action       │
│  "Predictive drive failure on SYS-A  │
│   within 7 days — replace slot 12"   │
└────────────────┬─────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌──────────────┐   ┌────────────────┐
│  Email notif │   │  Portal alert  │
│  (on-call)   │   │  + correlated  │
│              │   │  event group   │
└──────────────┘   └────────────────┘
```

Dell AIOps (part of the CloudIQ AI platform) uses machine learning to detect anomalies, correlate related events across infrastructure domains, and surface alerts that static threshold tools would miss. This page covers how AI-generated alerts work, how to interpret them, and how to manage alert correlation.

## AI Alert Types

Dell AIOps generates alerts in three main categories:

| Alert Type | Description |
|---|---|
| Anomaly Detection | Metric deviates significantly from learned baseline |
| Predicted Failure | ML model predicts component failure within a time window |
| Correlated Event | Multiple individual events grouped as a single root-cause alert |

Navigation: **CloudIQ > AIOps > Alerts**

## Understanding Anomaly Detection

Anomaly alerts fire when a metric exceeds a dynamically calculated confidence band. Unlike static thresholds, the band adjusts for daily, weekly, and seasonal patterns.

```bash
# Retrieve AI-generated anomaly alerts via CloudIQ API
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/alerts?filter=type%20eq%20%27ANOMALY%27&filter=state%20eq%20%27ACTIVE%27" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json" | jq '.results[] | {id, metric, system_name, deviation_percent, started_at}'

# Get anomaly detail including contributing metrics
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/alerts/<alertId>" \
  -H "Authorization: Bearer <access_token>" \
  -H "Accept: application/json"
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
