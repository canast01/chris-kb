# AWS Budgets

```
┌───────────────────────────────────────── AWS Cost — Budgets ──────────────────────────────────────────┐
│                                                                                                       │
│  AWS Budgets sets cost and usage thresholds with alerts and optional auto-actions.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Budget Types                 │  │             Budget Configuration            │   │
│   │            Cost: total spend ($)             │  │          Period: monthly/quarterly          │   │
│   │           Usage: units (GB, hours)           │  │         Filter: account/service/tag         │   │
│   │          RI utilisation: coverage %          │  │          Forecast: projected spend          │   │
│   │           Savings Plans coverage %           │  │         Alert: actual or forecasted         │   │
│   │         Comparison: vs prior period          │  │           SNS: notification target          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Alerts fire when actual or forecasted spend crosses threshold percentage                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Budget Actions                │  │                Best Practices               │   │
│   │          SCP: restrict service use           │  │              Per account budget             │   │
│   │            IAM: deny EC2 launches            │  │             Alert at 80% + 100%             │   │
│   │          Require approval: SSO gate          │  │        Forecast alert: early warning        │   │
│   │          Trigger: actual threshold           │  │           Tag-based: team budgets           │   │
│   │            Test: manually trigger            │  │        Review: monthly FinOps meeting       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AWS Budgets service · SNS · SCP engine · IAM · Cost Explorer data feed                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Budget action   = Automated response when budget threshold is breached                               │
│  Forecasted alert= Fires when projected end-of-period spend will exceed threshold                     │
│  Actual alert    = Fires when real spend to date crosses threshold                                    │
│  RI utilisation  = % of reserved instance hours actually consumed                                     │
│  Savings Plans coverage= % of eligible spend covered by Savings Plans                                 │
│  SCP action      = Budget action attaching an SCP to restrict further spending                        │
│  IAM action      = Budget action attaching IAM policy denying launch of resources                     │
│  FinOps          = Financial Operations; cloud cost management practice                               │
│  SNS target      = Budget alert publishes to SNS; subscribers get email/Slack/Lambda                  │
│  Tag filter       = Budget scoped to resources with specific tag key/value                            │
│  Period          = Evaluation window: monthly resets on 1st; quarterly on quarter start               │
│  Cost anomaly    = Separate service; detects unexpected spend spikes via ML                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
AWS Budgets: Alert Flow
──────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────┐
  │  Budget Definition                                   │
  │  Type: Cost / Usage / RI / Savings Plans             │
  │  Period: Monthly / Quarterly / Annual                │
  │  Amount: $500 / month                                │
  └───────────────────────┬──────────────────────────────┘
                          │
                          ▼
  ┌──────────────────────────────────────────────────────┐
  │  Threshold Alerts                                    │
  │  80% of budget ─────────────────────► Alert 1       │
  │  100% of budget ────────────────────► Alert 2       │
  │  100% forecasted ───────────────────► Alert 3       │
  └───────────────────────┬──────────────────────────────┘
                          │
                          ▼
  ┌───────────────┐   ┌───────────────┐   ┌────────────────┐
  │  SNS Topic    │   │  Email        │   │  Budget Action │
  │  → Slack/     │   │  direct to    │   │  Apply SCP     │
  │    PagerDuty  │   │  owner        │   │  Run SSM doc.  │
  └───────────────┘   └───────────────┘   └────────────────┘
```

## Overview

AWS Budgets notes for day-to-day infrastructure operations.

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
