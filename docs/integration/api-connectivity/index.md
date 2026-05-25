# API Connectivity

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    API Integration Flow                             │
│                                                                     │
│  ┌──────────┐   HTTPS/TLS    ┌──────────────────────────────────┐   │
│  │  Client  │───────────────►│       REST API Endpoint          │   │
│  │(app/curl)│                │  https://api.example.com/v1/...  │   │
│  └──────────┘                └────────────────┬─────────────────┘   │
│                                               │                     │
│                               ┌───────────────▼──────────────────┐  │
│                               │        Authentication            │  │
│                               │  Bearer Token │ API Key │ OAuth2  │  │
│                               └───────────────┬──────────────────┘  │
│                                               │                     │
│                               ┌───────────────▼──────────────────┐  │
│                               │         JSON Response            │  │
│                               │  200 OK │ 401 Unauth │ 429 Rate  │  │
│                               └──────────────────────────────────┘  │
│                                                                     │
│  Checks: DNS ► TLS cert ► auth token ► rate limits ► response       │
└─────────────────────────────────────────────────────────────────────┘
```

Test, diagnose, and maintain connectivity to internal and external APIs across infrastructure and platform services.
## Basic Connectivity Tests

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

## TLS / Certificate Checks

```bash
# Check TLS handshake and certificate chain
openssl s_client -connect api.example.com:443 -servername api.example.com </dev/null 2>&1 | \
  grep -E "Verify return|subject|issuer|Not After"

# Check cipher and protocol
curl -v --tlsv1.2 https://api.example.com 2>&1 | grep -E "SSL|cipher"

# Certificate expiry
echo | openssl s_client -connect api.example.com:443 2>/dev/null | openssl x509 -noout -enddate
```

## DNS Resolution

```bash
# Resolve API hostname
dig +short api.example.com
nslookup api.example.com

# Check for CNAME chain
dig api.example.com CNAME

# Test from container / pod namespace
kubectl run -it --rm debug --image=curlimages/curl -- curl -v https://api.example.com/health
```

## Authentication Checks

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

## Platform API Health Checks

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

## Rate Limiting and Throttling

```bash
# Check rate limit headers in response
curl -v https://api.example.com/endpoint 2>&1 | grep -i "x-rate-limit\|retry-after\|x-ratelimit"

# Test with retry on 429
curl --retry 5 --retry-delay 10 --retry-max-time 120 https://api.example.com/endpoint
```

## API Monitoring Script

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

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| `curl: (6) Could not resolve host` | DNS failure | `dig` hostname; check `/etc/resolv.conf`; check DNS server |
| `SSL: certificate verify failed` | CA not trusted | Add CA cert; check `CURL_CA_BUNDLE` env var |
| HTTP 401 Unauthorized | Token expired or wrong scope | Refresh token; verify scope includes required permission |
| HTTP 403 Forbidden | Correct identity but insufficient permissions | Review IAM policy / RBAC role assignment |
| HTTP 429 Too Many Requests | Rate limit hit | Implement exponential backoff; check rate limit headers |
| HTTP 503 / timeout | API endpoint down or overloaded | Check API status page; retry with backoff; escalate to service owner |
| Response time > 5s | Network latency? API overloaded? | `traceroute` to API host; check API latency metrics on provider side |
