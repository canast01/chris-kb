---
tags:
  - aws
---
# AWS AWS Backup


<div class="kb-summary">
AWS AWS Backup reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌─────────────────────────────────── AWS Backup — AWS Backup Service ───────────────────────────────────┐
│                                                                                                       │
│  Centralised backup service managing policies, jobs, and vaults across AWS services.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Service Overview               │  │             Supported Resources             │   │
│   │        Backup plans: schedule + rules        │  │           EC2: AMI + EBS snapshots          │   │
│   │        Backup vault: encrypted store         │  │           RDS: automated snapshots          │   │
│   │        Recovery points: per resource         │  │           EFS: file system backups          │   │
│   │           Cross-region: copy rule            │  │          DynamoDB: on-demand backup         │   │
│   │            Cross-account: OU copy            │  │            S3: continuous backup            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Backup plans target resources via tags; vaults hold recovery points with lifecycle                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Vault Configuration              │  │             Compliance Controls             │   │
│   │          KMS: customer-managed key           │  │           AWS Backup Audit Manager          │   │
│   │           Vault lock: WORM policy            │  │          Config rule: backup exists         │   │
│   │          Access policy: cross-acct           │  │           Report: coverage + jobs           │   │
│   │         Lifecycle: cold storage tier         │  │          Alert: SNS on job failure          │   │
│   │           Notifications: SNS topic           │  │            Org backup policy: SCP           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS S3 Glacier (cold tier) · KMS HSMs · SNS · AWS Regions for cross-region copy                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Backup plan     = Policy defining schedule, retention, and lifecycle for backups                     │
│  Backup vault    = Encrypted container storing recovery points; access-controlled                     │
│  Recovery point  = Snapshot of a resource at a specific point in time                                 │
│  Vault lock      = WORM policy preventing deletion of recovery points; compliance                     │
│  Cross-region copy= Rule copying backup to another AWS region for DR                                  │
│  Cross-account copy= Copies recovery points to a separate AWS account for isolation                   │
│  Audit Manager   = AWS service verifying backup compliance against control framework                  │
│  KMS CMK         = Customer-Managed Key encrypting the backup vault                                   │
│  Cold storage    = Cheaper long-term tier (Glacier); lower cost, higher restore time                  │
│  Lifecycle rule  = Transitions recovery points to cold storage after N days                           │
│  Org backup policy= Backup plan deployed org-wide via AWS Organizations                               │
│  WORM            = Write Once Read Many; immutable storage preventing modification                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS AWS Backup notes for day-to-day infrastructure operations.

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
