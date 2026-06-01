# AWS Cost Explorer / Billing


<div class="kb-summary">
AWS Cost Explorer / Billing reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌────────────────────────────────── AWS Cost — Cost Explorer Billing ───────────────────────────────────┐
│                                                                                                       │
│  Billing console: invoices, payment methods, tax settings, and consolidated billing.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Billing Console                │  │             Consolidated Billing            │   │
│   │          Invoices: monthly PDF/CSV           │  │          Org: single payer account          │   │
│   │           Payment: credit card/ACH           │  │           Volume discounts: pooled          │   │
│   │            Tax: VAT/GST settings             │  │         RI sharing: across accounts         │   │
│   │           Credits: applied balance           │  │             SP sharing: org-wide            │   │
│   │           Free tier: usage tracker           │  │         Billing entity: per account         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Management account pays consolidated bill; member accounts see their own usage                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Cost and Usage Report             │  │               FinOps Practices              │   │
│   │          CUR: granular billing CSV           │  │          Monthly review: all teams          │   │
│   │          S3 bucket: daily delivery           │  │        Chargeback: tag-based billing        │   │
│   │          Parquet: Athena-optimised           │  │        Forecasting: budget vs actual        │   │
│   │            Resource IDs: enabled             │  │        Unit economics: cost per unit        │   │
│   │         Versioning: overwrite/create         │  │        Waste: delete unused resources       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Billing service · S3 (CUR) · Athena · management account payment rails                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CUR             = Cost and Usage Report; most granular billing data available                        │
│  Consolidated billing= Single monthly invoice for all org accounts via management account             │
│  RI sharing      = Reserved instances purchased in one account benefit all org accounts               │
│  SP sharing      = Savings Plans apply to any account in the org by default                           │
│  Volume discount = AWS applies tiered pricing based on total org usage                                │
│  Chargeback      = Internally billing teams for their AWS spend via cost allocation                   │
│  Unit economics  = Cost per transaction, per user, or per API call                                    │
│  Free tier tracker= Billing console shows how close each service is to free tier limit                │
│  Tax settings    = VAT/GST registration applied to invoices by region                                 │
│  Credits         = AWS promotional credits applied before charging payment method                     │
│  Parquet format  = Columnar CUR format; faster Athena queries and lower S3 cost                       │
│  Resource IDs    = CUR option adding AWS resource ARN to each billing line item                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────── AWS Cost — Cost Explorer Billing ───────────────────────────────────┐
│                                                                                                       │
│  Billing console: invoices, payment methods, tax settings, and consolidated billing.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Billing Console                │  │             Consolidated Billing            │   │
│   │          Invoices: monthly PDF/CSV           │  │          Org: single payer account          │   │
│   │           Payment: credit card/ACH           │  │           Volume discounts: pooled          │   │
│   │            Tax: VAT/GST settings             │  │         RI sharing: across accounts         │   │
│   │           Credits: applied balance           │  │             SP sharing: org-wide            │   │
│   │           Free tier: usage tracker           │  │         Billing entity: per account         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Management account pays consolidated bill; member accounts see their own usage                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Cost and Usage Report             │  │               FinOps Practices              │   │
│   │          CUR: granular billing CSV           │  │          Monthly review: all teams          │   │
│   │          S3 bucket: daily delivery           │  │        Chargeback: tag-based billing        │   │
│   │          Parquet: Athena-optimised           │  │        Forecasting: budget vs actual        │   │
│   │            Resource IDs: enabled             │  │        Unit economics: cost per unit        │   │
│   │         Versioning: overwrite/create         │  │        Waste: delete unused resources       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Billing service · S3 (CUR) · Athena · management account payment rails                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CUR             = Cost and Usage Report; most granular billing data available                        │
│  Consolidated billing= Single monthly invoice for all org accounts via management account             │
│  RI sharing      = Reserved instances purchased in one account benefit all org accounts               │
│  SP sharing      = Savings Plans apply to any account in the org by default                           │
│  Volume discount = AWS applies tiered pricing based on total org usage                                │
│  Chargeback      = Internally billing teams for their AWS spend via cost allocation                   │
│  Unit economics  = Cost per transaction, per user, or per API call                                    │
│  Free tier tracker= Billing console shows how close each service is to free tier limit                │
│  Tax settings    = VAT/GST registration applied to invoices by region                                 │
│  Credits         = AWS promotional credits applied before charging payment method                     │
│  Parquet format  = Columnar CUR format; faster Athena queries and lower S3 cost                       │
│  Resource IDs    = CUR option adding AWS resource ARN to each billing line item                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Cost Explorer / Billing notes for day-to-day infrastructure operations.

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
