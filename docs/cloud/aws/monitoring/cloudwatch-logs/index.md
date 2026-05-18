# AWS CloudWatch Logs
## Overview

AWS CloudWatch Logs notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│               CloudWatch Logs Structure                 │
│                                                         │
│  Log Group (e.g. /aws/lambda/my-function)               │
│  └── Log Stream (one per Lambda invocation context)     │
│       └── Log Events (timestamp + message)              │
│                                                         │
│  Features:                                              │
│  ├── Metric Filters  → extract value → CloudWatch metric│
│  ├── Log Insights    → ad-hoc KQL-like query            │
│  ├── Subscription    → stream to Lambda / Kinesis       │
│  └── Retention       → set per log group (1d – 10yr)    │
│                                                         │
│  Sources: Lambda · EC2 (CW Agent) · ECS · VPC Flow Logs │
│           CloudTrail · RDS · API Gateway                │
└─────────────────────────────────────────────────────────┘
```

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
