# AWS Permission Review
## Overview

AWS Permission Review notes for day-to-day infrastructure operations.

```text
┌─────────────────────────────────────────────────────────┐
│               Permission Review Process                 │
│                                                         │
│  IAM Access Analyzer                                    │
│  └── Scans resource policies for external access        │
│        (S3 · IAM roles · KMS · Lambda · SQS)            │
│                                                         │
│  IAM Access Advisor                                     │
│  └── Last accessed date per service per user/role       │
│       (find and remove unused permissions)              │
│                                                         │
│  Credential Report                                      │
│  └── All users: password age · MFA · access key age     │
│                                                         │
│  Review cycle:                                          │
│  ├── Quarterly: review all human role assignments       │
│  ├── Monthly:   check unused roles / policies           │
│  └── On offboard: immediately revoke all access         │
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
