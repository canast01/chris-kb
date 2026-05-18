# AWS Internet Gateway
## Overview

AWS Internet Gateway notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                Internet Gateway (IGW)                   │
│                                                         │
│  Internet                                               │
│     │                                                   │
│     ▼                                                   │
│  IGW (attached to VPC — one IGW per VPC)                │
│     │                                                   │
│     ▼                                                   │
│  Public Subnet (route 0.0.0.0/0 → igw-xxxx)            │
│  └── Resource with public IP / Elastic IP               │
│                                                         │
│  IGW performs NAT for public IP ↔ private IP mapping    │
│  IGW is HA by design — AWS manages redundancy           │
│  No cost for the gateway itself; data transfer billed   │
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
