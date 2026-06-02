# Pure1 Standards


<div class="kb-summary">
Pure1 Standards reference covering Array Tagging Policy, Capacity Threshold Standards, Alert Notification Routing, Health Score Standards, API Access Standards and 3 more sections.
</div>

```
┌────────────────────────────────────── Pure1 — Design Standards ───────────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Registration Standards            │  │               Alert Standards               │   │
│   │             All arrays in Pure1              │  │              Email ops-storage@             │   │
│   │              Phonehome verified              │  │               ITSM webhook set              │   │
│   │            TCP 443 open outbound             │  │              Auto-case enabled              │   │
│   │              Tag env + location              │  │                Review weekly                │   │
│   │             Service account API              │  │            Capacity plan monthly            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  All FlashArrays and FlashBlades on TCP 443 to pure1.purestorage.com                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Phonehome verified = Array shows Connected; data age < 2 min in Pure1 UI                             │
│  ITSM webhook = Pure1 webhook configured to create ServiceNow incident on alert                       │
│  Auto-case enabled = Pure1 setting allowing automatic TAC case opening                                │
│  Tag = Pure1 org labels by env (prod/dev), location (dc1/dc2), and team                               │
│  Service account = Non-personal Pure1 account for API registration                                    │
│  Weekly review = Review Pure1 fleet health and open proactive alerts every Monday                     │
│  Capacity monthly = Monthly export of Pure1 forecast data for procurement planning                    │
│  Purity current = All arrays on supported Purity release; Pure1 flags end-of-life                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
