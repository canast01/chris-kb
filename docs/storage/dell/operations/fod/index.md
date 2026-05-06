# FOD — Flex on Demand

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Python CloudIQ burst usage reporter, Bash month-end billing extractor, and Ansible FOD audit playbook.</span>
</a>

</div>

## Purpose

Operational runbook for monitoring and reporting on Dell Flex on Demand (FOD) metered capacity consumption. FOD bills based on actual usage above the committed baseline — this page covers how to track consumption, identify burst events, and prepare month-end billing reports.

## Common Checks

- **Current consumption**: Query CloudIQ → Capacity for all FOD-enrolled systems and compare consumed TiB to the committed baseline
- **Burst events this month**: Check CloudIQ capacity history for any days where consumption exceeded the committed tier
- **Telemetry continuity**: Confirm CloudIQ is receiving uninterrupted telemetry from all FOD systems — gaps cause billing reconstruction from estimated data
- **SCG health**: Verify Secure Connect Gateway is healthy on all sites hosting FOD-enrolled arrays
- **Month-end bill preview**: Pull the CloudIQ API capacity report for the current billing period before the month closes and cross-check against the APEX Console billing preview

## Month-End Billing Procedure

1. On the last working day of the month, log into the CloudIQ dashboard and export capacity utilisation data for all FOD-enrolled systems for the full billing month
2. Identify any days where consumption exceeded the committed baseline — the delta is the burst amount that will be billed at the burst rate
3. Cross-reference with the APEX Console → Billing & Usage preview to confirm figures agree
4. If there is a discrepancy between CloudIQ and APEX Console, open a Dell billing query before the invoice is issued — post-invoice corrections are harder to obtain
5. Archive the monthly export to the shared drive and forward a summary to finance for cost centre reconciliation

## Incident Notes

For unexpected burst billing events:

- **Symptom**: Monthly bill higher than expected; CloudIQ shows consumption above committed baseline on specific dates
- **Impact**: Financial — burst TiB billed at the per-TiB burst rate specified in the FOD contract
- **Start time**: What date did consumption cross the committed threshold?
- **What changed**: Snapshot accumulation, new backup job, database growth, or data migration started on that date?
- **What was checked**: CloudIQ capacity trend, snapshot schedules, backup job sizes
- **Resolution**: Identify and remediate the cause of burst; adjust committed baseline at next contract renewal if growth is sustained

## Change Notes

For committed baseline adjustments:

- **Approval**: Baseline changes affect the monthly cost floor — finance approval required
- **Rollback plan**: Baseline reductions save money but increase burst risk; document current baseline and growth trend before reducing
- **Validation steps**: After baseline change, confirm the APEX Console reflects the new committed tier within 48 hours

## Best Practices

- Pull the CloudIQ capacity report weekly, not just at month-end — catching a burst event early allows you to address the root cause before it accumulates across the billing period
- Automate the monthly export via the CloudIQ API and email the report to finance automatically
- Set CloudIQ capacity alerts at the committed baseline value so burst events trigger an immediate notification
- Review the FOD contract annually — if sustained growth means persistent burst, renegotiating the committed baseline is cheaper than paying burst rates indefinitely
