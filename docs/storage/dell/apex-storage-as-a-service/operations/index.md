# Operations

> Part of the [APEX Storage as a Service](../) reference.

---
## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Log in to the Dell APEX console ([console.dell.com/apex](https |  |  |
| [ ] Check consumed capacity vs contracted capacity |  | flag if consumed capacity exceeds 80% of the contracted amount |
| [ ] Confirm all APEX systems are showing healthy in CloudIQ (health sc |  |  |
| [ ] Confirm no Dell-scheduled maintenance windows are active or pendin |  |  |

## Health Check

```bash
# Authenticate to Dell APEX API (console.dell.com)
# Obtain token via Dell API Gateway
APEX_TOKEN="<your_apex_api_token>"
APEX_BASE="https://apigw.dell.com/apex/v1"

# List all APEX storage systems and their health scores
curl -s -H "Authorization: Bearer ${APEX_TOKEN}" \
  "${APEX_BASE}/storage-systems" | \
  jq '.results[] | {name: .name, health_score: .health_score, status: .status, type: .type}'

# Check capacity consumed vs contracted for each system
curl -s -H "Authorization: Bearer ${APEX_TOKEN}" \
  "${APEX_BASE}/storage-systems" | \
  jq '.results[] | {name: .name, contracted_tb: .contracted_capacity_tb, consumed_tb: .consumed_capacity_tb, percent_consumed: (.consumed_capacity_tb / .contracted_capacity_tb * 100)}'

# Check for any active alerts on APEX systems via CloudIQ API
CLOUDIQ_TOKEN="<your_cloudiq_api_token>"
curl -s -H "Authorization: Bearer ${CLOUDIQ_TOKEN}" \
  "https://apigw.dell.com/cloudiq/v1/alerts?filter=state%20eq%20%22ACTIVE%22" | \
  jq '.results[] | select(.severity == "CRITICAL") | {resource: .resource_name, description: .description}'

# Check SLA tier assigned to each system
curl -s -H "Authorization: Bearer ${APEX_TOKEN}" \
  "${APEX_BASE}/storage-systems" | \
  jq '.results[] | {name: .name, sla_tier: .sla_tier, committed_iops: .committed_iops}'
```

## Change Readiness

- [ ] Contracted capacity headroom is sufficient for the planned workload increase (consumed < 80% of contracted)
- [ ] The current SLA tier (e.g., Optimized, Value) is appropriate for the planned workload's performance requirements
- [ ] Check the APEX console for any Dell-scheduled maintenance windows that overlap with the planned change
- [ ] If the workload increase is expected to exceed contracted capacity, contact Dell account team before the change to initiate a contract amendment
- [ ] Confirm CloudIQ is reporting the APEX system as healthy before proceeding

| Item | Status | Notes |
|---|---|---|
| Contracted capacity headroom confirmed sufficient | | |
| SLA tier appropriate for planned workload | | |
| No overlapping Dell-scheduled maintenance | | |
| Dell account team engaged if capacity amendment needed | | |
| APEX system healthy in CloudIQ before change | | |

## Incident Triage

**On alert or issue:**
1. Log in to CloudIQ and check the health score and active alerts for the affected APEX system
2. Review the anomaly timeline in CloudIQ to identify when the degradation began and correlate with any change activity
3. Check the APEX console for any active Dell-managed maintenance or known service incidents
4. If performance degradation is confirmed and not tied to a Dell maintenance window, open a Dell support case directly from the CloudIQ alert — Dell is responsible for infrastructure remediation
5. If capacity is approaching the contracted limit, log in to the APEX console and initiate a capacity increase request

| Symptom | Likely Cause | Action |
|---|---|---|
| APEX system performance degradation | Infrastructure fault (Dell-managed) or workload surge | Check CloudIQ health score and anomaly timeline; open Dell support case if hardware/infra fault |
| Capacity alert: approaching contracted limit | Workload growth exceeding contracted amount | Log in to APEX console, review consumed capacity, contact Dell account team to amend contract |
| System shows offline or unreachable | Dell-managed infrastructure outage or network issue | Check APEX console for service status, open P1 support case with Dell if not a planned window |
| SLA breach concern (IOPS below SLA) | Workload exceeds SLA tier commitment | Collect CloudIQ performance data, open support case with Dell SLA breach evidence |
| CloudIQ showing "Not Reporting" for APEX system | SCG connectivity failure | Check SCG appliance: `dsagw status`, `dsagw list-devices`, `dsagw connectivity-check` |

## Maintenance Window

Dell is responsible for APEX infrastructure maintenance. Customer responsibilities during Dell-scheduled windows:

1. Confirm receipt of Dell's maintenance notification and acknowledge the scheduled window
2. Assess potential workload impact during the window — notify application owners if I/O disruption is possible
3. Confirm no customer-side changes (provisioning, workload migrations) are scheduled to overlap with the Dell window
4. Monitor the APEX system in CloudIQ and the APEX console during the window
5. After the window: confirm the system health score has returned to pre-maintenance baseline
6. If the system did not recover automatically after the Dell window, open a Dell support case immediately

## Post-Change Validation

- [ ] APEX system health score in CloudIQ has returned to the pre-change baseline (>= 80)
- [ ] No new CRITICAL alerts generated after the change
- [ ] Capacity consumption is within the expected range — no unexpected increase
- [ ] SLA tier remains appropriate and IOPS commitments are being met (check CloudIQ analytics)
- [ ] SCG is reporting the APEX system as CONNECTED
- [ ] Application owners confirm no user-visible impact following the change
