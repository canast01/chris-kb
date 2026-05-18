# VxRail Support Case Prep
## Overview

Evidence, timeline, logs, screenshots, and clear issue summary for Dell support.

```
  ┌──────────────────────────────────────────────────────┐
  │            Dell Support Case Prep Flow               │
  │                                                      │
  │  Collect logs                                        │
  │  VxRail Mgr → Support → Generate bundle             │
  │  iDRAC → racadm getsel (hardware events)            │
  │                 │                                    │
  │                 ▼                                    │
  │  ┌──────────────────────────────────────────────┐    │
  │  │  Timeline                                    │    │
  │  │  When started │ what changed │ impact scope  │    │
  │  │  Exact timestamps from logs / vCenter events │    │
  │  └──────────────────────┬───────────────────────┘    │
  │                         ▼                            │
  │  ┌──────────────────────────────────────────────┐    │
  │  │  Screenshots                                 │    │
  │  │  VxRail Mgr alert │ vCenter alarm │ error msg│    │
  │  │  LCM job status if applicable                │    │
  │  └──────────────────────┬───────────────────────┘    │
  │                         ▼                            │
  │  ┌──────────────────────────────────────────────┐    │
  │  │  Clear issue summary                         │    │
  │  │  Service tag │ VxRail version │ node count   │    │
  │  │  Symptom │ impact │ steps taken              │    │
  │  └──────────────────────┬───────────────────────┘    │
  │                         ▼                            │
  │  Open SR ──► attach bundle ──► paste summary        │
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
