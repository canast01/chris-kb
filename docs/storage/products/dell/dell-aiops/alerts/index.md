---
tags:
  - dell
---
# Dell AIOps: AI-Generated Alerts, Anomaly Detection, and Correlation

<div class="kb-summary">
Dell AIOps: AI-Generated Alerts, Anomaly Detection, and Correlation reference covering Alert Correlation, Predicted Failure Alerts, Acknowledging and Dismissing AI Alerts, Common AI Alert Issues.

*Applies to: Dell AIOps*
</div>

```d2
direction: down

acknowledging_and_dismissing_ai_aler: "Acknowledging and Dismissing AI Alerts" {shape: rectangle}
common_ai_alert_issues: "Common AI Alert Issues" {shape: rectangle}

acknowledging_and_dismissing_ai_aler -> common_ai_alert_issues: uses
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


```text title="Expected output"
{"alertId":"alert-7f3c9e2a-b14d-4821-9f2e-d8c1a5b9e3f1","status":"acknowledged","timestamp":"2024-01-15T14:32:18Z","comment":"Under investigation - ticket INC0099123","acknowledgedBy":"admin@company.com"}
{"alertId":"alert-7f3c9e2a-b14d-4821-9f2e-d8c1a5b9e3f1","status":"dismissed","timestamp":"2024-01-15T14:32:45Z","reason":"FALSE_POSITIVE","comment":"Caused by planned backup job","dismissedBy":"admin@company.com"}
```

!!! warning "Common errors"
    **`{"error":"Unauthorized","message":"Invalid or expired access token"}`** — Regenerate the access token using your CloudIQ API credentials and update the `<access_token>` placeholder.
    **`{"error":"NotFound","message":"Alert alert-7f3c9e2a-b14d-4821-9f2e-d8c1a5b9e3f1 not found"}`** — Verify the `<alertId>` exists and is still active by listing alerts with a GET request to the `/alerts` endpoint.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Remove the `-k` flag if connecting to a trusted endpoint, or ensure your CA bundle is current with `curl --cacert /path/to/ca-bundle.crt`.
## Common AI Alert Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Alert fires during known maintenance | Model not aware of maintenance window | Mark windows in CloudIQ; dismiss and provide feedback |
| Low confidence anomaly alerts | Insufficient training data | Wait for 14+ days of baseline data |
| Correlated group missing events | Events on different systems not linked | Ensure all systems in same tenant/site group |
| Predicted failure does not materialise | Model false positive | Dismiss with feedback to improve future accuracy |
| Anomaly fires every day at same time | Recurring scheduled job creating pattern | Model should learn after 2–3 weeks; dismiss until then |
