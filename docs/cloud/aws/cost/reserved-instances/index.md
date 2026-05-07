# AWS Reserved Instances

```mermaid
flowchart LR
    Reserved_Instances["Reserved Instances"]
    Reserved_Instances --> S0["Where It Fits"]
    Reserved_Instances --> S1["Daily Checks"]
    Reserved_Instances --> S2["Health Commands"]
    Reserved_Instances --> S3["Common Issues"]
    Reserved_Instances --> S4["Operational Tasks"]
    Reserved_Instances --> S5["Upgrade Notes"]
    Reserved_Instances --> S6["Best Practices"]
```

## Overview

AWS Reserved Instances notes for day-to-day infrastructure operations.

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
