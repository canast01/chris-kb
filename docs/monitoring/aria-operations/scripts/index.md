# Aria Operations Scripts

Automation scripts interact with the Aria Operations REST API using Python and the `requests` library. All scripts authenticate via `/suite-api/api/auth/token/acquire` and pass the session token in the `Authorization: vRealizeOpsToken` header. Scripts are stored in the team repository under `scripts/aria-operations/`.

| Script | Purpose |
|---|---|
| `export_active_alerts.py` | Export all active alerts to CSV with severity, object, and timestamp |
| `capacity_report.py` | Generate cluster-level capacity utilisation report (CPU, memory, storage) |
| `top_n_vms.py` | Report top-N VMs by CPU contention and memory usage over a time range |
| `push_custom_metric.py` | Push custom metrics to Aria Operations via the REST ingest API |
| `generate_report.py` | Trigger and download a scheduled report programmatically |

All scripts require a `config.json` with `aria_host`, `username`, and `password` fields. Credentials should be sourced from a secrets manager rather than stored in plain text.
