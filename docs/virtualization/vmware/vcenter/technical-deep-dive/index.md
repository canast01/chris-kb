# vCenter Technical Deep Dive
## Overview

vCenter is part of the virtualization platform. This page is for technical operations, troubleshooting, upgrade planning, and support handoff.

## Platform Role

vCenter is the central management plane for VMware environments. It manages inventory, clusters, hosts, VMs, datastores, networks, permissions, alarms, tasks, events, and automation APIs.

## Core Components

- vCenter Server Appliance
- vSphere Client
- SSO domain
- vPostgres database
- Inventory service
- vpxd service
- vAPI endpoint
- Certificate authority services
- Task and event subsystem
- Backup scheduler

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
| vSphere Client / API | HTTPS | 443 |
| ESXi host management | HTTPS | 443 |
| Syslog | UDP/TCP | 514 |
| LDAP / LDAPS | TCP | 389 / 636 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

## Key Logs

- `/var/log/vmware/vpxd/vpxd.log`
- `/var/log/vmware/vsphere-ui/logs/vsphere_client_virgo.log`
- `/var/log/vmware/sso/`
- `/var/log/vmware/vapi/`
- `/var/log/vmware/applmgmt/`

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
service-control --status
service-control --status --all
vmon-cli --list
df -h
/usr/lib/applmgmt/backup_restore/py/vmware/appliance/backup_restore.py
~~~

## Common Failure Points

- Expired certificates
- SSO or identity source failure
- Appliance partition full
- vCenter service failure
- Host communication issue
- Backup target failure
- DNS or NTP drift
- Permission drift

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
