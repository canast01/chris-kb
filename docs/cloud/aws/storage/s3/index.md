---
tags:
  - aws
---
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

---

## S3 Storage Classes

```text
┌─────────────────────── S3 Storage Classes — Availability, Retrieval, and Cost ────────────────────────┐
│                                                                                                       │
│    Seven storage classes balance retrieval latency, availability, and storage cost.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Frequent Access Classes                  │  │      Infrequent Access Classes              │   │
│   │  Standard: 99.99% avail; 3+ AZ               │  │  Standard-IA: 99.9%; 3+ AZ; fee/get         │   │
│   │  Standard: no retrieval fee; default         │  │  Standard-IA: 30-day minimum storage        │   │
│   │  Intelligent-Tiering: auto-moves tiers       │  │  One Zone-IA: 99.5%; 1 AZ; cheaper          │   │
│   │  IT: monitoring fee; no retrieval fee        │  │  One Zone-IA: re-creatable data only        │   │
│   │  IT: moves after 30 days of no access        │  │  Both: per-GB retrieval fee applies         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Standard for frequent access; IA tiers for data accessed less than once a month.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Glacier Archive Classes                  │  │      Retrieval Comparison                   │   │
│   │  Glacier Instant: ms retrieval; 90-day       │  │  Standard: ms; no retrieval fee             │   │
│   │  Glacier Flexible: mins-hrs; 90-day          │  │  Standard-IA: ms; retrieval fee/GB          │   │
│   │  Glacier Deep Archive: 12-hr; 180-day        │  │  Glacier Instant: ms; per GB fee            │   │
│   │  Deep Archive: cheapest storage class        │  │  Glacier Flexible: bulk=5-12h, free         │   │
│   │  All Glacier: 11-nines durability; 3AZ       │  │  Deep Archive: standard=12h retrieval       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    S3 stores objects across 3+ AZs in a Region; 11 nines (99.999999999%) durability                   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    S3 Standard     = Default; frequent access; 3+ AZ; 99.99% availability                             │
│    Intelligent-Tiering = Auto-moves objects between tiers; monitoring fee per 1000                    │
│    Standard-IA     = Infrequent Access; 3+ AZ; lower storage cost; retrieval fee                      │
│    One Zone-IA     = Single AZ; 20% cheaper than Standard-IA; risk of AZ loss                         │
│    Glacier Instant = Archive; millisecond retrieval; 90-day minimum; per-GB fee                       │
│    Glacier Flexible= Archive; expedited(1-5min)/standard(3-5h)/bulk(5-12h) retrieval                  │
│    Deep Archive    = Cheapest; 12-hour standard retrieval; 180-day minimum                            │
│    Minimum duration= Classes have minimum storage billing periods; charged even if deleted            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```



---

## AWS Storage Services Comparison

```text
┌────────────────── AWS Storage Services — S3 vs EBS vs EFS vs FSx vs Instance Store ───────────────────┐
│                                                                                                       │
│    Five main storage types; choose by access pattern, sharing, and persistence needs.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      S3 (Object Storage)                     │  │      EBS (Block Storage)                    │   │
│   │  Objects in buckets; unlimited scale         │  │  Persistent block volumes for EC2           │   │
│   │  Globally unique bucket name                 │  │  Bound to a single AZ                       │   │
│   │  HTTP API (PUT/GET); not mountable           │  │  Mountable like a local disk (ext4)         │   │
│   │  11 nines durability; 3+ AZ by default       │  │  SSD (gp3/io2) or HDD (st1/sc1)             │   │
│   │  Use: backups, static web, data lake         │  │  Use: OS disk, DB, boot volume              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    EBS is block (like a hard drive); EFS is shared NFS; S3 is object (HTTP API).                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     EFS (Elastic File System)                │  │      Instance Store / FSx                   │   │
│   │  NFSv4 shared file system                    │  │  Instance Store: ephemeral local NVMe       │   │
│   │  Multi-AZ; automatically scales              │  │  Lost on stop/terminate/host failure        │   │
│   │  Mount simultaneously to many EC2            │  │  Highest I/O throughput; no extra $         │   │
│   │  Linux only; no Windows                      │  │  FSx for Windows: SMB, AD-integrated        │   │
│   │  Standard + Infrequent Access tiers          │  │  FSx for Lustre: HPC parallel FS            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    S3 infrastructure (3+ AZ) · EBS volumes in AZ · NFS cluster (EFS) · local NVMe                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    S3         = Object storage; buckets + keys; unlimited scale; HTTP GET/PUT API                     │
│    EBS        = Elastic Block Store; like a virtual hard drive; attached to one EC2                   │
│    EFS        = Elastic File System; NFS v4; shared across many Linux EC2 instances                   │
│    Instance Store = Local NVMe on the physical host; ephemeral; fastest raw IOPS                      │
│    FSx for Windows= Fully managed Windows file server; SMB protocol; AD integration                   │
│    FSx for Lustre = High-performance parallel file system; integrates with S3                         │
│    Storage Gateway= Hybrid storage; connects on-prem to S3/EBS/Tape via iSCSI/NFS                     │
│    Snow Family    = Physical devices (Snowcone/Snowball/Snowmobile) for data transfer                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
