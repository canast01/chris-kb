---
tags:
  - operations
  - pure
description: "CLI Reference reference covering Overview, Pure1 REST API, FlashArray CLI (per-array), Alerts."
---
# Evergreen — CLI Reference

<div class="kb-summary">
CLI Reference reference covering Overview, Pure1 REST API, FlashArray CLI (per-array), Alerts.

*Applies to: Evergreen*
</div>
![Evergreen — CLI Reference](../../../../../assets/storage-pure-evergreen-operations-cli-reference.svg)

![Evergreen — CLI Reference — Diagram](../../../../../assets/storage-pure-evergreen-operations-cli-reference-diagram.svg)

> Part of the [Evergreen Operations](index.md) reference.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

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


```text title="Expected output"
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwdXJlMTphcGlrZXk6YWJjMTIzIiwiZXhwIjoxNzA5MzM4OTQ1LCJpYXQiOjE3MDkzMzUzNDUsInN1YiI6InB1cmUxOmFwaWtleTphYmMxMjMifQ.SigNatureDataHere_kV8xJ2mK9pL4qR7sT0uV3wX6yZ9aB2cD5eF8gH1iJ4kL7mN0oP3qS6tU9vW2xY5zA8bC1dE4fG7hI0jK3lM6nO9pQ2rS5tU8vV1wX4yZ7aB0cD3eF6gH9iJ2kL5mN8oP1qS4tU7vV0wX3yZ6aA9bC2dE5fG8hI1jK4lM7nO0pQ1rS3tU6vV9wX2yZ5aA8bC1dE4fG7hI0jK3lM6nO9pQ2rS5tU8vV1wX4yZ7aB0cD3eF6gH9iJ2kL5mN8oP1qS4tU7vV0wX3yZ6aA9bC2dE5fG8hI1jK4lM7nO0pQ1rS3tU6vV9wX2yZ5aA8bC1dE4fG7hI0jK3lM6nO9pQ2rS5tU8vV1wX4yZ7aB0cD3eF6gH9iJ2kL5mN8oP1qS4tU7vV0wX3yZ6aA9bC2dE5fG8hI1jK4lM7nO0pQ1rS3tU6vV9wX2yZ5aA8bC1dE4fG7hI0jK3lM6nO9pQ2rS5tU8vV1wX4yZ7aB0cD3eF6gH9iJ2kL5mN8oP1qS4tU7vV0wX3yZ6aA9bC2dE5fG8hI1jK4lM7nO0pQ1rS3tU6vV9wX2yZ5aA8bC1dE4fG7hI0jK3lM6nO9pQ2rS5tU8vV1wX4yZ7aB0cD3eF6gH9iJ2kL5mN8oP1qS4tU7vV0wX3yZ6aA9bC2dE5fG
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


```text title="Expected output"
{
  "items": [
    {
      "id": "8b1d4c2a-9f3e-47b2-8c1f-5e6d7a9b0c1d",
      "name": "prod-fa-01",
      "model": "FlashArray//X70R4",
      "serial": "PUREARRAY123456",
      "version": "6.4.2",
      "capacity": 107374182400,
      "used": 53687091200,
      "status": "healthy"
    },
    {
      "id": "c3e9f1b4-2d5a-41c8-9e7f-3a6b8c2d1e5f",
      "name": "prod-fa-02",
      "model": "FlashArray//X70R4",
      "serial": "PUREARRAY789012",
      "version": "6.4.2",
      "capacity": 107374182400,
      "used": 71581388800,
      "status": "healthy"
    },
    {
      "id": "f7a2c5d8-1e9b-4f3a-8c2d-6b5e9a1f3c7d",
      "name": "dr-fa-01",
      "model": "FlashArray//X20R2",
      "serial": "PUREARRAY345678",
      "version": "6.3.8",
      "capacity": 53687091200,
      "used": 21474836480,
      "status": "healthy"
    }
  ],
  "more_items_token": null,
  "total_item_count": 3
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Add `-k` flag to skip certificate verification or update your CA bundle with `update-ca-certificates`.
    **`jq: command not found`** — Install `python3-json.tool` or use `python3 -m json.tool` instead of piping to `jq`.
    **`{"error_code":"401000","message":"Unauthorized"}`** — Verify `$TOKEN` is set with a valid Pure1 API token using `echo $TOKEN` and regenerate if expired.
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


```text title="Expected output"
{
  "items": [
    {
      "id": "sub-a1b2c3d4e5f6",
      "name": "Evergreen//Forever-Production",
      "status": "active",
      "expiration_date": "2099-12-31T23:59:59Z",
      "start_date": "2023-01-15T00:00:00Z"
    },
    {
      "id": "sub-x9y8z7w6v5u4",
      "name": "Evergreen//One-DR-Cluster",
      "status": "active",
      "expiration_date": "2025-06-30T23:59:59Z",
      "start_date": "2024-06-30T00:00:00Z"
    }
  ]
}
Evergreen//Forever-Production  status=active        expires=2099-12-31T23:59:59Z
Evergreen//One-DR-Cluster      status=active        expires=2025-06-30T23:59:59Z
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.pure1.purestorage.com`** — Verify network connectivity and DNS resolution; check if the Pure1 API endpoint is accessible from your network.
    **`{"error_code":"401","message":"Unauthorized"}`** — Ensure the `$TOKEN` environment variable is set to a valid Pure1 API token and has not expired.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1`** — Verify the API response is valid JSON; check for HTTP errors (e.g., 403, 500) by adding `-v` flag to curl to inspect response headers.
---

## FlashArray CLI (per-array)

Connect via SSH to the array management IP. User is typically `pureuser`.

```bash
ssh pureuser@flasharray01.example.com
```


```text title="Expected output"
The authenticity of host 'flasharray01.example.com (192.168.1.45)' can't be established.
ECDSA key fingerprint is SHA256:aBcD1EfGhIjKlMnOpQrStUvWxYz2345678901234567.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'flasharray01.example.com,192.168.1.45' (ECDSA) to the known_hosts file.
pureuser@flasharray01.example.com's password:
Connected to flasharray01 (10.20.30.40)
Purity Version: 6.4.2
You are now logged in as pureuser
flasharray01>
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname flasharray01.example.com: Name or service not known`** — Verify the hostname is correct and resolvable via DNS or add an entry to /etc/hosts.
    **`Permission denied (publickey,password).`** — Confirm the pureuser credentials are correct and the account exists on the Pure Storage array.
    **`ssh: connect to host flasharray01.example.com port 22: Connection timed out`** — Check network connectivity to the array and verify the management IP address is reachable and SSH service is running.
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


```text title="Expected output"
Name                          Version          Model
purearray-prod-01             6.4.2.1          FlashArray//X
purearray-prod-02             6.4.2.1          FlashArray//X
purearray-dr-01               6.4.1.8          FlashArray//X

Name                          Capacity(TiB)    Used(TiB)      Available(TiB)
purearray-prod-01             100.0            67.3           32.7
purearray-prod-02             100.0            71.2           28.8
purearray-dr-01               50.0             41.5           8.5

Name                          Severity         Code           Message
purearray-prod-01             warning          CRIT_0847      Controller 1 temperature elevated
purearray-prod-02             error            CRIT_1203      NVMe module 3 predictive failure
purearray-dr-01               warning          CRIT_0521      Replication lag > 5 minutes

Name                          Severity         Code           Message
purearray-prod-02             error            CRIT_1203      NVMe module 3 predictive failure

Upgrade readiness check: PASSED
All controllers healthy, sufficient free space, no blocking alerts detected.

Upgrade initiated on purearray-prod-01. Phase 1/3: Controller A firmware update (ETA: 12 minutes)
```

!!! warning "Common errors"
    **`purealert: command not found`** — Ensure the Pure Storage CLI toolkit is installed and the PATH includes the installation directory.
    **`Error: Array purearray-prod-01 has unacknowledged critical alerts. Resolve before upgrade.`** — Acknowledge or resolve all critical alerts using `purealert acknowledge <alert_id>` before retrying the upgrade.
    **`Error: Insufficient free space (8.5 TiB required, 6.2 TiB available)`** — Free up additional capacity by removing snapshots or replicating data off-array before attempting the upgrade.
### Space Breakdown

```bash
# Volume-level space (data reduction ratio)
purevol list --space

# Total shared space (snapshots, system overhead)
purearray list --space | awk 'NR==1 || /Total/'
```


```text title="Expected output"
Name                                    Volumes  Snapshots  Data Reduction
prod-db-vol-01                          847.3GB  124.5GB    2.3x
prod-db-vol-02                          612.1GB  89.2GB     1.9x
backup-archive-vol                      2.1TB    445.3GB    3.7x
dev-test-vol                            156.8GB  12.4GB     1.2x
...
Name                  Capacity  Data Reduction  Snapshots  System
array-prod-01         50.0TB    2.1x            8.3TB      2.1TB
Total                 50.0TB    2.1x            8.3TB      2.1TB
```

!!! warning "Common errors"
    **`purevol: command not found`** — Install the Pure Storage CLI tools or source the environment setup script (typically `/opt/purearray/bin/setup.sh`).
    **`Error: Array connection failed - unable to authenticate`** — Verify your Pure array credentials are set in `$PURE_API_TOKEN` or re-authenticate using `purearray login`.
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


```text title="Expected output"
{
  "items": [
    {
      "id": "alert-7f2c9e1a",
      "array_id": "7f2c9e1a-b4d2-4c8f-9e3a-2d1f5c8a9b0e",
      "severity": "error",
      "message": "Controller 0 temperature threshold exceeded",
      "timestamp": "2024-01-15T14:32:18Z",
      "state": "open"
    },
    {
      "id": "alert-3b8f1d2c",
      "array_id": "3b8f1d2c-a9e4-4b7d-8c2f-1a5e9d3c7b6f",
      "severity": "error",
      "message": "Replication lag > 60 seconds on pod-dr-01",
      "timestamp": "2024-01-15T13:47:52Z",
      "state": "open"
    }
  ],
  "more_items_count": 0
}

Severity: error
Array: purearray-prod-01
Message: NVMe SSD wear level critical
Timestamp: 2024-01-15T14:28:10Z
ID: alert-5c3a9f7b

(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Add `-k` flag to skip certificate validation or ensure your CA bundle is current: `curl -sk "https://api.pure1.purestorage.com/..."`
    **`Error: Invalid token or insufficient permissions`** — Verify the `$TOKEN` environment variable is set and the API token has alert read/write scope in Pure1.
    **`purealert: command not found`** — Install or source the Pure Storage CLI tools, or use the full path to the purealert binary if installed in a non-standard location.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Evergreen — Procedures](../procedures/)
- [Evergreen — Scripts](../scripts/)
- [Evergreen — Health Checks](../health-checks/)
