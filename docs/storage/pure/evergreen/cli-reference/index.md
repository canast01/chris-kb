---
tags:
  - pure
---
# Pure Evergreen CLI Reference


<div class="kb-summary">
Pure Evergreen CLI Reference reference covering Overview, Pure1 REST API, FlashArray CLI (per-array), Alerts.
</div>

```text
Evergreen Management Interfaces
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  Pure1 REST API                                    │
  │  ├── GET /arrays          — array inventory        │
  │  ├── GET /subscriptions   — entitlement + capacity │
  │  ├── GET /metrics         — performance data       │
  │  └── GET /alerts          — fleet-wide alerts      │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  Per-array Purity CLI (SSH to array mgmt IP)       │
  │  ├── purearray list --controller  — controller gen │
  │  ├── purearray list --space       — capacity used  │
  │  └── purearray phonehome list     — telemetry ok   │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

> Part of the [Evergreen](../index.md) reference.
---

## Overview

Pure Evergreen//Forever and Evergreen//One are subscription programs, not software. There is no dedicated Evergreen CLI binary. Management is performed via:

- **Pure1 REST API** — fleet-wide subscription, asset, and metric data
- **FlashArray CLI (purity)** — per-array operations, accessible via SSH or the array's web UI terminal
- **Pure1 portal** — subscription status, upgrade scheduling, and support management

---

## Pure1 REST API

Base URL: `https://api.pure1.purestorage.com/api/1.x`  
Authentication: OAuth2 Bearer token using a Pure1 API Client (registered in the Pure1 portal).

### Authenticate

```bash
# Generate a signed JWT from your private key, then exchange for a Bearer token
# (Pure1 uses RS256-signed JWT assertions — generate with pureapiclient or openssl)

# Using pureapiclient helper (pip install py-pure-client)
python3 - <<'EOF'
from pypureclient import PureOneClient
client = PureOneClient(app_id="pure1:apikey:abc123", private_key_file="/path/to/private.pem")
token = client._get_token()
print(token)
EOF

# Store token for curl use
TOKEN=$(python3 -c "
from pypureclient import PureOneClient
c = PureOneClient(app_id='pure1:apikey:abc123', private_key_file='/path/to/private.pem')
print(c._get_token())
")
```

### Arrays

```bash
# List all arrays in the fleet
curl -s "https://api.pure1.purestorage.com/api/1.x/arrays" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Filter by model
curl -s "https://api.pure1.purestorage.com/api/1.x/arrays?filter=model%3D%27FlashArray%2F//X70R4%27" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Show array names and Purity versions
curl -s "https://api.pure1.purestorage.com/api/1.x/arrays" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for a in data.get('items', []):
    print(f\"{a['name']:30s}  model={a.get('model','?'):20s}  version={a.get('version','?')}\")
"
```

### Fleet Management

```bash
# List fleets
curl -s "https://api.pure1.purestorage.com/api/1.x/fleets" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# List fleet assets (arrays in a fleet)
FLEET_ID="fleet-abc123"
curl -s "https://api.pure1.purestorage.com/api/1.x/fleet-assets?filter=fleet.id%3D%27${FLEET_ID}%27" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Subscriptions

```bash
# List all subscriptions (Evergreen//One, Evergreen//Forever)
curl -s "https://api.pure1.purestorage.com/api/1.x/subscriptions" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Show subscription name, status, start/end dates
curl -s "https://api.pure1.purestorage.com/api/1.x/subscriptions" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for s in data.get('items', []):
    print(f\"{s.get('name','?'):30s}  status={s.get('status','?'):12s}  \
expires={s.get('expiration_date','?')}\")
"

# Check committed vs consumed for a subscription
SUB_ID="sub-xyz789"
curl -s "https://api.pure1.purestorage.com/api/1.x/subscriptions/${SUB_ID}" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

### Metrics (Historical Performance)

```bash
# Available metric keys
curl -s "https://api.pure1.purestorage.com/api/1.x/metrics?resource_types=arrays" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for m in data.get('items', []):
    print(m.get('name',''))
" | sort

# Get 24-hour capacity history for an array
ARRAY_ID="array-id-here"
START=$(date -u -d "24 hours ago" +%s 2>/dev/null || date -u -v-24H +%s)000
END=$(date -u +%s)000

curl -s "https://api.pure1.purestorage.com/api/1.x/metrics/history" \
  -H "Authorization: Bearer $TOKEN" \
  -G \
  --data-urlencode "ids=${ARRAY_ID}" \
  --data-urlencode "names=array_total_capacity,array_used_capacity" \
  --data-urlencode "resolution=3600000" \
  --data-urlencode "start_time=${START}" \
  --data-urlencode "end_time=${END}" | python3 -m json.tool
```

---

## FlashArray CLI (per-array)

Connect via SSH to the array management IP. User is typically `pureuser`.

```bash
ssh pureuser@flasharray01.example.com
```

| Command | Purpose |
|---|---|
| `purearray list` | Array identity, model, Purity version |
| `purearray list --space` | Total, used, shared, system, and free space |
| `purearray list --controller` | Controller hardware info and status |
| `purealert list` | Active and historical alerts |
| `purearray upgrade --check` | Check upgrade readiness (NDU pre-check) |
| `purearray upgrade --exec` | Execute a non-disruptive upgrade |

```bash
# Array identity and version
purearray list

# Space summary (TiB)
purearray list --space

# All active alerts
purealert list

# Unacknowledged errors only
purealert list --flagged false --severity error

# Check upgrade readiness before NDU
purearray upgrade --check

# Run non-disruptive upgrade (Evergreen NDU)
purearray upgrade --exec
```

### Space Breakdown

```bash
# Volume-level space (data reduction ratio)
purevol list --space

# Total shared space (snapshots, system overhead)
purearray list --space | awk 'NR==1 || /Total/'
```

---

## Alerts

```bash
# Pure1 API — active error-severity alerts across all arrays
curl -s "https://api.pure1.purestorage.com/api/1.x/alerts?filter=severity%3D%27error%27" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool

# Per-array CLI
purealert list --severity error

# Acknowledge an alert (by ID)
purealert acknowledge --id 123
```
