# Dell AIOps CLI Reference

Dell AIOps does not provide a dedicated CLI tool. All interaction is via the CloudIQ web portal or CloudIQ REST API. This page documents the key REST API endpoints used for AIOps operations.
## Authentication

All API requests require an OAuth2 Bearer token obtained via the client credentials flow.

```bash
# Obtain access token
curl -s -X POST "https://api.cloudiq.dell.com/auth/oauth/v2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}" \
  | jq -r '.access_token'
```

## Key API Endpoints

### Systems

```bash
# List all monitored systems with health scores
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/systems" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Accept: application/json" | jq '.results[] | {name,type,health_score}'

# Get a specific system by ID
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/systems/${SYSTEM_ID}" \
  -H "Authorization: Bearer ${TOKEN}" | jq .
```

### Recommendations (AIOps)

```bash
# List all active recommendations
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/recommendations?filter=state%20eq%20'ACTIVE'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {id,title,severity,system_name}'

# Filter by severity
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/recommendations?filter=severity%20eq%20'Critical'%20and%20state%20eq%20'ACTIVE'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {id,title,recommended_action}'

# Get a specific recommendation
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/recommendations/${REC_ID}" \
  -H "Authorization: Bearer ${TOKEN}" | jq .
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
