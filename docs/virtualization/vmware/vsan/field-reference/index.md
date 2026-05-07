# vSAN Field Reference
## Overview

vSAN provides software-defined storage across ESXi hosts using local disks, storage policies, object placement, and cluster-level health services.

## Where It Fits

This sits in the virtualization stack with compute, storage, networking, monitoring, backup, automation, and security controls. Treat it as a Tier 1 infrastructure area when workloads depend on it.

## Architecture and Components

- vSAN cluster
- Disk groups or storage pool
- Cache and capacity devices
- Storage policies
- vSAN objects and components
- Witness or fault domains where used
- Resync and repair services
- vSAN health service

## Dependencies

Common dependencies:

- DNS
- NTP
- Active Directory or LDAP
- Network connectivity
- Storage availability
- Licensing
- Monitoring
- Backup or recovery tooling
- Vendor support access

## Ports and Protocols

| Function | Protocol | Typical Port |
|----------|----------|--------------|
| Management | HTTPS | 443 |
| Monitoring | SNMP | 161 |
| Logging | Syslog | 514 |
| API | HTTPS | 443 |

## Daily Operations

- Review vSAN Skyline Health.
- Check object health.
- Review resync activity.
- Confirm capacity and slack space.
- Check disk group health.
- Review storage policy compliance.
- Check latency and congestion indicators.

## Health Checks

- Cluster health
- Object health
- Disk group health
- Capacity usage
- Resync status
- Policy compliance
- Network health
- Physical disk health
- Performance metrics

## Upgrade Workflow

1. Verify compatibility.
2. Confirm backups or recovery point.
3. Validate maintenance window.
4. Check current platform health.
5. Apply the upgrade or patch.
6. Monitor logs and tasks.
7. Validate health after the change.
8. Record results and follow-up items.

## Backup and Recovery Considerations

- Confirm configuration backup coverage.
- Confirm appliance or platform backup status where supported.
- Confirm snapshots are used only when appropriate.
- Confirm restore steps are documented.
- Test recovery periodically.
- Keep backup evidence with change records.

## Common Issues

- Object inaccessible
- Resync backlog
- Capacity pressure
- Disk failure
- Disk group issue
- Storage policy non-compliance
- High latency
- Network partition or packet loss

## Troubleshooting Steps

1. Confirm scope.
2. Review recent changes.
3. Check alarms and events.
4. Review system logs.
5. Validate DNS, NTP, authentication, network, and storage.
6. Check resource utilization.
7. Escalate with timestamps, errors, screenshots, and support bundle if unresolved.

## Root Cause Examples

| Symptom | Possible Cause | Resolution |
|--------|----------------|------------|
| Object unhealthy | Host, disk, or network issue | Review object health, disk status, and resync details |
| Resync backlog | Rebuild, maintenance, or capacity issue | Review resync dashboard and throttle change activity |
| High latency | Disk, network, or capacity pressure | Check disk groups, congestion, and network health |
| Policy non-compliant | Capacity or placement issue | Review policy, fault domains, and available resources |

## Best Practices


| Recommendation | Detail |
|---|---|
| Maintain consistent patch levels. | Maintain consistent patch levels. |
| Monitor capacity trends. | Monitor capacity trends. |
| Document configuration changes. | Document configuration changes. |
| Perform routine health checks. | Perform routine health checks. |
| Test recovery procedures. | Test recovery procedures. |
| Keep support contracts current. | Keep support contracts current. |
| Keep naming and ownership clean. | Keep naming and ownership clean. |
| Validate changes after implementation. | Validate changes after implementation. |

## Certification Relevance

Useful certification study areas:

- Architecture design
- High availability
- Performance optimization
- Troubleshooting workflows
- Security controls
- Backup and recovery
- Lifecycle management
