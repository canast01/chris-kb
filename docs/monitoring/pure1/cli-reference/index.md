# Pure1 CLI Reference


<div class="kb-summary">
Pure1 provides a REST API authenticated via OAuth2 client credentials. The `pure1` CLI (if installed) wraps common API calls. All programmatic integrations should use the REST API directly. The API base URL is `https://api.pure1.purestorage.com/api/1.latest`.
</div>

---

## Authentication

Pure1 uses a self-signed RSA private key and a registered application ID for API access. Register the application at `https://pure1.purestorage.com/api-registration`.

```bash
# Generate RSA key pair for Pure1 API auth
openssl genrsa -out pure1-private.pem 2048
openssl rsa -in pure1-private.pem -pubout -out pure1-public.pem

# Create a JWT assertion (Python example)
python3 -c "
import jwt, time
payload = {'iss': '<application_id>', 'iat': int(time.time()), 'exp': int(time.time()) + 86400}
token = jwt.encode(payload, open('pure1-private.pem').read(), algorithm='RS256')
print(token)
"

# Exchange JWT for access token
curl -X POST https://api.pure1.purestorage.com/oauth2/1.0/token   -d "grant_type=urn:ietf:params:oauth:grant-type:token-exchange&subject_token=<jwt>&subject_token_type=urn:ietf:params:oauth:token-type:jwt"
```
```text
┌──────────────────────────────────── Pure1 — CLI and API Reference ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Pure1 REST API — Base URL: https://api.pure1.purestorage.com/api/1.latest           │   │
│   │           Auth: POST /oauth2/1.0/token (client_id + private_key JWT) → Bearer token           │   │
│   │          Arrays: GET /arrays — list all registered arrays with model, version, health         │   │
│   │            Metrics: GET /metrics?names=array_total_capacity&resource_names=<array>            │   │
│   │              Alerts: GET /alerts?filter=state='open' — active alerts across fleet             │   │
│   │                 Fleet health: GET /arrays?fields=name,model,os,version,health                 │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Pure1 API at api.pure1.purestorage.com · client runs from any internet-connected host                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Pure1 REST API = Programmatic access to fleet-wide metrics and alert data                            │
│  JWT auth = JSON Web Token signed with RSA private key for API authentication                         │
│  client_id = Application ID registered in Pure1 > API Registration                                    │
│  Bearer token = Short-lived (10 min) OAuth2 token; refresh before expiry                              │
│  arrays endpoint = Returns all arrays with model, Purity version, and health score                    │
│  metrics endpoint = Time-series metric retrieval; supports multiple arrays and metrics                │
│  alerts endpoint = Returns active alerts; filter by state, severity, or array                         │
│  resource_names = Array name filter for metric queries                                                │
│  fields param = Projection; return only needed fields to reduce payload size                          │
│  Pagination = Pure1 API uses continuation_token for large result sets                                 │
│  Rate limit = API enforces per-client limits; exponential backoff on 429                              │
│  py-pure-client = Pure-provided Python library wrapping Pure1 API                                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash

---

## Capacity

```bash
# Get capacity metrics for all arrays
curl -X GET "https://api.pure1.purestorage.com/api/1.latest/arrays?fields=name,capacity,space"   -H "Authorization: Bearer <token>"

# Get capacity for a specific array
curl -X GET "https://api.pure1.purestorage.com/api/1.latest/arrays?filter=name%3D%27<array_name>%27&fields=name,capacity,space"   -H "Authorization: Bearer <token>"
```

---

## Python SDK Example

```python
from py_pure_client import PureOneClient

client = PureOneClient(private_key_file="pure1-private.pem",
                       private_key_password=None,
                       app_id="<application_id>")

# List all arrays
arrays = client.get_arrays()
for a in arrays.items:
    print(a.name, a.model)

# Get active alerts
alerts = client.get_alerts(filter="state='open'")
for alert in alerts.items:
    print(alert.summary, alert.severity)
```
