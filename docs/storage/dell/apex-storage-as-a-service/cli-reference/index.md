# APEX Storage as a Service — API Reference

> Part of the [APEX Storage as a Service](../) reference.

```mermaid
flowchart LR
    API["API"]
    API --> S0["Quick-Reference Table"]
    API --> S1["Dell API Authentication"]
    API --> S2["APEX Systems API"]
    API --> S3["Subscription API"]
    API --> S4["Metrics API"]
    API --> S5["CloudIQ Integration"]
    API --> S6["Notes on APEX Management Boundaries"]
```

---

APEX Storage as a Service has no local CLI. All management is through the **Dell APEX Console** (web portal at console.dell.com) or the **Dell Technologies Cloud API** at `api.dell.com`. The API follows REST conventions and uses OAuth2 client credentials for authentication.

APEX Block Storage surfaces in CloudIQ for performance and health monitoring — see the [CloudIQ API reference](../../cloudiq/cli-reference/) for those endpoints.

> **API base URL**: `https://api.dell.com`  
> **Auth URL**: `https://api.dell.com/auth/oauth/v2/token`  
> **API key management**: console.dell.com → Settings → API Keys  
> **API documentation**: developer.dell.com

---

## Quick-Reference Table

| Operation | Method + Path |
|---|---|
| Get OAuth2 access token | `POST /auth/oauth/v2/token` |
| List APEX Block systems | `GET /apex/block/v1/systems` |
| Get APEX system details | `GET /apex/block/v1/systems/{id}` |
| Get system capacity | `GET /apex/block/v1/systems/{id}/capacity` |
| Get system health | `GET /apex/block/v1/systems/{id}/health` |
| List subscriptions | `GET /apex/subscriptions/v1` |
| Get subscription details | `GET /apex/subscriptions/v1/{id}` |
| Get subscription consumption | `GET /apex/subscriptions/v1/{id}/consumption` |
| Get performance metrics | `GET /apex/block/v1/systems/{id}/metrics` |
| List storage volumes | `GET /apex/block/v1/systems/{id}/volumes` |

---

## Dell API Authentication

APEX uses OAuth2 client credentials. Generate a `client_id` and `client_secret` in the APEX Console under **Settings → API Keys**. Access tokens expire after 3600 seconds.

```bash
CLIENT_ID="<your_client_id>"
CLIENT_SECRET="<your_client_secret>"
TOKEN_URL="https://api.dell.com/auth/oauth/v2/token"

# --- Get access token ---
RESPONSE=$(curl -s -X POST "${TOKEN_URL}" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials" \
  -d "client_id=${CLIENT_ID}" \
  -d "client_secret=${CLIENT_SECRET}")

TOKEN=$(echo "${RESPONSE}" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
EXPIRES_IN=$(echo "${RESPONSE}" | python3 -c "import sys,json; print(json.load(sys.stdin)['expires_in'])")

echo "Token acquired. Expires in ${EXPIRES_IN}s"

# --- Set convenience variables for subsequent calls ---
AUTH="Authorization: Bearer ${TOKEN}"
BASE="https://api.dell.com"
```

**Token management:**

| Field | Value |
|---|---|
| `grant_type` | Always `client_credentials` |
| `expires_in` | `3600` — re-authenticate before expiry in scripts |
| `token_type` | `Bearer` |
| Scope | Determined by API key permissions in APEX Console |

---

## APEX Systems API

