# VxRail Connectivity
## Overview

Connectivity to vCenter, hosts, Dell services, DNS, NTP, and support endpoints.

```
  ┌──────────────────────────────────────────────────────┐
  │         VxRail Manager Connectivity Map              │
  │                                                      │
  │  ┌───────────────────────────────────────────────┐   │
  │  │             VxRail Manager VM                 │   │
  │  └────────────────────┬──────────────────────────┘   │
  │                       │                              │
  │     ┌─────────────────┼──────────────────┐           │
  │     ▼                 ▼                  ▼           │
  │  ┌────────┐  ┌─────────────────┐  ┌───────────────┐  │
  │  │vCenter │  │  ESXi Hosts     │  │  iDRAC (BMC)  │  │
  │  │:443    │  │  :443 (vpxd)    │  │  :443 / IPMI  │  │
  │  └────────┘  └─────────────────┘  └───────────────┘  │
  │     │                                                 │
  │     ├──► DNS (port 53)  ── hostname resolution       │
  │     ├──► NTP (port 123) ── time sync                 │
  │     └──► Dell SRS/SupportAssist (HTTPS outbound)     │
  │                                                      │
  │  Failure path:                                       │
  │  DNS fail ──► VxRail Mgr loses host connectivity    │
  │  NTP skew ──► cert validation / LCM errors           │
  └──────────────────────────────────────────────────────┘
```

## Where It Fits

Use this page for VxRail operations, support checks, lifecycle work, troubleshooting, and change validation.

## Daily Checks


| Check | Command | Notes |
|---|---|---|
| Review VxRail Manager health. |  |  |
| Check vCenter and ESXi host health. |  |  |
| Review vSAN health. |  |  |
| Confirm no active failed tasks. |  |  |
| Review hardware alerts. |  |  |
| Check recent lifecycle or support events. |  |  |

## Health Commands

~~~bash
# Add environment-specific commands here
~~~

## Common Issues

- Lifecycle pre-check failure.
- Host hardware warning.
- vSAN health warning.
- Failed update bundle.
- VxRail Manager service issue.
- Version compatibility issue.
- Support bundle collection failure.

## Operational Tasks


| Task | Command |
|---|---|
| Review cluster health. |  |
| Validate node status. |  |
| Confirm support connectivity. |  |
| Check upgrade readiness. |  |
| Collect support evidence. |  |
| Document changes and follow-up items. |  |

## Upgrade Notes

- Confirm upgrade path.
- Review Dell compatibility guidance.
- Confirm vCenter, ESXi, vSAN, and firmware versions.
- Validate backups and rollback notes.
- Run post-upgrade checks.

## Best Practices


| Recommendation | Detail |
|---|---|
| Do not skip pre-checks. | Do not skip pre-checks. |
| Keep Dell and VMware versions aligned. | Keep Dell and VMware versions aligned. |
| Validate hardware health before lifecycle work. | Validate hardware health before lifecycle work. |
| Keep support bundle notes with the case. | Keep support bundle notes with the case. |
| Record post-change validation. | Record post-change validation. |
