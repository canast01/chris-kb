# Pure1 Scripts

Automation scripts use the Pure1 REST API with OAuth2 authentication. Scripts are maintained in the team scripts repository and scheduled via cron or CI pipeline for daily and weekly execution.

**Available scripts:**

| Script | Purpose | Schedule |
|---|---|---|
| `pure1_fleet_health.py` | Query all arrays for health status and export summary | Daily |
| `pure1_capacity_report.py` | Capacity trend report across all arrays | Weekly |
| `pure1_alert_export.py` | Export active alerts to CSV for incident review | Daily |
| `pure1_anomaly_query.py` | Query Pure1 Meta for workload anomaly detections | Weekly |

All scripts authenticate using a service account API key stored in the secrets manager. Implement exponential backoff for API rate limit handling (HTTP 429).
