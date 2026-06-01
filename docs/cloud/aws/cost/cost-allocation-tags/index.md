# AWS Cost Allocation Tags


<div class="kb-summary">
AWS Cost Allocation Tags reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌─────────────────────────────────── AWS Cost — Cost Allocation Tags ───────────────────────────────────┐
│                                                                                                       │
│  Cost allocation tags enable chargeback and showback by team, environment, and project.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Tag Types                   │  │                Required Tags                │   │
│   │         AWS-generated: aws:createdBy         │  │          Environment: prod/dev/test         │   │
│   │          User-defined: custom keys           │  │            Owner: team or person            │   │
│   │         Activate: in Billing console         │  │           CostCentre: finance code          │   │
│   │           Appear in CUR within 24h           │  │          Application: workload name         │   │
│   │          Max 50 user-defined active          │  │         Project: initiative tracker         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Tags must be activated in Billing console before appearing in cost reports                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Enforcement                  │  │                  Reporting                  │   │
│   │        SCP: deny without required tag        │  │         Cost Explorer: group by tag         │   │
│   │          Config rule: required-tags          │  │         CUR: raw billing CSV/Parquet        │   │
│   │         Tag policy: org-level govern         │  │            Budgets: filter by tag           │   │
│   │         AWS Config remediation: auto         │  │           Athena: query CUR in S3           │   │
│   │          Tagging IaC: Terraform/CFN          │  │            QuickSight: dashboard            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Billing · S3 (CUR) · Athena · Cost Explorer · Config · Organizations                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cost allocation tag= Tag activated in Billing; appears as column in CUR and Explorer                 │
│  CUR             = Cost and Usage Report; detailed per-resource billing data                          │
│  Tag policy      = Organizations policy enforcing tag key case and allowed values                     │
│  required-tags   = AWS Config rule flagging resources missing mandatory tags                          │
│  Chargeback      = Billing teams for their actual AWS spend based on tags                             │
│  Showback        = Showing teams their spend without billing them directly                            │
│  Athena          = Serverless SQL query engine; queries CUR stored in S3                              │
│  QuickSight      = AWS BI tool; visualises CUR/Athena data as dashboards                              │
│  aws:createdBy   = AWS-generated tag showing IAM principal that created resource                      │
│  Activate in Billing= Required step to include user tag in cost reports                               │
│  Tag compliance  = % of resources with all required tags; tracked in Config                           │
│  IaC tagging     = Define required tags in Terraform/CloudFormation at resource level                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────── AWS Cost — Cost Allocation Tags ───────────────────────────────────┐
│                                                                                                       │
│  Cost allocation tags enable chargeback and showback by team, environment, and project.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Tag Types                   │  │                Required Tags                │   │
│   │         AWS-generated: aws:createdBy         │  │          Environment: prod/dev/test         │   │
│   │          User-defined: custom keys           │  │            Owner: team or person            │   │
│   │         Activate: in Billing console         │  │           CostCentre: finance code          │   │
│   │           Appear in CUR within 24h           │  │          Application: workload name         │   │
│   │          Max 50 user-defined active          │  │         Project: initiative tracker         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Tags must be activated in Billing console before appearing in cost reports                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Enforcement                  │  │                  Reporting                  │   │
│   │        SCP: deny without required tag        │  │         Cost Explorer: group by tag         │   │
│   │          Config rule: required-tags          │  │         CUR: raw billing CSV/Parquet        │   │
│   │         Tag policy: org-level govern         │  │            Budgets: filter by tag           │   │
│   │         AWS Config remediation: auto         │  │           Athena: query CUR in S3           │   │
│   │          Tagging IaC: Terraform/CFN          │  │            QuickSight: dashboard            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Billing · S3 (CUR) · Athena · Cost Explorer · Config · Organizations                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Cost allocation tag= Tag activated in Billing; appears as column in CUR and Explorer                 │
│  CUR             = Cost and Usage Report; detailed per-resource billing data                          │
│  Tag policy      = Organizations policy enforcing tag key case and allowed values                     │
│  required-tags   = AWS Config rule flagging resources missing mandatory tags                          │
│  Chargeback      = Billing teams for their actual AWS spend based on tags                             │
│  Showback        = Showing teams their spend without billing them directly                            │
│  Athena          = Serverless SQL query engine; queries CUR stored in S3                              │
│  QuickSight      = AWS BI tool; visualises CUR/Athena data as dashboards                              │
│  aws:createdBy   = AWS-generated tag showing IAM principal that created resource                      │
│  Activate in Billing= Required step to include user tag in cost reports                               │
│  Tag compliance  = % of resources with all required tags; tracked in Config                           │
│  IaC tagging     = Define required tags in Terraform/CloudFormation at resource level                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Cost Allocation Tags notes for day-to-day infrastructure operations.

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
