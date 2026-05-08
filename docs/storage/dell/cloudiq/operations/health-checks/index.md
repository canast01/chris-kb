# CloudIQ — Health Checks

> Part of the [CloudIQ](../../) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Log in to CloudIQ ([cloudiq.dell.com](https://cloudiq.dell.com)) | | |
| [ ] Review all active CRITICAL alerts | | none should be outstanding at EOD without an open change or incident ticket |
| [ ] Check capacity forecast panel | | flag any system projected to reach full capacity within 30 days |
| [ ] Confirm all expected systems are reporting | | a system showing as "Not Reporting" requires investigation |
| [ ] If automation scripts use the CloudIQ REST API, check that the API token is valid | | |

## Health Check Commands

```bash
# Set environment variables before running
CLOUDIQ_TOKEN="<your_api_token>"
CLOUDIQ_BASE="https://apigw.dell.com/cloudiq/v1"

# List all systems and their current health scores
curl -s -H "Authorization: Bearer ${CLOUDIQ_TOKEN}" \
  "${CLOUDIQ_BASE}/storage-systems" | jq '.results[] | {name: .object_name, health: .health_score, type: .type}'

# Pull active alerts summary (severity: CRITICAL, WARNING)
curl -s -H "Authorization: Bearer ${CLOUDIQ_TOKEN}" \
  "${CLOUDIQ_BASE}/alerts?filter=state%20eq%20%22ACTIVE%22" | \
  jq '.results[] | {severity: .severity, resource: .resource_name, description: .description}'

# Capacity forecast — systems within 30 days of full
curl -s -H "Authorization: Bearer ${CLOUDIQ_TOKEN}" \
  "${CLOUDIQ_BASE}/storage-systems/capacity" | \
  jq '.results[] | select(.days_until_full != null and .days_until_full < 30) | {name: .object_name, days_until_full: .days_until_full, percent_used: .percent_used}'

# Check which systems are not currently reporting
curl -s -H "Authorization: Bearer ${CLOUDIQ_TOKEN}" \
  "${CLOUDIQ_BASE}/storage-systems" | \
  jq '.results[] | select(.connectivity_status != "CONNECTED") | {name: .object_name, connectivity: .connectivity_status}'
```

## Change Readiness

- [ ] No active CRITICAL alerts on the affected system in CloudIQ
- [ ] SCG connectivity status for the affected system shows CONNECTED
- [ ] Record the current health score as a pre-change baseline
- [ ] Confirm CloudIQ alert notifications are routing to the correct email or webhook destination
- [ ] If using the REST API for automation during the window, confirm token is valid

| Item | Status | Notes |
|---|---|---|
| No active CRITICAL alerts on target system | | |
| SCG connectivity: CONNECTED | | |
| Pre-change health score recorded | | |
| Alert notification routing confirmed | | |
| API token valid (if applicable) | | |

## Incident Triage

**On alert or issue:**
1. Log in to CloudIQ and identify the affected system and alert severity
2. Check the anomaly timeline on the system's detail page (Timeline tab) to identify when the issue began
3. Pull performance metrics from the Analytics tab to correlate with the alert timestamp
4. Check SCG connectivity — if the system shows "Not Reporting", the issue may be SCG rather than the storage array itself
5. Cross-reference with any change activity at the time the anomaly was detected
6. Open a Dell support case directly from the CloudIQ alert if the issue cannot be resolved internally

| Symptom | Likely Cause | Action |
|---|---|---|
| Health score dropped suddenly | Performance anomaly or hardware fault | Check Timeline tab, pull performance metrics, review active alerts |
| System shows "Not Reporting" | SCG connectivity failure | SSH to SCG, run `dsagw status` and `dsagw list-devices`, check proxy/firewall |
| CRITICAL alert: drive fault | Disk hardware failure | Confirm in array management UI, open Dell support case from CloudIQ alert |
| CRITICAL alert: capacity threshold | Array nearing full | Review capacity forecast, initiate capacity expansion or data reduction review |
| Alert notifications not received | Notification routing misconfigured | Verify notification settings under Settings > Alerts in CloudIQ |
| API returning 401 Unauthorized | Expired or revoked API token | Regenerate token in CloudIQ Settings > API Tokens |

## Post-Change Validation

- [ ] System health score has returned to the pre-change baseline (or improved)
- [ ] No new CRITICAL or WARNING alerts have been generated on the affected system
- [ ] SCG connectivity for the system shows CONNECTED in CloudIQ
- [ ] Capacity forecast is unchanged or improved (no unexpected capacity consumption)
- [ ] Alert notification routing is confirmed active — no suppression window left open
