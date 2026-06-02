# Dell AIOps CLI Reference


<div class="kb-summary">
Dell AIOps does not provide a dedicated CLI tool. All interaction is via the CloudIQ web portal or CloudIQ REST API. This page documents the key REST API endpoints used for AIOps operations.
</div>

## Authentication

All API requests require an OAuth2 Bearer token obtained via the client credentials flow.

```bash
# Obtain access token
curl -s -X POST "https://api.cloudiq.dell.com/auth/oauth/v2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}" \
  | jq -r '.access_token'
```
```text
┌───────────────────────────────── Dell AIOps — CLI and API Reference ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     AIOps REST API — Base URL: https://<aiops-host>/api/v1                    │   │
│   │                          Auth: POST /api/v1/auth/login → Bearer token                         │   │
│   │                  Alerts: GET /api/v1/alerts?status=open — list active alerts                  │   │
│   │                  Systems: GET /api/v1/systems — list monitored infrastructure                 │   │
│   │              Metrics: GET /api/v1/metrics/{system_id}?metric=latency_ms&range=1h              │   │
│   │                 Recommendations: GET /api/v1/recommendations?priority=critical                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  REST API on AIOps master node TCP 443 · CLI scripts run from any mgmt host                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Bearer token = Short-lived auth credential from /auth/login; include in Authorization header         │
│  status=open = Filter returning only unresolved alerts                                                │
│  system_id = Unique identifier for a monitored infrastructure component in AIOps                      │
│  metric param = Name of the metric to retrieve (latency_ms, iops, throughput_mb)                      │
│  range param = Time window for metric data (1h, 24h, 7d)                                              │
│  priority filter = Filter recommendations by Critical/High/Medium/Low                                 │
│  Pagination = Use limit/offset params; default 100 records per page                                   │
│  Webhook test = POST /api/v1/webhooks/{id}/test — verify webhook delivery                             │
│  Health check = GET /api/v1/health — confirm AIOps services are running                               │
│  Admin CLI = aiops-admin tool on host; used for backup, config, and service restart                   │
│  JSON response = All API responses in JSON format; parse with jq                                      │
│  Rate limit = API enforces per-client limits; retry with exponential backoff on 429                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Anomalies

```bash
# List active anomalies
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/anomalies?filter=state%20eq%20'ACTIVE'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {id,system_name,metric,detected_at}'

# Anomalies in last 24 hours
SINCE=$(date -u -v-1d +"%Y-%m-%dT%H:%M:%SZ")
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/anomalies?filter=created_at%20gt%20'${SINCE}'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results | length'
```

### Alerts

```bash
# List all active alerts
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/alerts?filter=state%20eq%20'ACTIVE'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {id,name,severity,system_name}'

# Alerts for a specific system
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/alerts?filter=system_id%20eq%20'${SYSTEM_ID}'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {name,severity,created_at}'
```

### Capacity

```bash
# Capacity data for a specific system
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/systems/${SYSTEM_ID}/capacity" \
  -H "Authorization: Bearer ${TOKEN}" | jq '{used_bytes,total_bytes,days_until_full}'
```

## Endpoint Summary

| Endpoint | Method | Purpose |
|---|---|---|
| `/cloudiq/rest/v1/systems` | GET | List all monitored systems |
| `/cloudiq/rest/v1/systems/{id}` | GET | System detail and health score |
| `/cloudiq/rest/v1/systems/{id}/capacity` | GET | Capacity data and forecast |
| `/cloudiq/rest/v1/recommendations` | GET | List AI-generated recommendations |
| `/cloudiq/rest/v1/recommendations/{id}` | GET | Recommendation detail |
| `/cloudiq/rest/v1/anomalies` | GET | List detected anomalies |
| `/cloudiq/rest/v1/alerts` | GET | List active alerts |
| `/cloudiq/rest/v1/audit-logs` | GET | Audit log entries |

## Filtering and Pagination

The CloudIQ API supports OData-style filters and pagination via `limit` and `offset` parameters:

```bash
# Paginated request — first 50 results
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/recommendations?limit=50&offset=0" \
  -H "Authorization: Bearer ${TOKEN}" | jq '{total: .total_results, count: (.results | length)}'

# Combined filter
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/recommendations?\
filter=severity%20eq%20'High'%20and%20state%20eq%20'ACTIVE'&limit=100" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {id,title,system_name}'
```

Full API documentation: [developer.dell.com/cloudiq](https://developer.dell.com/cloudiq)
