---
tags:
  - vxrail
description: "VxRail Service Health reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections."
---
# VxRail Service Health

<div class="kb-summary">
VxRail Service Health reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: VxRail 7.x · 8.x*
</div>

```d2
direction: down

where_it_fits: "Where It Fits" {shape: rectangle}
daily_checks: "Daily Checks" {shape: rectangle}
health_commands: "Health Commands" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}
operational_tasks: "Operational Tasks" {shape: rectangle}
upgrade_notes: "Upgrade Notes" {shape: rectangle}

where_it_fits -> daily_checks: uses
daily_checks -> health_commands: uses
health_commands -> common_issues: uses
common_issues -> operational_tasks: uses
operational_tasks -> upgrade_notes: uses
```

## Overview

VxRail Manager service status, UI access, alerts, and management plane checks.

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
