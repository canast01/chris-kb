# CloudIQ — Common Issues


<div class="kb-summary">
> Part of the [CloudIQ](../../index.md) reference.
</div>

---

## Quick Reference Table

| Symptom | Likely Cause | First Action |
|---|---|---|
| System not reporting in CloudIQ | SCG connectivity broken; SupportAssist disabled on array; array not registered to SCG | Check SCG status; run `systemctl status dsagw`; confirm array has SupportAssist enabled |
| Health score dropped suddenly | Hardware fault detected; capacity threshold crossed; performance anomaly | Open system in CloudIQ; review Timeline tab; check active alerts; cross-reference with array-side alerts |
| Health score shows `N/A` or `--` | System registered but no telemetry received yet | Allow 60 minutes after SCG registration; check dsagw logs if longer |
| API authentication failure (401) | Client secret expired or incorrect; token expired | Regenerate credentials in CloudIQ Settings → API Access; update automation scripts |
| API returns 403 Forbidden | API client lacks permissions for the requested operation | Check the role assigned to the API credential; Viewer role cannot acknowledge alerts or modify settings |
| Capacity forecast showing `Insufficient data` | Less than 7–14 days of telemetry collected | Wait for data accumulation; this resolves automatically |
| Capacity forecast trend incorrect | Sharp one-time data growth event skewing regression | Review the capacity trend graph; exclude outlier events if the UI supports it; wait for trend to stabilise |
| Alert not routing to email | Notification rule misconfigured; recipient address blocked by spam filter | Review Settings → Notifications; send a test notification; check the recipient's spam folder |
| Alert not routing to webhook | Webhook URL unreachable from Dell cloud; SSL certificate error on endpoint | Test the webhook URL from an external host; verify the endpoint returns 200 to a POST request |
| System shows correct health score but no performance data | Array-side performance statistics collection disabled | Enable performance stats collection on the array; for PowerMax, verify SRDF performance is enabled |
| SCG shows systems as unregistered after SCG rebuild | SCG was rebuilt or re-deployed; re-registration required | Re-register each system to the new SCG from the array management interface |
| CloudIQ dashboard shows `Service Unavailable` | Dell CloudIQ SaaS platform outage | Check [https://www.dell.com/support/incidents-outages](https://www.dell.com/support/incidents-outages); open a P1 case if extended outage |
| SSO login not working | SAML assertion not matching; IdP configuration drift | Review IdP metadata in CloudIQ Settings → Identity Provider; compare with IdP configuration |
| Alert not acknowledging via API | Incorrect alert ID; alert already resolved | Confirm the alert ID and current state via `GET /rest/v1/alerts/<id>` before patching |

---

## Detailed Troubleshooting

### System Not Reporting

A system showing `Not Reporting` or `No Data` in the CloudIQ dashboard indicates that the SCG is not successfully sending telemetry for that system.

**Step 1 — Check dsagw service on the SCG:**

```bash
# SSH to the SCG appliance
ssh admin@<scg-mgmt-ip>

# Check the core telemetry forwarding service
systemctl status dsagw

# If stopped or failed — restart it
systemctl restart dsagw

# Watch logs live for telemetry errors
journalctl -u dsagw -f
# Look for: "connection refused", "TLS handshake failed", "authentication error"
```
```text
┌───────────────────────────────────── Dell CloudIQ Common Issues ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Top issues: SCG offline, stale/missing telemetry, system not appearing in CloudIQ       │   │
│   │        Most problems root-cause to SCG connectivity loss or credential expiry on device       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          SCG Issues         │  │       Telemetry Issues      │  │      CloudIQ UI Issues      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       SCG service down      │  │       Stale data > 1h       │  │        System missing       │   │
│   │       Firewall blocked      │  │       Device poll fail      │  │      Wrong health score     │   │
│   │       Proxy auth fail       │  │         Cred expired        │  │       Alert not firing      │   │
│   │        SSL cert error       │  │       API unreachable       │  │       Login fails SSO       │   │
│   │       SCG version old       │  │       Incomplete data       │  │         Report blank        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │     Problem      │   Likely cause   │    First check    │       Fix        │      Verify      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │ Stale telemetry  │   SCG offline    │     scg status    │   Restart SCG    │   Check UI age   │   │
│   │  System missing  │  Not registered  │  scg device list  │    Add device    │  Appears in UI   │   │
│   │    Poll fail     │  Cred/firewall   │  scg device test  │   Fix creds/FW   │    Poll green    │   │
│   │   SCG offline    │  VM powered off  │   vSphere check   │   Power on VM    │  scg status OK   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Stale telemetry = Last-seen timestamp > 1 hour; data gap; UI shows last known state                │
│    Device poll fail= SCG cannot reach storage REST API; check IP, credentials, and port 443           │
│    Proxy auth fail = SCG proxy requires authentication; configure proxy creds in SCG settings         │
│    SSL cert error  = SCG cannot validate CloudIQ endpoint cert; add CA to SCG trust store             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Step 4 — Check SupportAssist on the array:**

For most Dell arrays, the array must have SupportAssist enabled and connected for telemetry to flow to CloudIQ:

- **PowerStore**: PowerStore Manager → Settings → Support → SupportAssist → Status should show `Connected`
- **PowerMax**: Unisphere → Settings → Connectivity → SupportAssist → Connected
- **Unity**: Unisphere for Unity → System → Connectivity → SupportAssist

---

### API Authentication Failures

```bash
# Reproduce the failure with verbose output
CLIENT_ID="<your-client-id>"
CLIENT_SECRET="<your-client-secret>"

curl -v -X POST "https://cloudiq.apis.dell.com/auth/oauth/v2/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}"

# Common error responses:
# HTTP 401: invalid_client — wrong client_id or client_secret
# HTTP 400: invalid_grant — grant_type value incorrect (must be 'client_credentials')
# HTTP 403: forbidden — credential exists but has been revoked or expired
```

**If the client secret is confirmed lost or expired:**

1. Log into the CloudIQ portal as an admin
2. Navigate to **Settings → API Access**
3. Locate the affected credential
4. Click **Regenerate Secret** — the old secret is immediately invalidated
5. Copy the new secret and update all scripts and vaults
6. Re-test authentication

---

### Webhook Not Delivering Alerts

```bash
# Step 1: Test the webhook endpoint externally (from a machine that has internet access)
curl -X POST "<your-webhook-url>" \
  -H "Content-Type: application/json" \
  -d '{"test": true, "source": "cloudiq-test"}' \
  -v

# Expected: HTTP 200 (or 201) response from the endpoint
# If HTTP 000 or connection refused: the endpoint is not reachable from the internet
# If HTTP 4xx: the endpoint is reachable but the payload format or auth is wrong

# Step 2: Review webhook configuration in CloudIQ
# Settings → Notifications → Webhook → inspect the endpoint URL and any custom headers

# Step 3: Send a test notification from CloudIQ
# Settings → Notifications → Webhook → Send Test
# Then check the endpoint for the incoming request

# Step 4: For ServiceNow webhook failures — check the ServiceNow scripted REST API logs:
# ServiceNow → System Log → Application Logs → filter by "cloudiq" or the REST API script name
```

**Common webhook delivery issues:**

| Issue | Diagnosis | Fix |
|---|---|---|
| Endpoint not reachable | `curl -v` returns connection refused or timeout | The webhook endpoint must be publicly reachable; use a cloud-hosted endpoint or ngrok for testing |
| SSL certificate error | Endpoint uses a self-signed or internal CA certificate | CloudIQ validates endpoint certificates; the endpoint must present a certificate from a trusted public CA |
| 401 from endpoint | Endpoint requires authentication in the POST body or header | Add authentication as a custom header in the CloudIQ webhook configuration |
| Payload format rejected | ServiceNow or Slack rejects the CloudIQ JSON format | Use a middleware (webhook relay, Zapier, AWS Lambda) to transform the payload |

---

### Incorrect or Stale Capacity Forecast

CloudIQ's capacity forecast uses a linear regression on historical data. The forecast can be inaccurate in specific scenarios:

| Scenario | Observed Symptom | Resolution |
|---|---|---|
| Array just onboarded | `Insufficient data` or very wide forecast range | Wait for at least 14 days of telemetry; forecast stabilises with more data |
| Large one-time data migration | Forecast shows "X days to full" with an unrealistic near-term date | Review the capacity trend graph; the regression will smooth the outlier over time (1–2 weeks) |
| Array was upgraded and capacity increased | Forecast shows growth trend that doesn't reflect new capacity | Allow 7 days for the new capacity baseline to be reflected |
| Thin-provisioned volumes over-allocated | Forecast shows capacity as fine but actual writes are growing faster | Monitor `total_used_capacity_gb` vs `total_physical_capacity_gb`; thin overcommit is not factored into the linear model |

```bash
# Query current capacity state to validate against CloudIQ forecast
TOKEN="<your-token>"
BASE="https://cloudiq.apis.dell.com/rest/v1"
SYSTEM_ID="<your-system-id>"

curl -s -X GET "${BASE}/systems/${SYSTEM_ID}/capacity" \
  -H "Authorization: Bearer ${TOKEN}" | python3 -m json.tool

# Key fields to check:
# total_subscribed_capacity_gb — logical allocated to hosts (thin provisioning)
# total_used_capacity_gb       — physical data actually written
# total_physical_capacity_gb   — total raw usable
# percent_used                 — physical used percentage
# days_to_full                 — forecast horizon
# forecast_confidence          — LOW/MEDIUM/HIGH; LOW means insufficient data
```

---

### SCG Connectivity Diagnostics

```bash
# Full SCG connectivity diagnostic sequence
# Run on the SCG appliance (SSH as admin)

echo "=== dsagw service status ==="
systemctl status dsagw

echo "=== DNS resolution ==="
nslookup cloudiq.dell.com
nslookup esrs3.emc.com

echo "=== Network connectivity ==="
curl -k --max-time 10 https://cloudiq.dell.com && echo "cloudiq.dell.com: REACHABLE" || echo "cloudiq.dell.com: UNREACHABLE"
curl -k --max-time 10 https://esrs3.emc.com   && echo "esrs3.emc.com: REACHABLE"   || echo "esrs3.emc.com: UNREACHABLE"

echo "=== Registered devices ==="
dsagw list-devices 2>/dev/null || echo "dsagw CLI not available — check SCG web UI"

echo "=== Recent dsagw log errors ==="
journalctl -u dsagw --since "1 hour ago" | grep -iE "error|fail|refused|timeout" | tail -20
```

---

### Anomaly Detection — Understanding False Positives

CloudIQ's anomaly detection uses ML models trained on historical baselines for each system. A sudden change in workload pattern can trigger an anomaly alert even if the change is expected (e.g., a scheduled batch job or a major application release).

When an anomaly alert fires for a known change:

1. Review the anomaly timeline in the CloudIQ system detail → **Timeline** tab
2. Confirm the anomaly timestamp correlates with the planned change
3. Acknowledge the alert in CloudIQ with a note referencing the change record
4. If recurring false positives for a known periodic workload: create a maintenance window to suppress alerts during the expected activity period

```bash
# Acknowledge an anomaly alert (dismiss as known/planned)
ALERT_ID="<alert-id>"
curl -s -X PATCH "${BASE}/alerts/${ALERT_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "ACKNOWLEDGED",
    "acknowledge_note": "Known: scheduled batch workload spike. CHG0012345"
  }' | python3 -m json.tool
```
