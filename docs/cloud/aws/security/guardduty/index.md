---
tags:
  - aws
  - security
---
# AWS GuardDuty


<div class="kb-summary">
AWS GuardDuty reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌──────────────────────────────────── GuardDuty — Threat Detection ─────────────────────────────────────┐
│                                                                                                       │
│  GuardDuty analyses CloudTrail, VPC Flow Logs, and DNS to detect threats with ML/signatures.          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Data Sources                 │  │              Finding Categories             │   │
│   │         CloudTrail management events         │  │          Backdoor: C2 communication         │   │
│   │          CloudTrail S3 data events           │  │       Cryptocurrency: mining activity       │   │
│   │         VPC Flow Logs: network flows         │  │         Recon: port scan / API probe        │   │
│   │           Route 53 DNS query logs            │  │       Stealth: policy change detection      │   │
│   │        EKS audit + runtime monitoring        │  │      Trojan: malware callback patterns      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Findings classified LOW/MED/HIGH; EventBridge routes findings to SNS/Lambda/SIEM.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Multi-Account Management           │  │               Response Actions              │   │
│   │      Delegated admin: security account       │  │       EventBridge rule: pattern match       │   │
│   │     Auto-enable for new member accounts      │  │         Lambda: isolate EC2 instance        │   │
│   │         Aggregate findings centrally         │  │           SNS: alert on-call team           │   │
│   │       Suppression rules: reduce noise        │  │        Security Hub: ingest findings        │   │
│   │        Export: EventBridge → S3/SIEM         │  │     Threat Intel: custom IP/domain list     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS GuardDuty ML infrastructure · Regional data processing · CloudTrail/Flow Log feeds               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Finding         = GuardDuty security alert with type, severity, and affected resource                │
│  Finding type    = Structured name: ThreatPurpose:ResourceTypeAffected/ThreatFamilyName               │
│  Severity        = Numeric 0.1–8.9 mapped to LOW/MEDIUM/HIGH                                          │
│  Delegated admin = Member account designated to manage GuardDuty org-wide                             │
│  Suppression rule= Filter that archives matching findings automatically to reduce noise               │
│  Trusted IP list = Whitelist of IPs that GuardDuty will not generate findings for                     │
│  Threat intel    = Custom IP/domain list uploaded to GuardDuty as threat indicator                    │
│  EKS protection  = GuardDuty monitors Kubernetes audit logs for anomalous activity                    │
│  Runtime monitoring= GuardDuty agent on EC2/ECS/EKS for process-level detection                       │
│  Malware protection= GuardDuty scans EBS volumes of flagged instances for malware                     │
│  EventBridge export= GuardDuty sends findings to EventBridge for automated routing                    │
│  30-day free trial= GuardDuty offers 30-day free trial per account per region                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Before you begin

- **Access:** Admin credentials on all affected systems
- **Change management:** security changes require CAB approval in most environments
- **Rollback plan:** document current state before any security control change
- **Testing:** validate in a non-production environment first where possible

---

## Overview

AWS GuardDuty notes for day-to-day infrastructure operations.

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
