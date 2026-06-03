# AWS Savings Plans


<div class="kb-summary">
AWS Savings Plans reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌────────────────────────────────────── AWS Cost — Savings Plans ───────────────────────────────────────┐
│                                                                                                       │
│  Savings Plans commit $/hour across EC2, Lambda, and Fargate for up to 66% savings.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Plan Types                  │  │              Commitment Options             │   │
│   │        Compute SP: EC2+Lambda+Fargate        │  │              Term: 1 or 3 years             │   │
│   │         EC2 Instance SP: per family          │  │        Payment: upfront/partial/none        │   │
│   │          SageMaker SP: ML workloads          │  │           Commit: $/hour threshold          │   │
│   │          Compute SP: 66% max saving          │  │         Flexible: any region/AZ/size        │   │
│   │         EC2 Instance SP: 72% saving          │  │            Org-wide: all accounts           │   │
│   └──────────────────────────────────────────────┘  ┌─────────────────────────────────────────────┐   │
│                                                                                                       │
│  Compute SP most flexible; EC2 Instance SP gives highest discount for locked family                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Management                  │  │                Best Practices               │   │
│   │        Recommendations: Cost Explorer        │  │           Analyse 3 months history          │   │
│   │        Utilisation report: coverage %        │  │          Commit to stable baseline          │   │
│   │         Coverage report: % of spend          │  │         Spiky load: on-demand + spot        │   │
│   │          Inventory: purchased plans          │  │        Quarterly review: utilisation        │   │
│   │         No marketplace: non-sellable         │  │         Prefer Compute SP: flexible         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS billing system · Cost Explorer · EC2/Lambda/Fargate capacity                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Compute SP      = Most flexible; applies to any EC2 family, Lambda, Fargate                          │
│  EC2 Instance SP = Locked to one instance family in one region; highest discount                      │
│  SageMaker SP    = Applies to SageMaker ML instance usage                                             │
│  Commitment $/hr = Hourly spend you agree to pay; usage below = wasted                                │
│  Utilisation     = % of commitment consumed; target > 80%                                             │
│  Coverage        = % of eligible spend covered by Savings Plans                                       │
│  On-demand top-up= Usage above commitment charges at on-demand rate                                   │
│  Org-wide sharing= SP purchased in management or any account applies org-wide                         │
│  No Marketplace  = Unlike RIs, Savings Plans cannot be resold; permanent commitment                   │
│  3-year term     = Longer commitment; higher discount; appropriate for stable services                │
│  Baseline        = Minimum consistent usage; commit $/hr equal to baseline cost                       │
│  Cost Explorer rec= Suggests optimal SP type and amount based on usage history                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Savings Plans notes for day-to-day infrastructure operations.

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

```bash
# Add environment-specific commands here
```

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
