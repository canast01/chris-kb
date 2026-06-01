# AWS Service Control Policies


<div class="kb-summary">
AWS Service Control Policies reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌────────────────────────────── AWS Governance — Service Control Policies ──────────────────────────────┐
│                                                                                                       │
│  SCPs define maximum permissions for OUs and accounts; deny by default override IAM.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                SCP Mechanics                 │  │             Common SCP Patterns             │   │
│   │         Allow list: explicit permits         │  │         Deny leave org: prevent exit        │   │
│   │          Deny list: explicit blocks          │  │          Require MFA: sensitive ops         │   │
│   │           Deny overrides IAM allow           │  │          Region lock: approved only         │   │
│   │             Root user not exempt             │  │        Protect CloudTrail: no delete        │   │
│   │            Management acct exempt            │  │           Block untagged resources          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Deny list strategy: start with FullAWSAccess then attach deny SCPs on top                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SCP Design                  │  │            Testing and Operations           │   │
│   │           Conditions: MFA, IP, tag           │  │           IAM simulator: test SCP           │   │
│   │           NotAction: invert match            │  │          Dry run: sandbox OU first          │   │
│   │         Resource: specific ARN scope         │  │         CloudTrail: SCP deny events         │   │
│   │          Principal: all (*) typical          │  │        AccessDenied: check SCP first        │   │
│   │        Tag condition: enforce tagging        │  │        Document: why each SCP exists        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Organizations SCP engine · IAM policy evaluator · CloudTrail · all accounts                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SCP             = Service Control Policy; restricts max permissions in accounts/OUs                  │
│  Allow list SCP  = Only listed actions permitted; everything else implicitly denied                   │
│  Deny list SCP   = Specific actions denied; FullAWSAccess permits everything else                     │
│  FullAWSAccess   = Default SCP allowing all actions; must be on root OU                               │
│  Root user exempt= SCP applies to root user of member accounts (not management)                       │
│  Management exempt= Management account not subject to any SCP                                         │
│  Region lock     = SCP denying all actions outside approved AWS regions                               │
│  NotAction       = SCP element matching everything except listed actions                              │
│  Condition       = JSON condition block; e.g. aws:MultiFactorAuthPresent: true                        │
│  IAM simulator   = Tests SCP effect on specific API calls before applying                             │
│  Dry run         = Apply SCP to sandbox OU containing test accounts first                             │
│  AccessDenied    = Error returned when SCP blocks an action; check Organizations                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────── AWS Governance — Service Control Policies ──────────────────────────────┐
│                                                                                                       │
│  SCPs define maximum permissions for OUs and accounts; deny by default override IAM.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                SCP Mechanics                 │  │             Common SCP Patterns             │   │
│   │         Allow list: explicit permits         │  │         Deny leave org: prevent exit        │   │
│   │          Deny list: explicit blocks          │  │          Require MFA: sensitive ops         │   │
│   │           Deny overrides IAM allow           │  │          Region lock: approved only         │   │
│   │             Root user not exempt             │  │        Protect CloudTrail: no delete        │   │
│   │            Management acct exempt            │  │           Block untagged resources          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Deny list strategy: start with FullAWSAccess then attach deny SCPs on top                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  SCP Design                  │  │            Testing and Operations           │   │
│   │           Conditions: MFA, IP, tag           │  │           IAM simulator: test SCP           │   │
│   │           NotAction: invert match            │  │          Dry run: sandbox OU first          │   │
│   │         Resource: specific ARN scope         │  │         CloudTrail: SCP deny events         │   │
│   │          Principal: all (*) typical          │  │        AccessDenied: check SCP first        │   │
│   │        Tag condition: enforce tagging        │  │        Document: why each SCP exists        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Organizations SCP engine · IAM policy evaluator · CloudTrail · all accounts                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SCP             = Service Control Policy; restricts max permissions in accounts/OUs                  │
│  Allow list SCP  = Only listed actions permitted; everything else implicitly denied                   │
│  Deny list SCP   = Specific actions denied; FullAWSAccess permits everything else                     │
│  FullAWSAccess   = Default SCP allowing all actions; must be on root OU                               │
│  Root user exempt= SCP applies to root user of member accounts (not management)                       │
│  Management exempt= Management account not subject to any SCP                                         │
│  Region lock     = SCP denying all actions outside approved AWS regions                               │
│  NotAction       = SCP element matching everything except listed actions                              │
│  Condition       = JSON condition block; e.g. aws:MultiFactorAuthPresent: true                        │
│  IAM simulator   = Tests SCP effect on specific API calls before applying                             │
│  Dry run         = Apply SCP to sandbox OU containing test accounts first                             │
│  AccessDenied    = Error returned when SCP blocks an action; check Organizations                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Service Control Policies notes for day-to-day infrastructure operations.

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
