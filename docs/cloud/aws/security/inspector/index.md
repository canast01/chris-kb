# AWS Inspector


<div class="kb-summary">
AWS Inspector reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌─────────────────────────────── AWS Inspector — Vulnerability Scanning ────────────────────────────────┐
│                                                                                                       │
│  Inspector continuously scans EC2, ECR container images, and Lambda for vulnerabilities.              │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Scan Targets                 │  │                Finding Types                │   │
│   │       EC2: OS packages + software CVEs       │  │      CVE: known software vulnerability      │   │
│   │       ECR: container image layers scan       │  │       Network: reachable port finding       │   │
│   │       Lambda: function code + packages       │  │       Code: Lambda code vulnerability       │   │
│   │       Auto-enabled: no config required       │  │       EPSS: exploit probability score       │   │
│   │      Continuous: rescan on new CVE pub       │  │       Severity: CRITICAL/HIGH/MED/LOW       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Inspector scores each finding with CVSS + EPSS; prioritise by exploitability score.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Multi-Account & Org              │  │             Remediation Workflow            │   │
│   │      Delegated admin: central findings       │  │       Security Hub: findings forwarded      │   │
│   │       Auto-enable on new org accounts        │  │       EventBridge: route critical CVEs      │   │
│   │      Suppression rules: noise reduction      │  │      Jira/ITSM: ticket via EventBridge      │   │
│   │       Export: JSON to S3 for analysis        │  │           Patch: SSM Patch Manager          │   │
│   │      Coverage: track enabled resources       │  │           Re-image: bake fixed AMI          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Inspector scanning infrastructure · SSM agent on EC2 · ECR registry endpoints                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CVE             = Common Vulnerabilities and Exposures; standardised vulnerability ID                │
│  CVSS            = Common Vulnerability Scoring System; 0–10 severity rating                          │
│  EPSS            = Exploit Prediction Scoring System; probability of exploitation                     │
│  Inspector score = Adjusted CVSS considering exploitability and network reachability                  │
│  Network finding = Inspector detects EC2 ports reachable from 0.0.0.0/0 via SG rules                  │
│  ECR scan        = Inspector scans container images pushed to ECR automatically                       │
│  Lambda scan     = Inspector analyses Lambda function code and package dependencies                   │
│  Continuous scan = Inspector rescans whenever a new CVE is published for known packages               │
│  Suppression rule= Filter that archives findings matching a specific pattern                          │
│  Delegated admin = Member account with org-wide Inspector visibility and management                   │
│  Coverage        = Percentage of resources successfully scanned by Inspector                          │
│  SSM agent       = Required on EC2 for Inspector to collect package inventory data                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Inspector notes for day-to-day infrastructure operations.

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
