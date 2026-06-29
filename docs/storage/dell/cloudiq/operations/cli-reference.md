---
tags:
  - dell
  - operations
---
# Dell CloudIQ CLI Reference
![Dell CloudIQ CLI Reference](../../../../assets/storage-dell-cloudiq-operations-cli-reference.svg)

```bash
CLIENT_ID="<your_client_id>"
CLIENT_SECRET="<your_client_secret>"
TOKEN_URL="https://cloudiq.apis.dell.com/auth/oauth/v2/token"

# --- Get access token ---
TOKEN=$(curl -s -X POST "${TOKEN_URL}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

echo "Token: ${TOKEN:0:40}..."   # Print first 40 chars to confirm success

# --- Reusable header for all subsequent calls ---
AUTH="Authorization: Bearer ${TOKEN}"
BASE="https://cloudiq.apis.dell.com/rest/v1"
```


```text title="Expected output"
Token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJzdWIiOi...
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: cloudiq.apis.dell.com`** — Verify network connectivity and DNS resolution; check that the CloudIQ API endpoint is accessible from your environment.
    **`json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)`** — Confirm CLIENT_ID and CLIENT_SECRET are correct and valid; check the token endpoint response with `curl -v` to see the actual error message from the API.
    **`curl: (35) error:1400D102:SSL routines:SSL_CTX_use_certificate:unsupported certificate type`** — Ensure your system's CA certificates are up-to-date with `update-ca-certificates` or equivalent for your OS.
```bash
# --- Current capacity utilisation for a system ---
curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/capacity" \
  -H "${AUTH}" | python3 -m json.tool

# Key capacity fields:
#   total_subscribed_capacity_gb – Logical size allocated to hosts
#   total_used_capacity_gb       – Physical data written
#   total_physical_capacity_gb   – Raw usable capacity
#   percent_used                 – Physical used %
#   days_to_full                 – Forecast days until full (based on trend)
#   forecast_confidence          – LOW / MEDIUM / HIGH

# --- Capacity forecast ---
curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/capacity/forecast" \
  -H "${AUTH}" | python3 -m json.tool

# Forecast with custom horizon (30 / 60 / 90 days)
curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/capacity/forecast?days=90" \
  -H "${AUTH}" | python3 -m json.tool
```

```text title="Expected output"
{
  "id": "sys-4a7c9e2f",
  "total_subscribed_capacity_gb": 524288,
  "total_used_capacity_gb": 387421,
  "total_physical_capacity_gb": 512000,
  "percent_used": 75.66,
  "days_to_full": 28,
  "forecast_confidence": "HIGH",
  "last_update": "2024-01-15T14:32:18Z"
}
{
  "forecast_points": [
    {
      "timestamp": "2024-02-14T14:32:18Z",
      "projected_used_gb": 412856,
      "percent_used": 80.62
    },
    {
      "timestamp": "2024-03-16T14:32:18Z",
      "projected_used_gb": 438291,
      "percent_used": 85.54
    },
    {
      "timestamp": "2024-04-15T14:32:18Z",
      "projected_used_gb": 463725,
      "percent_used": 90.47
    }
  ],
  "forecast_confidence": "HIGH",
  "trend_growth_gb_per_day": 812.5
}
{
  "forecast_points": [
    {
      "timestamp": "2024-04-15T14:32:18Z",
      "projected_used_gb": 463725,
      "percent_used": 90.47
    }
  ],
  "forecast_confidence": "MEDIUM",
  "trend_growth_gb_per_day": 812.5,
  "days_horizon": 90
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to api.cloudiq.dell.com port 443: Connection refused`** — Verify BASE URL is correct and CloudIQ API endpoint is reachable; check firewall rules and VPN connectivity.
    **`{"error": "Unauthorized", "code": 401}`** — Ensure AUTH header contains valid bearer token and hasn't expired; regenerate credentials in CloudIQ console if needed.
    **`jq: parse error: Invalid JSON at line 1`** — Confirm the API response is valid JSON by testing with `curl -s ... | head -c 200` to inspect raw output; check for HTML error pages instead of JSON.
```bash
# --- Get available performance metric types for a system ---
curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/metrics/query" \
  -H "${AUTH}" | python3 -m json.tool

# --- Query performance metrics ---
# Common metric keys: iops, throughput_mb, latency_ms, bandwidth_mb
curl -s -X POST "${BASE}/systems/${SYSTEM_ID}/metrics/query" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d "{
    \"metrics\": [\"iops\", \"latency_ms\", \"throughput_mb\"],
    \"start_time\": \"${START}\",
    \"end_time\": \"${END}\",
    \"granularity\": \"HOURLY\"
  }" | python3 -m json.tool

# --- Get real-time (latest) metrics ---
curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/metrics/last" \
  -H "${AUTH}" | python3 -m json.tool
```

