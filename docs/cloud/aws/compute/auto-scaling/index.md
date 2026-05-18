# AWS Auto Scaling
## Overview

AWS Auto Scaling notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                  Auto Scaling Group Flow                │
│                                                         │
│  Launch Template (AMI · instance type · SG · userdata)  │
│        │                                                │
│        ▼                                                │
│  Auto Scaling Group                                     │
│  ├── Min capacity  (floor — never scale below)          │
│  ├── Desired capacity (current target)                  │
│  └── Max capacity  (ceiling — never exceed)             │
│        │                                                │
│  CloudWatch Metric (CPU · custom) ──► Scale Policy      │
│        ├── scale out: desired + N  (add instances)      │
│        └── scale in:  desired - N  (remove instances)   │
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
