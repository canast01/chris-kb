---
tags:
  - dr
---
# Service Level Objectives (SLO)

<div class="kb-summary">
SLOs define quantitative targets for service reliability and performance. They form the basis for alerting thresholds, capacity decisions, and on-call escalation.
</div>

```d2
direction: down

slo_vs_sla_vs_sli: "SLO vs SLA vs SLI" {shape: rectangle}
common_slos_for_infrastructure: "Common SLOs for Infrastructure" {shape: rectangle}
error_budget: "Error Budget" {shape: rectangle}
slo_dashboard_requirements: "SLO Dashboard Requirements" {shape: rectangle}
alerting_from_slos: "Alerting from SLOs" {shape: rectangle}
slo_review_cadence: "SLO Review Cadence" {shape: rectangle}

slo_vs_sla_vs_sli -> common_slos_for_infrastructure: uses
common_slos_for_infrastructure -> error_budget: uses
error_budget -> slo_dashboard_requirements: uses
slo_dashboard_requirements -> alerting_from_slos: uses
alerting_from_slos -> slo_review_cadence: uses
```

## SLO vs SLA vs SLI

| Term | Definition |
|---|---|
| SLI (Service Level Indicator) | The actual measured metric (e.g., request success rate) |
| SLO (Service Level Objective) | The target for the SLI (e.g., 99.9% success rate) |
| SLA (Service Level Agreement) | Contractual commitment with consequences for breach |

Set SLOs internally; only publish SLAs externally when commercially required.

## Common SLOs for Infrastructure

| Service | SLI | SLO Target |
|---|---|---|
| Web application | HTTP success rate | ≥ 99.9% over 30 days |
| API service | P99 latency | ≤ 500ms |
| Database | Query success rate | ≥ 99.95% |
| Storage | I/O error rate | ≤ 0.01% |
| Backup | Jobs completing within window | ≥ 99% |
| Network | Packet loss | ≤ 0.1% |
| DNS | Resolution success | ≥ 99.99% |

## Error Budget

**Azure Monitor — availability metric:**
```bash
az monitor metrics list \
  --resource <app-resource-id> \
  --metric Availability \
  --start-time 2026-05-01 \
  --end-time 2026-05-06 \
  --interval PT1H \
  --aggregation Average
```

## SLO Dashboard Requirements

Each SLO should have a dashboard panel showing:
1. Current SLI value vs SLO target (green/amber/red)
2. 30-day trend
3. Error budget remaining (% and absolute time/requests)
4. Recent incidents that consumed budget

## Alerting from SLOs

Alert on error budget burn rate — not just current SLI value:

| Burn Rate | Severity | Action |
|---|---|---|
| >14× | Critical | Page immediately — budget exhausted in <2 hours |
| >6× | High | Alert on-call — budget exhausted in <5 hours |
| >3× | Medium | Investigate — budget exhausted in <10 hours |
| <1× | OK | Normal operation |

## SLO Review Cadence

| Cadence | Action |
|---|---|
| Monthly | Review SLO compliance; update error budget tracking |
| Quarterly | Review whether targets are still appropriate |
| After major incident | Assess if SLO needs tightening or if it correctly reflected impact |
| Before major release | Assess risk to SLO; establish rollback threshold |
