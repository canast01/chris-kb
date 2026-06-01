# Aria Operations — Monitoring Scripts

<div class="kb-summary">
Aria Operations Scripts reference covering Authentication, Push Custom Metric, Script Inventory, Token Refresh.
</div>

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
```
┌───────────────────────────────── Aria Operations — Scripts Reference ─────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                   REST API Automation — Python / PowerShell / Bash examples                   │   │
│   │               Token auth: POST /suite-api/api/auth/token/acquire → Bearer token               │   │
│   │                Alert query: GET /suite-api/api/alerts?status=ACTIVE → JSON list               │   │
│   │            Resource list: GET /suite-api/api/resources?resourceKind=VirtualMachine            │   │
│   │                  Custom metric push: POST /suite-api/api/resources/{id}/stats                 │   │
│   │           Report run: POST /suite-api/api/reports → returns reportId for status poll          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Scripts automate report generation, alert bulk-acknowledge, and custom metric injection            │
│                                                                                                       │
│                                                  ▼                                                    │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             Operational Scripts              │                 Admin Scripts                  │   │
│   │              bulk-ack-alerts.py              │              export-dashboards.py              │   │
│   │            push-custom-metrics.py            │          cleanup-orphaned-objects.py           │   │
│   │            rightsizing-report.py             │             license-usage-check.py             │   │
│   │             alert-summary-csv.py             │            adapter-status-check.py             │   │
│   │          group-membership-audit.py           │               backup-trigger.sh                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  REST API on master node TCP 443 · scripts run from any host with network access to master            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  suite-api = Aria Ops REST API path prefix; all endpoints start with /suite-api/api                   │
│  Bearer token = Short-lived auth token from /auth/token/acquire; valid ~30 minutes                    │
│  resourceKind = Object type filter (VirtualMachine, HostSystem, Datastore, etc.)                      │
│  Custom metric = Externally pushed metric stored alongside collected metrics for an object            │
│  Bulk acknowledge = API call to mark multiple active alerts as acknowledged in one request            │
│  Report trigger = POST to /api/reports to generate on-demand report without UI interaction            │
│  Orphaned object = Object remaining in Aria Ops after its source (VM, host) is deleted                │
│  Dashboard JSON = Exported dashboard definition; can be imported via API on another instance          │
│  Adapter status = Health state of an adapter (collecting, no-data, error) queryable via API           │
│  License usage = Object count against licensed capacity; reportable via Admin API                     │
│  Group membership = Objects belonging to a group; listable via /api/groups/{id}/members               │
│  Retry logic = Exponential backoff pattern for handling 429/503 from Aria Ops API                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```python

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
