# AWS CloudWatch
## Overview

AWS CloudWatch notes for day-to-day infrastructure operations.

```text
┌─────────────────────────────────────────────────────────┐
│                 CloudWatch Data Model                   │
│                                                         │
│  Namespace (e.g. AWS/EC2)                               │
│  └── Metric (e.g. CPUUtilization)                       │
│       └── Dimension (InstanceId=i-abc123)               │
│            └── Data Points (timestamp + value)          │
│                 └── Statistics (avg · max · p99 …)      │
│                                                         │
│  Sources of metrics:                                    │
│  ├── AWS services (auto-published free)                 │
│  ├── CloudWatch Agent (OS: memory · disk · process)     │
│  └── Custom metrics (PutMetricData API)                 │
│                                                         │
│  Retention: 1-min → 15 days · 5-min → 63 days           │
│             1-hr  → 455 days (15 months)                │
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
