# Pure1 CLI Reference

Pure1 provides a REST API authenticated via OAuth2 client credentials. The `pure1` CLI (if installed) wraps common API calls. All programmatic integrations should use the REST API directly. The API base URL is `https://api.pure1.purestorage.com/api/1.latest`.
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

---

## Health & Alerts

```bash
# List all active alerts across fleet
curl -X GET "https://api.pure1.purestorage.com/api/1.latest/alerts?filter=state%3D%27open%27"   -H "Authorization: Bearer <token>"

# List alerts for a specific array
curl -X GET "https://api.pure1.purestorage.com/api/1.latest/alerts?filter=arrays.name%3D%27<array_name>%27"   -H "Authorization: Bearer <token>"
```

---

## Metrics

```bash
# List available metrics
curl -X GET "https://api.pure1.purestorage.com/api/1.latest/metrics"   -H "Authorization: Bearer <token>"

# Query array-level IOPS
curl -X GET "https://api.pure1.purestorage.com/api/1.latest/metrics/history?ids=<metric_id>&resource_ids=<array_id>&start_time=<epoch>&end_time=<epoch>"   -H "Authorization: Bearer <token>"
```

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
