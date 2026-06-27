---
tags:
  - dell
  - troubleshooting
search:
  boost: 1.5
---
# CloudIQ — Escalation

<div class="kb-summary">
CloudIQ support escalation: how to collect the SCG log bundle and API traces, open a Dell support case, set severity, and follow the escalation path for CloudIQ data gaps, connectivity failures, and SaaS platform incidents.

*Applies to: CloudIQ*
</div>
![CloudIQ — Escalation](../../../../assets/storage-dell-cloudiq-troubleshooting-escalation.svg)




## Before you begin

- **Access:** Storage admin credentials on affected arrays; CloudIQ admin role (Settings access); Dell support portal account with entitlement to the affected systems
- **Gather first:** affected system name and serial number, time window of the data gap or error, and whether SCG shows connectivity to the affected array
- **Status check:** check the Dell support portal status page before escalating — CloudIQ SaaS maintenance windows are announced there
- **Scope:** confirm whether the issue affects one system, all systems in the org, or the CloudIQ platform globally (check other tenants if you have access)

---

## Severity Levels

| Priority | Condition | Response Time | Coverage |
|---|---|---|---|
| P1 | CloudIQ completely unavailable; unable to monitor any production systems | 2 hours | 24×7×365 |
| P2 | Degraded CloudIQ functionality: partial data, delayed alerts, missing metrics | 4 hours | 24×7×365 |
| P3 | Non-critical issue: UI display error, API edge case, one system missing data | Next business day | Business hours |
| P4 | General question or enhancement request | Next business day | Business hours |

## Pre-Escalation Triage Checklist

| Check | Where | Expected |
|---|---|---|
| CloudIQ UI accessible | Browse to `cloudiq.dell.com` | Dashboard loads |
| SCG service running | SCG web UI → Status | Service: Running |
| SCG connected to CloudIQ | SCG web UI → Connectivity | Connection status: Connected |
| Array registered in CloudIQ | CloudIQ → Infrastructure → Systems | Affected system appears in list |
| SCG connectivity to array | SCG web UI → Managed Systems | Array shows last contact < 5 min |
| SCG disk space | SCG appliance: `df -h` | Root volume < 80% full |
| SCG version current | SCG web UI → About | Version within last 2 releases |
| API accessible | `curl -sk https://cloudiq.dell.com/cloudiq/api/v1/systems -H "Authorization: Bearer <token>"` | HTTP 200 |

---

## Step-by-Step Data Collection

### 1. Collect SCG version and connectivity info

```bash
# SSH to SCG appliance (or access SCG console)
ssh admin@<scg-hostname>

# Check SCG version
scg version

# Check SCG service status
scg status

# Test connectivity to CloudIQ
scg connectivity test

# Test connectivity to a specific managed array
scg system connectivity --system-id <system-serial-number>
```

### 2. Collect SCG log bundle

```bash
# From the SCG CLI:
scg logs collect --output /tmp/scg-logs-$(date +%F).zip

# Alternative: from the SCG web UI
# Navigate to: Admin → Support → Collect Support Bundle
# Download the resulting ZIP file

# The logs bundle contains:
#   - SCG application logs from /var/log/dsagw/
#   - Connectivity test results
#   - System registration details
#   - Error trace for the last 48 hours
```

### 3. Collect application logs manually (if scg logs collect fails)

```bash
# Application logs directory
ls -lt /var/log/dsagw/ | head -10
tar czf /tmp/scg-applogs-$(date +%F).tar.gz /var/log/dsagw/*.log /var/log/dsagw/*.log.*

# Check for specific error patterns
grep -i "error\|exception\|connection refused\|timeout" /var/log/dsagw/application.log | tail -100

# Check system registration
scg system list
scg system status --system-id <system-serial-number>
```

### 4. Collect CloudIQ API diagnostics

```bash
# Get CloudIQ OAuth token (from CloudIQ Settings → API Keys)
TOKEN="<your-api-key>"

# List all systems in CloudIQ
curl -sk "https://cloudiq.dell.com/cloudiq/api/v1/systems" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json" | python3 -m json.tool > /tmp/cloudiq-systems.json

# Get last ingestion time for a specific system
SYSTEM_ID="<system-id-from-cloudiq-ui>"
curl -sk "https://cloudiq.dell.com/cloudiq/api/v1/systems/${SYSTEM_ID}" \
  -H "Authorization: Bearer $TOKEN" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f'System: {data.get(\"system_name\")}')
print(f'Type: {data.get(\"system_type\")}')
print(f'Last telemetry: {data.get(\"last_seen_timestamp\")}')
print(f'Health: {data.get(\"system_health_score\")}')
"

# If UI issue — browser console errors
# F12 → Console tab → reload the page → Export Console as file
```

