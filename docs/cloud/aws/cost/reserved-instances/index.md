# AWS Reserved Instances


<div class="kb-summary">
AWS Reserved Instances reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌──────────────────────────────────── AWS Cost — Reserved Instances ────────────────────────────────────┐
│                                                                                                       │
│  Reserved Instances provide up to 72% EC2 discount for 1- or 3-year commitments.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   RI Types                   │  │               Payment Options               │   │
│   │        Standard: fixed instance type         │  │          All upfront: max discount          │   │
│   │          Convertible: change family          │  │           Partial upfront: hybrid           │   │
│   │          Zonal: capacity reserve AZ          │  │         No upfront: monthly billing         │   │
│   │         Regional: flexible AZ usage          │  │            1-year: ~40% discount            │   │
│   │        Also: RDS/ElastiCache/Redshift        │  │          3-year: up to 72% discount         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Regional RIs flexible across AZ and size; Zonal RIs reserve capacity in specific AZ                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Management                  │  │                Best Practices               │   │
│   │        RI Marketplace: resell unused         │  │         Convertible for flexibility         │   │
│   │         Utilisation report: coverage         │  │         Baseline: commit stable load        │   │
│   │         Coverage report: % reserved          │  │           Spiky: on-demand + spot           │   │
│   │         Org sharing: across accounts         │  │        Review: quarterly utilisation        │   │
│   │            Modify: split or merge            │  │        Savings Plans: often preferred       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS EC2 capacity pool · billing system · RI Marketplace · Cost Explorer                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Standard RI     = Fixed instance family/size; largest discount; not exchangeable                     │
│  Convertible RI  = Can exchange for different family/size/OS; ~54% max discount                       │
│  Zonal RI        = Reserves capacity in specific AZ; smaller size flexibility                         │
│  Regional RI     = Applies to any AZ in region; size-flexible within family                           │
│  All upfront     = Entire term cost paid day 1; maximum discount                                      │
│  RI Marketplace  = AWS marketplace to sell unused Standard RIs to other customers                     │
│  Utilisation     = % of reserved hours consumed; low = wasted spend                                   │
│  Coverage        = % of eligible usage covered by RIs vs on-demand                                    │
│  Org sharing     = RI discount applies to any account in the organisation                             │
│  Savings Plans   = More flexible alternative; recommended over RIs for most workloads                 │
│  Baseline load   = Steady minimum usage; appropriate to commit with RIs                               │
│  Modify RI       = Split one RI into smaller sizes or merge smaller into larger                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Reserved Instances notes for day-to-day infrastructure operations.

## Where It Fits

Use this page for build work, support checks, troubleshooting, standards, and operational review.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Confirm service health. |  |  |
| Review alerts. |  |  |
| Check recent changes. |  |  |
| Confirm capacity and performance are within normal range. |  |  |

## Health Commands

~~~bash
# Add environment-specific commands here
~~~

## Common Issues

- Misconfiguration after change work.
- Missing access or permissions.
- Alert noise without clear ownership.
- Drift from documented standards.

## Operational Tasks


| Task | Command |
|---|---|
| Review current configuration. |  |
| Validate dependencies. |  |
| Record changes. |  |
| Confirm monitoring coverage. |  |

## Upgrade Notes

- Check release notes before upgrades.
- Validate backup or rollback options.
- Confirm maintenance window and communication plan.
- Test after the change.

## Best Practices


| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Document ownership. | Document ownership. |
| Use least privilege access. | Use least privilege access. |
| Validate changes after implementation. | Validate changes after implementation. |
