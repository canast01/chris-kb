# Evergreen — CLI Reference

```text
Evergreen Management — CLI/API Access Points
  ┌────────────────────────────────────────────────────┐
  │  Pure1 REST API (jwt auth, api.pure1.purestorage)  │
  │  ├── /metrics/history  — fleet performance data    │
  │  ├── /arrays           — array inventory + health  │
  │  ├── /subscriptions    — entitlement + capacity    │
  │  └── /alerts           — fleet alerts              │
  └────────────────────────────────────────────────────┘
  ┌────────────────────────────────────────────────────┐
  │  Purity CLI (SSH to array management IP)           │
  │  ├── purearray list               — array status   │
  │  ├── purearray list --controller  — controller gen │
  │  ├── purearray phonehome list     — phone-home ok  │
  │  └── purearray list --space       — capacity used  │
  └────────────────────────────────────────────────────┘
```

> Part of the [Evergreen Operations](../index.md) reference.

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
