---
tags:
  - aws
---
# AWS Patch Manager


<div class="kb-summary">
AWS Patch Manager reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: AWS*
</div>

```text
┌───────────────────────────────────── AWS Compute — Patch Manager ─────────────────────────────────────┐
│                                                                                                       │
│  SSM Patch Manager automates OS patching across EC2 fleet using baselines and groups.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Patch Baseline                │  │                 Patch Groups                │   │
│   │        OS: Amazon Linux/RHEL/Windows         │  │             Tag: Patch Group key            │   │
│   │          Approval: critical auto 7d          │  │            Env: prod/staging/dev            │   │
│   │         Classification: Security/Bug         │  │           Stagger: dev before prod          │   │
│   │         Custom: include/exclude list         │  │         Register baseline per group         │   │
│   │        AWS default baselines: per OS         │  │         Compliance report per group         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Baseline defines what to patch; patch group targets which instances receive it                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Patching Execution              │  │                  Compliance                 │   │
│   │         Maintenance window: schedule         │  │          describe-patch-compliance          │   │
│   │      Run Command: AWS-RunPatchBaseline       │  │         Config rule: patch compliant        │   │
│   │          Scan: missing patches only          │  │        Dashboard: per-instance state        │   │
│   │           Install: apply + reboot            │  │            SNS: alert on failure            │   │
│   │          No-reboot: --reboot-option          │  │       Patch latency: days since avail       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  SSM Agent on EC2 · SSM service endpoints · CloudWatch · SNS · Config                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Patch baseline  = Policy defining which patches are approved for installation                        │
│  Patch group     = EC2 instances tagged Patch Group=<value>; mapped to baseline                       │
│  Maintenance window= Scheduled time during which patching runs; limits blast radius                   │
│  AWS-RunPatchBaseline= SSM document that scans or installs patches on instances                       │
│  Scan mode       = Reports missing patches without installing; safe for auditing                      │
│  Install mode    = Downloads and installs patches; may reboot instance                                │
│  Approval delay  = Days after patch release before it is auto-approved in baseline                    │
│  Compliance state= Compliant (all approved patches installed) or NonCompliant                         │
│  Patch latency   = Average days between patch availability and installation                           │
│  No-reboot option= Installs patches but skips reboot; manual reboot required later                    │
│  Config rule     = Detects instances with NonCompliant patch state automatically                      │
│  SSM Agent       = Software on instance that executes patch commands from SSM                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Patch Manager notes for day-to-day infrastructure operations.

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
