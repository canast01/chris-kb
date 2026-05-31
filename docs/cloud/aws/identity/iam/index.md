---
title: AWS Identity — IAM
---

# AWS Identity — IAM

```text
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
