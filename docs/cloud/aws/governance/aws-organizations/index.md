# AWS AWS Organizations

```
┌───────────────────────────────── AWS Governance — AWS Organizations ──────────────────────────────────┐
│                                                                                                       │
│  AWS Organizations manages multi-account hierarchy, SCPs, and consolidated billing.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Organization Structure            │  │           Service Control Policies          │   │
│   │            Root: single top-level            │  │          Attached: to OU or account         │   │
│   │          OUs: nested up to 5 levels          │  │        Effect: Deny or allow boundary       │   │
│   │             Accounts: leaf nodes             │  │      Inheritance: child inherits parent     │   │
│   │           Management: billing root           │  │         FullAWSAccess: default allow        │   │
│   │          Member: standard accounts           │  │           MFA enforcement example           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SCPs limit maximum permissions; IAM policies still needed to grant permissions                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Org-Wide Services               │  │              Account Management             │   │
│   │            CloudTrail: org trail             │  │          create-account: provision          │   │
│   │              Config: aggregator              │  │           move-account: change OU           │   │
│   │            GuardDuty: org enable             │  │         close-account: decommission         │   │
│   │           Security Hub: delegated            │  │        invite-account-to-organization       │   │
│   │          Backup: org backup policy           │  │          Tag policies: enforcement          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Organizations service (global) · SCP policy engine · all member accounts                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Root            = Top of OU hierarchy; SCPs here apply to every account in org                       │
│  OU              = Organizational Unit; groups accounts with common SCP requirements                  │
│  SCP             = Service Control Policy; restricts what actions accounts can perform                │
│  FullAWSAccess   = Default SCP allowing all actions; must be paired with deny SCPs                    │
│  SCP inheritance = Child OUs and accounts inherit all SCPs from parent OUs                            │
│  Delegated admin = Member account granted admin access for specific org services                      │
│  Org trail       = CloudTrail trail in management account capturing all member API calls              │
│  Tag policy      = Organizations policy enforcing tag key standardisation                             │
│  Backup policy   = Organizations policy deploying backup plans to member accounts                     │
│  close-account   = Initiates 90-day closure period; resources still accessible                        │
│  create-account  = Provisions new member account; email alias required                                │
│  Management account= Cannot have SCPs applied to it; exempt from OU restrictions                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
AWS Organizations: Root → OUs → Accounts → SCPs
──────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────┐
  │  Root (SCP: FullAWSAccess)                           │
  │  ┌────────────────────────────────────────────────┐  │
  │  │  OU: Production (SCP: deny-delete-cloudtrail)  │  │
  │  │  ┌──────────────────────────────────────────┐  │  │
  │  │  │ Account: prod-us-east-1                  │  │  │
  │  │  │ Account: prod-eu-west-1                  │  │  │
  │  │  └──────────────────────────────────────────┘  │  │
  │  └────────────────────────────────────────────────┘  │
  │  ┌────────────────────────────────────────────────┐  │
  │  │  OU: Development (SCP: deny-production-regions)│  │
  │  │  ┌──────────────────────────────────────────┐  │  │
  │  │  │ Account: dev-sandbox                     │  │  │
  │  │  └──────────────────────────────────────────┘  │  │
  │  └────────────────────────────────────────────────┘  │
  └──────────────────────────────────────────────────────┘

  SCP Evaluation (per request):
  Root SCP ──► OU SCP ──► Account SCP ──► IAM Policy
  All must Allow ──► access granted
  Any Deny ─────────────────────► access denied
```

## Overview

AWS AWS Organizations notes for day-to-day infrastructure operations.

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
