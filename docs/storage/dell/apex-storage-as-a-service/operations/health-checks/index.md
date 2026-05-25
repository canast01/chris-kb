# APEX Storage as a Service — Health Checks

> Part of the [APEX Storage as a Service](../../index.md) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Log in to the Dell APEX console and review the Dashboard for any active service alerts | | |
| [ ] Check current committed vs. consumed capacity | | flag if consumed capacity exceeds 80% of the contracted amount |
| [ ] Confirm all APEX systems are showing healthy in CloudIQ | | health score >= 80 |
| [ ] Confirm no Dell-scheduled maintenance windows are active or pending | | |

## Health Check Commands

```bash
# Authenticate to Dell APEX API
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
```

## Change Readiness

- [ ] Contracted capacity headroom is sufficient for the planned workload increase (consumed < 80% of contracted)
- [ ] The current SLA tier is appropriate for the planned workload's performance requirements
- [ ] Check the APEX console for any Dell-scheduled maintenance windows that overlap with the planned change
- [ ] If the workload increase is expected to exceed contracted capacity, contact Dell account team before the change to initiate a contract amendment
- [ ] Confirm CloudIQ is reporting the APEX system as healthy before proceeding

## Post-Change Validation

- [ ] APEX system health score in CloudIQ has returned to the pre-change baseline (>= 80)
- [ ] No new CRITICAL alerts generated after the change
- [ ] Capacity consumption is within the expected range — no unexpected increase
- [ ] SLA tier remains appropriate and IOPS commitments are being met
- [ ] SCG is reporting the APEX system as CONNECTED
- [ ] Application owners confirm no user-visible impact following the change
