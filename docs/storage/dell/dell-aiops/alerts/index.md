---
tags:
  - dell
---
# Dell AIOps: AI-Generated Alerts, Anomaly Detection, and Correlation

<div class="kb-summary">
Dell AIOps: AI-Generated Alerts, Anomaly Detection, and Correlation reference covering Alert Correlation, Predicted Failure Alerts, Acknowledging and Dismissing AI Alerts, Common AI Alert Issues.

*Applies to: Dell AIOps*
</div>

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
