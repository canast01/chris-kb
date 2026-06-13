---
tags:
  - dell
  - operations
---
# APEX Storage as a Service — Health Checks


<div class="kb-summary">
Part of the [APEX Storage as a Service](../index.md) reference.

*Applies to: APEX Storage-as-a-Service*
</div>
```text
┌─────────────────────────────────── Dell Apex STaaS — Health Checks ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Apex STaaS health checks: routine verification of operational status and performance     │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Owner            │   │
│   │           Hardware          │  │       NVMe/SAS arrays       │  │             Dell            │   │
│   │          Management         │  │         Apex Console        │  │           Customer          │   │
│   │          Monitoring         │  │         CloudIQ/SCG         │  │            Shared           │   │
│   │           Billing           │  │       Committed+burst       │  │         Dell billing        │   │
│   │           Network           │  │        iSCSI VLAN/FC        │  │           Customer          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell array hardware on-premises · customer iSCSI VLAN / FC fabric · Apex Console SaaS    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Apex STaaS         = on-prem Dell storage consumed as a cloud service with subscription billing    │
│    Apex Console       = cloud portal; provision volumes, view usage, and raise support requests       │
│    Committed base     = minimum contracted capacity tier; billed monthly regardless of actual use     │
│    Burst capacity     = pre-installed unlocked storage above committed; billed when consumed          │
│    SCG                = Secure Connect Gateway; relays array telemetry to CloudIQ for analysis        │
│    CloudIQ            = Dell AIOps SaaS; health scores, capacity forecasts, firmware advisories       │
│    NVMe tier          = all-flash performance tier; sub-millisecond latency for database workloads    │
│    Capacity tier      = SAS/NL-SAS lower cost tier; suited to bulk storage and backup targets         │
│    iSCSI CHAP         = Challenge Handshake Auth Protocol; authenticates iSCSI initiators to array    │
│    FC port sec.       = FC fabric binding and port security; restricts which HBAs can log in          │
│    vVols              = Virtual Volumes; per-VM storage objects exposed via VASA provider to vCenter  │
│    OOB mgmt           = out-of-band management network for direct array controller access             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Service health:** APEX Console → Services — all services Active
2. **Capacity consumption:** APEX Console → Consumption — check against committed capacity
3. **Performance metrics:** review IOPS and latency trends in APEX Console
4. **Support case status:** check any open support cases related to service health
5. **Billing alerts:** review any billing or consumption threshold alerts
6. **SLA compliance:** verify uptime metrics meet contracted SLA in APEX Console
7. **Data protection status:** verify snapshots and replication are completing per schedule

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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Apex Storage As A Service — Procedures](procedures/)
- [Apex Storage As A Service — CLI Reference](cli-reference/)
- [Apex Storage As A Service — Common Issues](../troubleshooting/common-issues/)
