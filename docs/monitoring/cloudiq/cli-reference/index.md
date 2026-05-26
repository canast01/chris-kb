# CloudIQ CLI Reference

CloudIQ is accessed programmatically via its REST API using OAuth2 client credentials. There is no standalone CLI binary; all automation uses the REST API directly. The API base URL is `https://cloudiq.apis.dell.com`.
---

## Authentication

CloudIQ uses OAuth2 client credentials. Generate a client ID and secret from the CloudIQ portal under Settings → API Access.

```bash
# Request an access token
curl -X POST https://cloudiq.apis.dell.com/auth/oauth/v2/token   -H "Content-Type: application/x-www-form-urlencoded"   -d "grant_type=client_credentials&client_id=<client_id>&client_secret=<client_secret>"

# The response contains access_token — use it as Bearer token in all requests
# Token expires in 3600 seconds (1 hour)
```
```

---

## Capacity

```bash
# List capacity metrics for all systems
curl -X GET "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage-systems/capacity"   -H "Authorization: Bearer <token>"

# Get capacity for a specific system
curl -X GET "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage-systems/<system_id>/capacity"   -H "Authorization: Bearer <token>"

# Get capacity forecast
curl -X GET "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage-systems/<system_id>/capacity/forecast"   -H "Authorization: Bearer <token>"
```

---

## Performance

```bash
# Get performance metrics for a system
curl -X GET "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage-systems/<system_id>/metrics"   -H "Authorization: Bearer <token>"

# Filter by metric type (iops, latency, bandwidth)
curl -X GET "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage-systems/<system_id>/metrics?filter=metric_name%20eq%20%22iops%22"   -H "Authorization: Bearer <token>"
```

---

## Recommendations

```bash
# List all recommendations
curl -X GET "https://cloudiq.apis.dell.com/cloudiq/rest/v1/recommendations"   -H "Authorization: Bearer <token>"

# List recommendations for a specific system
curl -X GET "https://cloudiq.apis.dell.com/cloudiq/rest/v1/recommendations?filter=system_id%20eq%20%22<system_id>%22"   -H "Authorization: Bearer <token>"
```

---

## Python Automation Example

```python
import requests

# Authenticate
token_resp = requests.post(
    "https://cloudiq.apis.dell.com/auth/oauth/v2/token",
    data={"grant_type": "client_credentials",
          "client_id": "<client_id>",
          "client_secret": "<client_secret>"}
)
token = token_resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# List all systems
systems = requests.get(
    "https://cloudiq.apis.dell.com/cloudiq/rest/v1/storage-systems",
    headers=headers
).json()

for s in systems.get("results", []):
    print(s["system_name"], s.get("health_score"))
```
