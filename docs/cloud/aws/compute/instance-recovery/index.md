---
tags:
  - aws
---
# AWS Instance Recovery


<div class="kb-summary">
AWS Instance Recovery reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: AWS*
</div>

```text
┌─────────────────────────────────── AWS Compute — Instance Recovery ───────────────────────────────────┐
│                                                                                                       │
│  EC2 recovery mechanisms: CloudWatch alarm recovery, reboot, restore from AMI/snapshot.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Automatic Recovery              │  │              Health Check Types             │   │
│   │         CW alarm: StatusCheckFailed          │  │         System check: host hardware         │   │
│   │           Action: recover instance           │  │            Instance check: OS/NIC           │   │
│   │          Retains: IP, EBS, EIP, SG           │  │         ELB health: app-level check         │   │
│   │            Moves to healthy host             │  │          Custom: CloudWatch metric          │   │
│   │           Notification: SNS topic            │  │         ASG: replaces failed member         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  CW alarm triggers automatic recovery; ASG replaces terminated instances automatically                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Manual Recovery Steps             │  │                 DR Scenarios                │   │
│   │            Console: stop → start             │  │         Corrupt OS: restore from AMI        │   │
│   │          Reboot: keeps EBS + config          │  │       Lost data: EBS snapshot restore       │   │
│   │         Detach root vol: chroot fix          │  │        AZ failure: relaunch in new AZ       │   │
│   │        Serial console: no-network fix        │  │       Region failure: cross-region AMI      │   │
│   │         SSM run-command: fix config          │  │         RTO target: define per tier         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  EC2 host · Nitro hypervisor · EBS · CloudWatch · SNS · multiple AZs                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  StatusCheckFailed_System= Host hardware or network issue; triggers auto-recovery                     │
│  StatusCheckFailed_Instance= OS-level failure; requires reboot or manual fix                          │
│  recover action  = CloudWatch alarm action moving instance to healthy host                            │
│  Retains EIP     = Elastic IP stays associated after automatic recovery                               │
│  Detach root vol = Mount root EBS on rescue instance to repair offline OS                             │
│  Serial console  = Out-of-band access for instances without network connectivity                      │
│  chroot          = Linux technique to access and fix a mounted OS root filesystem                     │
│  Cross-region AMI= AMI copied to DR region; launch instances there on region failure                  │
│  ASG replacement = ASG terminates failed instance and launches new one automatically                  │
│  Stop → Start    = Moves instance to new host; clears most transient failures                         │
│  RTO             = Recovery Time Objective; maximum acceptable downtime per tier                      │
│  ELB health check= Removes unhealthy instance from load balancer target group                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Instance Recovery notes for day-to-day infrastructure operations.

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
