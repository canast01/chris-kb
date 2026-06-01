# AWS S3


<div class="kb-summary">
AWS S3 reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌───────────────────────────────────────── S3 — Object Storage ─────────────────────────────────────────┐
│                                                                                                       │
│  S3 stores objects in buckets; 11 nines durability; access controlled by policies and ACLs.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Bucket Configuration             │  │               Storage Classes               │   │
│   │        Global namespace: unique name         │  │          Standard: frequent access          │   │
│   │      Region-bound: data stays regional       │  │        Intelligent-Tiering: auto-move       │   │
│   │      Versioning: preserve all versions       │  │        Standard-IA: infrequent access       │   │
│   │         Object Lock: WORM protection         │  │       One Zone-IA: single AZ; cheaper       │   │
│   │      Event notification: Lambda/SNS/SQS      │  │        Glacier/Deep Archive: archival       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Access control via bucket policy + Block Public Access; IAM for programmatic access.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Access Control                │  │              Advanced Features              │   │
│   │      Bucket policy: resource-based JSON      │  │          Multipart upload: > 100MB          │   │
│   │       Block Public Access: 4 settings        │  │      Transfer Acceleration: CloudFront      │   │
│   │        SSE-KMS: audit every API call         │  │         Select: SQL filter in-place         │   │
│   │      Presigned URL: time-limited access      │  │          Requester Pays: shift cost         │   │
│   │         VPC endpoint: private access         │  │        Static website: index + error        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS S3 storage infrastructure (3+ AZ) · CloudFront edge for acceleration · Regional endpoints        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Bucket          = Container for objects; globally unique name; region-bound storage                  │
│  Object          = File + metadata; identified by key (full path); up to 5TB                          │
│  Versioning      = Preserves all versions of an object; delete = delete marker                        │
│  Object Lock     = WORM protection; governance or compliance mode; delete prevention                  │
│  Bucket policy   = JSON resource policy controlling access to bucket and objects                      │
│  Block Public Access= Four settings preventing public ACLs and bucket policies                        │
│  Presigned URL   = Time-limited URL granting temporary access to a private object                     │
│  Glacier         = S3 archive tier; minutes to hours retrieval; very low storage cost                 │
│  Intelligent-Tiering= Auto-moves objects between tiers based on 30-day access pattern                 │
│  Multipart upload= Parallel upload of large objects in parts; required > 5GB                          │
│  S3 Select       = SQL queries filtering object content server-side; reduces data transfer            │
│  11 nines        = 99.999999999% durability; objects stored across 3+ AZs                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS S3 notes for day-to-day infrastructure operations.

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
