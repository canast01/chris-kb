# InsightIQ Scripts

Automation scripts interact with the InsightIQ REST API and OneFS CLI to export performance data and generate reports. Scripts are stored in the team repository under `scripts/insightiq/`.

| Script | Purpose |
|---|---|
| `export_performance.py` | Query InsightIQ REST API to export throughput and latency data for a date range |
| `generate_report.py` | Automate weekly utilisation report generation and email distribution |
| `threshold_alert.py` | Compare latest metrics to thresholds and forward alerts via SNMP or syslog to monitoring platform |
| `cluster_health_check.py` | Check all cluster connection statuses via InsightIQ API and alert on disconnected clusters |

Scripts use the InsightIQ REST API (`/api/v2/`) and authenticate with the local admin credentials (stored in a secrets manager). For SNMP forwarding, scripts use the `pysnmp` library targeting the enterprise monitoring platform OID namespace.
