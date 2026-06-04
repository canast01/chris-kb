# Pure1 — Scripts Reference

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
```text
┌────────────────────────────────────── Pure1 — Scripts Reference ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Pure1 REST API scripts using py-pure-client library                      │   │
│   │                get-fleet.py: list all arrays with health, version, and capacity               │   │
│   │               get-alerts.py: active alerts across fleet; flag Critical to Slack               │   │
│   │                capacity-check.py: arrays with < 90 days to full; email to team                │   │
│   │              phonehome-check.py: arrays not Connected; alert if data age > 5 min              │   │
│   │                  perf-report.py: pull IOPS/latency for all arrays; CSV export                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Scripts run from any internet-connected host · Python 3 + py-pure-client                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  py-pure-client = pip install py-pure-client; Pure-provided Python library                            │
│  JWT auth = RSA-signed JWT for Pure1 API; use Pure1Client from py-pure-client                         │
│  client_id = Pure1 API registration ID from org settings                                              │
│  private_key = RSA private key path; corresponding public key registered in Pure1                     │
│  Fleet list = client.get_arrays() returns all arrays with health and metadata                         │
│  Alert list = client.get_alerts(filter="state='open'") for active alerts                              │
│  Metrics = client.get_metrics(names=[...], resource_names=[...]) for time-series                      │
│  Phonehome status = array.status field; Connected or Disconnected                                     │
│  Data age = time since last phonehome; compute from array.last_updated                                │
│  CSV export = pandas DataFrame from metric response; df.to_csv()                                      │
│  Cron = Schedule daily via crontab for capacity and phonehome checks                                  │
│  Slack webhook = POST alert summary to Slack channel incoming webhook URL                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
