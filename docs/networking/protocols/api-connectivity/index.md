---
tags:
  - networking
---
# Integration — API Connectivity

```bash
# HTTP status check
curl -o /dev/null -sw "%{http_code} %{time_total}s\n" https://api.example.com/health

# Full response headers (useful for auth debugging)
curl -v -I https://api.example.com/endpoint

# Test with Bearer token
curl -s -H "Authorization: Bearer <token>" https://api.example.com/v1/resource | jq .

# Test with API key header
curl -s -H "X-API-Key: <key>" https://api.example.com/v1/resource

# Test POST with JSON body
curl -s -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"key":"value"}' \
  https://api.example.com/v1/resource | jq .
```


```text title="Expected output"
200 0.342s
*   Trying 203.0.113.45:443...
* Connected to api.example.com (203.0.113.45) port 443 (#0)
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* Server certificate:
*  subject: CN=api.example.com; O=Example Corp; C=US
*  start date: Jan 15 10:22:14 2024 GMT
*  expire date: Jan 14 10:22:14 2025 GMT
*  issuer: C=US; O=Let's Encrypt; CN=R3
* HTTP/1.1 200 OK
* content-type: application/json
* x-ratelimit-limit: 1000
* x-ratelimit-remaining: 987
* x-ratelimit-reset: 1705329600
{
  "status": "healthy",
  "version": "2.4.1",
  "timestamp": "2024-01-15T14:32:18Z"
}
{
  "id": "res_7f2c9d1a",
  "data": [
    {"name": "item1", "created": "2024-01-10"},
    {"name": "item2", "created": "2024-01-12"}
  ]
}
{
  "id": "res_8b4e1f2c",
  "status": "created",
  "resource_uri": "/v1/resource/res_8b4e1f2c"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Add `-k` flag to skip verification in dev environments, or update your CA bundle with `update-ca-certificates` on Linux.
    **`curl: (7) Failed to connect to api.example.com port 443: Connection refused`** — Verify the API endpoint is accessible and not blocked by firewall rules; check with `telnet api.example.com 443` or `nc -zv api.example.com 443`.
    **`{"error":"Unauthorized","code":"INVALID_TOKEN"}`** — Replace `<token>` with a valid Bearer token from your authentication provider and ensure it hasn't expired.
```bash
# OAuth2 — obtain token via client credentials flow
curl -s -X POST https://auth.example.com/oauth/token \
  -d "grant_type=client_credentials&client_id=<id>&client_secret=<secret>&scope=read" | jq .access_token

# Azure — get bearer token via managed identity
curl -s "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01&resource=https://management.azure.com/" \
  -H "Metadata: true" | jq .access_token

# AWS — call API via IAM role (SigV4 — use AWS CLI)
aws sts get-caller-identity    # verify identity before API calls

# Check token expiry (JWT)
echo "<jwt-payload-base64>" | base64 -d | jq .exp | xargs -I {} date -d @{}
```

```text title="Expected output"
"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjbGllbnRfYXBwIiwic2NvcGUiOiJyZWFkIiwiaWF0IjoxNjk5NDU2Nzg5LCJleHAiOjE2OTk0NjAzODl9.x5K9mP2qL8vN3oR7sT1wQ4jZ6aB9cD2eF5gH8iJ0kL"
"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBpZCI6ImM4ZjZkNTQ4LWY2ZTItNDc5Ny04YzQ5LWI3ZDJjMzQ1YWJjZCIsImV4cCI6MTY5OTQ2MDM4OX0.aBcDeFgHiJkLmNoPqRsTuVwXyZ1a2b3c4d5e6f7g8h9i0j1k2l3m4n5o6p7q8r9s0t"
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/api-service"
}
Thu Oct 12 14:33:09 UTC 2023
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Add `-k` flag to skip certificate validation in dev environments, or ensure your CA bundle is current with `update-ca-certificates`.
    **`jq: parse error: Invalid numeric literal at line 1 column 7`** — Verify the API endpoint returned valid JSON by testing with `curl -s <url> | head -c 200` before piping to jq.
    **`command not found: jq`** — Install jq with `apt-get install jq` (Debian/Ubuntu) or `brew install jq` (macOS).
