---
tags:
  - operations
  - pure
---
# Pure1 Cloud Management

<div class="kb-summary">
Pure1 Cloud Management reference covering Accessing Pure1, Key Navigation Areas, Capacity Planning, Pure1 AI (Copilot), Phone-Home Connectivity and 2 more sections.

*Applies to: FlashArray Purity 6.x*
</div>

![Pure1 Cloud Management — Diagram](../../../../assets/storage-pure-operations-pure1-diagram.svg)

Pure1 is Pure Storage's cloud-based management and monitoring platform. It provides a unified view of all FlashArray and FlashBlade systems.

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Accessing Pure1

Log in at **pure1.purestorage.com** with your Pure Storage account credentials.

## Key Navigation Areas

| Section | Purpose |
|---|---|
| **Storage → Arrays** | Array inventory, health, and status |
| **Storage → Fleet** | Consolidated view of all arrays |
| **Analysis → Capacity** | Current and forecast capacity per array |
| **Analysis → Performance** | IOPS, throughput, latency over time |
| **Analysis → Workload** | Per-volume / per-file-system performance breakdown |
| **Alerts** | Active and historical alerts across all arrays |
| **Support → Cases** | Open and track support cases |
| **Billing** | Evergreen subscription and usage reports |

## Capacity Planning

**Pure1 → Analysis → Capacity → Forecast**

Pure1 uses AI to predict when an array will reach capacity based on consumption trends. Review forecasts monthly to plan expansion ahead of time.

## Pure1 AI (Copilot)

Pure1 includes AI-driven:
- Anomaly detection — flags unusual performance or capacity trends
- Predictive failure analysis — identifies hardware at risk
- Workload insights — identifies top consumers

## Phone-Home Connectivity

Arrays must be able to reach Pure1 for proactive monitoring. Required outbound access:

| Destination | Port | Protocol |
|---|---|---|
| pure1.purestorage.com | 443 | HTTPS |
| phone-home.purestorage.com | 443 | HTTPS |

```bash
# Verify phone-home status — FlashArray
purecli phone-home list

# Verify phone-home status — FlashBlade
purefb phone-home list
```


```text title="Expected output"
Phone Home Status — FlashArray (FA-405):
  Enabled: true
  Last Phone Home: 2024-01-15T14:32:18Z
  Next Scheduled: 2024-01-16T02:32:18Z
  Status: Connected
  Proxy: None

Phone Home Status — FlashBlade (FB-2000):
  Enabled: true
  Last Phone Home: 2024-01-15T13:45:22Z
  Next Scheduled: 2024-01-16T01:45:22Z
  Status: Connected
  Proxy: None
```

!!! warning "Common errors"
    **`purecli: command not found`** — Install the Pure Storage Python SDK with `pip install purestorage` or ensure the Pure CLI is in your PATH.
    **`Error: Unable to connect to array at 192.168.1.100`** — Verify network connectivity to the FlashArray management IP and confirm credentials are set via `purecli login` or environment variables.
    **`Error: Phone Home is disabled on this array`** — Enable phone-home on the array via the management console or use `purecli phone-home enable` if supported by your Pure OS version.
## Role-Based Access in Pure1

Pure1 supports multiple roles:
- **Array Admin** — full array management
- **Storage Admin** — provisioning without system changes
- **Read-only** — monitoring and reporting only

Manage users under **Settings → Users** in Pure1.

## Pure1 API

Pure1 provides a REST API for automation and integration:

```bash
# Authenticate and get token
curl -X POST https://api.pure1.purestorage.com/oauth2/1.0/token \
    -d "grant_type=client_credentials&client_id=<id>&client_secret=<secret>"

# List arrays
curl -H "Authorization: Bearer <token>" \
    https://api.pure1.purestorage.com/api/1.latest/arrays
```


```text title="Expected output"
{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwdXJlMV9hcGkiLCJleHAiOjE3MDk4MzI0MDB9.abc123xyz","token_type":"Bearer","expires_in":3600}
{
  "items": [
    {
      "id": "8c1e8d5a-7b2f-4c9e-a1d3-5f6g7h8i9j0k",
      "name": "array-prod-01",
      "model": "FlashArray//X",
      "version": "6.4.2",
      "status": "healthy"
    },
    {
      "id": "9d2f9e6b-8c3g-5d0f-b2e4-6g7h8i9j0k1l",
      "name": "array-prod-02",
      "model": "FlashArray//X",
      "version": "6.4.2",
      "status": "healthy"
    },
    {
      "id": "0e3g0f7c-9d4h-6e1g-c3f5-7h8i9j0k1l2m",
      "name": "array-dr-01",
      "model": "FlashArray//C",
      "version": "6.3.8",
      "status": "healthy"
    }
  ],
  "continuation_token": null
}
```

!!! warning "Common errors"
    **`{"error_description":"invalid_client","error":"invalid_grant"}`** — Verify that client_id and client_secret are correct and URL-encoded if they contain special characters.
    **`{"error_description":"The access token expired","error":"invalid_token"}`** — Regenerate a fresh token using the POST /oauth2/1.0/token endpoint before making API calls.
    **`curl: (60) SSL certificate problem: unable to get local issuer certificate`** — Add `-k` flag to bypass certificate verification in test environments, or ensure your system's CA bundle is up to date.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Pure Storage — Alerts](../alerts/)
- [Pure Storage — Support Cases](../support-cases/)
- [Pure Storage — Overview](../../)
