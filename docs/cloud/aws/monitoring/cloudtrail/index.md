# AWS CloudTrail
## Overview

AWS CloudTrail notes for day-to-day infrastructure operations.

```text
┌─────────────────────────────────────────────────────────┐
│               CloudTrail Architecture                   │
│                                                         │
│  AWS API call (Console · CLI · SDK · Service)           │
│        │                                                │
│        ▼                                                │
│  CloudTrail Event                                       │
│  ├── Management events (control plane — free 90d)       │
│  ├── Data events       (S3 obj ops · Lambda invoke)     │
│  └── Insight events    (unusual API activity)           │
│        │                                                │
│        ▼                                                │
│  Trail (all-region recommended)                         │
│  ├── S3 bucket (log archive account)                    │
│  └── CloudWatch Logs (for metric filter alerts)         │
│                                                         │
│  Integrity: log file validation (SHA-256 hash chain)    │
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
