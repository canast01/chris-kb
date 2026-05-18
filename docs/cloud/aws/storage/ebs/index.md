# AWS EBS
## Overview

AWS EBS notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                EBS Volume Architecture                  │
│                                                         │
│  EC2 Instance ──── EBS Volume (same AZ required)        │
│                     ├── Type: gp3 (default, cost-eff.)  │
│                     ├── Type: io2 (high IOPS, 64k+)     │
│                     ├── Type: st1 (throughput HDD)       │
│                     └── Type: sc1 (cold HDD, cheap)     │
│                                                         │
│  EBS Volume ──► Snapshot ──► S3 (incremental)           │
│                               │                         │
│                    copy cross-region for DR              │
│                    restore as new volume                 │
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
