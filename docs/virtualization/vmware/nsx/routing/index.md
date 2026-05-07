# NSX Routing

```mermaid
flowchart LR
    NSX_Routing["NSX Routing"]
    NSX_Routing --> S0["Where It Fits"]
    NSX_Routing --> S1["Daily Checks"]
    NSX_Routing --> S2["Health Commands"]
    NSX_Routing --> S3["Common Issues"]
    NSX_Routing --> S4["Operational Tasks"]
    NSX_Routing --> S5["Upgrade Notes"]
    NSX_Routing --> S6["Best Practices"]
```

## Overview

BGP, static routes, route advertisement, troubleshooting, and validation.

## Where It Fits

Use this page for VMware platform support, daily checks, troubleshooting, upgrade prep, and operational review.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review active alarms. |  |  |
| Check recent failed tasks. |  |  |
| Confirm service health. |  |  |
| Confirm capacity and performance are normal. |  |  |
| Check recent changes. |  |  |

## Health Commands

~~~bash
# Add environment-specific commands here
~~~

## Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

## Operational Tasks


| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

## Upgrade Notes

- Confirm compatibility.
- Review known issues.
- Confirm rollback plan.
- Validate health before and after the change.

## Best Practices


| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Keep versions aligned. | Keep versions aligned. |
| Avoid unsupported version combinations. | Avoid unsupported version combinations. |
| Document exceptions. | Document exceptions. |
| Validate after every change. | Validate after every change. |
