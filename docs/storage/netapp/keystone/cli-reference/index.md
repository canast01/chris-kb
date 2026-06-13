---
tags:
  - netapp
---
# NetApp Keystone — CLI Reference

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
```text
┌─────────────────────────────────── NetApp Keystone — CLI Reference ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        CLI interfaces: ONTAP CLI (SSH), Keystone Collector CLI (Linux), Active IQ REST        │   │
│   │        ONTAP CLI: volume show, vserver show, storage aggregate show, net interface show       │   │
│   │         Collector CLI: keystone-collector status, collect, upload, logs, config-check         │   │
│   │          Active IQ REST: GET /v1/keystone/capacity, GET /v1/keystone/billing/invoices         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    SSH to cluster mgmt LIF -> ONTAP CLI; SSH to Collector VM -> collector-manager CLI                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          ONTAP CLI          │  │        Collector CLI        │  │        Active IQ API        │   │
│   │         volume show         │  │          ks status          │  │        GET /capacity        │   │
│   │         vserver show        │  │          ks collect         │  │        GET /invoices        │   │
│   │          aggr show          │  │          ks upload          │  │         GET /billing        │   │
│   │         net int show        │  │           ks logs           │  │         Auth: Bearer        │   │
│   │      storage disk show      │  │       ks config-check       │  │         TLS required        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    ONTAP CLI privilege levels: admin (default), advanced (diag-level commands)                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Command      │   Description    │     Interface     │      Level       │      Notes       │   │
│   │   volume show    │   List volumes   │     ONTAP CLI     │      admin       │     Per SVM      │   │
│   │    aggr show     │    List aggrs    │     ONTAP CLI     │      admin       │    Disk usage    │   │
│   │    ks status     │   Coll. health   │     Collector     │    Linux root    │    Svc status    │   │
│   │    ks upload     │   Force upload   │     Collector     │    Linux root    │    Debug use     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: SSH from jump host to cluster mgmt LIF (22/TCP); HTTPS to Active IQ (443)                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ONTAP CLI          = SSH-based command shell on cluster mgmt LIF; fsm-driven                       │
│    Privilege level    = admin (normal) vs advanced (set -priv advanced); diag for support             │
│    vserver show       = Lists all SVMs; use -vserver <name> to filter                                 │
│    volume show -space = Adds used/available columns; key for Keystone sizing                          │
│    aggr show -space   = Aggregate capacity; Keystone committed is at aggr level                       │
│    ks status          = Keystone Collector service status; checks upload backlog                      │
│    ks collect         = Manually trigger ONTAP REST poll; useful after fix                            │
│    ks upload          = Force metric upload to Active IQ; bypasses schedule                           │
│    ks config-check    = Validates Collector config (API creds, endpoints, proxy)                      │
│    Bearer token       = Active IQ REST auth; retrieved via NetApp SSO login                           │
│    net int show       = Lists all LIFs; confirms data/mgmt LIF status and IP                          │
│    storage disk show  = Physical disk info; checks spares, broken, and RAID groups                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# List service levels (tiers) available under a subscription
curl -s "https://api.activeiq.netapp.com/v1/keystone/subscriptions/${SUBSCRIPTION_ID}/service-levels" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```
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
```bash
# Volumes with thick guarantee (count against committed immediately)
volume show -space-guarantee volume -fields size,used,space-guarantee

# Volumes with thin/none guarantee (count against committed as written)
volume show -space-guarantee none -fields size,used,space-guarantee
```
```bash
BLUEXP_TOKEN="<bluexp_bearer_token>"

# List Digital Wallet assets
curl -s "https://api.bluexp.netapp.com/marketplace/api/v1/subscriptions" \
  -H "Authorization: Bearer $BLUEXP_TOKEN" | python3 -m json.tool

# Check capacity pool status
curl -s "https://api.bluexp.netapp.com/marketplace/api/v1/capacity-pools" \
  -H "Authorization: Bearer $BLUEXP_TOKEN" | python3 -m json.tool
```
