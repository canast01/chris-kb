# Aria Operations — Scripts

```
Aria Operations API — Script Interaction Pattern
┌─────────────────────────────────────────────────────┐
│  Script / Automation Pipeline                       │
└──────────────────────┬──────────────────────────────┘
                       │ 1. Authenticate
                       │    POST /suite-api/api/auth/token/acquire
                       │    → token (valid 30 min)
                       ▼
┌─────────────────────────────────────────────────────┐
│  Aria Operations REST API                           │
│  Authorization: vRealizeOpsToken <token>            │
│                                                     │
│  GET  /api/alerts?activeOnly=true   active alerts   │
│  GET  /api/resources?resourceKind=  object query    │
│       ClusterComputeResource                        │
│  POST /api/resources/query          filtered query  │
│  POST /api/analytics/run            force recalc    │
│  GET  /api/cluster/nodes            node status     │
│  POST /api/backups/<id>/actions/    trigger backup  │
│       backup                                        │
└──────────────────────┬──────────────────────────────┘
                       │ 2. Parse JSON response
                       ▼
┌─────────────────────────────────────────────────────┐
│  Output / Integration                               │
│  → CSV export (alerts, capacity, idle VMs)          │
│  → monitoring dashboard (HTTP POST)                 │
│  → ITSM integration                                 │
│  NOTE: re-authenticate every 25 min for long runs   │
└─────────────────────────────────────────────────────┘
```

## Authentication Helper (Python)

```python
#!/usr/bin/env python3
"""Acquire an Aria Operations API token."""
import requests
import urllib3
urllib3.disable_warnings()

ARIA_OPS_HOST = "aria-ops.domain.local"
USERNAME = "admin"
PASSWORD = "changeme"
AUTH_SOURCE = "LOCAL"  # or "LDAP" for AD accounts

def get_token():
    url = f"https://{ARIA_OPS_HOST}/suite-api/api/auth/token/acquire"
    payload = {
        "username": USERNAME,
        "authSource": AUTH_SOURCE,
        "password": PASSWORD
    }
    r = requests.post(url, json=payload, verify=False)
    r.raise_for_status()
    return r.json()["token"]

if __name__ == "__main__":
    token = get_token()
    print(f"Token: {token}")
```

---

## Export Active Alerts to CSV (Python)

```python
#!/usr/bin/env python3
"""Export all active critical/immediate alerts to CSV."""
import requests
import csv
import urllib3
urllib3.disable_warnings()

ARIA_OPS_HOST = "aria-ops.domain.local"
TOKEN = "your-token-here"

def get_alerts():
    url = f"https://{ARIA_OPS_HOST}/suite-api/api/alerts"
    headers = {"Authorization": f"vRealizeOpsToken {TOKEN}"}
    params = {"activeOnly": "true", "criticality": ["CRITICAL", "IMMEDIATE"]}
    r = requests.get(url, headers=headers, params=params, verify=False)
    r.raise_for_status()
    return r.json().get("alerts", [])

def export_alerts(alerts, filename="alerts_export.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Alert ID", "Name", "Object", "Criticality", "Status", "Start Time"])
        for a in alerts:
            writer.writerow([
                a.get("id"),
                a.get("type", {}).get("name"),
                a.get("resourceName"),
                a.get("criticality"),
                a.get("status"),
                a.get("startTimeUTC")
            ])
    print(f"Exported {len(alerts)} alerts to {filename}")

if __name__ == "__main__":
    alerts = get_alerts()
    export_alerts(alerts)
```

---

## Capacity Report (PowerShell)

```powershell
# Export cluster capacity summary via REST API
$AriaOpsHost = "aria-ops.domain.local"
$Token       = "your-token-here"

$Headers = @{ Authorization = "vRealizeOpsToken $Token" }

# Get all cluster compute resources
$Uri = "https://$AriaOpsHost/suite-api/api/resources?resourceKind=ClusterComputeResource"
$Response = Invoke-RestMethod -Uri $Uri -Headers $Headers -SkipCertificateCheck

foreach ($cluster in $Response.resourceList) {
    Write-Output "Cluster: $($cluster.resourceKey.name)"
}
```

---

## Cluster Health Check (Bash)

```bash
#!/usr/bin/env bash
# Quick Aria Operations cluster health check
HOST="aria-ops.domain.local"

echo "=== Aria Operations Cluster Health ==="
ssh admin@$HOST "vracli cluster health"

echo ""
echo "=== Adapter Status ==="
ssh admin@$HOST "vracli adapter list"

echo ""
echo "=== Service Status ==="
ssh admin@$HOST "vracli status"
```

---

## Alert Export via REST (Bash / curl)

```bash
#!/usr/bin/env bash
HOST="aria-ops.domain.local"
USER="admin"
PASS="changeme"

# Get token
TOKEN=$(curl -sk -X POST "https://$HOST/suite-api/api/auth/token/acquire" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$USER\",\"authSource\":\"LOCAL\",\"password\":\"$PASS\"}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

echo "Token acquired"

# Export active alerts
curl -sk -H "Authorization: vRealizeOpsToken $TOKEN" \
  "https://$HOST/suite-api/api/alerts?activeOnly=true" \
  | python3 -m json.tool > /tmp/aria-ops-alerts-$(date +%Y%m%d).json

echo "Alerts saved to /tmp/aria-ops-alerts-$(date +%Y%m%d).json"
```

---

## Related Sections

- [CLI Reference](../cli-reference/index.md) — vracli and REST API basics
- [Operations](../index.md) — operational runbooks
- [Troubleshooting](../../troubleshooting/index.md) — diagnostic use cases
