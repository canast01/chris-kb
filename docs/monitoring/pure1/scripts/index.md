# Pure1 Scripts

## Authentication

Pure1 REST API v1 uses RSA JWT authentication. The private key is stored in the secrets manager and loaded at runtime. Never store the private key in the repository or in plain text configuration files.

```python
import jwt, time, uuid, requests
from cryptography.hazmat.primitives import serialization

PURE1_API = "https://api.pure1.purestorage.com/api/1.latest"

def get_pure1_token(client_id: str, key_id: str, private_key_pem: str) -> str:
    """Obtain a Pure1 API access token using RSA private key."""
    private_key = serialization.load_pem_private_key(
        private_key_pem.encode(), password=None
    )
    payload = {
        "iss": client_id, "sub": client_id,
        "aud": "pure1:auth:mfa",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
        "jti": str(uuid.uuid4())
    }
    id_token = jwt.encode(payload, private_key, algorithm="RS256",
                          headers={"kid": key_id})
    resp = requests.post(
        "https://api.pure1.purestorage.com/oauth2/1.0/token",
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "subject_token": id_token,
            "subject_token_type": "urn:ietf:params:oauth:token-type:json_web_token"
        }
    )
    resp.raise_for_status()
    return resp.json()["access_token"]

def pure1_get(path: str, token: str, params: dict = None) -> dict:
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    resp = requests.get(f"{PURE1_API}{path}", headers=headers, params=params)
    resp.raise_for_status()
    return resp.json()
```

## Fleet Health Query

```python
def get_fleet_health(token: str) -> list:
    """Return all arrays with name, model, OS, and version."""
    data = pure1_get("/arrays", token)
    return [
        {
            "name": a["name"],
            "model": a.get("model"),
            "os": a.get("os"),
            "version": a.get("version"),
            "id": a["id"]
        }
        for a in data.get("items", [])
    ]
```

## Capacity Report

```python
import csv
from datetime import datetime, timezone

def capacity_report(token: str, output_file: str):
    """Export capacity data for all arrays."""
    arrays = pure1_get("/arrays", token).get("items", [])
    metrics = pure1_get("/metrics/history", token, params={
        "names": "array_total_capacity,array_used_space,array_data_reduction",
        "resolution": "86400000",   # 1-day resolution (ms)
        "end_time": int(datetime.now(timezone.utc).timestamp() * 1000)
    }).get("items", {})

    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "array_name", "total_tb", "used_tb", "used_pct", "data_reduction"
        ])
        writer.writeheader()
        for a in arrays:
            m = metrics.get(a["id"], {})
            total = m.get("array_total_capacity", 0)
            used  = m.get("array_used_space", 0)
            dr    = m.get("array_data_reduction", 0)
            writer.writerow({
                "array_name": a["name"],
                "total_tb": round(total / 1e12, 2) if total else "N/A",
                "used_tb":  round(used  / 1e12, 2) if used  else "N/A",
                "used_pct": round((used / total * 100), 1) if total else "N/A",
                "data_reduction": round(dr, 2) if dr else "N/A"
            })
    print(f"Capacity report written to {output_file}")
```

## Active Alert Export

```python
def export_alerts(token: str, output_file: str):
    """Export all active alerts to CSV."""
    data = pure1_get("/alerts", token, params={"filter": "state='open'"})
    alerts = data.get("items", [])
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "id", "summary", "severity", "array_name", "created"
        ])
        writer.writeheader()
        for a in alerts:
            writer.writerow({
                "id":         a["id"],
                "summary":    a.get("summary"),
                "severity":   a.get("severity"),
                "array_name": a.get("arrays", [{}])[0].get("name", "unknown"),
                "created":    a.get("created")
            })
    print(f"Exported {len(alerts)} alerts to {output_file}")
```

## Pure1 Meta Anomaly Query

```python
def query_anomalies(token: str) -> list:
    """Return active workload anomalies from Pure1 Meta."""
    data = pure1_get("/workloads", token,
                     params={"filter": "anomaly_state='active'"})
    return [
        {
            "workload_id": w["id"],
            "array": w.get("array_name"),
            "anomaly_type": w.get("anomaly_type"),
            "detected": w.get("anomaly_detected_at")
        }
        for w in data.get("items", [])
    ]
```

## Exponential Backoff for Rate Limiting

```python
import time, random

def pure1_get_with_retry(path: str, token: str, max_retries: int = 5) -> dict:
    for attempt in range(max_retries):
        resp = requests.get(
            f"{PURE1_API}{path}",
            headers={"Authorization": f"Bearer {token}"}
        )
        if resp.status_code == 429:
            wait = (2 ** attempt) + random.uniform(0, 1)
            print(f"Rate limited — waiting {wait:.1f}s (attempt {attempt + 1})")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Max retries exceeded for {path}")
```

## Script Inventory

| Script | Purpose | Schedule |
|---|---|---|
| `pure1_fleet_health.py` | Query all arrays for health status and export summary | Daily |
| `pure1_capacity_report.py` | Capacity trend report across all arrays | Weekly |
| `pure1_alert_export.py` | Export active alerts to CSV for incident review | Daily |
| `pure1_anomaly_query.py` | Query Pure1 Meta for active workload anomaly detections | Weekly |
| `pure1_tag_compliance.py` | Report arrays missing mandatory tags (Site, Environment, Owner) | Weekly |

Scripts are stored in `scripts/pure1/`. Load `client_id`, `key_id`, and `private_key_pem` from the secrets manager at runtime. Implement exponential backoff for HTTP 429 responses.
