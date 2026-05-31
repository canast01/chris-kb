# AWS Account Structure

```text
┌───────────────────────────────── AWS Governance — Account Structure ──────────────────────────────────┐
│                                                                                                       │
│  Multi-account structure with OU hierarchy isolating workloads by env and function.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 OU Hierarchy                 │  │             Foundation Accounts             │   │
│   │             Root: org top level              │  │          Management: billing + org          │   │
│   │          Security OU: tooling accts          │  │          Log Archive: central logs          │   │
│   │          Infrastructure OU: shared           │  │           Audit/Security: tooling           │   │
│   │          Workloads OU: per team/env          │  │         Network: TGW + DirectConnect        │   │
│   │          Sandbox OU: dev/experiment          │  │           Shared Services: DNS/AD           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Foundation accounts built first; workload accounts provisioned per team or environment               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Account Vending                │  │                  Guardrails                 │   │
│   │           Control Tower: automated           │  │            SCPs: preventive at OU           │   │
│   │          Account Factory: template           │  │           Config rules: detective           │   │
│   │           IAM Identity Center: SSO           │  │           Security Hub: aggregated          │   │
│   │           Email alias: per account           │  │             CloudTrail: org-wide            │   │
│   │          CMDB: register new account          │  │            GuardDuty: org-enabled           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Organizations · Control Tower · IAM Identity Center · CloudTrail · Config                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OU              = Organizational Unit; logical account grouping with shared SCPs                     │
│  Management account= Root of AWS Organization; no workloads; billing owner                            │
│  Log Archive     = Account receiving all org CloudTrail and Config delivery                           │
│  Control Tower   = AWS service automating multi-account setup with guardrails                         │
│  Account Factory = Control Tower feature provisioning accounts from template                          │
│  Account vending = Automated process for provisioning a new AWS account to spec                       │
│  SCP             = Service Control Policy; preventive restriction at OU level                         │
│  Network OU      = Dedicated OU for Transit Gateway and connectivity accounts                         │
│  Sandbox OU      = Isolated OU with relaxed SCPs for experimentation                                  │
│  Email alias     = Shared mailbox per account; avoids personal email as owner                         │
│  CMDB            = Configuration Management Database; records account metadata                        │
│  Security Hub org= Aggregates security findings from all accounts in organisation                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
AWS Account Structure: Management → OUs → Members
──────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────┐
  │  Management Account (Root)                          │
  │  Billing, SCPs, Organizations                       │
  └───────────────────────┬──────────────────────────────┘
             ┌────────────┼──────────────────┐
             ▼            ▼                  ▼
  ┌──────────────┐ ┌─────────────┐ ┌─────────────────┐
  │  OU: Security│ │ OU: Workload│ │ OU: Sandbox     │
  │              │ │             │ │                 │
  │ ┌──────────┐ │ │ ┌─────────┐ │ │ ┌─────────────┐ │
  │ │ Log      │ │ │ │ Prod    │ │ │ │ Developer   │ │
  │ │ Archive  │ │ │ │ Account │ │ │ │ Accounts    │ │
  │ │ Account  │ │ │ └─────────┘ │ │ └─────────────┘ │
  │ └──────────┘ │ │ ┌─────────┐ │ └─────────────────┘
  │ ┌──────────┐ │ │ │ Staging │ │
  │ │ Audit    │ │ │ │ Account │ │
  │ │ Account  │ │ │ └─────────┘ │
  │ └──────────┘ │ │ ┌─────────┐ │
  └──────────────┘ │ │ Dev     │ │
                   │ │ Account │ │
                   │ └─────────┘ │
                   └─────────────┘
```

## Overview

AWS Account Structure notes for day-to-day infrastructure operations.

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
