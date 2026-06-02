---
title: AWS Identity — IAM
---

# AWS Identity — IAM


<div class="kb-summary">
IAM reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────────────────── AWS Identity — IAM ──────────────────────────────────────────┐
│                                                                                                       │
│  IAM: users, roles, groups, and policies controlling all AWS API access.                              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                IAM Principals                │  │                 Policy Types                │   │
│   │         Users: human + programmatic          │  │       Identity: attached to user/role       │   │
│   │         Roles: service or cross-acct         │  │           Resource: on S3/KMS/SQS           │   │
│   │           Groups: user collections           │  │            SCP: OU-level boundary           │   │
│   │         Service accounts: automation         │  │          Permission boundary: limit         │   │
│   │            Root: avoid; use roles            │  │         Session: AssumeRole context         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Effective permissions = intersection of all applicable policy types                                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Policy Evaluation               │  │                Best Practices               │   │
│   │        1. Explicit deny: always wins         │  │        Least privilege: minimal perms       │   │
│   │              2. SCP: must allow              │  │       Roles over users: no static keys      │   │
│   │           3. Resource policy check           │  │        Groups: manage at group level        │   │
│   │            4. Permission boundary            │  │         No wildcard: specify actions        │   │
│   │          5. Identity policy: allow           │  │           Review: quarterly unused          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  IAM service (global, free) · STS · CloudTrail · IAM Access Analyzer                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Principal       = Entity making AWS API request: user, role, service, account                        │
│  Policy          = JSON document defining allowed or denied actions on resources                      │
│  Managed policy  = Standalone reusable policy; AWS-managed or customer-managed                        │
│  Inline policy   = Embedded directly in user/role; deleted with the principal                         │
│  Permission boundary= IAM policy capping max permissions a principal can have                         │
│  IAM Access Analyzer= Identifies resources accessible from outside the account                        │
│  Explicit deny   = Deny statement that always overrides any allow                                     │
│  Policy evaluation= Order: explicit deny → SCP → resource policy → boundary → identity                │
│  Least privilege = Grant only permissions required for the specific task                              │
│  IAM group       = Collection of users inheriting same policies; simplifies management                │
│  Service role    = IAM role a service (Lambda, EC2) assumes to call other services                    │
│  Root user       = Account owner; has full access; protect with MFA; do not use daily                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS IAM notes for day-to-day infrastructure operations.

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

---

## IAM Identity Model



---

## IAM Policy Evaluation Order

```
┌──────────────────────────────── IAM Policy Evaluation — Decision Flow ────────────────────────────────┐
│                                                                                                       │
│    Every AWS API call follows this exact evaluation order; explicit deny always wins.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      Evaluation Steps (in order)             │  │      Details                                │   │
│   │  1. Explicit Deny in any policy              │  │  Any deny = DENY; no override               │   │
│   │  2. AWS Organizations SCP                    │  │  Must allow the action at OU level          │   │
│   │  3. Resource-based policy                    │  │  S3 bucket/KMS key/SQS policy check         │   │
│   │  4. IAM Permission Boundary                  │  │  Sets maximum allowed permissions           │   │
│   │  5. Session Policy (AssumeRole)              │  │  Further limits role session                │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    After step 5: if no explicit allow found in identity policy, default = DENY.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      Common Deny Scenarios                   │  │      Common Allow Scenarios                 │   │
│   │  SCP blocks action in OU                     │  │  SCP allows + identity policy allows        │   │
│   │  Explicit Deny in identity policy            │  │  Resource policy grants cross-account       │   │
│   │  Permission boundary excludes action         │  │  Role trust policy allows AssumeRole        │   │
│   │  No identity policy allows action            │  │  Session + identity policy both allow       │   │
│   │  KMS key policy denies user access           │  │  Least privilege: narrowest allow set       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    IAM policy engine (global service) · STS · CloudTrail logging all API decisions                    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Explicit Deny   = Deny statement in any policy; overrides all allows; step 1                       │
│    SCP             = Service Control Policy; restricts max perms at OU/account level                  │
│    Resource policy = Policy attached to a resource (S3, KMS); can allow cross-account                 │
│    Permission boundary = IAM policy capping the maximum perms a principal can have                    │
│    Session policy  = Passed during AssumeRole; further restricts session permissions                  │
│    Identity policy = Policy attached to user/group/role via managed or inline                         │
│    Default deny    = Implicit deny when no explicit allow is found; not logged                        │
│    Cross-account   = Resource policy can grant access from another AWS account                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
