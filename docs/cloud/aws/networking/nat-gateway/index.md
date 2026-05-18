# AWS NAT Gateway
## Overview

AWS NAT Gateway notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                  NAT Gateway Flow                       │
│                                                         │
│  Private Subnet                                         │
│  └── EC2 (private IP 10.0.1.10)                         │
│        │  outbound request (e.g. yum update)            │
│        ▼                                                │
│  NAT Gateway (in public subnet · Elastic IP)            │
│  ├── Source NATs request to its Elastic IP              │
│  └── Returns response to originating EC2               │
│        │                                                │
│        ▼                                                │
│  IGW ──► Internet (outbound only — inbound blocked)     │
│                                                         │
│  Deploy one NAT GW per AZ (for HA / AZ redundancy)      │
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
