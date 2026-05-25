# CloudIQ REST API Reference

> Part of the [CloudIQ](../../index.md) reference.
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
```

**Token management:**

| Field | Value |
|---|---|
| `grant_type` | Always `client_credentials` |
| `expires_in` | `3600` (1 hour); re-authenticate before expiry |
| Scope | Determined by API key permissions set in portal |

---

## Systems API

```bash
# --- List all monitored systems ---
curl -s -X GET "${BASE}/systems" \
  -H "${AUTH}" | python3 -m json.tool

# List systems with pagination (default page size: 100)
curl -s -X GET "${BASE}/systems?limit=50&offset=0" \
  -H "${AUTH}" | python3 -m json.tool

# Filter systems by type (e.g. POWERFLEX, POWERMAX, UNITY_XT, POWERSTORE)
curl -s -X GET "${BASE}/systems?type=POWERMAX" \
  -H "${AUTH}" | python3 -m json.tool

# Filter systems by a specific site/location tag
curl -s -X GET "${BASE}/systems?location=DC1" \
  -H "${AUTH}" | python3 -m json.tool

# --- Get details for a specific system ---
SYSTEM_ID="<system-id>"   # From the list above; e.g. "PS00xxxxxxx"

curl -s -X GET "${BASE}/systems/${SYSTEM_ID}" \
  -H "${AUTH}" | python3 -m json.tool

# Key fields returned:
#   id               – CloudIQ system identifier
#   model            – Array model string
#   type             – Product type (POWERMAX, UNITY_XT, etc.)
#   health_score     – 0–100 score (100 = fully healthy)
#   health_issue_count – Number of open health issues
#   location         – User-defined location label
#   firmware_version – Current firmware / software version
#   capacity_impact  – Capacity health indicator

# --- Get system health score history ---
curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/health-scores" \
  -H "${AUTH}" | python3 -m json.tool

# Get health issues (root causes of score degradation)
curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/health-issues" \
  -H "${AUTH}" | python3 -m json.tool
```

---

## Alerts API

```bash
# --- List all active alerts ---
curl -s -X GET "${BASE}/alerts" \
  -H "${AUTH}" | python3 -m json.tool

# --- Filter alerts by severity ---
# Severity values: CRITICAL, HIGH, MEDIUM, LOW, INFO
curl -s -X GET "${BASE}/alerts?severity=CRITICAL" \
  -H "${AUTH}" | python3 -m json.tool

curl -s -X GET "${BASE}/alerts?severity=HIGH&severity=CRITICAL" \
  -H "${AUTH}" | python3 -m json.tool

# --- Filter alerts by system ---
curl -s -X GET "${BASE}/alerts?system_id=${SYSTEM_ID}" \
  -H "${AUTH}" | python3 -m json.tool

# --- Filter alerts by state ---
# States: ACTIVE, ACKNOWLEDGED, RESOLVED
curl -s -X GET "${BASE}/alerts?state=ACTIVE" \
  -H "${AUTH}" | python3 -m json.tool

# --- Get details for a specific alert ---
ALERT_ID="<alert-id>"

curl -s -X GET "${BASE}/alerts/${ALERT_ID}" \
  -H "${AUTH}" | python3 -m json.tool

# Key alert fields:
#   id               – Alert identifier
#   severity         – CRITICAL / HIGH / MEDIUM / LOW / INFO
#   state            – ACTIVE / ACKNOWLEDGED / RESOLVED
#   description      – Human-readable alert text
#   resource_name    – Affected resource
#   create_time      – ISO8601 timestamp
#   acknowledge_time – Set when acknowledged

# --- Acknowledge an alert ---
curl -s -X PATCH "${BASE}/alerts/${ALERT_ID}" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d '{"state": "ACKNOWLEDGED"}' | python3 -m json.tool
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
