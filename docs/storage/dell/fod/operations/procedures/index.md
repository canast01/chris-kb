# FOD — Procedures

> Part of the [Flex on Demand](../../) reference.

---

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

## Operational Tasks

| Task | Notes |
|---|---|
| Enrol an array in FOD | Work with the Dell account team to set the committed baseline at contract time |
| Review monthly metered usage report | From CloudIQ or APEX Console; compare to contracted baseline |
| Adjust committed baseline | At contract renewal, based on observed consumption trend |
| Request physical capacity addition | When burst headroom is running low — Dell adds capacity under the FOD agreement |
| Export CloudIQ usage data via API | For internal chargeback or capacity planning reporting |
