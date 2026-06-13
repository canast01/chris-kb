---
tags:
  - aws
---
# AWS Compliance Review


<div class="kb-summary">
AWS Compliance Review reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: AWS*
</div>

```text
┌───────────────────────────────── AWS Governance — Compliance Review ──────────────────────────────────┐
│                                                                                                       │
│  Periodic compliance review using Security Hub, Audit Manager, and Config dashboards.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Review Cadence                │  │                    Tools                    │   │
│   │          Weekly: Security Hub score          │  │        Security Hub: findings + score       │   │
│   │         Monthly: Config compliance %         │  │           Audit Manager: evidence           │   │
│   │           Quarterly: access review           │  │          Config: rule compliance %          │   │
│   │           Annual: penetration test           │  │           Trusted Advisor: checks           │   │
│   │          On-demand: incident audit           │  │            Inspector: vuln report           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Security Hub score tracked weekly; quarterly access review drives remediation                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Compliance Frameworks             │  │             Remediation Process             │   │
│   │            CIS AWS Foundations v3            │  │        Triage: severity CRITICAL/HIGH       │   │
│   │         AWS Foundational Best Pract.         │  │            Assign: team ownership           │   │
│   │          NIST CSF: via Security Hub          │  │          SLA: 7d critical, 30d high         │   │
│   │         PCI DSS: if card data scope          │  │         Verify: re-check rule state         │   │
│   │         SOC 2: Audit Manager reports         │  │      Exception: documented suppression      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Security Hub · Audit Manager · Config · Inspector · Trusted Advisor · CloudTrail                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Security Hub score= Percentage of security checks passing; target > 90%                              │
│  CIS AWS v3      = Center for Internet Security AWS benchmark; prescriptive controls                  │
│  Audit Manager   = Maps AWS findings to SOC 2, PCI, NIST evidence requirements                        │
│  Trusted Advisor = AWS service flagging cost, security, and performance issues                        │
│  Inspector       = Vulnerability scanner for EC2 AMIs and container images                            │
│  NIST CSF        = National Institute of Standards and Technology Cybersecurity Framework             │
│  SOC 2           = Service Organisation Control 2; trust services criteria audit                      │
│  PCI DSS         = Payment Card Industry Data Security Standard                                       │
│  Penetration test= AWS permission required for external security testing                              │
│  Exception       = Suppressed finding with documented business justification                          │
│  Remediation SLA = Maximum time allowed to fix findings by severity level                             │
│  Access review   = Quarterly check of IAM users, roles, and permission sets                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Compliance Review notes for day-to-day infrastructure operations.

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
