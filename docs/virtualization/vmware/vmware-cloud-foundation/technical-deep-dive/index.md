# VMware Cloud Foundation Technical Deep Dive

## Overview

VMware Cloud Foundation is part of the virtualization platform. This page is for technical operations, troubleshooting, upgrade planning, and support handoff.

## Platform Role

VMware Cloud Foundation provides an integrated private cloud stack using SDDC Manager to manage vSphere, vSAN, NSX, workload domains, lifecycle, and credentials.

## Core Components

- SDDC Manager
- Management domain
- Workload domains
- vCenter
- ESXi
- vSAN
- NSX
- Lifecycle Manager
- Password and certificate management
- Bundle repository

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
| SDDC Manager UI/API | HTTPS | 443 |
| vCenter | HTTPS | 443 |
| NSX Manager | HTTPS | 443 |
| ESXi host management | HTTPS | 443 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

## Key Logs

- SDDC Manager logs
- Lifecycle operation logs
- vCenter logs
- NSX Manager logs
- ESXi host logs
- Bring-up logs

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

~~~bash
systemctl status lcm
systemctl status domainmanager
systemctl status operationsmanager
systemctl status commonsvcs
df -h
journalctl -xe
~~~

## Common Failure Points

- Lifecycle bundle issue
- Compatibility mismatch
- Password drift
- Certificate drift
- Workload domain health issue
- SDDC Manager service issue
- NSX/vCenter dependency failure
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

- Keep versions aligned.
- Keep certificates tracked.
- Keep DNS and NTP clean.
- Keep alerting actionable.
- Document support ownership.
- Avoid undocumented changes.
