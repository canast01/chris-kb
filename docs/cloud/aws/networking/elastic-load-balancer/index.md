# AWS Elastic Load Balancer
## Overview

AWS Elastic Load Balancer notes for day-to-day infrastructure operations.

```text
┌─────────────────────────────────────────────────────────┐
│                  ELB Traffic Flow                       │
│                                                         │
│  Client ──► ALB (Application Load Balancer — Layer 7)   │
│              ├── Listener: HTTPS :443                   │
│              ├── Rules: path /api/* → target group A    │
│              │          path /*    → target group B     │
│              └── Target Group                           │
│                   ├── EC2 instance (healthy ✓)          │
│                   ├── EC2 instance (healthy ✓)          │
│                   └── EC2 instance (unhealthy ✗ skip)   │
│                                                         │
│  NLB (Network Load Balancer — Layer 4 TCP/UDP)          │
│  └── Static IP per AZ · ultra-low latency · TLS passthrough│
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
