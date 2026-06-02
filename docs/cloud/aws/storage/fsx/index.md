# AWS FSx


<div class="kb-summary">
AWS FSx reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌───────────────────────────────── FSx — Managed File System Flavours ──────────────────────────────────┐
│                                                                                                       │
│  FSx provides fully managed file systems: Windows SMB, Lustre HPC, ONTAP, and OpenZFS.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         FSx for Windows File Server          │  │                FSx for Lustre               │   │
│   │      SMB protocol: Windows native share      │  │            HPC/ML: sub-ms latency           │   │
│   │        AD integration: Kerberos auth         │  │          S3 integration: data repo          │   │
│   │       DFS namespace: scale-out shares        │  │       SSD: scratch or persistent tier       │   │
│   │        Multi-AZ HA with standby node         │  │            Up to 1 TB/s aggregate           │   │
│   │      Shadow copies, VSS, DFS-R support       │  │         EKS/ECS: CSI driver support         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  FSx for ONTAP: full NetApp features in AWS; FSx for OpenZFS: NFS with ZFS snapshots.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                FSx for ONTAP                 │  │               FSx for OpenZFS               │   │
│   │         NFS/SMB/iSCSI multi-protocol         │  │            NFS v3/v4 file system            │   │
│   │       SnapMirror: on-prem replication        │  │           ZFS snapshots and clones          │   │
│   │       FlexVols, thin provision, dedup        │  │          Up to 12.5 GB/s throughput         │   │
│   │         Multi-AZ: HA primary/standby         │  │        Low latency: SSD storage only        │   │
│   │      StorageVMs: multi-tenancy support       │  │       POSIX: Linux workload lift/shift      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS managed storage infrastructure · SSD arrays per AZ · Regional file system endpoints              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FSx             = Amazon FSx; family of managed third-party file system services                     │
│  SMB             = Server Message Block; Windows file sharing protocol                                │
│  DFS namespace   = Distributed File System namespace; aggregates shares under one path                │
│  Shadow copy     = Windows VSS snapshot; FSx supports application-consistent copies                   │
│  Lustre          = High-performance parallel file system; POSIX; used for HPC/ML                      │
│  S3 data repo    = FSx for Lustre imports from and exports to an S3 bucket                            │
│  FSx ONTAP       = NetApp ONTAP managed by AWS; supports FlexVols and SnapMirror                      │
│  StorageVM       = ONTAP SVM; logical isolation within a file system for multi-tenancy                │
│  SnapMirror      = ONTAP replication technology; replicate to on-prem or another FSx                  │
│  OpenZFS         = Open source file system with ZFS features; NFS access; low latency                 │
│  Multi-AZ FSx    = Primary + standby in different AZs; automatic failover on failure                  │
│  CSI driver      = Container Storage Interface; allows EKS pods to mount FSx volumes                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS FSx notes for day-to-day infrastructure operations.

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
