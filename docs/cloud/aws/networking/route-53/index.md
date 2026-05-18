# AWS Route 53
## Overview

AWS Route 53 notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                Route 53 Architecture                    │
│                                                         │
│  Hosted Zone (example.com)                              │
│  ├── A record: www → ALB alias                          │
│  ├── CNAME: api.example.com → internal.example.com      │
│  └── MX, TXT, NS, SOA records                           │
│                                                         │
│  Routing Policies:                                      │
│  ├── Simple        one IP / one resource                │
│  ├── Weighted      A (80%) / B (20%) — canary           │
│  ├── Latency       nearest AWS region responds          │
│  ├── Failover      primary → secondary on health fail   │
│  └── Geolocation   route by user country/region         │
│                                                         │
│  Health checks: HTTP · HTTPS · TCP · CloudWatch alarm   │
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
