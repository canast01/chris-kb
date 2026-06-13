---
tags:
  - aws
---
# AWS Systems Manager


<div class="kb-summary">
AWS Systems Manager reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: AWS*
</div>

```text
┌──────────────────────────────────── AWS Compute — Systems Manager ────────────────────────────────────┐
│                                                                                                       │
│  SSM provides fleet management: session access, patch, run-command, and parameter store.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Core Capabilities               │  │                Fleet Manager                │   │
│   │          Session Manager: SSH-free           │  │         Inventory: software + config        │   │
│   │          Run Command: fleet scripts          │  │          Compliance: patch + assoc          │   │
│   │          Patch Manager: OS updates           │  │          Node Management: overview          │   │
│   │       Parameter Store: config/secrets        │  │          Explorer: org-wide health          │   │
│   │        Automation: runbook playbooks         │  │         OpsCenter: incident tickets         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SSM Agent on each instance connects outbound to SSM endpoints; no inbound ports                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Automation                  │  │              Setup Requirements             │   │
│   │           Runbooks: SSM documents            │  │         SSM Agent: pre-installed AMI        │   │
│   │         Trigger: EventBridge/console         │  │    IAM role: AmazonSSMManagedInstanceCore   │   │
│   │          Approval step: human gate           │  │           VPC endpoint or internet          │   │
│   │          Multi-account: change mgr           │  │         Hybrid: on-prem registration        │   │
│   │          Rollback: stop on failure           │  │         Tag: managed instance label         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SSM service endpoints · SSM Agent · EC2/on-prem nodes · VPC endpoints · KMS                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SSM Agent       = Lightweight daemon on EC2 or on-prem; polls SSM for commands                       │
│  Session Manager = Secure interactive shell via SSM; no SSH port or key pair                          │
│  Run Command     = Execute SSM documents on target instances; returns output                          │
│  Parameter Store = Hierarchical config store; String, StringList, SecureString                        │
│  Automation      = Multi-step runbook; can approve, branch, loop, call APIs                           │
│  OpsCenter       = Operational issues (OpsItems) linked to AWS resources                              │
│  Explorer        = Aggregated ops dashboard across accounts in an org                                 │
│  Inventory       = Collects installed software, network config, Windows registry                      │
│  AmazonSSMManagedInstanceCore= Minimum IAM policy required for SSM management                         │
│  VPC endpoint    = Allows SSM Agent to communicate without internet access                            │
│  Hybrid activation= Registers on-prem servers as managed instances in SSM                             │
│  Change Manager  = Approval workflow for SSM Automation across multiple accounts                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Systems Manager notes for day-to-day infrastructure operations.

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
