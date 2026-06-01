# AWS S3 Replication


<div class="kb-summary">
AWS S3 Replication reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────────────── S3 Replication — CRR & SRR ──────────────────────────────────────┐
│                                                                                                       │
│  S3 replication copies objects asynchronously to destination buckets; versioning required.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Replication Types               │  │                Configuration                │   │
│   │        CRR: Cross-Region Replication         │  │       Versioning must be enabled both       │   │
│   │         SRR: Same-Region Replication         │  │       IAM role: source assumes to dest      │   │
│   │      Cross-account: specify dest owner       │  │       Prefix/tag filter: scope objects      │   │
│   │     Batch replication: existing objects      │  │       Storage class: same or override       │   │
│   │       RTC: 99.99% replicated in 15 min       │  │         Encryption: KMS key at dest         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  New objects replicate automatically; existing objects require Batch Replication job.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           What Does Not Replicate            │  │                  Monitoring                 │   │
│   │         Objects before rule creation         │  │        CloudWatch: ReplicationLatency       │   │
│   │      Objects in Glacier or Deep Archive      │  │          ReplicationObjects metric          │   │
│   │         Delete markers (by default)          │  │           S3 Replication Dashboard          │   │
│   │        Lifecycle-transitioned objects        │  │       Replication status tag on object      │   │
│   │          Objects already replicated          │  │       EventBridge: replication failure      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS S3 replication infrastructure · Cross-region AWS backbone · Regional endpoints                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CRR             = Cross-Region Replication; copies to a bucket in another region                     │
│  SRR             = Same-Region Replication; copies within same region for log aggregation             │
│  RTC             = Replication Time Control; SLA 99.99% replicated within 15 minutes                  │
│  Batch replication= Replicates existing objects using S3 Batch Operations job                         │
│  Replication status= Object metadata: PENDING, COMPLETED, FAILED, or REPLICA                          │
│  Delete marker replication= Optional: replicate delete markers to keep buckets in sync                │
│  Replica ownership= Option to give replica ownership to destination account                           │
│  Bidirectional   = Two rules (A→B + B→A) creates active-active replication                            │
│  Replication role= IAM role that S3 assumes to read from source and write to dest                     │
│  Multi-destination= One source bucket replicating to multiple destination buckets                     │
│  Encryption replication= Replicated objects can be re-encrypted with destination KMS key              │
│  Async replication= Objects replicated asynchronously; dest lags source slightly                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────────────── S3 Replication — CRR & SRR ──────────────────────────────────────┐
│                                                                                                       │
│  S3 replication copies objects asynchronously to destination buckets; versioning required.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Replication Types               │  │                Configuration                │   │
│   │        CRR: Cross-Region Replication         │  │       Versioning must be enabled both       │   │
│   │         SRR: Same-Region Replication         │  │       IAM role: source assumes to dest      │   │
│   │      Cross-account: specify dest owner       │  │       Prefix/tag filter: scope objects      │   │
│   │     Batch replication: existing objects      │  │       Storage class: same or override       │   │
│   │       RTC: 99.99% replicated in 15 min       │  │         Encryption: KMS key at dest         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  New objects replicate automatically; existing objects require Batch Replication job.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           What Does Not Replicate            │  │                  Monitoring                 │   │
│   │         Objects before rule creation         │  │        CloudWatch: ReplicationLatency       │   │
│   │      Objects in Glacier or Deep Archive      │  │          ReplicationObjects metric          │   │
│   │         Delete markers (by default)          │  │           S3 Replication Dashboard          │   │
│   │        Lifecycle-transitioned objects        │  │       Replication status tag on object      │   │
│   │          Objects already replicated          │  │       EventBridge: replication failure      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS S3 replication infrastructure · Cross-region AWS backbone · Regional endpoints                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CRR             = Cross-Region Replication; copies to a bucket in another region                     │
│  SRR             = Same-Region Replication; copies within same region for log aggregation             │
│  RTC             = Replication Time Control; SLA 99.99% replicated within 15 minutes                  │
│  Batch replication= Replicates existing objects using S3 Batch Operations job                         │
│  Replication status= Object metadata: PENDING, COMPLETED, FAILED, or REPLICA                          │
│  Delete marker replication= Optional: replicate delete markers to keep buckets in sync                │
│  Replica ownership= Option to give replica ownership to destination account                           │
│  Bidirectional   = Two rules (A→B + B→A) creates active-active replication                            │
│  Replication role= IAM role that S3 assumes to read from source and write to dest                     │
│  Multi-destination= One source bucket replicating to multiple destination buckets                     │
│  Encryption replication= Replicated objects can be re-encrypted with destination KMS key              │
│  Async replication= Objects replicated asynchronously; dest lags source slightly                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS S3 Replication notes for day-to-day infrastructure operations.

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
