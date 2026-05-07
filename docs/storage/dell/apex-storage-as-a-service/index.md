# APEX Storage as a Service

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
</div>

## Overview

Dell APEX Storage as a Service (STaaS) is a consumption-based storage model where Dell provisions, owns, and manages the physical infrastructure on-premises at the customer site. Capacity is metered monthly based on committed and burst usage, billed through the APEX Console. The underlying platforms are PowerStore, PowerScale, or PowerFlex, managed by Dell — the customer interacts primarily with the APEX Console or REST API for visibility, capacity requests, and billing reporting.

## Where It Fits

- Organisations that want on-premises storage economics without capital expenditure or operational management overhead
- Environments requiring predictable $/TiB subscription pricing with burst capacity headroom
- Multi-platform environments (block, file, object) under a single consumption agreement
- IT teams that want to outsource hardware lifecycle management (firmware, hardware replace, capacity adds) to Dell
- Capacity planning scenarios where future growth is uncertain and over-provisioning risk needs to be avoided

## Daily Checks

- Log in to the APEX Console and review the Dashboard for any active service alerts or infrastructure health warnings
- Check current committed vs. consumed capacity to confirm usage is within the subscription tier
- Review the Billing & Usage page for any unexpected burst consumption events
- Confirm the on-premises infrastructure is connected and reporting telemetry to APEX (APEX requires Secure Connect Gateway connectivity)
- Review any pending service requests or open incidents in the APEX Console support portal

## Health Commands

~~~bash
# Authenticate to the APEX REST API and retrieve a bearer token
curl -s -X POST "https://console.cloudapex.dell.com/api/v1/auth/token" \
  -H "Content-Type: application/json" \
  -d '{"client_id":"<client_id>","client_secret":"<client_secret>"}' \
  | jq -r '.access_token'

# List all subscriptions for the account
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/subscriptions" | jq .

# Get capacity metrics for a specific subscription
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/subscriptions/<subscription_id>/capacity" | jq .

# Get active alerts for all APEX resources
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/alerts?status=active" | jq .

# List service requests
curl -s -H "Authorization: Bearer <token>" \
  "https://console.cloudapex.dell.com/api/v1/service-requests" | jq .
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Infrastructure health warning in APEX Console | On-premises hardware fault or connectivity loss from Secure Connect Gateway | Check SCG connectivity; review hardware alerts on the underlying platform (PowerStore/PowerScale/PowerFlex) |
| Burst capacity charges unexpected | Workload growth or snapshot/backup accumulation pushing usage above committed tier | Review consumed capacity trend in APEX Console; identify growth sources; raise committed tier if sustained |
| APEX Console shows infrastructure as offline | Secure Connect Gateway appliance down or network path to Dell blocked | Check SCG appliance health and outbound HTTPS connectivity on port 443 to Dell APEX endpoints |
| Capacity request delayed | Service request not raised in APEX Console, or SLA window not yet elapsed | Raise a capacity increase request via APEX Console; review the contracted SLA response time |
| Billing discrepancy | Consumed capacity reported differently between on-premises platform and APEX Console | Allow 24 hours for telemetry sync; open a support case via APEX Console if discrepancy persists |

## Operational Tasks

- Raise a capacity increase request via APEX Console → Subscriptions → Request Capacity Increase
- Review monthly usage report from APEX Console → Billing & Usage and export for finance reconciliation
- Add or modify user access to the APEX Console under Administration → Users & Roles
- Open a support case for hardware or service issues via APEX Console → Support → Create Service Request
- Download the APEX API specification from the Console developer portal to build custom monitoring integrations
- Review the underlying platform health (PowerStore/PowerScale/PowerFlex) directly on the on-premises management interfaces if deeper diagnostics are needed

## Upgrade Notes

1. Hardware firmware and lifecycle upgrades for APEX STaaS are Dell's responsibility — do not initiate firmware changes on APEX-managed infrastructure without coordination
2. Monitor the APEX Console for Dell-initiated maintenance notifications; Dell will schedule maintenance windows for upgrades and communicate via the Console
3. Confirm Secure Connect Gateway is at the current recommended version — SCG upgrades can be triggered from the APEX Console or SCG management interface
4. After any Dell-initiated maintenance, verify all subscriptions show healthy status in APEX Console and confirm on-premises platform availability from the host side

## Best Practices

- Keep Secure Connect Gateway appliances highly available (deploy two SCG appliances for redundancy) — loss of SCG connectivity causes telemetry gaps and may trigger alerts
- Monitor committed vs. consumed capacity monthly and request tier increases at least 30 days before hitting the committed threshold to avoid burst pricing
- Use the APEX REST API to build automated capacity reports that feed into internal capacity planning tools
- Review APEX Console alerts daily; infrastructure issues are Dell's responsibility to remediate but you need to confirm SLA compliance
- Document the subscription ID, contract end date, committed tier, and burst thresholds in a runbook so on-call staff can quickly interpret APEX Console data
