---
tags:
  - aws
---
# AWS Cost Anomaly Detection


<div class="kb-summary">
AWS Cost Anomaly Detection reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌────────────────────────────────── AWS Cost — Cost Anomaly Detection ──────────────────────────────────┐
│                                                                                                       │
│  ML-based service detecting unexpected cost spikes across services, accounts, and tags.               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Monitor Configuration             │  │             Alert Configuration             │   │
│   │          Monitor: AWS service level          │  │           Threshold: $ or % impact          │   │
│   │           Monitor: linked account            │  │          Frequency: daily or weekly         │   │
│   │            Monitor: cost category            │  │           SNS: email/Slack/Lambda           │   │
│   │           Monitor: custom tag key            │  │         Root cause: service + usage         │   │
│   │          ML: learns spend patterns           │  │          Acknowledge: mark reviewed         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ML baseline takes ~10 days to establish; anomalies detected against that pattern                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Anomaly Details                │  │             Investigation Steps             │   │
│   │           Impact: total $ overage            │  │          Cost Explorer: drill down          │   │
│   │         Root cause: top contributor          │  │           CloudTrail: who launched          │   │
│   │          Duration: start/end dates           │  │          Config: resource timeline          │   │
│   │           Score: confidence 0-100            │  │         Tag: find untagged resource         │   │
│   │        Feedback: expected/unexpected         │  │          Budget action: stop spend          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Cost Anomaly Detection service · SNS · Cost Explorer · CloudTrail                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Anomaly monitor = Scope definition for anomaly detection: service, account, or tag                   │
│  ML model        = Learns historical spend patterns; flags deviations as anomalies                    │
│  Anomaly score   = Confidence level 0-100; higher = more likely genuine anomaly                       │
│  Root cause      = Service and usage type contributing most to the cost spike                         │
│  Impact $        = Dollar amount by which spend exceeded expected baseline                            │
│  Acknowledge     = Mark anomaly as reviewed; improves ML model feedback                               │
│  Feedback        = Mark anomaly as expected/unexpected; trains future detection                       │
│  Alert threshold = Minimum $ or % impact before alert fires                                           │
│  Daily alert     = Sends notification each day an ongoing anomaly persists                            │
│  Weekly summary  = Single weekly digest of all anomalies in the period                                │
│  Cost Explorer   = Used to drill into anomaly root cause by service/region/tag                        │
│  Budget action   = Preventive control to stop spending when anomaly is detected                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Overview

AWS Cost Anomaly Detection notes for day-to-day infrastructure operations.

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
