# Pure Evergreen//One CLI Reference

> Part of the [Evergreen//One](../) reference.
---

## Overview

Pure Evergreen//One is Pure Storage's as-a-service (STaaS) subscription. Capacity is consumed against a reserved tier and may enter burst above that level. There is no standalone CLI — management is via the **Pure1 REST API**, the **Pure1 portal**, and the **per-array FlashArray CLI** for physical checks.

---

## Pure1 REST API — Subscription

Base URL: `https://api.pure1.purestorage.com/api/1.x`

Authenticate as described in the [Pure Evergreen CLI Reference](../../evergreen/cli-reference/). Obtain a Bearer token via OAuth2 (RS256 JWT assertion using a Pure1 API Client).

### List Subscriptions

```bash
# All subscriptions (Evergreen//One will appear with type "evergreen-one" or "STaaS")
curl -s "https://api.pure1.purestorage.com/api/1.x/subscriptions" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Filter for Evergreen//One subscriptions
curl -s "https://api.pure1.purestorage.com/api/1.x/subscriptions?filter=subscription_type%3D%27Evergreen%2F%2FOne%27" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Subscription Assets

Assets are the arrays assigned to an Evergreen//One subscription.

```bash
# List all subscription assets
curl -s "https://api.pure1.purestorage.com/api/1.x/subscription-assets" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Filter by subscription ID
SUB_ID="sub-eo-12345"
curl -s "https://api.pure1.purestorage.com/api/1.x/subscription-assets?filter=subscription.id%3D%27${SUB_ID}%27" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Capacity: Reserved vs Consumed vs Burst

```bash
# Get usage details for a subscription
curl -s "https://api.pure1.purestorage.com/api/1.x/subscriptions/${SUB_ID}" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
# Top-level capacity fields vary by API version — print all
for k, v in data.items():
    if 'capacity' in k.lower() or 'tier' in k.lower() or 'reserved' in k.lower():
        print(f'{k}: {v}')
"

# Parse and display reserved vs consumed (with burst flag)
curl -s "https://api.pure1.purestorage.com/api/1.x/subscriptions/${SUB_ID}" \
  -H "Authorization: Bearer $TOKEN" | python3 - <<'EOF'
import sys, json

data = json.load(sys.stdin)
tiers = data.get("tiers", data.get("usageDetails", []))

for tier in tiers:
    name      = tier.get("name", tier.get("serviceLevel", "unknown"))
    reserved  = float(tier.get("reserved_capacity", tier.get("committedCapacity", 0)))
    consumed  = float(tier.get("consumed_capacity", tier.get("consumedCapacity",  0)))
    burst_cap = float(tier.get("burst_capacity",    tier.get("burstCapacity",     0)))
    pct       = (consumed / reserved * 100) if reserved > 0 else 0
    in_burst  = consumed > reserved

    flag = "BURST" if in_burst else ("WARN >90%" if pct >= 90 else "OK")
    print(f"[{flag:10s}] {name:25s}  reserved={reserved:8.2f} TiB  "
          f"consumed={consumed:8.2f} TiB  burst_cap={burst_cap:8.2f} TiB  ({pct:.1f}%)")
EOF
```

---

## Burst Usage Tracking

Burst consumption above the reserved tier incurs additional charges on the next bill cycle.

```bash
# Daily burst summary script — run as a cron job
cat <<'SCRIPT' > /usr/local/bin/check-pure-burst.py
#!/usr/bin/env python3
"""Check Pure Evergreen//One burst usage via Pure1 API."""
import json, sys, urllib.request, urllib.parse

TOKEN = open("/etc/pure1/token").read().strip()
SUB_ID = "sub-eo-12345"

req = urllib.request.Request(
    f"https://api.pure1.purestorage.com/api/1.x/subscriptions/{SUB_ID}",
    headers={"Authorization": f"Bearer {TOKEN}"}
)
data = json.loads(urllib.request.urlopen(req).read())

for tier in data.get("tiers", []):
    reserved = float(tier.get("reserved_capacity", 0))
    consumed = float(tier.get("consumed_capacity", 0))
    if consumed > reserved:
        excess = consumed - reserved
        print(f"BURST: {tier['name']} — {excess:.2f} TiB above reserved ({consumed:.2f}/{reserved:.2f})")
        sys.exit(1)

print("OK: No burst usage detected")
sys.exit(0)
SCRIPT
chmod +x /usr/local/bin/check-pure-burst.py
```

---

## Per-Array Check (FlashArray CLI)

SSH to the array management IP as `pureuser`.

```bash
# Array space summary
purearray list --space

# Controller hardware and status
purearray list --controller

# Volume-level space with data reduction
purevol list --space

# Check effective capacity vs raw for sizing against subscription tier
purearray list --space | grep -E "Total|Free|System"
```

### Calculate Effective Consumption

```bash
# Correlation: Pure1 subscription "consumed" = effective logical data on array(s)
# Per-array breakdown (SSH):
ssh pureuser@flasharray01.example.com "purearray list --space" | \
  awk '/Total/ {print "Array used:", $2, "TiB"}'
```

---

## SLA and Tier Information

Contract details (SLA tiers, committed capacity, burst ceiling) are managed through the Pure1 portal or via the API — there is no local CLI for subscription contract details.

```bash
# Show tier definitions for the subscription
curl -s "https://api.pure1.purestorage.com/api/1.x/subscriptions/${SUB_ID}" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('Subscription name:', data.get('name','?'))
print('Status:', data.get('status','?'))
print('Start:', data.get('start_date','?'))
print('End:  ', data.get('expiration_date','?'))
for tier in data.get('tiers', []):
    print(f\"  Tier: {tier.get('name','?'):20s}  Reserved: {tier.get('reserved_capacity','?')} TiB\")
"
```

---

## Alerts and Health

```bash
# Pure1 API — error alerts across all subscription assets
curl -s "https://api.pure1.purestorage.com/api/1.x/alerts?filter=severity%3D%27error%27" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Per-array CLI — active alerts
purealert list

# Filter by severity
purealert list --severity error
purealert list --severity warning

# Acknowledge an alert
purealert acknowledge --id 456

# Get hardware health
purehw list
purehw list --type drive
purehw list --type fan
purehw list --type psu
```
