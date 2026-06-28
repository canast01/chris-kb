---
tags:
  - vxrail
---
# VxRail Technical Deep Dive

<div class="kb-summary">
VxRail Technical Deep Dive reference covering Overview, Platform Role, Core Components, Main Dependencies, Ports and Protocols and 7 more sections.

*Applies to: VxRail 7.x · 8.x*
</div>

## Overview

VxRail is part of the virtualization platform. This page is for technical operations, troubleshooting, upgrade planning, and support handoff.

## Platform Role

VxRail is a Dell integrated HCI platform built on VMware vSphere and vSAN with Dell lifecycle, hardware, and support integration.

## Core Components

- VxRail Manager
- vCenter
- ESXi hosts
- vSAN cluster
- Dell hardware
- iDRAC
- Lifecycle services
- Support bundle tooling
- Secure Remote Services / support connectivity

## Main Dependencies

- DNS resolution
- NTP/time sync
- Authentication source
- Management network
- Storage access
- Certificate trust
- Monitoring
- Backup/recovery process
- Vendor support access

## Ports and Protocols

| Use | Protocol | Port |
|-----|----------|------|
| VxRail Manager UI/API | HTTPS | 443 |
| vCenter | HTTPS | 443 |
| ESXi host management | HTTPS | 443 |
| iDRAC | HTTPS | 443 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

## Key Logs

- VxRail Manager logs
- Lifecycle operation logs
- Support bundles
- ESXi logs
- vCenter logs
- iDRAC hardware logs

## Health Checks

- Confirm management access.
- Review current alarms.
- Review recent failed tasks.
- Validate DNS and NTP.
- Confirm certificate status.
- Check service health.
- Check capacity and performance.
- Confirm monitoring data is current.
- Review recent changes.

## Useful Commands

```bash
df -h
systemctl --failed
systemctl status vmware-marvin
journalctl -xe
curl -k https://localhost/rest/vxm/internal/system
```

## Common Failure Points

- LCM pre-check failure
- Bundle compatibility issue
- Hardware warning
- vSAN health issue
- VxRail Manager service issue
- Support bundle failure
- iDRAC connectivity issue
- DNS/NTP issue

## Troubleshooting Workflow

1. Confirm the impact and scope.
2. Check recent changes.
3. Review alerts, tasks, and events.
4. Validate DNS, NTP, authentication, and certificates.
5. Check service status.
6. Check storage and network dependencies.
7. Review logs.
8. Capture screenshots, timestamps, errors, and task IDs.
9. Escalate with clean evidence if needed.

## Upgrade and Compatibility Notes

- Check product interoperability before upgrades.
- Confirm supported version path.
- Confirm backup or rollback method.
- Confirm maintenance window.
- Run pre-checks before change work.
- Validate health after the change.
- Document version before and after.

## Best Practices

| Recommendation | Detail |
|---|---|
| Keep versions aligned. | Keep versions aligned. |
| Keep certificates tracked. | Keep certificates tracked. |
| Keep DNS and NTP clean. | Keep DNS and NTP clean. |
| Keep alerting actionable. | Keep alerting actionable. |
| Document support ownership. | Document support ownership. |
| Avoid undocumented changes. | Avoid undocumented changes. |
