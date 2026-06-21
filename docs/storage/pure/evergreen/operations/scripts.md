---
tags:
  - operations
  - pure
---
# Evergreen — Script Reference


<div class="kb-summary">
Script Reference reference covering Subscription Capacity Report, Alert Configuration Audit, Evergreen//One SLA Consumption Tracker, Protection Group Replication Status.

*Applies to: Evergreen*
</div>
![Evergreen — Script Reference](../../../../assets/storage-pure-evergreen-operations-scripts.svg)


```text
  Pure Script Execution Paths

  Purity CLI (SSH)               Pure1 REST API
  ┌──────────────────────────────────────────── ┐           ┌ ────────────────────────────────────────────┐
  │  puritysh        │           │  Bearer token auth   │
  │  purearray list  │           │  GET /arrays         │
  │  purevol list    │           │  GET /metrics/history│
  │  purealert list  │           │  GET /subscriptions  │
  │  purepgroup list │           └──────────┬───────────┘
  └──────────────────┘                      │
                                            ▼
  Pure PowerShell SDK              ┌────────────────────┐
  ┌──────────────────┐             │  Python / Bash     │
  │  New-PfaArray    │             │  eo1_usage.py      │
  │  Get-PfaVolumes  │             │  burst_alert.sh    │
  │  Set-PfaVolume   │             │  sla_check.py      │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Alert audit: curl ──► /api/2.x/alert-watchers
  Replication:  curl ──► /api/2.x/protection-groups
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Subscription Capacity Report

Queries Pure1 API to report consumed vs committed TiB across all arrays in the Evergreen subscription.

```python
#!/usr/bin/env python3
"""
pure1-capacity-report.py
Requires: pip install requests
"""
import requests, json, os

PURE1_API_BASE = "https://api.pure1.purestorage.com/api/1.0"
API_TOKEN = os.environ.get("PURE1_API_TOKEN", "")

def get_auth_header():
    resp = requests.post(
        f"{PURE1_API_BASE}/oauth2/1.0/token",
        data={"grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
              "subject_token": API_TOKEN,
              "subject_token_type": "urn:ietf:params:oauth:token-type:jwt"}
    )
    resp.raise_for_status()
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}

def main():
    headers = get_auth_header()

    arrays = requests.get(f"{PURE1_API_BASE}/arrays", headers=headers).json()
    metrics = requests.get(
        f"{PURE1_API_BASE}/metrics/history",
        headers=headers,
        params={"names": "array_total_capacity,array_data_reduction",
                "resolution": 86400000}
    ).json()

    print(f"{'Array':<30} {'Model':<15} {'Capacity TiB':>14}")
    print("-" * 62)
    for a in arrays.get("items", []):
        print(f"{a.get('name','?'):<30} {a.get('model','?'):<15} "
              f"{a.get('capacity', 0) / 2**40:>13.2f}")

if __name__ == "__main__":
    main()
```

## Alert Configuration Audit

Lists current alert notification rules across all arrays managed by Evergreen//One or Evergreen//Flex.

```bash
#!/usr/bin/env bash
# pure-alert-audit.sh
# Audits alert rules on a single FlashArray
ARRAY_IP="<array-ip>"
TOKEN="<api-token>"

echo "=== Alert Rules on $ARRAY_IP ==="
curl -s -k -H "x-auth-token: $TOKEN" \
    "https://$ARRAY_IP/api/2.16/alert-watchers" | jq -r '.items[] | "\(.name)\t\(.enabled)"'

echo ""
echo "=== Open Alerts ==="
curl -s -k -H "x-auth-token: $TOKEN" \
    "https://$ARRAY_IP/api/2.16/alerts?filter=state%3D%27open%27" | \
    jq -r '.items[] | "[\(.severity)] \(.summary)"'
```

## Evergreen//One SLA Consumption Tracker

Tracks consumed TiB vs SLA committed TiB over time, alerting when within 90% of commitment.

```bash
#!/usr/bin/env bash
# evg-sla-check.sh
# Requires pure1 CLI or jq + curl with Pure1 token
COMMITTED_TIB=500   # edit to match your commitment
TOKEN="<pure1-token>"

CONSUMED=$(curl -s -k -H "Authorization: Bearer $TOKEN" \
    "https://api.pure1.purestorage.com/api/1.0/subscriptions" | \
    jq '[.items[].consumed_tib] | add // 0')

PCT=$(echo "scale=1; $CONSUMED * 100 / $COMMITTED_TIB" | bc)
echo "Consumed: ${CONSUMED} TiB / ${COMMITTED_TIB} TiB committed (${PCT}%)"

THRESHOLD=90
if (( $(echo "$PCT >= $THRESHOLD" | bc -l) )); then
    echo "WARNING: SLA consumption above ${THRESHOLD}% threshold"
fi
```

## Protection Group Replication Status

```bash
#!/usr/bin/env bash
# pg-replication-status.sh
ARRAY_IP="<source-array-ip>"
TOKEN="<api-token>"

echo "=== Protection Group Replication Status ==="
curl -s -k -H "x-auth-token: $TOKEN" \
    "https://$ARRAY_IP/api/2.16/protection-groups" | \
    jq -r '.items[] | "\(.name)\t replication_enabled=\(.replication_enabled // "N/A")"'
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Evergreen — Procedures](procedures/)
- [Evergreen — CLI Reference](cli-reference/)
- [Evergreen — Health Checks](health-checks/)
