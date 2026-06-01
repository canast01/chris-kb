# Service Availability Monitoring


<div class="kb-summary">
Service Availability Monitoring reference covering Availability Calculation, Uptime Monitoring Tools, Azure Monitor — Availability Test, AWS Route 53 Health Checks, Availability Incident Tracking and 1 more sections.
</div>

## Availability Calculation

```text
Availability % = (Total time - Downtime) / Total time × 100

99.9%  → 8.7 hours downtime/year (43.8 min/month)
99.95% → 4.4 hours downtime/year (21.9 min/month)
99.99% → 52 minutes downtime/year (4.4 min/month)
```
┌───────────────────────────────── Performance — Service Availability ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Measure and report service availability; track downtime; compare against SLA targets     │   │
│   │     Availability = (total time - downtime) / total time * 100; track per service per month    │   │
│   │         Planned maintenance excluded from calculation if pre-approved and communicated        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Availability Tiers              │  │                 Measurement                 │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           99.9% = 8.7h/yr downtime           │  │           Monitor: synthetic check          │   │
│   │               99.95% = 4.4h/yr               │  │          Log outage: start/end time         │   │
│   │              99.99% = 52 min/yr              │  │          Calculate monthly percent          │   │
│   │             99.999% = 5.2 min/yr             │  │            Report to stakeholders           │   │
│   │           Target per service tier            │  │             Trend vs SLA target             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │   Availability   │   Downtime/yr    │    Downtime/mo    │       Tier       │     Example      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      99.9%       │    8.7 hours     │      43.8 min     │     Standard     │     Dev/test     │   │
│   │      99.95%      │    4.4 hours     │      21.9 min     │     Business     │  Internal apps   │   │
│   │      99.99%      │      52 min      │      4.4 min      │     Critical     │  Prod services   │   │
│   │     99.999%      │     5.2 min      │       26 sec      │     Mission      │    Core infra    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Synthetic check = Automated probe that tests service endpoint; detects outages before users        │
│    Maintenance window= Planned downtime; communicated in advance; excluded from availability calc     │
│    Error budget  = 1 - SLO; allowable downtime; consumed by incidents and planned maintenance         │
│    Nines         = Number of 9s in availability %; four nines (99.99%) = 52 min/yr max                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```powershell

## AWS Route 53 Health Checks

```bash
# Create HTTP health check
aws route53 create-health-check \
  --caller-reference "$(date +%s)" \
  --health-check-config '{
    "Type": "HTTPS",
    "FullyQualifiedDomainName": "<app-host>",
    "Port": 443,
    "ResourcePath": "/health",
    "RequestInterval": 30,
    "FailureThreshold": 3
  }'

# Get health check status
aws route53 get-health-check-status --health-check-id <id> \
  --query 'HealthCheckObservations[*].{Region:Region,Status:StatusReport.Status}'
```

## Availability Incident Tracking

```markdown
Incident:       APP-2026-042
Service:        ERP Application
Start time:     2026-05-05 14:23 UTC
End time:       2026-05-05 15:07 UTC
Downtime:       44 minutes
SLO impact:     Monthly budget: 43.8 min — budget consumed 100%
Root cause:     Database connection pool exhausted due to slow query
Detection:      Monitoring alert fired at 14:24 (1 min after start)
Resolution:     Restarted connection pool; fixed query index
```

## Reporting

| Report | Frequency | Audience |
|---|---|---|
| Availability dashboard | Real-time | Operations team |
| Monthly SLO compliance | Monthly | Management, service owners |
| Incident post-mortem | After each P1/P2 | Management, tech leads |
| Quarterly availability trend | Quarterly | CISO, IT management |
