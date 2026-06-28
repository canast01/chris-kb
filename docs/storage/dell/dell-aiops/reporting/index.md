---
tags:
  - dell
---
# Dell AIOps — Reporting

```bash
# Generate an executive health summary report
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/reports" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "EXECUTIVE_HEALTH_SUMMARY",
    "scope": "ALL_SYSTEMS",
    "date_range": {
      "start": "2026-04-01T00:00:00Z",
      "end": "2026-04-30T23:59:59Z"
    },
    "format": "PDF",
    "include_recommendations": true,
    "include_predictions": true
  }'

# Check generation status
curl -sk -X GET \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/reports/<reportId>" \
  -H "Authorization: Bearer <access_token>" \
  | jq '{status, download_url}'

# Download the report
curl -sk -X GET "<download_url>" \
  -H "Authorization: Bearer <access_token>" \
  -o aiops-exec-summary.pdf
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
