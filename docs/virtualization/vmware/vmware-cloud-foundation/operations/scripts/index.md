# VCF Operations — Scripts

```
VCF API Automation — Data Flow
┌─────────────────────────────────────────────────────┐
│  Automation Script / Pipeline                       │
│  (Python / Bash / PowerShell)                       │
└──────────────────────┬──────────────────────────────┘
                       │ HTTPS POST /v1/tokens
                       ▼
┌─────────────────────────────────────────────────────┐
│  SDDC Manager REST API                              │
│  https://<sddc-mgr>/v1                             │
│                                                     │
│  GET /v1/domains      ◄── list workload domains    │
│  GET /v1/clusters     ◄── list all clusters        │
│  GET /v1/hosts        ◄── list managed hosts       │
│  POST /v1/system/     ◄── trigger health check     │
│       health-summary                               │
│  PATCH /v1/credentials ◄── rotate credentials     │
└──────────────────────┬──────────────────────────────┘
                       │ returns JSON
                       ▼
┌─────────────────────────────────────────────────────┐
│  Script Output / Integration                        │
│  → stdout / CSV / JSON                              │
│  → monitoring platform (HTTP POST)                  │
│  → ITSM ticketing system                           │
│  → CMDB asset discovery                            │
└─────────────────────────────────────────────────────┘
```

VCF REST API scripts use the SDDC Manager API base URL `https://<sddc-mgr-fqdn>/v1` with Basic authentication. The primary use cases are listing workload domain inventory, polling component health, and triggering SoS health checks programmatically for integration with monitoring platforms. Python is preferred for VCF API scripts due to the available `requests` library on the SDDC Manager appliance.

## List All Workload Domains (Python)

```python
#!/usr/bin/env python3
import requests, sys, json
from requests.auth import HTTPBasicAuth

sddc = sys.argv[1]; user = sys.argv[2]; pw = sys.argv[3]
r = requests.get(f"https://{sddc}/v1/domains",
                 auth=HTTPBasicAuth(user, pw), verify=False)
for d in r.json().get("elements", []):
    print(f"{d['name']:30} status={d['status']}  type={d['type']}")
```

## Trigger SoS Health Check and Poll Result (Bash)

```bash
#!/usr/bin/env bash
SDDC=$1; USER=$2; PASS=$3
# Trigger health check task
TASK=$(curl -sk -u "$USER:$PASS" -X POST \
  "https://$SDDC/v1/system/health-summary" | jq -r '.id')
echo "SoS task ID: $TASK"
# Poll until complete
while true; do
  STATUS=$(curl -sk -u "$USER:$PASS" \
    "https://$SDDC/v1/tasks/$TASK" | jq -r '.status')
  echo "  Status: $STATUS"
  [[ "$STATUS" == "Successful" || "$STATUS" == "Failed" ]] && break
  sleep 10
done
```
