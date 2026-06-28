---
tags:
  - operations
  - vxrail
---
# VxRail Support Case Prep

<div class="kb-summary">
VxRail Support Case Prep reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: VxRail 7.x / 8.x*
</div>

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Overview

Evidence, timeline, logs, screenshots, and clear issue summary for Dell support.

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

```bash
# Add environment-specific commands here
```

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

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [VxRail — Backup & Restore](backup-restore.md)
- [VxRail — CLI Reference](cli-reference.md)
- [VxRail Cluster Expansion](cluster-expansion.md)
- [VxRail Operations](index.md)
- [VxRail — Architecture](../../architecture/)
- [VxRail — Deploy](../../deploy/)
- [VxRail Security](../../security/)
- [VxRail Troubleshooting](../../troubleshooting/)
