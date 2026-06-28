---
tags:
  - dell
---
# Dell AIOps — Scripts Reference

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

## See also

- [Dell AIOps — Overview](../../)
