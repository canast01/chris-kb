# AWS Subnets
## Overview

AWS Subnets notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                  Subnet Types                           │
│                                                         │
│  PUBLIC SUBNET                  PRIVATE SUBNET          │
│  ─────────────                  ──────────────          │
│  Route: 0.0.0.0/0 → IGW         No IGW route            │
│  Resources can have public IPs  Private IPs only        │
│  Used for:                      Used for:               │
│  ├── ALB (load balancer)        ├── EC2 app servers      │
│  ├── NAT Gateway                ├── ECS tasks           │
│  └── Bastion (if needed)        └── Lambda (VPC mode)   │
│                                                         │
│  ISOLATED SUBNET                                        │
│  ─────────────────                                      │
│  No route to IGW or NAT GW      Used for: RDS · cache   │
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
