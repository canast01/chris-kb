# AWS EC2

```text
┌────────────────────────────────────────── AWS Compute — EC2 ──────────────────────────────────────────┐
│                                                                                                       │
│  Elastic Compute Cloud: instance types, purchasing options, networking, and storage.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Instance Families               │  │              Purchasing Options             │   │
│   │         General: m7i, t3 (burstable)         │  │          On-demand: pay per second          │   │
│   │           Compute: c7i (high CPU)            │  │          Reserved: 1/3yr commitment         │   │
│   │            Memory: r7i (high RAM)            │  │          Spot: spare capacity, -90%         │   │
│   │          Storage: i4i (NVMe local)           │  │          Savings plan: flexible RI          │   │
│   │           Accelerated: p4/g5 (GPU)           │  │          Dedicated host: compliance         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Instance family chosen for workload type; purchasing model optimises cost                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Networking                  │  │                   Storage                   │   │
│   │          ENI: virtual network card           │  │              Root EBS: OS disk              │   │
│   │            Public IP: auto-assign            │  │          Data EBS: persistent block         │   │
│   │          Elastic IP: static public           │  │        Instance store: ephemeral NVMe       │   │
│   │         Enhanced networking: SR-IOV          │  │            EFS mount: shared NFS            │   │
│   │       Placement group: latency/spread        │  │          FSx: Windows/Lustre mount          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Nitro hypervisor · Nitro cards (network/storage) · physical host · AZ data centre                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ENI             = Elastic Network Interface; virtual NIC attachable to EC2                           │
│  Elastic IP      = Static public IPv4 address; persists across stop/start                             │
│  SR-IOV          = Single Root I/O Virtualisation; enables enhanced networking                        │
│  Placement group = Cluster (low latency) or spread (fault isolation) placement                        │
│  Spot instance   = Uses spare EC2 capacity; can be interrupted with 2-min notice                      │
│  Reserved instance= 1 or 3-year commitment for up to 72% discount                                     │
│  Savings plan    = Flexible commitment by $/hour; applies across instance families                    │
│  Dedicated host  = Physical server for BYOL or compliance isolation requirements                      │
│  Instance store  = NVMe SSD physically attached to host; lost on stop/terminate                       │
│  Burstable (t3)  = Accumulates CPU credits when idle; bursts above baseline                           │
│  Nitro hypervisor= AWS-built hypervisor offloading I/O to dedicated Nitro cards                       │
│  IMDS v2         = Instance Metadata Service v2; token-required for security                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS EC2 notes for day-to-day infrastructure operations.

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
