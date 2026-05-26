# AWS EBS

```
┌────────────────────────────────────── EBS — Elastic Block Store ──────────────────────────────────────┐
│                                                                                                       │
│  EBS provides persistent block storage for EC2; volume type determines performance tier.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Volume Types                 │  │              Performance Specs              │   │
│   │       gp3: general SSD; default choice       │  │        gp3: 16,000 IOPS / 1,000 MB/s        │   │
│   │        gp2: older general SSD; burst         │  │         io2 Block Express: 256K IOPS        │   │
│   │     io2: provisioned IOPS; multi-attach      │  │           st1: 500 MB/s throughput          │   │
│   │        st1: throughput HDD; big data         │  │            sc1: 250 MB/s cold HDD           │   │
│   │       sc1: cold HDD; infrequent access       │  │       gp2: burst 3,000 IOPS to credit       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  EBS volumes are AZ-scoped; use snapshots to move data across AZs or regions.                         │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Advanced Features               │  │                Best Practices               │   │
│   │      Multi-attach: io1/io2 up to 16 EC2      │  │      Enable account default encryption      │   │
│   │       Encryption: AES-256 via KMS CMK        │  │          Use gp3 over gp2 (cheaper)         │   │
│   │     Modify in-place: resize/type change      │  │        Snapshots before risky changes       │   │
│   │     Fast snapshot restore: instant data      │  │        CloudWatch IOPS metric alerts        │   │
│   │      Nitro-based: max performance gains      │  │        Delete volumes on termination        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS AZ SSD/HDD storage arrays · Dedicated EBS network separate from EC2 data path                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  gp3             = General Purpose SSD v3; independently set IOPS and throughput                      │
│  io2 Block Express= Highest performance SSD; up to 256K IOPS; SAP HANA workloads                      │
│  IOPS            = Input/output operations per second; determines random I/O speed                    │
│  Throughput      = Data transfer rate in MB/s; determines sequential I/O speed                        │
│  Multi-attach    = io1/io2 feature allowing up to 16 EC2 instances to share a volume                  │
│  Burst credit    = gp2 earns credits at baseline; spends at 3,000 IOPS during burst                   │
│  Modify in-place = Change volume type, size, or IOPS without stopping EC2 instance                    │
│  FSR             = Fast Snapshot Restore; initialises volume data instantly from snapshot             │
│  AZ-scoped       = EBS volume lives in one AZ; detach and re-attach within same AZ only               │
│  Snapshot        = Point-in-time backup of EBS volume stored durably in S3                            │
│  Nitro EC2       = Instance family required for max EBS performance (most modern types)               │
│  Delete on term  = Volume option; if enabled, volume deleted when instance terminates                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS EBS notes for day-to-day infrastructure operations.

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
