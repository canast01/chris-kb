# AWS AMIs


<div class="kb-summary">
AWS AMIs reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────────────────── AWS Compute — AMIs ──────────────────────────────────────────┐
│                                                                                                       │
│  Amazon Machine Images: golden image pipeline, lifecycle management, and sharing.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                AMI Components                │  │                  AMI Types                  │   │
│   │            Root snapshot: OS disk            │  │          AWS-managed: Amazon Linux          │   │
│   │        Block device mapping: volumes         │  │          Marketplace: vendor images         │   │
│   │         Launch permissions: who uses         │  │            Custom: golden images            │   │
│   │          Kernel: AKI (paravirtual)           │  │           Community: public shared          │   │
│   │          Architecture: x86 or arm64          │  │          Private: account-specific          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Golden AMIs baked via EC2 Image Builder pipeline; shared to target accounts via RAM                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Golden Image Pipeline             │  │             Lifecycle Management            │   │
│   │           Base: AWS or vendor AMI            │  │           Deprecate: old versions           │   │
│   │            Harden: CIS benchmark             │  │         Deregister: remove from list        │   │
│   │           Patch: SSM patch manager           │  │        Delete snapshots: cost control       │   │
│   │             Test: Inspector scan             │  │           Share: RAM cross-account          │   │
│   │            Publish: Image Builder            │  │          Tag: version + build date          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  EC2 build instance · EBS (snapshot storage) · S3 (Image Builder artifacts) · KMS                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AMI             = Amazon Machine Image; template for launching EC2 instances                         │
│  Golden image    = Hardened, pre-patched AMI used as approved base for all instances                  │
│  EC2 Image Builder= Managed service automating golden AMI creation and testing                        │
│  Block device map= Defines root and additional EBS volumes attached at launch                         │
│  Deprecate       = Marks AMI as outdated; still launchable but flagged for replacement                │
│  Deregister      = Removes AMI from list; underlying snapshots must be deleted separately             │
│  RAM             = Resource Access Manager; shares AMIs to other AWS accounts/OUs                     │
│  Launch permission= Controls which accounts can use the AMI to launch instances                       │
│  Inspector scan  = Vulnerability assessment run on AMI during Image Builder pipeline                  │
│  CIS benchmark   = Center for Internet Security OS hardening checklist                                │
│  arm64           = Graviton processor architecture; better price/performance for some                 │
│  Snapshot backing= Each AMI is backed by one or more EBS snapshots in S3                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS AMIs notes for day-to-day infrastructure operations.

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
