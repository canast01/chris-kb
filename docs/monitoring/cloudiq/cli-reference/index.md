# CloudIQ CLI Reference

CloudIQ is accessed programmatically via its REST API, authenticated using OAuth2 client credentials. There is no standalone CLI; all automation uses the REST API directly.

**CloudIQ REST API:**

| Endpoint | Purpose |
|---|---|
| `POST /oauth2/token` | Obtain OAuth2 access token (client credentials) |
| `GET /cloudiq/rest/v1/storage-systems` | Fleet inventory and health scores |
| `GET /cloudiq/rest/v1/alerts?state=ACTIVE` | Active alerts |
| `GET /cloudiq/rest/v1/storage-systems/{id}/capacity` | Capacity data for a specific system |
| `GET /cloudiq/rest/v1/recommendations` | AIOps recommendations |
| `GET /cloudiq/rest/v1/anomalies` | Detected anomalies |

**Authentication example (Python):**

```python
import requests
resp = requests.post("https://cloudiq.dell.com/oauth2/token",
    data={"grant_type": "client_credentials",
          "client_id": CLIENT_ID, "client_secret": CLIENT_SECRET})
token = resp.json()["access_token"]
```