```bash
# Azure Resource Manager API
az rest --method get --url "https://management.azure.com/subscriptions?api-version=2022-12-01" | jq '.value | length'

# AWS — test API reachability
aws sts get-caller-identity --region eu-west-1

# Kubernetes API
kubectl get --raw /healthz
kubectl get --raw /readyz

# Vault (HashiCorp)
curl -s http://vault:8200/v1/sys/health | jq '{sealed:.sealed,initialized:.initialized}'
```

```text title="Expected output"
2
{
    "UserId": "AIDACKCEVSQ6C2EXAMPLE",
    "Account": "123456789012",
    "Arn": "arn:aws:iam::123456789012:user/admin-user"
}
ok
ok
{
  "sealed": false,
  "initialized": true
}
```

!!! warning "Common errors"
    **`ERROR: AUTHENTICATION_FAILED`** — Ensure your Azure CLI credentials are current by running `az login` and verify the subscription ID is correct.
    **`Unable to locate credentials`** — Configure AWS credentials using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` environment variables.
    **`Connection refused`** — Verify the Vault service is running and accessible at the specified address with `curl -v http://vault:8200/v1/sys/health`.
```bash
# Check rate limit headers in response
curl -v https://api.example.com/endpoint 2>&1 | grep -i "x-rate-limit\|retry-after\|x-ratelimit"

# Test with retry on 429
curl --retry 5 --retry-delay 10 --retry-max-time 120 https://api.example.com/endpoint
```

```text title="Expected output"
*   Trying 203.0.113.45:443...
* Connected to api.example.com (203.0.113.45) port 443 (#0)
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
* TLSv1.3 (IN), TLS handshake, Server hello (2):
* TLSv1.3 (IN), TLS handshake, Certificate (11):
* TLSv1.3 (IN), TLS handshake, Finished (20):
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
* TLSv1.3 (OUT), TLS handshake, Finished (20):
< HTTP/2 200
< x-ratelimit-limit: 1000
< x-ratelimit-remaining: 987
< x-ratelimit-reset: 1704067200
< retry-after: 3600
{"status": "success", "data": {"id": "req-8f2a9c1e", "timestamp": "2024-01-01T14:32:15Z"}}
```

!!! warning "Common errors"
    **`curl: (6) Could not resolve host name`** — Verify the API endpoint hostname is correct and DNS resolution is working with `nslookup api.example.com`.
    **`curl: (35) OpenSSL SSL_connect: SSL: CERTIFICATE_VERIFY_FAILED`** — Add `--insecure` flag to bypass certificate verification in development environments, or ensure your CA bundle is up-to-date with `update-ca-certificates`.
    **`curl: (28) Operation timeout. The timeout specified has expired.`** — Increase the timeout with `--max-time 30` or check if the API endpoint is responding by testing with a simpler health check endpoint first.
```bash
#!/bin/bash
# Quick health check across multiple endpoints
declare -A ENDPOINTS=(
  ["azure-mgmt"]="https://management.azure.com/subscriptions?api-version=2022-12-01"
  ["app-api"]="https://api.example.com/health"
  ["vault"]="http://vault:8200/v1/sys/health"
)

for name in "${!ENDPOINTS[@]}"; do
  code=$(curl -o /dev/null -sw "%{http_code}" "${ENDPOINTS[$name]}" 2>/dev/null)
  echo "$name: HTTP $code"
done
```

```d2
direction: down

component_a: "Component A" {shape: rectangle}
component_b: "Component B" {shape: rectangle}
component_c: "Component C" {shape: rectangle}

component_a -> component_b: uses
component_b -> component_c: uses
```
