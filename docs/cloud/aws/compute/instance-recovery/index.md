# AWS Instance Recovery
## Overview

AWS Instance Recovery notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│               EC2 Instance Recovery Flow                │
│                                                         │
│  CloudWatch Alarm                                       │
│  └── Metric: StatusCheckFailed_System ≥ 1 for 2 min     │
│        │                                                │
│        ▼                                                │
│  Alarm Action: recover                                  │
│        │                                                │
│        ▼                                                │
│  AWS migrates instance to healthy host                  │
│  ├── Same instance ID preserved                         │
│  ├── Same private/public IPs preserved                  │
│  ├── Same EBS volumes reattached                        │
│  └── In-memory state lost (equivalent to reboot)        │
│                                                         │
│  Note: does NOT work for instance-store root volumes     │
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
