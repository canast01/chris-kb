# Aria Suite Lifecycle — Scripts


<div class="kb-summary">
Scripts reference covering Pre-Upgrade Disk Check, Environment Health Summary, Bulk Locker Password Export (Alias List), NTP Validation Across All Product Nodes, Trigger Upgrade via API (Non-Interactive).
</div>

  LCM Automation Scripts
```
┌─────────────────────────────────────────────────────────────────┐
│  Script                    Purpose                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ cert-expiry-check.sh   Query Locker → list certs         │   │
│  │                         expiring within N days           │   │
│  │ pre-upgrade-disk.sh    Check all mounts < threshold      │   │
│  │                         pass/fail gate before upgrade    │   │
│  │ lcm-health-summary.sh  Env health + running requests     │   │
│  │                         + disk usage summary             │   │
│  │ locker-password-export  Alias + username list (no values)│   │
│  │ ntp-check.sh           SSH to all nodes; check time sync │   │
│  │ trigger-upgrade.sh     API-driven upgrade with polling   │   │
│  │                         until COMPLETED/FAILED           │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                 │
│  All scripts: POST /lcm/authz/api/v2/login → bearer token       │
│  API base: https://<lcm>/lcm/lcmservice/api/v2                  │
└─────────────────────────────────────────────────────────────────┘
```
```
┌─────────────────────────────────────── Aria Suite LCM Scripts ────────────────────────────────────────┐
│                                                                                                       │
│  REST API scripts for LCM environment management, product queries, and cert actions.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Auth & Environment Scripts          │  │            Product Query Scripts            │   │
│   │         POST /lcm/api/v1/auth/login          │  │           GET /lcm/api/v1/products          │   │
│   │         GET /lcm/api/v1/environments         │  │           Filter by environment ID          │   │
│   │          Check env status via REST           │  │           GET product version info          │   │
│   │           Monitor request progress           │  │           List available upgrades           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Auth scripts get tokens; env scripts check state; product scripts drive upgrades.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Request Trigger Scripts            │  │            Cert & Health Scripts            │   │
│   │            POST /request/upgrade             │  │            GET /lcm/api/v1/health           │   │
│   │          POST /request/cert-rotate           │  │             GET cert expiry list            │   │
│   │           GET /request/{id}/status           │  │            Alert on expiry < 30d            │   │
│   │             Poll until COMPLETED             │  │         Script cert rotation trigger        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  LCM VM; scripts from jump host or CI/CD with HTTPS access to LCM API port 443                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM REST API        = HTTP/JSON interface for all LCM automation tasks                               │
│  POST /auth/login    = Returns session token for subsequent API calls                                 │
│  GET /environments   = Lists all environments with ID, name, and product count                        │
│  GET /products       = Lists managed products with version and health status                          │
│  POST /request       = Triggers a LCM action (upgrade, cert-rotate, etc.)                             │
│  Request ID          = Unique ID for a LCM action; poll for status                                    │
│  GET /request/status = Polls action status: PENDING, IN_PROGRESS, COMPLETED                           │
│  GET /health         = Returns LCM and managed product health summary                                 │
│  Cert Expiry Script  = Queries cert list; sends alert if expiry < 30 days                             │
│  Upgrade Script      = Triggers version upgrade for a product via REST                                │
│  Cert Rotate Script  = Triggers LCM cert rotation action via REST API                                 │
│  CI/CD Integration   = Scripts run on schedule for drift detection and reporting                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

---

## Environment Health Summary

Queries LCM API and prints the health status of all environments and products.

```bash
#!/usr/bin/env bash
# Usage: ./lcm-health-summary.sh <lcm-fqdn> <username> <password>
LCM=$1; USER=$2; PASS=$3

TOKEN=$(curl -sk -X POST "https://$LCM/lcm/authz/api/v2/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}" | jq -r '.token')

echo "=== LCM Environment Health ==="
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/lcmservice/api/v2/environments" | \
  jq -r '.[] | "Environment: \(.environmentName)  Health: \(.environmentHealth)"'

echo ""
echo "=== Running Requests ==="
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/lcmservice/api/v2/requests?state=RUNNING" | \
  jq -r '.[] | "[\(.requestType)] ID:\(.requestId)  Started:\(.startTime)"'

echo ""
echo "=== Disk Usage on LCM Appliance ==="
df -h / /data /var/log 2>/dev/null | column -t
```

---

## Bulk Locker Password Export (Alias List)

Exports the list of password aliases and associated usernames stored in Locker (values are never exposed via API).

```bash
#!/usr/bin/env bash
LCM=$1; USER=$2; PASS=$3

TOKEN=$(curl -sk -X POST "https://$LCM/lcm/authz/api/v2/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}" | jq -r '.token')

echo "alias,username,description"
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/locker/api/v2/passwords" | \
  jq -r '.passwords[] | [.alias, .userName, .description] | @csv'
```

---

## NTP Validation Across All Product Nodes

After LCM deploys products, verify NTP sync on all appliances to prevent certificate failures.

```bash
#!/usr/bin/env bash
# Usage: ./ntp-check.sh
# Edit NODES to match your environment
NODES=(
  "lcm-prod-01.example.local"
  "vidm-prod-01.example.local"
  "vrops-prod-01.example.local"
  "vrops-prod-02.example.local"
  "vra-prod-01.example.local"
  "vrli-prod-01.example.local"
)

for node in "${NODES[@]}"; do
  echo -n "$node: "
  ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@"$node" \
    "chronyc tracking 2>/dev/null | grep 'System time'" 2>/dev/null || echo "SSH failed"
done
```

---

## Trigger Upgrade via API (Non-Interactive)

Useful for scripted maintenance windows. Substitute environment ID and payload from UI inspection.

```bash
#!/usr/bin/env bash
LCM=$1; USER=$2; PASS=$3; ENV_ID=$4; PRODUCT_ID=$5; TARGET_VERSION=$6

TOKEN=$(curl -sk -X POST "https://$LCM/lcm/authz/api/v2/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}" | jq -r '.token')

# Trigger upgrade
RESPONSE=$(curl -sk -X POST -H "x-xenon-auth-token: $TOKEN" \
  -H "Content-Type: application/json" \
  "https://$LCM/lcm/lcmservice/api/v2/environments/$ENV_ID/products/$PRODUCT_ID/upgrade" \
  -d "{\"targetVersion\":\"$TARGET_VERSION\"}")

REQUEST_ID=$(echo "$RESPONSE" | jq -r '.requestId')
echo "Upgrade triggered — Request ID: $REQUEST_ID"
echo "Monitor: https://$LCM/lcm/lcmservice/api/v2/requests/$REQUEST_ID"

# Poll until complete
while true; do
  STATE=$(curl -sk -H "x-xenon-auth-token: $TOKEN" \
    "https://$LCM/lcm/lcmservice/api/v2/requests/$REQUEST_ID" | jq -r '.state')
  echo "$(date '+%H:%M:%S') — Request state: $STATE"
  [[ "$STATE" == "COMPLETED" || "$STATE" == "FAILED" ]] && break
  sleep 60
done
```
