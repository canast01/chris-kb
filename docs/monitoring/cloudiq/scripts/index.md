# CloudIQ Scripts

Automation scripts use the CloudIQ REST API with OAuth2 client credentials authentication. Scripts are stored in the team repository and run on a scheduled basis.

| Script | Purpose | Schedule |
|---|---|---|
| `cloudiq_fleet_health.py` | Query all systems for health scores and export summary | Daily |
| `cloudiq_alert_export.py` | Export active alerts to CSV | Daily |
| `cloudiq_capacity_report.py` | Capacity trend report for all systems | Weekly |
| `cloudiq_health_history.py` | Health score history query for trend analysis | Weekly |
| `cloudiq_critical_to_snow.py` | Auto-create ServiceNow ticket on CRITICAL alert | Event-driven |

All scripts authenticate via client_id and client_secret stored in the secrets manager. Credentials must be updated in the secrets manager when rotated.
