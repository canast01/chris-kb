# Aria Operations Scripts

## Authentication

All scripts authenticate via the Aria Operations REST API token endpoint. The session token is passed in the `Authorization: vRealizeOpsToken` header for subsequent requests.

```python
import requests, json

def get_token(host, username, password):
    url = f"https://{host}/suite-api/api/auth/token/acquire"
    payload = {"username": username, "password": password}
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    resp = requests.post(url, json=payload, headers=headers, verify=True)
    resp.raise_for_status()
    return resp.json()["token"]
```

Store `aria_host`, `username`, and `password` in a secrets manager. Load via environment variables or a vault client — never hardcode credentials.

## Export Active Alerts

```python
def export_active_alerts(host, token):
    url = f"https://{host}/suite-api/api/alerts"
    headers = {
        "Authorization": f"vRealizeOpsToken {token}",
        "Accept": "application/json"
    }
    params = {"activeOnly": "true", "pageSize": 1000}
    resp = requests.get(url, headers=headers, params=params, verify=True)
    resp.raise_for_status()
    alerts = resp.json().get("alerts", [])
    # alerts contains: alertId, type, status, severity, updateTime, resourceId
    return alerts
```

## Query Resource Metrics

```python
def get_metric(host, token, resource_id, metric_key, start_ts, end_ts):
    """Fetch a named metric for a resource over a time range."""
    url = f"https://{host}/suite-api/api/resources/{resource_id}/stats"
    headers = {
        "Authorization": f"vRealizeOpsToken {token}",
        "Accept": "application/json"
    }
    params = {
        "statKey": metric_key,
        "begin": start_ts,   # epoch milliseconds
        "end": end_ts
    }
    resp = requests.get(url, headers=headers, params=params, verify=True)
    resp.raise_for_status()
    return resp.json()
```

Common metric keys:
- `cpu|usage_average` — VM CPU usage %
- `mem|usage_average` — VM memory usage %
- `disk|commandsAveraged_average` — disk IOPS
- `net|usage_average` — network usage KBps

## Push Custom Metric

```python
def push_custom_metric(host, token, resource_id, metric_key, value, timestamp_ms):
    url = f"https://{host}/suite-api/api/resources/stats/addstatscollection"
    headers = {
        "Authorization": f"vRealizeOpsToken {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "stat-contents": [{
            "resourceId": resource_id,
            "stat-list": {
                "stat": [{
                    "timestamps": [timestamp_ms],
                    "data": [value],
                    "statKey": {"key": metric_key}
                }]
            }
        }]
    }
    resp = requests.post(url, headers=headers, json=payload, verify=True)
    resp.raise_for_status()
```

## Script Inventory

| Script | Purpose | Schedule |
|---|---|---|
| `export_active_alerts.py` | Export all active alerts to CSV with severity, object, and timestamp | Daily |
| `capacity_report.py` | Generate cluster-level capacity utilisation report (CPU, memory, storage) | Weekly |
| `top_n_vms.py` | Report top-N VMs by CPU contention and memory usage over a time range | Weekly |
| `push_custom_metric.py` | Push custom metrics to Aria Operations via the REST ingest API | On demand |
| `generate_report.py` | Trigger and download a scheduled report programmatically | On demand |

Scripts are stored in the team repository under `scripts/aria-operations/`. A `config.json` template with required fields (`aria_host`, `username`, `password`) is provided — populate from the secrets manager at runtime.

## Token Refresh

Tokens expire after 30 minutes (default). For long-running scripts, re-acquire the token before expiry or catch HTTP 401 responses and re-authenticate:

```python
from datetime import datetime, timedelta

token_expiry = datetime.utcnow() + timedelta(minutes=28)

def get_valid_token(host, username, password, current_token):
    if datetime.utcnow() >= token_expiry:
        return get_token(host, username, password)
    return current_token
```
