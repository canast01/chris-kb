# AWS EBS Snapshots

```mermaid
flowchart LR
    EBS_Snapshots["EBS Snapshots"]
    EBS_Snapshots --> S0["Where It Fits"]
    EBS_Snapshots --> S1["Daily Checks"]
    EBS_Snapshots --> S2["Health Commands"]
    EBS_Snapshots --> S3["Common Issues"]
    EBS_Snapshots --> S4["Operational Tasks"]
    EBS_Snapshots --> S5["Upgrade Notes"]
    EBS_Snapshots --> S6["Best Practices"]
```

## Overview

AWS EBS Snapshots notes for day-to-day infrastructure operations.

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
