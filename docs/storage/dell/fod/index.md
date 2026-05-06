# Dell Flex on Demand

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Python metered usage reporter, Bash burst detection script, and Ansible FOD audit playbook.</span>
</a>

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>SYMCLI burst usage commands and Unisphere REST API for FOD status and capacity tracking.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Daily burst usage review, headroom checks, change readiness, and monthly consumption reporting.</span>
</a>

</div>

## Overview

Dell Flex on Demand (FOD) is a consumption-based capacity model in which additional storage capacity is pre-installed in the array but metered — you pay only for what you use above the committed baseline. Usage is reported monthly via the CloudIQ telemetry pipeline, and burst consumption above the committed tier is billed at a per-TiB rate. FOD provides the cost efficiency of a cloud-like model on-premises without requiring physical capacity additions. It is available on PowerMax, PowerStore, and PowerScale platforms.

## Where It Fits

- Environments with variable workload patterns where paying for peak capacity all the time is wasteful
- Dev/test environments that need burst capacity periodically but a low committed baseline
- Businesses that want to avoid capital expenditure on storage but remain on-premises
- Organisations running APEX Flex on Demand subscriptions as part of a broader APEX agreement
- Situations where procurement lead times are too long to meet workload growth demands

## Daily Checks

- Review CloudIQ → Capacity for current metered consumption vs. committed baseline across all FOD-enrolled arrays
- Check for burst usage events in the current billing period that may increase the monthly charge
- Verify CloudIQ telemetry is active and reporting — FOD metering depends entirely on CloudIQ connectivity
- Confirm FOD-enrolled arrays are not approaching the physical installed ceiling (above which no more burst is available)
- Review the Dell MyAccount / APEX Console billing summary at month-end to validate metered charges

## Health Commands

~~~bash
# CloudIQ REST API — get capacity metrics for a system (requires CloudIQ API token)
curl -s -H "Authorization: Bearer <cloudiq_token>" \
  "https://cloudiq.dell.com/cloudiq/rest/v1/storage-systems?system_id=<system_id>" | jq .

# PowerMax — show current thin pool utilisation (metered capacity is tracked here)
symcfg -sid <SID> -pool -dp list

# PowerStore — show capacity summary via PowerStore REST API
curl -s -k -u "admin:<pass>" \
  "https://<powerstore-host>/api/rest/capacity" | jq .

# PowerScale — show total cluster usable capacity and used
isi storagepool list

# Confirm CloudIQ telemetry is active (check SCG/CloudIQ agent status)
systemctl status dell-cloudiq-agent 2>/dev/null || \
  service dell-cloudiq-agent status 2>/dev/null || echo "Agent not found on this host"
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Unexpected burst charges on FOD bill | Workload spike or snapshot/backup growth pushed usage above committed baseline | Review CloudIQ capacity trend for the billing period; identify the growth driver; adjust committed baseline if sustained |
| CloudIQ reports no telemetry for a FOD-enrolled system | Secure Connect Gateway offline or CloudIQ agent not running | Check SCG appliance health; verify outbound HTTPS connectivity to Dell CloudIQ endpoints |
| FOD capacity ceiling reached (no more burst available) | All pre-installed burst capacity is consumed | Contact Dell account team to install additional physical capacity under the FOD agreement |
| Committed baseline appears incorrect in APEX Console | Baseline was set at contract time and workload changed | Submit a baseline adjustment request through APEX Console or Dell account team |

## Operational Tasks

- Enrol an array in FOD by working with the Dell account team to set the committed baseline and install pre-burst capacity
- Review monthly metered usage report from CloudIQ or APEX Console and compare to committed baseline
- Adjust the committed baseline up or down at contract renewal based on observed consumption patterns
- Request physical capacity addition when burst headroom is running low — Dell adds capacity under the FOD agreement
- Export CloudIQ usage data via API for internal chargeback or capacity planning reporting

## Upgrade Notes

1. FOD billing is unaffected by firmware upgrades, but confirm CloudIQ telemetry resumes promptly after any maintenance that takes the array offline
2. After adding physical burst capacity under a FOD agreement, confirm CloudIQ reflects the new total installed capacity
3. If the array is migrated or replaced, work with Dell to transfer the FOD contract to the new system SID

## Best Practices

- Set the committed baseline conservatively at contract start and adjust upward at renewal — it is easier to raise a baseline than recover overbilled burst charges
- Monitor CloudIQ capacity trends weekly so burst events are visible before the end-of-month bill
- Ensure Secure Connect Gateway redundancy — a single SCG failure that causes telemetry gaps can complicate billing disputes
- Automate monthly usage extraction via CloudIQ API and feed it into a finance reporting system to eliminate manual reconciliation
