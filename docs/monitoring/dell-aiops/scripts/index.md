# Dell AIOps Scripts

Automation scripts interact with the CloudIQ REST API using Python and the `requests` library. OAuth2 client credentials are stored in a secrets manager and loaded at runtime. Scripts are stored in the team repository under `scripts/dell-aiops/`.

| Script | Purpose |
|---|---|
| `export_recommendations.py` | Export all active AIOps recommendations to CSV with severity, system, and recommended action |
| `anomaly_trend.py` | Analyse anomaly frequency by system over a rolling 30-day window to identify persistently noisy systems |
| `recommendation_to_itsm.py` | Forward Critical and High recommendations to ServiceNow via REST API to create change requests |
| `health_score_report.py` | Generate weekly health score report across all storage systems, flagging systems below threshold |

All scripts require a `config.json` with `client_id` and `client_secret` for CloudIQ OAuth2 authentication. Token refresh is handled automatically within the script session.
