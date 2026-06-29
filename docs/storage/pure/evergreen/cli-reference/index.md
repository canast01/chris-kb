---
tags:
  - pure
---
# Pure Evergreen CLI Reference

<div class="kb-summary">
Pure Evergreen CLI Reference reference covering Overview, Pure1 REST API, FlashArray CLI (per-array), Alerts.

*Applies to: Evergreen*
</div>

![Pure Evergreen CLI Reference — Diagram](../../../../assets/storage-pure-evergreen-cli-reference-diagram.svg)

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


```text title="Expected output"
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJwdXJlMTphcGlrZXk6YWJjMTIzIiwic3ViIjoicHVyZTphcGlrZXk6YWJjMTIzIiwiaWF0IjoxNzA5MzE2ODAwLCJleHAiOjE3MDkzMjA0MDB9.aBcD1eFgHiJkLmNoPqRsTuVwXyZ2a3b4c5d6e7f8g9h0i1j2k3l4m5n6o7p8q9r0s1t2u3v4w5x6y7z8
```

!!! warning "Common errors"
    **`ModuleNotFoundError: No module named 'pypureclient'`** — Install the required package with `pip install py-pure-client`.
    **`FileNotFoundError: [Errno 2] No such file or directory: '/path/to/private.pem'`** — Verify the private key file path is correct and the file exists at the specified location.
    **`ValueError: Invalid app_id format`** — Ensure the app_id follows the format `pure1:apikey:<your_api_key>` with valid credentials from your Pure1 account.
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


```text title="Expected output"
{
  "items": [
    {
      "id": "5b4c8e9a-1234-5678-90ab-cdef12345678",
      "name": "prod-array-01",
      "model": "FlashArray//X70R4",
      "version": "6.4.2",
      "status": "healthy"
    },
    {
      "id": "7f2d1c3b-abcd-ef01-2345-6789abcdef01",
      "name": "dr-array-02",
      "model": "FlashArray//X20R2",
      "version": "6.3.8",
      "status": "healthy"
    }
  ],
  "continuation_token": null
}

prod-array-01                 model=FlashArray//X70R4      version=6.4.2
dr-array-02                   model=FlashArray//X20R2      version=6.3.8
backup-array-03               model=FlashArray//X50R3      version=6.2.5
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.pure1.purestorage.com`** — Verify network connectivity and DNS resolution; check if your firewall allows HTTPS egress to Pure1 API endpoints.
    **`{"error_code":"401","message":"Unauthorized"}`** — Ensure the `$TOKEN` environment variable is set with a valid Pure1 API token and has not expired.
    **`jq: parse error: Invalid UTF-8 in string`** — Verify the API response is valid JSON by testing with `curl -s <url> | head -c 500` to inspect raw output.
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


```text title="Expected output"
{
  "continuation_token": null,
  "items": [
    {
      "id": "fleet-abc123",
      "name": "production-fleet",
      "organization_id": "org-789xyz",
      "created_at": "2023-06-15T10:22:44Z",
      "updated_at": "2024-01-20T14:55:12Z"
    },
    {
      "id": "fleet-def456",
      "name": "staging-fleet",
      "organization_id": "org-789xyz",
      "created_at": "2023-08-02T09:11:30Z",
      "updated_at": "2024-01-19T16:33:45Z"
    }
  ]
}
{
  "continuation_token": null,
  "items": [
    {
      "id": "array-001",
      "name": "fa-m70-prod-01",
      "fleet": {
        "id": "fleet-abc123"
      },
      "model": "FlashArray//M70",
      "serial": "5b8c9e2f1a4d",
      "status": "healthy"
    },
    {
      "id": "array-002",
      "name": "fa-m70-prod-02",
      "fleet": {
        "id": "fleet-abc123"
      },
      "model": "FlashArray//M70",
      "serial": "7c3f2e9b5a1d",
      "status": "healthy"
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.pure1.purestorage.com`** — Verify network connectivity and DNS resolution; check firewall rules allowing outbound HTTPS to Pure1 API endpoints.
    **`{"error_code":"INVALID_TOKEN","message":"Invalid or expired authentication token"}`** — Regenerate the API token in Pure1 console and ensure `$TOKEN` variable is set correctly with `export TOKEN="your-token-here"`.
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Update your CA certificate bundle or use `curl -k` flag (not recommended for production); verify your system's certificate store is current.
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


