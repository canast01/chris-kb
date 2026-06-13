---
tags:
  - aws
---
# AWS Backup Plans


<div class="kb-summary">
AWS Backup Plans reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌────────────────────────────────────── AWS Backup — Backup Plans ──────────────────────────────────────┐
│                                                                                                       │
│  Backup plans define schedule, lifecycle, vault, and copy rules for targeted resources.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Plan Structure                │  │              Rule Configuration             │   │
│   │         Rules: one or more per plan          │  │            Schedule: cron or rate           │   │
│   │         Resources: tag-based select          │  │         Start window: 60 min default        │   │
│   │        Vault: destination for points         │  │           Completion window: 8 hr           │   │
│   │         Plan versions: track changes         │  │           Retention: days to keep           │   │
│   │         Org policy: deploy org-wide          │  │           Copy: region or account           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Tag-based selection targets resources; rules define when and where backups go                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Lifecycle Configuration            │  │                Best Practices               │   │
│   │         Warm tier: standard storage          │  │     3-2-1: 3 copies, 2 media, 1 offsite     │   │
│   │           Cold tier: after N days            │  │        Prod: daily + weekly + monthly       │   │
│   │         Expire: delete after M days          │  │          Dev: daily 7-day retention         │   │
│   │         Min 90 days in cold storage          │  │           Cross-region: DR account          │   │
│   │         Cold storage saves ~60% cost         │  │           Test restore: quarterly           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Backup service · S3 Glacier (cold tier) · target resources · KMS · SNS                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Backup plan     = Policy containing rules that define backup schedule and lifecycle                  │
│  Backup rule     = Single schedule+lifecycle+vault combination within a plan                          │
│  Tag-based select= Backup plan assigns resources matching specified tag key/value                     │
│  Start window    = Time after scheduled start within which job must begin                             │
│  Completion window= Max time allowed for backup job before it is marked failed                        │
│  Warm tier       = Standard S3 storage class; fast restore, higher cost                               │
│  Cold tier       = Glacier storage; lower cost but 12-hour restore time                               │
│  3-2-1 rule      = 3 copies, 2 storage types, 1 offsite; standard DR practice                         │
│  Org policy      = Backup plan deployed to all accounts via AWS Organizations                         │
│  Plan version    = Immutable snapshot of plan configuration for audit trail                           │
│  Retention days  = How long recovery points are kept before automatic deletion                        │
│  Quarterly test  = Best practice: restore from backup to verify recoverability                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Backup Plans notes for day-to-day infrastructure operations.

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
