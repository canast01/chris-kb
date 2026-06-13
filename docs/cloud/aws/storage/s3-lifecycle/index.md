---
tags:
  - aws
---
# AWS S3 Lifecycle


<div class="kb-summary">
AWS S3 Lifecycle reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: AWS*
</div>

```text
┌────────────────────────────── S3 Lifecycle — Automated Tiering & Expiry ──────────────────────────────┐
│                                                                                                       │
│  S3 lifecycle rules automate transitioning objects to cheaper tiers and expiring old data.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Rule Scoping                 │  │               Transition Rules              │   │
│   │         Prefix: apply to path prefix         │  │       Standard → Standard-IA: 30 days       │   │
│   │          Tags: filter by object tag          │  │        Standard-IA → Glacier: 60 days       │   │
│   │         Object size: min/max filters         │  │       Glacier → Deep Archive: 180 days      │   │
│   │       Versioned: current or noncurrent       │  │       Any class → Intelligent-Tiering       │   │
│   │      Applies to whole bucket or subset       │  │      Min days in class before next move     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Expiration rules delete objects or delete markers; clean up incomplete multipart uploads.            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Expiration Rules               │  │                 Cost Impact                 │   │
│   │     Delete current version after N days      │  │       Standard-IA: 58% cheaper storage      │   │
│   │      Delete noncurrent version after N       │  │        Glacier: 70%+ cheaper than Std       │   │
│   │        Delete expired delete markers         │  │        Deep Archive: lowest cost tier       │   │
│   │      Abort incomplete multipart uploads      │  │       Minimum storage duration charges      │   │
│   │      Max noncurrent versions to retain       │  │        Retrieval fees: IA and Glacier       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS S3 storage tiers · Glacier vault infrastructure · Regional S3 control plane                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Lifecycle rule  = Configuration defining when objects transition or expire                           │
│  Transition      = Lifecycle action moving object to a cheaper storage class                          │
│  Expiration      = Lifecycle action permanently deleting an object after N days                       │
│  Current version = Latest version of an object in a versioned bucket                                  │
│  Noncurrent version= Previous version after a new upload overwrites; retained by versioning           │
│  Delete marker   = Placeholder created when deleting a versioned object; no data                      │
│  Minimum storage = IA: 30 days; Glacier: 90 days; charged even if deleted earlier                     │
│  Retrieval fee   = Per-GB charge to access IA or Glacier objects; varies by speed                     │
│  Incomplete upload= Multipart upload parts accumulate cost; set expiry rule to clean up               │
│  Tag filter      = Lifecycle rule applies only to objects with specific tag key-value                 │
│  Intelligent-Tiering= No retrieval fees; auto-moves between tiers after 30 days inactivity            │
│  Deep Archive    = Lowest cost S3 tier; 12–48h retrieval; for compliance long-term data               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS S3 Lifecycle notes for day-to-day infrastructure operations.

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
