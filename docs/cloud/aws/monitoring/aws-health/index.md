# AWS Health
## Overview

AWS Health notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                  AWS Health Overview                    │
│                                                         │
│  AWS Service Health Dashboard                           │
│  └── Global service status (public · all regions)       │
│                                                         │
│  Personal Health Dashboard (your account)               │
│  ├── Service issues affecting your resources            │
│  ├── Scheduled maintenance (EC2 retirement · patching)  │
│  └── Account-specific advisories                        │
│        │                                                │
│        ▼                                                │
│  EventBridge (aws.health event source)                  │
│  └── Rule: health event → SNS → PagerDuty / email       │
│                                                         │
│  AWS Health API: programmatic access to all events      │
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