```text title="Expected output"
{
  "metrics": [
    "iops",
    "throughput_mb",
    "latency_ms",
    "bandwidth_mb",
    "cache_hit_ratio",
    "read_write_ratio"
  ]
}
{
  "query_id": "q-7f2a9c1e-4b3d-11ed-9e2f-0242ac110002",
  "system_id": "APM00213400001",
  "metrics": [
    {
      "metric_type": "iops",
      "data_points": [
        {"timestamp": "2024-01-15T08:00:00Z", "value": 4521.3},
        {"timestamp": "2024-01-15T09:00:00Z", "value": 5847.2},
        {"timestamp": "2024-01-15T10:00:00Z", "value": 6234.1}
      ]
    },
    {
      "metric_type": "latency_ms",
      "data_points": [
        {"timestamp": "2024-01-15T08:00:00Z", "value": 2.14},
        {"timestamp": "2024-01-15T09:00:00Z", "value": 2.89},
        {"timestamp": "2024-01-15T10:00:00Z", "value": 3.12}
      ]
    }
  ],
  "status": "completed"
}
{
  "timestamp": "2024-01-15T10:47:32Z",
  "system_id": "APM00213400001",
  "iops": 5923.7,
  "throughput_mb": 1847.3,
  "latency_ms": 2.67,
  "bandwidth_mb": 2156.4,
  "cache_hit_ratio": 0.847
}
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to cloudiq.example.com port 443: Connection refused`** — Verify BASE URL is correct and CloudIQ API endpoint is accessible; check firewall rules and service status.
    **`{"error": "Unauthorized", "code": 401}`** — Ensure AUTH header contains valid API token and hasn't expired; regenerate token in CloudIQ console if needed.
    **`{"error": "Invalid metric type", "code": 400}`** — Verify metric names match available types from the first query (iops, throughput_mb, latency_ms, etc.) and check JSON syntax for typos.
```bash
# --- List all existing tags ---
curl -s -X GET "${BASE}/tags" \
  -H "${AUTH}" | python3 -m json.tool

# --- Create a new tag ---
curl -s -X POST "${BASE}/tags" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "env:production",
    "description": "Production environment systems"
  }' | python3 -m json.tool

TAG_ID="<tag-id>"   # Returned from the create response

# --- Assign a tag to a system ---
curl -s -X POST "${BASE}/systems/${SYSTEM_ID}/tags" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d "{\"tag_ids\": [\"${TAG_ID}\"]}" | python3 -m json.tool

# --- List tags assigned to a system ---
curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/tags" \
  -H "${AUTH}" | python3 -m json.tool

# --- Remove a tag from a system ---
curl -s -X DELETE "${BASE}/systems/${SYSTEM_ID}/tags/${TAG_ID}" \
  -H "${AUTH}"

# --- Filter systems by tag ---
curl -s -X GET "${BASE}/systems?tag_id=${TAG_ID}" \
  -H "${AUTH}" | python3 -m json.tool

# --- Delete a tag (removes it globally) ---
curl -s -X DELETE "${BASE}/tags/${TAG_ID}" \
  -H "${AUTH}"
```


```text title="Expected output"
[
  {
    "id": "tag-5f8c2a1b-9e4d-47c3-b2f1-6d3e8a9c1f5a",
    "name": "env:production",
    "description": "Production environment systems",
    "created_at": "2024-01-15T10:32:18Z",
    "system_count": 12
  },
  {
    "id": "tag-7a3f1c9d-2e5b-41a8-9f6c-4b2d8e1a3c7f",
    "name": "tier:critical",
    "description": "Critical tier systems",
    "created_at": "2024-01-14T14:22:05Z",
    "system_count": 8
  }
]
{
  "id": "tag-5f8c2a1b-9e4d-47c3-b2f1-6d3e8a9c1f5a",
  "name": "env:production",
  "description": "Production environment systems",
  "created_at": "2024-01-15T10:32:18Z"
}
{
  "system_id": "SYS-EMC-001",
  "tags_assigned": 1,
  "status": "success"
}
[
  {
    "id": "tag-5f8c2a1b-9e4d-47c3-b2f1-6d3e8a9c1f5a",
    "name": "env:production",
    "assigned_at": "2024-01-15T10:33:42Z"
  }
]
(no output — command completes silently)
{
  "systems": [
    {
      "id": "SYS-EMC-001",
      "name": "dell-unity-prod-01",
      "model": "Unity 550F",
      "ip_address": "192.168.1.45"
    }
  ],
  "total_count": 1
}
(no output — command completes silently)
```

!!! warning "Common errors"
    **`curl: (7) Failed to connect to api.cloudiq.dell.com port 443: Connection refused`** — Verify BASE URL is correct and CloudIQ API endpoint is accessible; check network connectivity and firewall rules.
    **`{"error": "Unauthorized", "code": 401}`** — Ensure AUTH header contains valid API token and has not expired; regenerate credentials in CloudIQ console if needed.
    **`{"error": "Tag not found", "code": 404}`** — Confirm TAG_ID variable is set correctly from the create response and the tag has not already been deleted.
## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Cloudiq — Procedures](../procedures/)
- [Cloudiq — Scripts](../scripts/)
- [Cloudiq — Health Checks](../health-checks/)
