# AWS EFS


<div class="kb-summary">
AWS EFS reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌────────────────────────────────────── EFS — Elastic File System ──────────────────────────────────────┐
│                                                                                                       │
│  EFS provides shared NFS file storage for EC2 and Lambda; scales automatically to petabytes.          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             EFS Characteristics              │  │              Performance Modes              │   │
│   │            NFS v4.1/v4.0 protocol            │  │         General Purpose: low latency        │   │
│   │         Multi-AZ: mount from any AZ          │  │      Max I/O: high aggregate throughput     │   │
│   │      Pay per GB stored; no provisioning      │  │      Bursting: scales with file system      │   │
│   │     Encryption: KMS at rest; TLS transit     │  │         Elastic: recommended default        │   │
│   │           POSIX permissions + ACLs           │  │      Provisioned: guaranteed throughput     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Mount targets per AZ; security group on mount target controls NFS port 2049 access.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Storage Classes                │  │               Access Patterns               │   │
│   │        Standard: frequently accessed         │  │        EC2: mount in user-data script       │   │
│   │        Standard-IA: infrequent access        │  │         Lambda: /mnt/* mount config         │   │
│   │       One Zone: single AZ; lower cost        │  │       ECS/EKS: persistent volume claim      │   │
│   │      Lifecycle: auto-tier after N days       │  │       Access Points: per-app directory      │   │
│   │        Intelligent-Tiering: auto-move        │  │         DataSync: on-prem migration         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS EFS storage infrastructure per AZ · Mount target ENIs in each VPC subnet                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Mount target    = ENI in a subnet; endpoint for NFS connections from EC2 or Lambda                   │
│  Access Point    = Application-specific entry point enforcing POSIX user and root path                │
│  General Purpose = Default performance mode; low latency for most workloads                           │
│  Max I/O         = Higher aggregate throughput; higher latency; for parallel workloads                │
│  Elastic throughput= Auto-scales up to 10 GB/s without provisioning; recommended                      │
│  Bursting throughput= Scales with file system size; earns burst credits when idle                     │
│  Standard-IA     = Infrequent Access storage class; 92% cheaper than Standard                         │
│  Lifecycle policy= Automatically moves files to IA after 7, 14, 30, 60, or 90 days                    │
│  One Zone        = Single-AZ EFS; 47% cheaper than standard; no cross-AZ redundancy                   │
│  NFS port 2049   = TCP port used for NFS connections; allow in mount target SG                        │
│  DataSync        = AWS service for migrating on-premises NFS data to EFS                              │
│  Encryption at rest= KMS CMK encrypts all EFS file system data and metadata                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── EFS — Elastic File System ──────────────────────────────────────┐
│                                                                                                       │
│  EFS provides shared NFS file storage for EC2 and Lambda; scales automatically to petabytes.          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             EFS Characteristics              │  │              Performance Modes              │   │
│   │            NFS v4.1/v4.0 protocol            │  │         General Purpose: low latency        │   │
│   │         Multi-AZ: mount from any AZ          │  │      Max I/O: high aggregate throughput     │   │
│   │      Pay per GB stored; no provisioning      │  │      Bursting: scales with file system      │   │
│   │     Encryption: KMS at rest; TLS transit     │  │         Elastic: recommended default        │   │
│   │           POSIX permissions + ACLs           │  │      Provisioned: guaranteed throughput     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Mount targets per AZ; security group on mount target controls NFS port 2049 access.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Storage Classes                │  │               Access Patterns               │   │
│   │        Standard: frequently accessed         │  │        EC2: mount in user-data script       │   │
│   │        Standard-IA: infrequent access        │  │         Lambda: /mnt/* mount config         │   │
│   │       One Zone: single AZ; lower cost        │  │       ECS/EKS: persistent volume claim      │   │
│   │      Lifecycle: auto-tier after N days       │  │       Access Points: per-app directory      │   │
│   │        Intelligent-Tiering: auto-move        │  │         DataSync: on-prem migration         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS EFS storage infrastructure per AZ · Mount target ENIs in each VPC subnet                         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Mount target    = ENI in a subnet; endpoint for NFS connections from EC2 or Lambda                   │
│  Access Point    = Application-specific entry point enforcing POSIX user and root path                │
│  General Purpose = Default performance mode; low latency for most workloads                           │
│  Max I/O         = Higher aggregate throughput; higher latency; for parallel workloads                │
│  Elastic throughput= Auto-scales up to 10 GB/s without provisioning; recommended                      │
│  Bursting throughput= Scales with file system size; earns burst credits when idle                     │
│  Standard-IA     = Infrequent Access storage class; 92% cheaper than Standard                         │
│  Lifecycle policy= Automatically moves files to IA after 7, 14, 30, 60, or 90 days                    │
│  One Zone        = Single-AZ EFS; 47% cheaper than standard; no cross-AZ redundancy                   │
│  NFS port 2049   = TCP port used for NFS connections; allow in mount target SG                        │
│  DataSync        = AWS service for migrating on-premises NFS data to EFS                              │
│  Encryption at rest= KMS CMK encrypts all EFS file system data and metadata                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS EFS notes for day-to-day infrastructure operations.

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
