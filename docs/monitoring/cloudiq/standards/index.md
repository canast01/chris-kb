# CloudIQ Standards
## System Tagging Policy

Every system onboarded to CloudIQ must be tagged with the three mandatory tags before being considered operational. Tags enable reporting, alert routing, and capacity forecasting by site, environment, and team.

| Tag Key | Required | Example Values |
|---|---|---|
| Site | Yes | `dc1`, `dc2`, `dr-site` |
| Environment | Yes | `prod`, `non-prod`, `dev` |
| Team | Yes | `storage-ops`, `db-team`, `platform` |

Apply tags immediately after onboarding a system:

```text
CloudIQ portal > Assets > [System] > Tags > Add Tag
```

Untagged systems must be remediated within 48 hours of onboarding. Monthly audit: report on untagged systems via REST API or dashboard filter.

## Health Score Thresholds

Health scores run from 0–100. The following thresholds drive operational response.

| Health Score | Status | Action Required |
|---|---|---|
| 90–100 | Healthy | Normal monitoring |
| 80–89 | Needs Attention | Review in next weekly ops meeting |
| 60–79 | At Risk | Investigate within 48 hours; raise in daily stand-up |
| Below 60 | Critical | Raise incident in ServiceNow; investigate same business day |

## Alert Notification Routing

| Severity | Notification Channel | SLA |
|---|---|---|
| CRITICAL | PagerDuty (on-call rotation) | Acknowledge within 15 minutes |
| WARNING | Email — storage-ops distribution list | Review within 4 hours |
| INFO | CloudIQ portal only | Review in daily checklist |

Notification rules are configured in **CloudIQ portal > Settings > Notifications**. Each rule must be documented with the owner team and review date.

## Capacity Warning Levels

| Metric | Warning Threshold | Critical Threshold |
|---|---|---|
| Usable capacity used | 70% | 85% |
| Raw capacity used | 75% | 90% |
| Virtual pool used | 70% | 85% |
| Data reduction ratio decline | > 20% drop from 30-day baseline | > 30% drop |

Capacity alerts at WARNING trigger an email to the storage team. CRITICAL triggers a ServiceNow incident and PagerDuty page.

## Dashboard Standards

| Dashboard | Purpose | Owner | Review Frequency |
|---|---|---|---|
| CloudIQ Fleet Overview | All systems health score summary | Storage team | Daily |
| Capacity Trend | 30/60/90 day capacity trends per system type | Storage team | Weekly |
| AIOps Recommendations | Active AI-driven recommendations | Storage team | Daily |

Dashboards are named using the convention `CloudIQ-[Topic]-[Scope]`.

## API Access Policy

- One API client per consuming system (Splunk, Grafana, automation scripts)
- Client secrets stored in the team secrets manager; never committed to code repositories
- Rotation schedule: every 12 months; rotation date tracked in the credential register
- Read-only scope for all monitoring/reporting clients; write scope requires additional justification

## Change Management Integration

CRITICAL health score alerts and High AIOps recommendations that require infrastructure changes must be actioned via the standard change management process:

1. Raise a ServiceNow change request referencing the CloudIQ alert/recommendation
2. Obtain change approval before making changes to production systems
3. Close the change record with outcome notes after completion
