# AWS AMIs
## Overview

AWS AMIs notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                     AMI Architecture                    │
│                                                         │
│  Source EC2 Instance                                    │
│  └── Create Image ──► AMI (registered in EC2)           │
│                        ├── Root volume snapshot (EBS)   │
│                        ├── Launch permissions           │
│                        ├── Kernel / RAM disk IDs        │
│                        └── Block device mapping         │
│                                                         │
│  AMI ──► Launch ──► New EC2 Instance                    │
│                     (identical root disk + config)      │
│                                                         │
│  AMI types: Amazon Linux · Ubuntu · Windows · custom    │
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
