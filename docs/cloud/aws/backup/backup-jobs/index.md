---
tags:
  - aws
---
# AWS Backup Jobs


<div class="kb-summary">
AWS Backup Jobs reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌────────────────────────────────────── AWS Backup — Backup Jobs ───────────────────────────────────────┐
│                                                                                                       │
│  Backup jobs execute on schedule or on-demand; monitor status, duration, and failures.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Job Lifecycle                 │  │                  Job Types                  │   │
│   │          Created: plan triggers job          │  │          Backup: resource to vault          │   │
│   │        Running: snapshot in progress         │  │         Copy: vault to vault/region         │   │
│   │       Completed: recovery point saved        │  │          Restore: point to resource         │   │
│   │          Failed: SNS alert + retry           │  │          On-demand: manual trigger          │   │
│   │         Expired: retention lifecycle         │  │           Continuous: S3/SAP HANA           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Jobs created by plan schedule; status monitored via console, CLI, or EventBridge                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Monitoring                  │  │               Troubleshooting               │   │
│   │           Console: Jobs dashboard            │  │        IAM: BackupRole missing perms        │   │
│   │            CLI: list-backup-jobs             │  │            KMS: key access denied           │   │
│   │         CloudWatch: BackupJobsFailed         │  │        Resource busy: snapshot limit        │   │
│   │        EventBridge: job state change         │  │        Service quota: job concurrency       │   │
│   │          SNS: failure notification           │  │          Retry: on-demand after fix         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Backup service · KMS HSM · SNS · CloudWatch · target resource (EBS/RDS/EFS)                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Recovery point  = Immutable snapshot stored in vault; created on job completion                      │
│  BackupRole      = IAM role AWS Backup assumes to access resources for backup                         │
│  BackupJobsFailed= CloudWatch metric counting failed backup jobs in a period                          │
│  EventBridge     = Routes backup job state-change events to Lambda or SNS                             │
│  Continuous backup= Point-in-time recovery for S3; RPO of 1 hour                                      │
│  Copy job        = Replicates recovery point to another vault or region                               │
│  Restore job     = Creates new resource from a recovery point                                         │
│  On-demand job   = Manual one-off backup outside of plan schedule                                     │
│  Service quota   = AWS limit on concurrent backup jobs per account                                    │
│  Snapshot limit  = EBS limit on concurrent snapshots per volume                                       │
│  SNS notification= Alert sent to subscribed email/Slack/Lambda on job failure                         │
│  list-backup-jobs= AWS CLI command to query job history and status                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Backup Jobs notes for day-to-day infrastructure operations.

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
