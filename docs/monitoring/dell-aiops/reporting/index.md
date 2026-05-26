# Dell AIOps: Executive Reports, Trend Analysis, and Capacity Planning Exports

Dell AIOps extends CloudIQ reporting with AI-enriched content: trend analysis, predicted capacity curves, and executive-level infrastructure health summaries. This page covers the available report types, scheduling, and export options.

## AIOps Report Types

Navigation: **CloudIQ > AIOps > Reports**

| Report | Audience | Frequency |
|---|---|---|
| Executive Health Summary | CTO/CIO, management | Monthly |
| Infrastructure Trend Analysis | Architects, engineers | Weekly |
| Capacity Planning Forecast | Storage administrators | Monthly |
| Recommendations Effectiveness | Operations leads | Monthly |
| Anomaly and Incident Timeline | Operations, security | On-demand / weekly |
| Bottleneck History | Performance engineers | On-demand |

## Generating an AIOps Report On-Demand

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

Capacity planning export fields:

| Field | Description |
|---|---|
| `system_name` | Array or cluster name |
| `current_used_percent` | Current utilisation |
| `predicted_30d_percent` | Projected utilisation in 30 days |
| `predicted_90d_percent` | Projected utilisation in 90 days |
| `days_until_full` | Projected runway |
| `confidence` | Model confidence score (0–1) |

## Scheduling AIOps Reports

```bash
# Schedule a monthly executive summary to management
curl -sk -X POST \
  "https://cloudiq.apis.dell.com/cloudiq/rest/v1/aiops/report_schedules" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "EXECUTIVE_HEALTH_SUMMARY",
    "frequency": "MONTHLY",
    "day_of_month": 1,
    "time_utc": "06:00",
    "format": "PDF",
    "recipients": ["cto@example.com", "storage-lead@example.com"]
  }'
```

## Common Reporting Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Executive summary shows incomplete data | Some systems have no telemetry | Check system connectivity status before generating |
| Prediction section blank | < 14 days of data | Allow longer data collection period |
| CSV export missing columns | Old API version | Upgrade to latest API endpoint version |
| Report not delivered | Email relay not configured | Check CloudIQ notification settings |
| Trend shows large unexplained spike | Bulk data migration or test | Note in report commentary; exclude from trend if needed |
