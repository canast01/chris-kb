# Operations

> Part of the [Flex on Demand](../) reference.

---

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| [ ] Check if FOD burst is currently active on any array |  | burst should only be active if a planned workload increase justified it |
| [ ] Review what percentage of the burst ceiling is consumed |  | flag if above 80% of the burst allowance |
| [ ] Confirm whether the current month's consumption report is availabl |  |  |
| [ ] Check that base capacity allocation has not changed unexpectedly |  |  |

## Health Check

```bash
# Authenticate to Unisphere REST API
# Replace <unisphere_ip>, <user>, and <password> with actual values
TOKEN=$(curl -s -k -X POST \
  "https://<unisphere_ip>:8443/univmax/restapi/version/system/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"<user>","password":"<password>"}' | jq -r '.token')

# Get FOD/flex capacity status for the array
curl -s -k \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://<unisphere_ip>:8443/univmax/restapi/100/sloprovisioning/symmetrix/<sid>" | \
  jq '{sid: .symmetrixId, total_usable_cap_gb: .total_usable_cap_gb, total_subscribed_cap_gb: .total_subscribed_cap_gb}'

# Get SRP details to review burst and allocated capacity
curl -s -k \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://<unisphere_ip>:8443/univmax/restapi/100/sloprovisioning/symmetrix/<sid>/srp" | \
  jq '.srpId[]'

# Get detailed SRP capacity including emulation and burst state
curl -s -k \
  -H "Authorization: ${TOKEN}" \
  -H "Content-Type: application/json" \
  "https://<unisphere_ip>:8443/univmax/restapi/100/sloprovisioning/symmetrix/<sid>/srp/<srp_id>" | \
  jq '{srp: .srpId, emulation: .emulation, reserved_cap_percent: .reserved_cap_percent, total_usable_cap_gb: .srp_capacity.usable_total_tb}'
```

## Change Readiness

- [ ] Estimate expected capacity growth from the planned workload increase (in TB)
- [ ] Confirm the FOD burst ceiling is sufficient to cover the planned increase without being exceeded
- [ ] If the planned increase is expected to be sustained (not a temporary burst), notify the Dell account team to discuss adjusting the base contracted capacity
- [ ] Confirm the billing implications are understood — sustained burst usage is charged at the burst rate
- [ ] Document the current base and burst consumption figures before the workload change

| Item | Status | Notes |
|---|---|---|
| Expected capacity growth estimated | | |
| Burst headroom sufficient for planned increase | | |
| Dell account team notified if sustained increase | | |
| Billing implications understood and documented | | |
| Pre-change base and burst consumption recorded | | |

## Incident Triage

**On alert or issue:**
1. Log in to the Dell APEX console (console.dell.com/apex) or Unisphere to check current burst consumption
2. Identify when burst was triggered and which workloads drove the increase
3. If the burst ceiling has been reached, new capacity allocations will fail — immediately assess which workloads can be reduced or tiered
4. Contact the Dell account team to request an emergency burst ceiling increase or expedited base capacity expansion
5. Review the previous month's consumption report to determine if a sustained base capacity increase is warranted

| Symptom | Likely Cause | Action |
|---|---|---|
| Burst ceiling reached, no new capacity available | Workload growth exceeded contracted burst allowance | Reduce provisioning, contact Dell account team for emergency ceiling raise |
| Unexpected billing charges | Sustained burst usage above contracted base | Pull consumption report, identify workloads driving burst, plan base capacity increase |
| Capacity allocation error in Unisphere | Array reporting over-subscription beyond burst | Check SRP utilization via REST API, confirm burst state, open Dell support case |
| FOD consumption not resetting at month boundary | Reporting/billing cycle misalignment | Confirm billing cycle dates with Dell account team, pull consumption report |

## Maintenance Window

FOD itself has no software maintenance requirement. However, any planned workload or storage change that will affect consumption must be documented:

1. Before the window: record current base capacity consumption and burst consumption (in TB and %)
2. Perform the planned workload or storage configuration change
3. Monitor capacity consumption in Unisphere during the window — watch for unexpected burst activation
4. After the window: compare post-change consumption figures against pre-change baseline
5. If the change caused a sustained increase in capacity, update the capacity planning record and notify the Dell account team within 5 business days

## Post-Change Validation

- [ ] FOD burst consumption returns to the pre-change baseline after any temporary workload increase
- [ ] Burst is not active where it was not expected to be
- [ ] Monthly consumption report updated to reflect any intentional capacity changes
- [ ] Dell account team notified if sustained capacity increase is expected to exceed the contracted base
- [ ] Capacity planning records updated with new baseline figures
