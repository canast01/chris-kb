# AWS EBS Snapshots


<div class="kb-summary">
AWS EBS Snapshots reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌───────────────────────────────── EBS Snapshots — Backup & Lifecycle ──────────────────────────────────┐
│                                                                                                       │
│  EBS snapshots are incremental S3-backed backups; DLM automates creation and retention.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Snapshot Mechanics              │  │             Snapshot Operations             │   │
│   │       Incremental: only changed blocks       │  │      Create: from volume or running EC2     │   │
│   │     Stored in S3 (not visible in bucket)     │  │     Restore: create new volume from snap    │   │
│   │       Regional: copy to other regions        │  │       AMI: create image from snapshot       │   │
│   │          Encrypted: uses volume CMK          │  │         Share: to account or public         │   │
│   │       Charged for changed blocks only        │  │       Copy: cross-region with new key       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DLM policy automates snapshot schedules and retention; use FSR for fast restores.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         DLM (Data Lifecycle Manager)         │  │               Snapshot Archive              │   │
│   │      Policy: tag-based volume targeting      │  │        Archive tier: 75% cost saving        │   │
│   │       Schedule: frequency + retention        │  │         Restore: 24–72h from archive        │   │
│   │       Cross-region copy rule in policy       │  │        Recycle Bin: accidental delete       │   │
│   │         Fast snapshot restore option         │  │        Recycle retention: 1–365 days        │   │
│   │       EventBridge: notify on creation        │  │      Compliance lock: prevent early del     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS S3 snapshot storage backend · Cross-region replication infrastructure · Archive tier             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Incremental snapshot= After first full, subsequent snaps store only changed blocks                   │
│  DLM             = Data Lifecycle Manager; manages EBS snapshot automation policies                   │
│  FSR             = Fast Snapshot Restore; pre-initialises snapshot data for instant restore           │
│  Snapshot archive= Cold tier for infrequently accessed snapshots; lower cost                          │
│  Recycle Bin     = Soft-delete retention for snapshots; recover within retention period               │
│  Snapshot lock   = Compliance mode preventing modification or deletion of snapshots                   │
│  Cross-region copy= Create copy of snapshot in another region; re-encrypt with new key                │
│  Shared snapshot = Owner can share snapshot to specific accounts or make public                       │
│  Encrypted snap  = Snapshot of encrypted volume is always encrypted; cannot disable                   │
│  Volume from snap= New EBS volume restored from snapshot data; any size ≥ original                    │
│  Retention count = DLM policy keeps N most recent snapshots; deletes older ones                       │
│  Tag targeting   = DLM policy targets volumes with specific tag key-value pairs                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS EBS Snapshots notes for day-to-day infrastructure operations.

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
