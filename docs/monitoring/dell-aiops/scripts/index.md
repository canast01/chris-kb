# Dell AIOps Scripts
## Authentication

Dell AIOps is accessed via the CloudIQ REST API using OAuth2 client credentials. All scripts load credentials from the secrets manager at runtime.

```python
import requests, os

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

## Export Active Recommendations

```python
import csv

def export_recommendations(token: str, output_file: str):
    data = api_get("/recommendations", token,
                   params={"filter": "state eq 'ACTIVE'"})
    recs = data.get("results", [])
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "title", "severity", "system_id",
            "system_name", "recommended_action", "created_at"
        ])
        writer.writeheader()
        for r in recs:
            writer.writerow({
                "id": r["id"],
                "title": r.get("title"),
                "severity": r.get("severity"),
                "system_id": r.get("system_id"),
                "system_name": r.get("system_name"),
                "recommended_action": r.get("recommended_action"),
                "created_at": r.get("created_at")
            })
    print(f"Exported {len(recs)} recommendations to {output_file}")
```

## Anomaly Trend Analysis (30-Day Rolling Window)

```python
from datetime import datetime, timedelta, timezone

def anomaly_trend(token: str) -> dict:
    """Count anomalies per system over a rolling 30-day window."""
    since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    data = api_get("/anomalies", token,
                   params={"filter": f"created_at gt '{since}'"})
    counts = {}
    for a in data.get("results", []):
        system = a.get("system_name", "unknown")
        counts[system] = counts.get(system, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))
```

## Forward Critical Recommendations to ServiceNow

```python
SNOW_URL  = os.environ["SNOW_URL"]
SNOW_AUTH = (os.environ["SNOW_USER"], os.environ["SNOW_PASSWORD"])

def create_snow_change(rec: dict) -> str:
    payload = {
        "short_description": f"Dell AIOps {rec['severity']}: {rec['title']}",
        "description": (
            f"System: {rec.get('system_name')}\n"
            f"Recommended Action: {rec.get('recommended_action')}\n"
            f"CloudIQ Recommendation ID: {rec['id']}"
        ),
        "category": "Storage",
        "assignment_group": "storage-ops",
        "type": "emergency" if rec["severity"] == "Critical" else "normal"
    }
    resp = requests.post(f"{SNOW_URL}/api/now/table/change_request",
                         auth=SNOW_AUTH, json=payload)
    resp.raise_for_status()
    return resp.json()["result"]["number"]

def process_critical_recommendations(token: str):
    data = api_get("/recommendations", token,
                   params={"filter": "severity eq 'Critical' and state eq 'ACTIVE'"})
    for rec in data.get("results", []):
        ticket = create_snow_change(rec)
        print(f"Created ServiceNow ticket {ticket} for recommendation {rec['id']}")
```

## Weekly Health Score Report

```python
def health_score_report(token: str, threshold: int = 80) -> list:
    """Return systems with health score below threshold."""
    systems = api_get("/systems", token).get("results", [])
    below_threshold = [
        {"name": s["name"], "type": s["type"], "health_score": s.get("health_score")}
        for s in systems
        if s.get("health_score") is not None and s["health_score"] < threshold
    ]
    below_threshold.sort(key=lambda x: x["health_score"])
    return below_threshold
```

## Script Inventory

| Script | Purpose | Schedule |
|---|---|---|
| `export_recommendations.py` | Export all active AIOps recommendations to CSV | Daily |
| `anomaly_trend.py` | Anomaly frequency by system — rolling 30-day window | Weekly |
| `recommendation_to_itsm.py` | Forward Critical/High recommendations to ServiceNow | Event-driven |
| `health_score_report.py` | Weekly health score report — flag systems below threshold | Weekly |

Scripts are stored in `scripts/dell-aiops/`. Load `client_id` and `client_secret` from the secrets manager — never commit credentials to the repository.
