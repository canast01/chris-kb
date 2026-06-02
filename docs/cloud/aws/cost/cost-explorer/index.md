# AWS Cost Explorer


<div class="kb-summary">
AWS Cost Explorer reference covering Overview, Daily Checks, Operational Tasks, Common Issues, Maintenance Notes.
</div>

```
┌────────────────────────────────────── AWS Cost — Cost Explorer ───────────────────────────────────────┐
│                                                                                                       │
│  Cost Explorer visualises and analyses AWS spend with filtering, grouping, and forecasts.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Visualisation                 │  │            Filtering and Grouping           │   │
│   │          Bar/line: daily or monthly          │  │          Group by: service, account         │   │
│   │         Date range: up to 13 months          │  │              Group by: tag key              │   │
│   │          Granularity: daily/monthly          │  │           Filter: region, AZ, type          │   │
│   │          Forecast: 12 months ahead           │  │            Filter: linked account           │   │
│   │          Saved reports: share views          │  │             API: GetCostAndUsage            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Explorer shows 13 months history; use API for programmatic cost data retrieval                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             RI and Savings Plans             │  │                 Right-Sizing                │   │
│   │            RI utilisation report             │  │          Right-size: underused EC2          │   │
│   │              RI coverage report              │  │        Recommendations: instance type       │   │
│   │            SP utilisation report             │  │          Savings: projected savings         │   │
│   │           SP recommendations: buy            │  │        CloudWatch CPU: low util flag        │   │
│   │          Amortised vs blended cost           │  │         Memory: CloudWatch agent req        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Billing data pipeline · Cost Explorer service · CUR S3 bucket                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cost Explorer    = Console and API for visualising and analysing AWS spend                           │
│  Granularity      = Daily shows day-level detail; monthly aggregates per calendar month               │
│  Amortised cost   = RI upfront fee spread across the reservation term                                 │
│  Blended rate     = Average effective rate across reserved and on-demand instances                    │
│  RI utilisation   = % of purchased reserved instance hours consumed                                   │
│  RI coverage      = % of eligible on-demand spend covered by reservations                             │
│  SP recommendation= Suggested Savings Plans commitment to reduce on-demand spend                      │
│  Right-sizing     = Identifying over-provisioned instances to downsize                                │
│  GetCostAndUsage  = API returning cost data with same filters as console                              │
│  Saved report     = Stored filter/group configuration; shareable via URL                              │
│  Forecast         = ML projection of future spend based on historical trends                          │
│  CUR             = Cost and Usage Report; raw billing data backing Explorer                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Cost Explorer is a core cloud infrastructure service used for production operations, automation, monitoring, and platform support.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review service health |  |  |
| Check active alerts |  |  |
| Validate access permissions |  |  |
| Confirm backup or recovery coverage where applicable |  |  |
| Review recent configuration changes |  |  |

## Operational Tasks


| Task | Command |
|---|---|
| Confirm resource status |  |
| Review logs and metrics |  |
| Validate security configuration |  |
| Check cost or capacity trends |  |
| Document changes |  |

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| Access denied | IAM or RBAC issue | Review permissions |
| Service unavailable | Regional or dependency issue | Check service health |
| High cost | Resource growth or unused assets | Review usage and tagging |
| Connectivity failure | Network or security rule issue | Validate routes and rules |

## Maintenance Notes

- Review configuration before changes
- Validate rollback plan
- Test in non-production where possible
- Confirm monitoring after changes