```text title="Expected output"
{
  "items": [
    {
      "id": "sub-abc123def456",
      "name": "Evergreen//One-FlashArray",
      "status": "active",
      "expiration_date": "2025-12-31T23:59:59Z",
      "committed_capacity_gb": 102400,
      "consumed_capacity_gb": 87654
    },
    {
      "id": "sub-xyz789",
      "name": "Evergreen//Forever-FlashBlade",
      "status": "active",
      "expiration_date": "2099-12-31T23:59:59Z",
      "committed_capacity_gb": 51200,
      "consumed_capacity_gb": 12288
    }
  ],
  "pagination": {
    "offset": 0,
    "limit": 100,
    "total": 2
  }
}
Evergreen//One-FlashArray      status=active        expires=2025-12-31T23:59:59Z
Evergreen//Forever-FlashBlade  status=active        expires=2099-12-31T23:59:59Z

{
  "id": "sub-xyz789",
  "name": "Evergreen//Forever-FlashBlade",
  "status": "active",
  "expiration_date": "2099-12-31T23:59:59Z",
  "committed_capacity_gb": 51200,
  "consumed_capacity_gb": 12288,
  "renewal_date": "2024-01-15T00:00:00Z"
}
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.pure1.purestorage.com`** — Verify network connectivity and DNS resolution; check if your firewall allows outbound HTTPS to Pure1 API endpoints.
    **`{"error_code":"401","message":"Unauthorized"}`** — Ensure the `$TOKEN` environment variable is set with a valid Pure1 API token and has not expired.
    **`jq: command not found`** — Install `python3-json` or use `python3 -m json.tool` as shown in the example (already included in the script).
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


```text title="Expected output"
array_bandwidth_in
array_bandwidth_out
array_data_reduction
array_empty_blocks
array_iops
array_latency
array_queue_depth
array_replication_bandwidth_in
array_replication_bandwidth_out
array_total_capacity
array_used_capacity
...

{
  "items": [
    {
      "name": "array_total_capacity",
      "resource_id": "array-id-here",
      "time": 1704067200000,
      "value": 109951162777600
    },
    {
      "name": "array_used_capacity",
      "resource_id": "array-id-here",
      "time": 1704067200000,
      "value": 54975581388800
    },
    {
      "name": "array_total_capacity",
      "resource_id": "array-id-here",
      "time": 1704070800000,
      "value": 109951162777600
    },
    {
      "name": "array_used_capacity",
      "resource_id": "array-id-here",
      "time": 1704070800000,
      "value": 55025581388800
    }
  ]
}
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.pure1.purestorage.com`** — Verify network connectivity and DNS resolution; check if the Pure1 API endpoint is accessible from your network.
    **`{"error_code":"INVALID_TOKEN","message":"Invalid or expired bearer token"}`** — Regenerate a valid API token in Pure1 and export it to `$TOKEN` before running the command.
    **`jq: command not found`** — Install `jq` package or use `python3 -m json.tool` as shown in the example to parse JSON output.
---

## FlashArray CLI (per-array)

Connect via SSH to the array management IP. User is typically `pureuser`.

```bash
ssh pureuser@flasharray01.example.com
```


```text title="Expected output"
The authenticity of host 'flasharray01.example.com (192.0.2.45)' can't be established.
ECDSA key fingerprint is SHA256:aBcD1EfGhIjKlMnOpQrStUvWxYz2A3b4C5d6E7f8G9h.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added 'flasharray01.example.com,192.0.2.45' (ECDSA) to the list of known_hosts.
Password:
Connected to flasharray01.example.com
pureuser@flasharray01>
```

!!! warning "Common errors"
    **`ssh: Could not resolve hostname flasharray01.example.com: Name or service not known`** — Verify the hostname is correct and resolvable via DNS or add an entry to /etc/hosts.
    **`Permission denied (publickey,password).`** — Confirm the pureuser account exists on the array and the password is correct, or configure SSH key authentication.
    **`ssh: connect to host flasharray01.example.com port 22: Connection timed out`** — Check network connectivity to the array and verify the SSH service is running on port 22.
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
Name                          Version          Serial
pure-fa-m70-prod-01           6.4.5.1234       5678ab9cdef01234
pure-fa-m70-prod-02           6.4.5.1234       5678ab9cdef01235

