# Aria Suite Lifecycle — Scripts

```text
  LCM Automation Scripts
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

Automation scripts for LCM target three primary use cases: pre-upgrade validation (confirming disk space, certificate validity, and product health before initiating an upgrade), certificate expiry monitoring (scanning all Locker entries and alerting when within a configurable threshold), and scheduled health checks via the LCM REST API. Scripts use the LCM API base URL `https://<lcm-fqdn>/lcm/lcmservice/api/v2` with Basic or token authentication.

---

## Certificate Expiry Monitor

Queries the Locker API and prints certificates expiring within a configurable threshold.

```bash
#!/usr/bin/env bash
# Usage: ./cert-expiry-check.sh <lcm-fqdn> <username> <password> <warn-days>
LCM=$1; USER=$2; PASS=$3; WARN=${4:-30}

TOKEN=$(curl -sk -X POST "https://$LCM/lcm/authz/api/v2/login" \
  -H 'Content-Type: application/json' \
  -d "{\"username\":\"$USER\",\"password\":\"$PASS\"}" | jq -r '.token')

echo "=== Certificates expiring within $WARN days ==="
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/locker/api/v2/certificates" | \
  jq --argjson w "$WARN" \
  '.certificates[] | select((.daysToExpiry|tonumber) <= $w) |
   "[\(.daysToExpiry) days] \(.alias) — expires \(.expirationDate)"' -r

echo "=== All Locker certificates ==="
curl -sk -H "x-xenon-auth-token: $TOKEN" \
  "https://$LCM/lcm/locker/api/v2/certificates" | \
  jq -r '.certificates[] | "\(.alias)\t\(.daysToExpiry) days\t\(.expirationDate)"' | \
  sort -t$'\t' -k2 -n
```

---

## Pre-Upgrade Disk Check

Run on the LCM appliance as root before any upgrade workflow.

```bash
#!/usr/bin/env bash
# Run on LCM appliance as root before any upgrade
THRESHOLD=80
ALL_OK=true

for mount in / /data /tmp /var/log; do
  if mountpoint -q "$mount"; then
    used=$(df -h "$mount" | awk 'NR==2{print $5}' | tr -d '%')
    echo "$mount: ${used}% used"
    if [[ $used -ge $THRESHOLD ]]; then
      echo "  WARNING: $mount exceeds ${THRESHOLD}% — free space before upgrading"
      ALL_OK=false
    fi
  fi
done

if $ALL_OK; then
  echo "PASS: All filesystems within threshold"
else
  echo "FAIL: Disk space check failed — do not proceed with upgrade"
  exit 1
fi
```

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
