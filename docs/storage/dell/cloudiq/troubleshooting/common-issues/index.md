# Dell CloudIQ Common Issues

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
