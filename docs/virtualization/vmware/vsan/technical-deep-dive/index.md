# vSAN Technical Deep Dive

## Overview

vSAN is part of the virtualization platform. This page is for technical operations, troubleshooting, upgrade planning, and support handoff.

## Platform Role

vSAN provides software-defined storage by pooling local disks from ESXi hosts and presenting policy-based storage to virtual machines.

## Core Components

- vSAN cluster
- Disk groups or ESA storage pools
- Cache and capacity devices
- Storage policies
- Objects and components
- Witness or fault domains where used
- Resync engine
- Health service

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
| vSAN transport | TCP/UDP | 2233 |
| vSAN cluster service | TCP | 12321 |
| vCenter management | HTTPS | 443 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

## Key Logs

- `/var/log/vmkernel.log`
- `/var/log/vsanmgmt.log`
- `/var/log/clomd.log`
- `/var/log/cmmdsd.log`
- `/var/log/vobd.log`

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
esxcli vsan cluster get
esxcli vsan health cluster list
esxcli vsan storage list
esxcli vsan debug object list
esxcli network ip interface list
vsish -e get /vmkModules/lsom/disks/
~~~

## Common Failure Points

- Disk failure
- Disk group issue
- Capacity pressure
- Object non-compliance
- Resync backlog
- Network packet loss
- Fault domain imbalance
- Policy mismatch

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
