# NetApp Keystone CLI Reference

> Part of the [Keystone](../) reference.

---

## Overview

NetApp Keystone is a subscription-based STaaS offering managed through BlueXP and the ActiveIQ / Keystone REST API. There is no standalone CLI binary; interaction is via REST API (curl/Python) or the BlueXP web UI. ONTAP CLI is used for raw capacity checking on the underlying volumes and aggregates.

---

## Keystone REST API

Base URL: `https://api.activeiq.netapp.com`  
Authentication: OAuth2 Bearer token obtained from the NetApp identity service.

### Authenticate (OAuth2)

```bash
# Exchange client credentials for a bearer token
TOKEN=$(curl -s -X POST "https://netapp-cloud-account.auth0.com/oauth/token" \
  -H "Content-Type: application/json" \
  -d '{
    "grant_type": "client_credentials",
    "client_id": "<YOUR_CLIENT_ID>",
    "client_secret": "<YOUR_CLIENT_SECRET>",
    "audience": "https://api.activeiq.netapp.com"
  }' | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Token acquired"
```

### Subscriptions

```bash
# List all Keystone subscriptions
curl -s -X GET "https://api.activeiq.netapp.com/v1/keystone/subscriptions" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" | python3 -m json.tool

# Get details for a specific subscription
SUBSCRIPTION_ID="KS-12345"
curl -s -X GET "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Usage Reporting

```bash
# Get current usage for a subscription
curl -s -X GET \
  "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/usage" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Usage with date range (ISO8601)
curl -s -X GET \
  "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/usage?from=2024-11-01T00:00:00Z&to=2024-11-30T23:59:59Z" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Parse committed vs consumed vs burst in one shot
curl -s "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/usage" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for tier in data.get('usageDetails', []):
    print(f\"{tier['serviceLevel']:20s}  committed={tier['committedCapacity']:>8} TiB  \
consumed={tier['consumedCapacity']:>8} TiB  burst={tier.get('burstCapacity',0):>8} TiB\")
"
```

### Service Level Listing

```bash
# List service levels (tiers) available under a subscription
curl -s "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/service-levels" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

---

## Burst Usage Alerting

Keystone subscriptions have a committed tier and a burst tier. Consuming above the committed level incurs burst charges.

```bash
# Check if any tier is in burst (consumed > committed)
curl -s "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/usage" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
alert = False
for tier in data.get('usageDetails', []):
    committed = float(tier.get('committedCapacity', 0))
    consumed  = float(tier.get('consumedCapacity',  0))
    pct = (consumed / committed * 100) if committed > 0 else 0
    status = 'BURST' if consumed > committed else ('WARN' if pct >= 90 else 'OK')
    print(f\"{status}  {tier['serviceLevel']:20s}  {pct:5.1f}%  ({consumed:.1f} / {committed:.1f} TiB)\")
    if status != 'OK':
        alert = True
sys.exit(1 if alert else 0)
"
```

---

## ONTAP CLI — Capacity Tracking

Use these commands on the underlying ONTAP cluster to cross-check capacity data reported to Keystone.

```bash
# All volumes: size, used, available
volume show -fields size,used,available,percent-used

# Sort by percent-used (highest first)
volume show -fields size,used,percent-used | sort -k4 -rn

# Aggregate-level capacity
storage aggregate show -fields size,used,available,percent-used

# SVM-level logical space view
vserver show -fields name -type data
volume show -vserver <svm_name> -fields size,used,logical-used,available

# QoS workload to correlate per-volume performance with Keystone tier
qos workload show -fields workload-name,volume,policy-group

# Check volume space guarantee (impacts Keystone committed capacity)
volume show -fields space-guarantee,size,used
```

### Thin vs Thick Provisioning Check

```bash
# Volumes with thick guarantee (count against committed immediately)
volume show -space-guarantee volume -fields size,used,space-guarantee

# Volumes with thin/none guarantee (count against committed as written)
volume show -space-guarantee none -fields size,used,space-guarantee
```

---

## BlueXP Digital Wallet (UI-equivalent API)

Keystone subscription wallet data is also exposed through BlueXP Digital Wallet:

```bash
BLUEXP_TOKEN="<bluexp_bearer_token>"

# List Digital Wallet assets
curl -s "https://api.bluexp.netapp.com/marketplace/api/v1/subscriptions" \
  -H "Authorization: Bearer $BLUEXP_TOKEN" | python3 -m json.tool

# Check capacity pool status
curl -s "https://api.bluexp.netapp.com/marketplace/api/v1/capacity-pools" \
  -H "Authorization: Bearer $BLUEXP_TOKEN" | python3 -m json.tool
```
