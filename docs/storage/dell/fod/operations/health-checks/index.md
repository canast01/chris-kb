# FOD — Health Checks

> Part of the [Flex on Demand](../../) reference.

---

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| [ ] Check if FOD burst is currently active on any array | | burst should only be active if a planned workload increase justified it |
| [ ] Review what percentage of the burst ceiling is consumed | | flag if above 80% of the burst allowance |
| [ ] Confirm whether the current month's consumption report is available | | |
| [ ] Check that base capacity allocation has not changed unexpectedly | | |

## Health Check Commands

```bash
# Authenticate to Unisphere REST API
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
  "https://<unisphere_ip>:8443/univmax/restapi/100/sloprovisioning/symmetrix/<sid>/srp/<srp_id>" | \
  jq '{srp: .srpId, reserved_cap_percent: .reserved_cap_percent, total_usable_cap_gb: .srp_capacity.usable_total_tb}'
```

## Change Readiness

- [ ] Estimate expected capacity growth from the planned workload increase (in TB)
- [ ] Confirm the FOD burst ceiling is sufficient to cover the planned increase without being exceeded
- [ ] If the planned increase is expected to be sustained (not a temporary burst), notify the Dell account team to discuss adjusting the base contracted capacity
- [ ] Confirm the billing implications are understood — sustained burst usage is charged at the burst rate
- [ ] Document the current base and burst consumption figures before the workload change

## Post-Change Validation

- [ ] FOD burst consumption returns to the pre-change baseline after any temporary workload increase
- [ ] Burst is not active where it was not expected to be
- [ ] Monthly consumption report updated to reflect any intentional capacity changes
- [ ] Dell account team notified if sustained capacity increase is expected to exceed the contracted base
- [ ] Capacity planning records updated with new baseline figures
