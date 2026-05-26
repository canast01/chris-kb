# CloudIQ Scripts
## Authentication

CloudIQ REST API uses OAuth2 client credentials. All scripts load `client_id` and `client_secret` from the secrets manager at runtime.

```python
import requests

TOKEN_URL = "https://api.cloudiq.dell.com/auth/oauth/v2/token"
API_BASE  = "https://api.cloudiq.dell.com/cloudiq/rest/v1"

def get_token(client_id: str, client_secret: str) -> str:
    resp = requests.post(TOKEN_URL, data={
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    })
    resp.raise_for_status()
    return resp.json()["access_token"]

def api_get(path: str, token: str, params: dict = None) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    resp = requests.get(f"{API_BASE}{path}", headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()
```

## Export Active Alerts

```python
import csv, datetime

def export_alerts(token: str, output_file: str):
    data = api_get("/alerts", token, params={"filter": "state eq 'ACTIVE'"})
    alerts = data.get("results", [])
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "name", "severity",
                                                "system_id", "created_at"])
        writer.writeheader()
        for a in alerts:
            writer.writerow({
                "id": a["id"],
                "name": a.get("name"),
                "severity": a.get("severity"),
                "system_id": a.get("system_id"),
                "created_at": a.get("created_at")
            })
    print(f"Exported {len(alerts)} alerts to {output_file}")
```

## Capacity Trend Query

```python
def get_capacity(token: str, system_id: str) -> dict:
    """Return capacity data for a specific system."""
    return api_get(f"/systems/{system_id}/capacity", token)
```

## Create ServiceNow Incident on CRITICAL Alert (Event-Driven)

```python
import os

SNOW_URL      = os.environ["SNOW_INSTANCE_URL"]
SNOW_USER     = os.environ["SNOW_USER"]
SNOW_PASSWORD = os.environ["SNOW_PASSWORD"]

def create_snow_incident(alert: dict):
    payload = {
        "short_description": f"CloudIQ CRITICAL: {alert['name']} on {alert.get('system_name', 'unknown')}",
        "severity": "1",
        "assignment_group": "storage-ops",
        "description": f"Alert ID: {alert['id']}\nSeverity: {alert['severity']}\nCreated: {alert['created_at']}"
    }
    resp = requests.post(
        f"{SNOW_URL}/api/now/table/incident",
        auth=(SNOW_USER, SNOW_PASSWORD),
        json=payload
    )
    resp.raise_for_status()
    return resp.json()["result"]["number"]
```

## Script Inventory

| Script | Purpose | Schedule |
|---|---|---|
| `cloudiq_fleet_health.py` | Query all systems for health scores and export summary | Daily |
| `cloudiq_alert_export.py` | Export active alerts to CSV | Daily |
| `cloudiq_capacity_report.py` | Capacity trend report for all systems | Weekly |
| `cloudiq_health_history.py` | Health score history query for trend analysis | Weekly |
| `cloudiq_critical_to_snow.py` | Auto-create ServiceNow ticket on CRITICAL alert | Event-driven |

Scripts are stored in `scripts/cloudiq/` in the team repository. A `config.json.template` is provided — populate `client_id` and `client_secret` from the secrets manager at runtime. Never commit secrets to the repository.

## Rate Limiting

CloudIQ REST API enforces rate limits. Implement retry with exponential backoff for HTTP 429 responses:

```python
import time

def api_get_with_retry(path, token, max_retries=3):
    for attempt in range(max_retries):
        resp = requests.get(f"{API_BASE}{path}",
                            headers={"Authorization": f"Bearer {token}"})
        if resp.status_code == 429:
            wait = 2 ** attempt
            print(f"Rate limited — waiting {wait}s before retry")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Max retries exceeded for {path}")
```
