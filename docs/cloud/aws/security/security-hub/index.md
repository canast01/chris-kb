# AWS Security Hub


<div class="kb-summary">
AWS Security Hub reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```
┌───────────────────────────── Security Hub — Aggregated Security Posture ──────────────────────────────┐
│                                                                                                       │
│  Security Hub aggregates findings from AWS services and third parties into a central score.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Data Sources (Finding Integrations)      │  │             Compliance Standards            │   │
│   │          GuardDuty: threat findings          │  │          CIS AWS Benchmark v1.4/3.0         │   │
│   │      Inspector: vulnerability findings       │  │        AWS Foundational Security Best       │   │
│   │       Config: non-compliant resources        │  │                PCI DSS v3.2.1               │   │
│   │         IAM Access Analyzer findings         │  │             NIST SP 800-53 Rev 5            │   │
│   │      Macie, Firewall Manager, 3rd party      │  │        Custom standard (self-managed)       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Security score = % controls passing; findings routed via EventBridge to SIEM/ticketing.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Multi-Account Management           │  │               Finding Workflow              │   │
│   │      Delegated admin: security account       │  │        Status: NEW/NOTIFIED/RESOLVED        │   │
│   │        Auto-enable on new org members        │  │         Workflow: assign owner/notes        │   │
│   │      Cross-region aggregation: one pane      │  │       Suppression: auto-archive rules       │   │
│   │      Finding aggregation region option       │  │          EventBridge: route to SIEM         │   │
│   │      Custom actions: EventBridge target      │  │        ASFF: standard finding format        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Security Hub regional service · EventBridge integration infrastructure · ASFF schema             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Security Hub    = AWS service aggregating security findings with posture scoring                     │
│  Security score  = Percentage of enabled standard controls passing across all accounts                │
│  ASFF            = Amazon Security Finding Format; standardised JSON finding schema                   │
│  Control         = Specific check within a compliance standard; PASS/FAIL/NO_DATA                     │
│  Standard        = Collection of controls, e.g. CIS Benchmark or FSBP                                 │
│  Delegated admin = Member account with org-wide Security Hub management rights                        │
│  Custom action   = User-defined action sending selected findings to EventBridge                       │
│  Finding aggregation= Option to centralise findings from all regions to one region                    │
│  Suppression rule= Auto-archive filter for expected/accepted findings                                 │
│  Workflow status = Finding lifecycle: NEW → NOTIFIED → IN_PROGRESS → RESOLVED                         │
│  FSBP            = AWS Foundational Security Best Practices; AWS-maintained standard                  │
│  Macie           = Data protection service; sends S3 sensitive data findings to Hub                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────── Security Hub — Aggregated Security Posture ──────────────────────────────┐
│                                                                                                       │
│  Security Hub aggregates findings from AWS services and third parties into a central score.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Data Sources (Finding Integrations)      │  │             Compliance Standards            │   │
│   │          GuardDuty: threat findings          │  │          CIS AWS Benchmark v1.4/3.0         │   │
│   │      Inspector: vulnerability findings       │  │        AWS Foundational Security Best       │   │
│   │       Config: non-compliant resources        │  │                PCI DSS v3.2.1               │   │
│   │         IAM Access Analyzer findings         │  │             NIST SP 800-53 Rev 5            │   │
│   │      Macie, Firewall Manager, 3rd party      │  │        Custom standard (self-managed)       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Security score = % controls passing; findings routed via EventBridge to SIEM/ticketing.              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Multi-Account Management           │  │               Finding Workflow              │   │
│   │      Delegated admin: security account       │  │        Status: NEW/NOTIFIED/RESOLVED        │   │
│   │        Auto-enable on new org members        │  │         Workflow: assign owner/notes        │   │
│   │      Cross-region aggregation: one pane      │  │       Suppression: auto-archive rules       │   │
│   │      Finding aggregation region option       │  │          EventBridge: route to SIEM         │   │
│   │      Custom actions: EventBridge target      │  │        ASFF: standard finding format        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Security Hub regional service · EventBridge integration infrastructure · ASFF schema             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Security Hub    = AWS service aggregating security findings with posture scoring                     │
│  Security score  = Percentage of enabled standard controls passing across all accounts                │
│  ASFF            = Amazon Security Finding Format; standardised JSON finding schema                   │
│  Control         = Specific check within a compliance standard; PASS/FAIL/NO_DATA                     │
│  Standard        = Collection of controls, e.g. CIS Benchmark or FSBP                                 │
│  Delegated admin = Member account with org-wide Security Hub management rights                        │
│  Custom action   = User-defined action sending selected findings to EventBridge                       │
│  Finding aggregation= Option to centralise findings from all regions to one region                    │
│  Suppression rule= Auto-archive filter for expected/accepted findings                                 │
│  Workflow status = Finding lifecycle: NEW → NOTIFIED → IN_PROGRESS → RESOLVED                         │
│  FSBP            = AWS Foundational Security Best Practices; AWS-maintained standard                  │
│  Macie           = Data protection service; sends S3 sensitive data findings to Hub                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS Security Hub notes for day-to-day infrastructure operations.

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