```bash
# --- List all APEX Block Storage systems ---
curl -s -X GET "${BASE}/apex/block/v1/systems" \
  -H "${AUTH}" | python3 -m json.tool

# List with pagination
curl -s -X GET "${BASE}/apex/block/v1/systems?limit=50&offset=0" \
  -H "${AUTH}" | python3 -m json.tool

# Filter by location / site
curl -s -X GET "${BASE}/apex/block/v1/systems?location=DC1" \
  -H "${AUTH}" | python3 -m json.tool

# --- Get details for a specific APEX system ---
SYSTEM_ID="<system-id>"    # From list response

curl -s -X GET "${BASE}/apex/block/v1/systems/${SYSTEM_ID}" \
  -H "${AUTH}" | python3 -m json.tool

# Key system fields:
#   id                  – APEX system identifier
#   name                – Friendly name (set in APEX Console)
#   model               – Hardware model (e.g. "PowerStore 3200T")
#   type                – BLOCK / FILE
#   location            – Data centre / site label
#   status              – ACTIVE / PROVISIONING / DEGRADED / OFFLINE
#   software_version    – Current firmware/OS version
#   health_status       – GOOD / WARNING / CRITICAL

# --- Get system health ---
curl -s -X GET "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/health" \
  -H "${AUTH}" | python3 -m json.tool

# Health response fields:
#   health_score        – 0–100 (100 = fully healthy)
#   health_issues[]     – Array of active health concerns
#   last_updated        – ISO8601 timestamp

# --- Get capacity for a system ---
curl -s -X GET "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/capacity" \
  -H "${AUTH}" | python3 -m json.tool

# Capacity fields:
#   committed_capacity_tb    – Contracted committed capacity
#   burst_capacity_tb        – Available burst ceiling
#   used_capacity_tb         – Currently consumed
#   available_capacity_tb    – committed + burst - used
#   percent_used             – Utilisation percentage

# --- List storage volumes on a system ---
curl -s -X GET "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/volumes" \
  -H "${AUTH}" | python3 -m json.tool

# Get a specific volume
VOLUME_ID="<volume-id>"
curl -s -X GET "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/volumes/${VOLUME_ID}" \
  -H "${AUTH}" | python3 -m json.tool
```

---

## Subscription API

APEX subscriptions define contracted capacity, term, service tier, and billing model. Use these endpoints to track contracted vs consumed figures.

```bash
# --- List all APEX subscriptions ---
curl -s -X GET "${BASE}/apex/subscriptions/v1" \
  -H "${AUTH}" | python3 -m json.tool

# Filter by product type
curl -s -X GET "${BASE}/apex/subscriptions/v1?product_type=BLOCK" \
  -H "${AUTH}" | python3 -m json.tool

# Filter by status
curl -s -X GET "${BASE}/apex/subscriptions/v1?status=ACTIVE" \
  -H "${AUTH}" | python3 -m json.tool

# --- Get details for a specific subscription ---
SUB_ID="<subscription-id>"

curl -s -X GET "${BASE}/apex/subscriptions/v1/${SUB_ID}" \
  -H "${AUTH}" | python3 -m json.tool

# Key subscription fields:
#   id                      – Subscription identifier
#   product_type            – BLOCK / FILE / OBJECT
#   service_tier            – e.g. "Performance", "Capacity"
#   committed_capacity_tb   – Contracted base capacity (TB)
#   burst_capacity_tb       – Burst ceiling (TB above committed)
#   contract_start_date     – ISO8601
#   contract_end_date       – ISO8601
#   auto_renewal            – true/false
#   status                  – ACTIVE / EXPIRED / SUSPENDED

# --- Get subscription consumption (contracted vs consumed) ---
curl -s -X GET "${BASE}/apex/subscriptions/v1/${SUB_ID}/consumption" \
  -H "${AUTH}" | python3 -m json.tool

# Consumption fields:
#   committed_capacity_tb    – Contracted TB
#   burst_capacity_tb        – Burst ceiling TB
#   current_usage_tb         – TB currently in use
#   peak_usage_tb            – Peak TB used this billing period
#   burst_usage_tb           – TB used above committed (billed at burst rate)
#   billing_period_start     – ISO8601 start of current billing month
#   billing_period_end       – ISO8601 end of current billing month

# --- Check if burst is in use ---
curl -s -X GET "${BASE}/apex/subscriptions/v1/${SUB_ID}/consumption" \
  -H "${AUTH}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
committed = data.get('committed_capacity_tb', 0)
current   = data.get('current_usage_tb', 0)
burst     = data.get('burst_usage_tb', 0)
ceiling   = data.get('burst_capacity_tb', 0)
print(f'Committed: {committed:.1f} TB  Used: {current:.1f} TB  Burst: {burst:.1f} TB  Ceiling: {ceiling:.1f} TB')
if burst > 0:
    pct = (burst/ceiling*100) if ceiling else 0
    print(f'BURST ACTIVE: {burst:.1f} TB at {pct:.1f}% of burst ceiling')
"
```

---

## Metrics API