### 5. Write the timeline

```text
CloudIQ Org: mycompany (Org ID: found in Settings > Organization)
Affected system: PowerStore-1000T SN: CKM00xxxxxxxx
SCG version: 5.18.0.1
SCG hostname: scg01.corp.local

Issue first observed: 2026-06-15 08:00 UTC
Last data seen in CloudIQ: 2026-06-14 20:00 UTC

Error observed:
  - CloudIQ dashboard shows system offline for 12 hours
  - SCG connectivity test: PASS to CloudIQ; FAIL to PowerStore-1000T
  - SCG log: "Connection timeout to 10.10.10.50 (PowerStore Management IP)"

Steps already taken:
  - Verified SCG service is running
  - Confirmed PowerStore Management IP is reachable from SCG host (ping OK)
  - Ran scg connectivity test — shows timeout at HTTPS handshake stage

Changes in prior 24h:
  - TLS certificate on PowerStore management interface was rotated

Blast radius:
  - PowerStore metrics unavailable in CloudIQ for 12 hours
  - Capacity and performance alerts not firing for this system
```

---

## How to Open a Dell Support Case

1. Go to **support.dell.com** and sign in with your Dell account (linked to your ProSupport contract).

2. Click **Create Service Request** or **Start Support Request**.

3. Under **Product**, search for and select the storage system in question (or select CloudIQ directly if the issue is platform-wide).

4. Under **Category**, select **CloudIQ / Data Connectivity** or **Monitoring and Analytics**.

5. Under **Priority**, select:
   - **P1**: CloudIQ completely down; all systems unmonitored; production SLA at risk
   - **P2**: Degraded CloudIQ; missing data for one or more systems; alert delays
   - **P3**: Non-critical display or API issue; one system missing data
   - **P4**: General question

6. In the **Summary** field: `CloudIQ — PowerStore SN CKM00xxx data not appearing since 2026-06-14 20:00 UTC — SCG connectivity test failing`.

7. In the **Description**, paste:
   - SCG version and hostname
   - Affected system name, type, and serial number
   - CloudIQ Org ID (Settings → Organization)
   - Timeline (from step 5 above)
   - Output of `scg connectivity test`
   - What you have already checked

8. Upload attachments:
   - `scg-logs-<date>.zip` — full SCG log bundle
   - `cloudiq-systems.json` — API response with system status
   - Browser console export (if UI issue)
   - `scg-applogs-<date>.tar.gz` (if bundle collection failed)

9. Click **Submit**. Case number arrives by email.

---

## Escalation Path

![CloudIQ — Escalation — Diagram](../../../../assets/storage-dell-cloudiq-troubleshooting-escalation-diagram.svg)

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Delete and re-register the SCG appliance to fix connectivity | Loses SCG configuration, system registrations, and historical data | Fix the connectivity issue (certificate, proxy, firewall); re-register only as a last resort with Dell guidance |
| Restart SCG services during active data collection | Interrupts the log bundle collection and loses in-memory error state | Stop `scg logs collect` first; restart services; then collect a new log bundle after restart |
| Update the SCG version during an active P1 incident | SCG updates can change connectivity parameters and mask the original cause | Complete the incident first; schedule SCG update during a maintenance window |
| Remove and re-add the affected storage system from CloudIQ | Deletes historical data for the system in CloudIQ (irreversible) | Leave the system registered; fix the ingest issue through Dell support |

---

## Useful Commands for Case Updates

```bash
# Quick state snapshot for case updates
scg version
scg status
scg connectivity test
scg system list | grep -E "System Name|Status|Last Contact"

# Check SCG disk space (low disk causes log collection failures)
df -h /var/log

# Test CloudIQ API endpoint reachability from SCG
curl -sk -o /dev/null -w "%{http_code} %{time_total}s\n" \
  https://cloudiq.dell.com/cloudiq/api/v1/systems

# Count recent errors in SCG application log
grep -c "ERROR" /var/log/dsagw/application.log

# Show last 50 errors in SCG log
grep "ERROR" /var/log/dsagw/application.log | tail -50
```

---

## Verify resolution

- Confirm `scg connectivity test` passes for the previously affected system
- Verify the system appears in CloudIQ dashboard with a last-seen timestamp within the last 5 minutes
- Check CloudIQ health score and capacity metrics are populating for the affected system
- Monitor for 30 minutes to confirm data continues to arrive (metrics update every 5–15 minutes)
- Confirm alerts are firing correctly for the recovered system (test by temporarily reducing a threshold)

---

## See also

- [CloudIQ — Diagnostics](diagnostics/)
- [CloudIQ — Common Issues](common-issues/)
