# AWS EFS
## Overview

AWS EFS notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                  EFS Architecture                       │
│                                                         │
│  EFS File System (regional — spans all AZs)             │
│  ├── Mount Target AZ-a  (ENI in subnet-a)               │
│  ├── Mount Target AZ-b  (ENI in subnet-b)               │
│  └── Mount Target AZ-c  (ENI in subnet-c)               │
│                                                         │
│  EC2 (AZ-a) ──NFS4.1──► Mount Target AZ-a ──► EFS       │
│  EC2 (AZ-b) ──NFS4.1──► Mount Target AZ-b ──► EFS       │
│  (multiple EC2s read/write same filesystem concurrently) │
│                                                         │
│  Performance modes: General Purpose (default) · Max I/O │
│  Throughput modes:  Bursting · Provisioned · Elastic    │
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
