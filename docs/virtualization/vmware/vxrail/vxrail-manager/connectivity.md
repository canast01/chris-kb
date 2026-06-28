---
tags:
  - vxrail
---
# VxRail Connectivity

<div class="kb-summary">
VxRail Connectivity reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.

*Applies to: VxRail 7.x · 8.x*
</div>
![VxRail Connectivity](../../../../assets/virtualization-vmware-vxrail-vxrail-manager-connectivity.svg)




```d2
direction: right

center: "VxRail" {shape: hexagon}
where_it_fits: "Where It Fits" {shape: rectangle}
daily_checks: "Daily Checks" {shape: rectangle}
health_commands: "Health Commands" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}
operational_tasks: "Operational Tasks" {shape: rectangle}
upgrade_notes: "Upgrade Notes" {shape: rectangle}

center -> where_it_fits
center -> daily_checks
center -> health_commands
center -> common_issues
center -> operational_tasks
center -> upgrade_notes
```

## Overview

Connectivity to vCenter, hosts, Dell services, DNS, NTP, and support endpoints.

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
