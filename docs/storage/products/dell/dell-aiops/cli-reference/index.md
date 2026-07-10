---
tags:
  - dell
---
# Dell AIOps — CLI and API Reference

```bash
# Obtain access token
curl -s -X POST "https://api.cloudiq.dell.com/auth/oauth/v2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}" \
  | jq -r '.access_token'
```


```text title="Expected output"
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjbGllbnRfYWlvcHNfMDEyMzQ1Njc4OTAiLCJpc3MiOiJodHRwczovL2FwaS5jbG91ZGlxLmRlbGwuY29tIiwiaWF0IjoxNjk4NzY1NDMyLCJleHAiOjE2OTg3NjkwMzIsInNjb3BlIjoicmVhZCB3cml0ZSIsImF1ZCI6ImFwaS5jbG91ZGlxLmRlbGwuY29tIn0.aBcDeFgHiJkLmNoPqRsTuVwXyZ1a2b3c4d5e6f7g8h9i0j
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.cloudiq.dell.com`** — Verify network connectivity and DNS resolution; check if the CloudIQ API endpoint is accessible from your network.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure `CLIENT_ID` and `CLIENT_SECRET` environment variables are set correctly and the API endpoint is responding with valid JSON.
    **`jq: error (at <stdin>:1): Cannot index string with string "access_token"`** — Verify the credentials are valid; an authentication failure returns an error object instead of a token object.
```bash
# List active anomalies
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/anomalies?filter=state%20eq%20'ACTIVE'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {id,system_name,metric,detected_at}'

# Anomalies in last 24 hours
SINCE=$(date -u -v-1d +"%Y-%m-%dT%H:%M:%SZ")
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/anomalies?filter=created_at%20gt%20'${SINCE}'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results | length'
```

```text title="Expected output"
{
  "id": "anom_5f8c2a1b9e4d7c3a",
  "system_name": "vmax-prod-01",
  "metric": "response_time_ms",
  "detected_at": "2024-01-15T14:32:18Z"
}
{
  "id": "anom_7d3e9f2c1a5b8e6g",
  "system_name": "unity-backup-02",
  "metric": "cache_hit_ratio",
  "detected_at": "2024-01-15T11:47:52Z"
}
{
  "id": "anom_2k9m4p1x8r3v5w0q",
  "system_name": "powerstore-dr-03",
  "metric": "latency_percentile_95",
  "detected_at": "2024-01-15T09:15:33Z"
}
42
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.cloudiq.dell.com`** — Verify network connectivity and DNS resolution; check if CloudIQ API endpoint is accessible from your network.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure the API token is valid and has not expired; re-authenticate and regenerate the Bearer token.
    **`date: illegal time format`** — Use `date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%SZ"` on Linux systems instead of the BSD `-v` flag.
```bash
# List all active alerts
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/alerts?filter=state%20eq%20'ACTIVE'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {id,name,severity,system_name}'

# Alerts for a specific system
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/alerts?filter=system_id%20eq%20'${SYSTEM_ID}'" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {name,severity,created_at}'
```

```text title="Expected output"
{
  "id": "alert-2847-prod-01",
  "name": "Storage Pool Capacity Warning",
  "severity": "WARNING",
  "system_name": "vmax-cluster-prod"
}
{
  "id": "alert-5921-dr-02",
  "name": "Replication Lag Detected",
  "severity": "CRITICAL",
  "system_name": "unity-dr-secondary"
}
{
  "id": "alert-1634-dev-03",
  "name": "Controller Temperature High",
  "severity": "WARNING",
  "system_name": "powerstore-dev"
}
{
  "name": "Snapshot Quota Exceeded",
  "severity": "CRITICAL",
  "created_at": "2024-01-15T09:42:31Z"
}
{
  "name": "Disk Predictive Failure",
  "severity": "WARNING",
  "created_at": "2024-01-15T08:17:22Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Add `-k` flag to curl or configure your CA bundle with `--cacert /path/to/ca-bundle.crt`.
    **`jq: parse error: Cannot index number with string "id"`** — Verify the API response is valid JSON and the filter returned results; check that `${TOKEN}` and `${SYSTEM_ID}` variables are set correctly.
    **`curl: (401) Unauthorized`** — Regenerate your API token and ensure it is exported as `TOKEN` environment variable before running the command.
```bash
# Capacity data for a specific system
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/systems/${SYSTEM_ID}/capacity" \
  -H "Authorization: Bearer ${TOKEN}" | jq '{used_bytes,total_bytes,days_until_full}'
```

```text title="Expected output"
{
  "used_bytes": 5497558138880,
  "total_bytes": 10995116277760,
  "days_until_full": 247
}
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host: api.cloudiq.dell.com`** — Verify network connectivity and DNS resolution; check if your firewall allows outbound HTTPS to Dell CloudIQ endpoints.
    **`jq: parse error: Invalid JSON text at line 1`** — Ensure the API token is valid and not expired; run `curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/systems/${SYSTEM_ID}/capacity" -H "Authorization: Bearer ${TOKEN}"` without jq to inspect the raw response.
    **`curl: (401) Unauthorized`** — Confirm the Bearer token is correctly set in the `TOKEN` variable and has not expired; regenerate the token from the CloudIQ portal if necessary.
```bash
# Paginated request — first 50 results
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/recommendations?limit=50&offset=0" \
  -H "Authorization: Bearer ${TOKEN}" | jq '{total: .total_results, count: (.results | length)}'

# Combined filter
curl -s "https://api.cloudiq.dell.com/cloudiq/rest/v1/recommendations?\
filter=severity%20eq%20'High'%20and%20state%20eq%20'ACTIVE'&limit=100" \
  -H "Authorization: Bearer ${TOKEN}" | jq '.results[] | {id,title,system_name}'
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```

## See also

- [Dell AIOps — Overview](../../)
