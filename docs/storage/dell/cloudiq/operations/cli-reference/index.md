# CloudIQ REST API Reference


<div class="kb-summary">
> Part of the [CloudIQ](../../index.md) reference.
</div>

---

CloudIQ has no local CLI. All programmatic interaction is via the **CloudIQ REST API** at `https://cloudiq.apis.dell.com`. Authentication uses the OAuth2 **client credentials** flow. API keys (client ID + secret) are generated in the CloudIQ web portal under **Settings → API Keys**.

> **Base URL**: `https://cloudiq.apis.dell.com`  
> **Token URL**: `https://cloudiq.apis.dell.com/auth/oauth/v2/token`  
> **Docs**: https://developer.dell.com/apis/4588/versions/6.0/docs

---

## Quick-Reference Command Table

| Operation | Method + Path |
|---|---|
| Get OAuth2 token | `POST /auth/oauth/v2/token` |
| List all systems | `GET /rest/v1/systems` |
| Get system health | `GET /rest/v1/systems/{id}` |
| List active alerts | `GET /rest/v1/alerts` |
| Filter alerts by severity | `GET /rest/v1/alerts?severity=HIGH` |
| Acknowledge an alert | `PATCH /rest/v1/alerts/{id}` |
| Get capacity forecast | `GET /rest/v1/systems/{id}/capacity` |
| Get performance metrics | `GET /rest/v1/systems/{id}/metrics` |
| List tags | `GET /rest/v1/tags` |
| Assign tag to system | `POST /rest/v1/systems/{id}/tags` |

---

## Authentication

CloudIQ uses OAuth2 client credentials. The access token is a Bearer JWT valid for 3600 seconds.

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
```text
┌───────────────────────────────────── Dell CloudIQ CLI Reference ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              CloudIQ management via SCG CLI (SSH to SCG VM) and CloudIQ REST API              │   │
│   │             SCG CLI: system status, device list, connectivity test, log collection            │   │
│   │            CloudIQ REST API: retrieve assets, health scores, metrics, alert history           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          SCG Status         │  │       SCG Device Mgmt       │  │         CloudIQ API         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │          scg status         │  │       scg device list       │  │        GET /v1/assets       │   │
│   │       scg connectivity      │  │        scg device add       │  │        GET /v1/health       │   │
│   │       scg log collect       │  │      scg device remove      │  │       GET /v1/metrics       │   │
│   │         scg version         │  │       scg device test       │  │        GET /v1/alerts       │   │
│   │         scg upgrade         │  │       scg device show       │  │       POST /v1/reports      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Common workflows: check status → list devices → test connectivity → collect logs                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        scg status                — show SCG service state, version, registered devices        │   │
│   │             scg connectivity --test   — verify outbound HTTPS to CloudIQ endpoints            │   │
│   │         scg device list           — show all registered storage systems and poll state        │   │
│   │            scg log collect           — bundle SCG logs for support; output to /tmp            │   │
│   │           curl -H "Authorization: Bearer $TOKEN" https://cloudiq.dell.com/v1/assets           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SCG CLI      = SSH to SCG VM (admin user); menu-driven or direct scg commands                      │
│    Bearer token = OAuth 2.0 token from CloudIQ API key; passed in Authorization header                │
│    scg device test= Validates REST API credentials and connectivity for a registered system           │
│    /v1/assets   = CloudIQ REST endpoint: returns all storage assets with attributes                   │
│    /v1/health   = CloudIQ REST endpoint: returns health scores for all systems                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Capacity API

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

---

## Performance API

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

---

## Tags API

Tags in CloudIQ allow grouping and filtering systems by environment, owner, location, or any custom label.

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
