---
tags:
  - aws
---
# AWS Auto Scaling


<div class="kb-summary">
AWS Auto Scaling reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: AWS*
</div>

```text
┌───────────────────────────────────── AWS Compute — Auto Scaling ──────────────────────────────────────┐
│                                                                                                       │
│  EC2 Auto Scaling adjusts fleet size based on demand using scaling policies and health.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              ASG Configuration               │  │               Launch Template               │   │
│   │         Min / Max / Desired capacity         │  │          AMI: golden image version          │   │
│   │             AZs: multi-AZ spread             │  │        Instance type: on-demand/spot        │   │
│   │           Health check: EC2 or ELB           │  │             IAM instance profile            │   │
│   │            Cooldown: 300s default            │  │         User data: bootstrap script         │   │
│   │        Lifecycle hooks: custom logic         │  │          Security group assignment          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ASG maintains desired capacity; scaling policies adjust desired up or down on demand                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Scaling Policies               │  │               Instance Refresh              │   │
│   │           Target tracking: CPU 70%           │  │           Rolling replace: new AMI          │   │
│   │        Step scaling: threshold bands         │  │          Min healthy %: 90 default          │   │
│   │         Scheduled: predictable load          │  │           Checkpoint: pause at N%           │   │
│   │          Predictive: ML-based scale          │  │             Rollback: on failure            │   │
│   │           Scale-in protection: pin           │  │        Warm pool: pre-warm instances        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  EC2 instances · ELB · CloudWatch (metrics trigger) · multiple AZs · SNS (notifications)              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ASG             = Auto Scaling Group; manages a fleet of EC2 instances                               │
│  Launch template = Instance configuration used to launch new ASG members                              │
│  Target tracking = Adjusts capacity to keep metric (e.g. CPU) at target value                         │
│  Step scaling    = Adds/removes N instances per threshold band breached                               │
│  Cooldown        = Pause after scaling action to let metrics stabilise                                │
│  Lifecycle hook  = Pauses instance at launch or termination for custom processing                     │
│  Instance refresh= Replaces all ASG instances with new launch template version                        │
│  Warm pool       = Pre-started stopped instances; reduce scale-out latency                            │
│  Scale-in protection= Prevents specific instance from being terminated during scale-in                │
│  Min healthy %   = % of instances that must stay healthy during instance refresh                      │
│  Predictive scaling= Uses ML to forecast load and pre-scale ahead of demand                           │
│  ELB health check= ASG uses ELB target health to decide if instance is unhealthy                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Auto Scaling notes for day-to-day infrastructure operations.

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
