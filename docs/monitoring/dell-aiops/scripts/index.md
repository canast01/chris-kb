# Dell AIOps — Scripts

<div class="kb-summary">
Dell AIOps Scripts reference covering Authentication, Forward Critical Recommendations to ServiceNow, Weekly Health Score Report, Script Inventory.
</div>

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
┌─────────────────────────────────── Dell AIOps — Scripts Reference ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            AIOps REST API scripts — Python examples                           │   │
│   │                get-token.py: POST /api/v1/auth/login → Bearer token for session               │   │
│   │            get-alerts.py: GET /api/v1/alerts?status=open → CSV with severity/system           │   │
│   │            capacity-check.py: GET /api/v1/capacity → flag systems < 90 days to full           │   │
│   │            recommendations.py: GET /api/v1/recommendations → post Critical to Slack           │   │
│   │             adapter-health.py: GET /api/v1/adapters → verify all collecting status            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Scripts run from management host · Python 3.8+ with requests · AIOps TCP 443                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Bearer token = Short-lived credential from /auth/login; pass in Authorization header                 │
│  status=open = Filter for unresolved alerts only                                                      │
│  capacity endpoint = Returns per-system current and forecast capacity data                            │
│  recommendations endpoint = Returns prioritised AI action items                                       │
│  adapters endpoint = Returns health status for each configured data source adapter                    │
│  Slack webhook = Incoming webhook URL for posting summaries to a Slack channel                        │
│  Cron schedule = Automated execution (e.g., daily at 06:00 for capacity check)                        │
│  Environment vars = Store AIOps URL, username, password in env; never hardcode                        │
│  Exponential backoff = Retry logic for 429/503 responses from AIOps API                               │
│  CSV output = Writing alert/capacity data to CSV for spreadsheet import                               │
│  Collecting status = Adapter state confirming data being received; opposite of No Data                │
│  Requests library = pip install requests; standard Python HTTP client                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```python

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
