---
tags:
  - aws
---
# AWS CloudWatch Alarms


<div class="kb-summary">
AWS CloudWatch Alarms reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: AWS*
</div>

```text
┌─────────────────────────────── CloudWatch Alarms — Threshold Alerting ────────────────────────────────┐
│                                                                                                       │
│  CloudWatch Alarms evaluate metrics against thresholds and trigger automated responses.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Alarm Configuration              │  │                 Alarm Types                 │   │
│   │       Metric: namespace + name + dims        │  │        Static: fixed threshold value        │   │
│   │         Period: evaluation interval          │  │          Anomaly detection: ML band         │   │
│   │     Evaluation periods: N of M breaches      │  │      Composite: Boolean of child alarms     │   │
│   │        Threshold: comparison + value         │  │          Metric math: formula-based         │   │
│   │     Missing data: breaching/notBreaching     │  │         Billing alarm: account spend        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Alarms in ALARM state trigger actions; composite alarms reduce alert noise with logic.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Alarm Actions                 │  │                Best Practices               │   │
│   │       SNS: notify teams via email/SMS        │  │        Use composite to reduce noise        │   │
│   │      EC2: stop/reboot/terminate/recover      │  │         Datapoints to alarm: N of M         │   │
│   │      Auto Scaling: scale-out/in policy       │  │        Set breaching for missing data       │   │
│   │       Systems Manager OpsItem creation       │  │         Tag alarms with team/service        │   │
│   │      Lambda: custom remediation trigger      │  │        Test with set-alarm-state CLI        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS CloudWatch control plane · Regional endpoints · SNS delivery infrastructure                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Evaluation period= Time window for one metric data point comparison against threshold                │
│  Datapoints to alarm= Number of breaching periods needed before alarm state triggers                  │
│  N of M            = Alarm triggers when N out of last M evaluation periods breach                    │
│  ALARM state       = Threshold breached for required number of consecutive/total periods              │
│  OK state          = Metric is within acceptable range for all evaluation periods                     │
│  INSUFFICIENT_DATA = Not enough metric data points to evaluate the alarm condition                    │
│  Composite alarm   = Parent alarm whose state is computed from child alarm states                     │
│  Anomaly band      = ML-derived upper/lower bounds; alarm fires outside the band                      │
│  treat missing data= How to count missing data points: notBreaching, breaching, ignore                │
│  EC2 recover action= Auto-recover instance on system check failure; preserves private IP              │
│  Billing alarm     = Monitors EstimatedCharges metric; requires billing alerts enabled                │
│  OpsItem action    = Creates Systems Manager OpsItem when alarm fires for ITSM tracking               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS CloudWatch Alarms notes for day-to-day infrastructure operations.

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
