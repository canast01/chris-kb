# AWS Cost Explorer / Billing

```
Cost Explorer Billing: Account → Breakdown → Report
──────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────┐
  │  AWS Account (or Management Account)                 │
  │  Billing period: monthly                             │
  └──────────────────────────┬───────────────────────────┘
                             │
                ┌────────────┼───────────────────┐
                ▼            ▼                   ▼
  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐
  │  By Service     │ │  By Account     │ │  By Region   │
  │  EC2: $X        │ │  Prod: $X       │ │  eu-west: $X │
  │  RDS: $Y        │ │  Dev:  $Y       │ │  us-east: $Y │
  │  S3:  $Z        │ │  Staging: $Z    │ │              │
  └─────────────────┘ └─────────────────┘ └──────────────┘
                             │
                ┌────────────┼───────────────────┐
                ▼            ▼                   ▼
  ┌─────────────────┐ ┌─────────────────┐ ┌──────────────┐
  │  By Tag         │ │  Forecast       │ │  RI / SP     │
  │  env=prod       │ │  Next 30 days   │ │  Coverage    │
  │  team=platform  │ │  trend line     │ │  Utilisation │
  └─────────────────┘ └─────────────────┘ └──────────────┘
```

## Overview

AWS Cost Explorer / Billing notes for day-to-day infrastructure operations.

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
