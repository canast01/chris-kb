# AWS S3 Replication
## Overview

AWS S3 Replication notes for day-to-day infrastructure operations.

```
┌─────────────────────────────────────────────────────────┐
│                  S3 Replication Flow                    │
│                                                         │
│  Source Bucket (eu-west-1)                              │
│  ├── Versioning: enabled (required)                     │
│  └── Replication rule: prefix / tag filter              │
│        │                                                │
│        ▼  (async · new objects only)                    │
│  Destination Bucket                                     │
│  ├── Same-Region Replication (SRR) — same account/cross │
│  └── Cross-Region Replication (CRR) — DR · compliance   │
│                                                         │
│  SRR use cases: log aggregation · test/prod sync        │
│  CRR use cases: DR · latency reduction · compliance     │
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