```bash
# --- Get available metric types for a system ---
curl -s -X GET "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/metrics/types" \
  -H "${AUTH}" | python3 -m json.tool

# Common metric keys:
#   iops              – Total IOPS (read + write)
#   read_iops         – Read IOPS
#   write_iops        – Write IOPS
#   latency_ms        – Average latency in milliseconds
#   throughput_mb     – MB/s (read + write combined)
#   read_throughput_mb
#   write_throughput_mb
#   cpu_utilization   – Controller CPU %

# --- Set time range helpers ---
END=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
START_1H=$(date -u -v-1H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null \
         || date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%SZ")
START_24H=$(date -u -v-24H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null \
          || date -u -d "24 hours ago" +"%Y-%m-%dT%H:%M:%SZ")
START_30D=$(date -u -v-30d +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null \
          || date -u -d "30 days ago" +"%Y-%m-%dT%H:%M:%SZ")

# --- Get performance metrics (last 24 hours, hourly granularity) ---
curl -s -X POST "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/metrics" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d "{
    \"metrics\":     [\"iops\", \"latency_ms\", \"throughput_mb\"],
    \"start_time\":  \"${START_24H}\",
    \"end_time\":    \"${END}\",
    \"granularity\": \"HOURLY\"
  }" | python3 -m json.tool

# --- Get last-known (real-time) metrics snapshot ---
curl -s -X GET "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/metrics/current" \
  -H "${AUTH}" | python3 -m json.tool

# --- 30-day performance trend (daily granularity) ---
curl -s -X POST "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/metrics" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d "{
    \"metrics\":     [\"iops\", \"latency_ms\"],
    \"start_time\":  \"${START_30D}\",
    \"end_time\":    \"${END}\",
    \"granularity\": \"DAILY\"
  }" | python3 -m json.tool

# --- Volume-level performance metrics ---
curl -s -X POST \
  "${BASE}/apex/block/v1/systems/${SYSTEM_ID}/volumes/${VOLUME_ID}/metrics" \
  -H "${AUTH}" \
  -H "Content-Type: application/json" \
  -d "{
    \"metrics\":     [\"iops\", \"latency_ms\"],
    \"start_time\":  \"${START_24H}\",
    \"end_time\":    \"${END}\",
    \"granularity\": \"HOURLY\"
  }" | python3 -m json.tool
```

---

## CloudIQ Integration

APEX Block Storage systems are automatically ingested into CloudIQ for health scoring, alerting, and capacity forecasting. Use the CloudIQ API to monitor APEX systems alongside other Dell products.

```bash
# CloudIQ base URL and auth are separate — see CloudIQ API Reference
CIQ_TOKEN="<cloudiq_access_token>"        # See CloudIQ auth section
CIQ_BASE="https://cloudiq.apis.dell.com/rest/v1"

# --- List APEX systems visible in CloudIQ ---
curl -s -X GET "${CIQ_BASE}/systems?type=POWERSTORE" \
  -H "Authorization: Bearer ${CIQ_TOKEN}" | python3 -m json.tool

# --- Get health score for an APEX system in CloudIQ ---
APEX_CIQ_ID="<cloudiq-system-id>"

curl -s -X GET "${CIQ_BASE}/systems/${APEX_CIQ_ID}" \
  -H "Authorization: Bearer ${CIQ_TOKEN}" | python3 -m json.tool

# --- Get CloudIQ alerts for APEX systems ---
curl -s -X GET "${CIQ_BASE}/alerts?system_id=${APEX_CIQ_ID}&state=ACTIVE" \
  -H "Authorization: Bearer ${CIQ_TOKEN}" | python3 -m json.tool

# --- Capacity forecast via CloudIQ ---
curl -s -X GET "${CIQ_BASE}/systems/${APEX_CIQ_ID}/capacity/forecast?days=90" \
  -H "Authorization: Bearer ${CIQ_TOKEN}" | python3 -m json.tool
```

> APEX systems appear in CloudIQ with the model of the underlying hardware (e.g. `PowerStore 3200T`). Filter by type `POWERSTORE`, `POWERMAX`, or `UNITY_XT` depending on which APEX SKU is deployed. See the [CloudIQ CLI Reference](../../cloudiq/cli-reference/) for full CloudIQ API coverage.

---

## Notes on APEX Management Boundaries

| Task | Interface |
|---|---|
| Order / provision new APEX system | APEX Console (console.dell.com) |
| Resize contracted capacity | APEX Console → Subscription → Modify |
| Create / delete volumes | APEX Console or APEX Block API |
| Monitor health and alerts | CloudIQ (console.dell.com/cloudiq) |
| View billing / consumption | APEX Console → Billing or Subscription API |
| Performance metrics | APEX Block API or CloudIQ API |
| Firmware upgrades | Dell-managed (SaaS — no customer action required) |
| Hardware replacement | Dell field service — no customer CLI |
