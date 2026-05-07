# Pure1 Standards

```mermaid
flowchart LR
    Pure1_Standards["Pure1 Standards"]
    Pure1_Standards --> S0["Array Tagging Policy"]
    Pure1_Standards --> S1["Capacity Threshold Standards"]
    Pure1_Standards --> S2["Alert Notification Routing"]
    Pure1_Standards --> S3["Health Score Standards"]
    Pure1_Standards --> S4["API Access Standards"]
    Pure1_Standards --> S5["Reporting Cadence"]
    Pure1_Standards --> S6["Purity Version Standards"]
    Pure1_Standards --> S7["Change Management"]
```

## Array Tagging Policy

Every FlashArray and FlashBlade registered in Pure1 must carry the three mandatory tags. Tags are used for reporting, alert routing, capacity forecasting by business unit, and chargeback.

| Tag Key | Required | Example Values |
|---|---|---|
| Site | Yes | `dc1`, `dc2`, `dr-site` |
| Environment | Yes | `prod`, `non-prod`, `dev` |
| Owner | Yes | `storage-ops`, `db-team`, `platform` |

Apply tags immediately after a new array appears in Pure1 (within 24 hours of onboarding).

Monthly tag compliance check:

```bash
# Using Pure1 REST API to find untagged arrays
# See scripts/pure1/tag_compliance.py
```

## Capacity Threshold Standards

| Metric | Warning | Critical | Action |
|---|---|---|---|
| Usable capacity used | 70% | 85% | Warning: track; Critical: raise capacity planning request same day |
| Data reduction ratio decline | > 15% below 30-day baseline | > 25% decline | Investigate workload change; review dedup/compression settings |
| Days to capacity exhaustion | 45 days | 15 days | 45 days: plan expansion; 15 days: emergency action |

Capacity alerts are configured in **Pure1 > Administration > Notifications** with severity-based routing.

## Alert Notification Routing

| Severity | Channel | SLA |
|---|---|---|
| CRITICAL | PagerDuty (on-call) + ServiceNow incident | Acknowledge within 15 minutes |
| WARNING | Email — storage-ops distribution list | Review within 4 hours |
| INFO | Pure1 portal only | Review in daily checklist |

Notification rules are configured per array tag filter (e.g., separate rules for prod vs. non-prod).

## Health Score Standards

Pure1 array health is expressed as a pass/fail component health model rather than a numerical score. The equivalent operational thresholds:

| Array Status | Action |
|---|---|
| Healthy (all components green) | Normal monitoring |
| Degraded (non-critical component fault) | Raise in daily stand-up; investigate within 4 hours |
| Error / Critical fault | Raise ServiceNow incident immediately; engage Pure Storage support |

## API Access Standards

- One API service account per consuming system (Splunk, Grafana, automation scripts, Aria Operations)
- API keys are RSA private keys — store securely in the secrets manager (not in filesystem or repos)
- Rotation schedule: annual; rotation dates tracked in the credential register
- Read-only API access for monitoring and reporting; no write access unless required

## Reporting Cadence

| Report | Schedule | Format | Audience |
|---|---|---|---|
| Weekly Capacity Report | Weekly (Monday 07:00) | Email + CSV | Storage team |
| Monthly Fleet Health Summary | Monthly, 1st working day | PDF | Storage team + management |
| Capacity Trend Archive | Weekly (automated script) | CSV → shared drive | Capacity planning |

Reports are generated via the `pure1_capacity_report.py` script and distributed via email. Archive capacity trend data to the shared drive for 2-year retention.

## Purity Version Standards

- Production arrays: must be on a supported Purity release (not EOS)
- Non-production arrays: may lag production by one minor version
- All arrays: plan upgrades within 6 months of EOS announcement
- Review Pure Storage release calendar quarterly

## Change Management

All planned Purity upgrades and array configuration changes must be logged in ServiceNow as standard change records. Emergency changes (e.g., critical patch) use the emergency change process with post-change documentation within 24 hours.
