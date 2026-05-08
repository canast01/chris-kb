# APEX Storage as a Service — Diagnostics

> Part of the [APEX Storage as a Service](../../) reference.

---

```bash
# Authenticate to Dell APEX API and retrieve a bearer token
curl -s -X POST "https://console.cloudapex.dell.com/api/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"client_id":"<client_id>","client_secret":"<client_secret>"}' \
  | jq -r '.access_token'

# List all subscriptions for the account
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/subscriptions" | jq .

# Get capacity metrics for a specific subscription
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/subscriptions/<subscription_id>/capacity" | jq .

# Get active alerts for all APEX resources
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/alerts?status=active" | jq .

# List service requests
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/service-requests" | jq .
```

## SCG Diagnostics

If APEX systems are not reporting:

```bash
# On the SCG appliance
dsagw status
dsagw connectivity-check
dsagw list-devices
dsagw log show --last 100
```
