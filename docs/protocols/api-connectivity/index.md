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
```text
┌─────────────────────────────────── Integration — API Connectivity ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Test REST API connectivity: reachability, authentication, TLS cert chain, response codes   │   │
│   │       Auth types: API key (header), Bearer token (OAuth2/JWT), Basic (base64), mTLS cert      │   │
│   │          TLS: verify cert chain with curl -v; check expiry; confirm CA in trust store         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Connectivity Testing             │  │                Common Issues                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           curl -v https://endpoint           │  │        SSL: unable to verify → add CA       │   │
│   │       curl -H "Authorization: Bearer"        │  │          401 = bad token or expired         │   │
│   │          openssl s_client -connect           │  │         403 = auth OK; no permission        │   │
│   │         Check cert expiry (s_client)         │  │          502/504 = upstream timeout         │   │
│   │         Test via proxy: curl --proxy         │  │         Connection refused = FW/DNS         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Bearer token   = Short-lived JWT or opaque token; sent in Authorization: Bearer <token>            │
│    OAuth2         = Delegation framework; client obtains token from IdP; presents to API              │
│    mTLS           = Mutual TLS; both client and server authenticate with certificates                 │
│    SNI            = Server Name Indication; TLS extension; server selects correct cert by hostname    │
│    HTTP 401       = Unauthorized; credentials missing or invalid; re-authenticate                     │
│    HTTP 403       = Forbidden; authenticated but not authorised for the resource                      │
│    openssl s_client= Test TLS handshake; shows cert chain, expiry, cipher negotiated                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
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
```bash
# Check rate limit headers in response
curl -v https://api.example.com/endpoint 2>&1 | grep -i "x-rate-limit\|retry-after\|x-ratelimit"

# Test with retry on 429
curl --retry 5 --retry-delay 10 --retry-max-time 120 https://api.example.com/endpoint
```
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