Name                          Capacity(TiB)    Used(TiB)      Free(TiB)
pure-fa-m70-prod-01           100.0            67.3           32.7
pure-fa-m70-prod-02           100.0            71.2           28.8

AlertID                       Severity         Component      Timestamp
alert-5f8e2c1a-9d4b-4e2f      warning          controller     2024-01-15T14:32:18Z
alert-7g3h9k2m-1p5q-6r7s      critical         disk           2024-01-15T13:45:22Z
alert-2b4c8d9e-3f6g-7h8i      warning          network        2024-01-15T12:18:05Z

AlertID                       Severity         Message
alert-9x2y3z4a-5b6c-7d8e      error            Drive predictive failure on slot 4
alert-1m2n3o4p-5q6r-7s8t      error            Controller temperature threshold exceeded

Upgrade readiness check: PASSED
- All controllers healthy
- No active alerts blocking upgrade
- Sufficient free space available
- Estimated downtime: 0 minutes (NDU capable)

Upgrade execution started
Upgrade progress: 100%
Array pure-fa-m70-prod-01 upgraded to 6.4.6.1245
Array pure-fa-m70-prod-02 upgraded to 6.4.6.1245
Non-disruptive upgrade completed successfully
```

!!! warning "Common errors"
    **`Error: Unable to connect to array management interface at <ip>:443`** — Verify array hostname/IP is reachable and management services are running with `ping` and `ssh` tests.
    **`Error: Upgrade check failed - Active alerts prevent upgrade`** — Acknowledge or resolve all critical and error-level alerts before attempting upgrade with `purealert acknowledge <alert-id>`.
    **`Error: Insufficient free space for upgrade (requires 15 TiB, available 8 TiB)`** — Free up array capacity by deleting snapshots or data, or add additional storage before retrying upgrade.
### Space Breakdown

```bash
# Volume-level space (data reduction ratio)
purevol list --space

# Total shared space (snapshots, system overhead)
purearray list --space | awk 'NR==1 || /Total/'
```


```text title="Expected output"
Name                          Volumes  Data Reduction
vol-prod-db-01                    1        2.5x
vol-backup-archive                1        1.8x
vol-dev-test-01                   1        3.2x
vol-analytics-02                  1        2.1x
vol-cache-layer                   1        4.7x
...
Name                          Capacity  Data Reduction  Total Reduction
purearray-01                   100.0TB        2.3x           2.8x
Total                          100.0TB        2.3x           2.8x
```

!!! warning "Common errors"
    **`purevol: command not found`** — Ensure the Pure Storage CLI is installed and the `purearray` package is in your PATH, or source the Pure environment setup script.
    **`Error: Array not reachable at <ip>`** — Verify network connectivity to the array and that your `PURE_ARRAY` environment variable or CLI credentials are correctly configured.
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
      "id": "alert-7f3c9e2a",
      "array_id": "7f3c9e2a-1b4d-4e8f-9c2a-5d6e7f8g9h0i",
      "severity": "error",
      "message": "NVMe drive failure detected on shelf 2, slot 14",
      "created": "2024-01-15T09:23:47Z",
      "acknowledged": false
    },
    {
      "id": "alert-8g4d0f3b",
      "array_id": "8g4d0f3b-2c5e-5f9g-0d3b-6e7f8g9h0i1j",
      "severity": "error",
      "message": "Replication lag exceeded threshold on pod-us-west",
      "created": "2024-01-15T08:15:22Z",
      "acknowledged": false
    }
  ],
  "total_items": 2
}

Severity: error
Array: purearray-prod-01
Message: NVMe drive failure detected on shelf 2, slot 14
ID: alert-7f3c9e2a
Created: 2024-01-15T09:23:47Z

Severity: error
Array: purearray-prod-02
Message: Replication lag exceeded threshold on pod-us-west
ID: alert-8g4d0f3b
Created: 2024-01-15T08:15:22Z

Alert 123 acknowledged successfully.
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.pure1.purestorage.com`** — Verify network connectivity and DNS resolution, or check if the Pure1 API endpoint is accessible from your network.
    **`Error: Invalid token or authentication failed`** — Ensure the `$TOKEN` environment variable is set to a valid Pure1 API token with appropriate permissions.
    **`Error: Alert ID 123 not found`** — Verify the alert ID exists by running `purealert list` first and use the correct ID from the output.
## See also

- [Evergreen — Overview](../../)
