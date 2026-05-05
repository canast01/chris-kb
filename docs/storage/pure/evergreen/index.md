# Pure Evergreen

## Overview

Pure Evergreen is an enterprise storage platform or storage service used to support production workloads, protection, replication, capacity management, and operational recovery.

## Where It Fits

- Primary storage operations
- Application and VM data services
- Backup and recovery workflows
- Replication and disaster recovery
- Performance and capacity planning

## Daily Checks

- Review active alerts
- Check capacity usage
- Validate replication or protection status
- Confirm support connectivity
- Review performance trends
- Check recent configuration changes

## Health Commands

~~~bash
show status
show alerts
show capacity
show replication
show version
~~~

## Common Issues

| Symptom | Likely Cause | Action |
|---|---|---|
| High latency | Backend contention or host path issue | Review performance and paths |
| Capacity warning | Growth, snapshots, or retention | Review usage and cleanup options |
| Replication lag | Network, target, or workload pressure | Check replication status |
| Host path down | SAN zoning, cabling, or multipathing | Validate fabric and host paths |

## Operational Tasks

- Provision storage
- Expand volumes or file systems
- Review snapshots
- Validate replication
- Confirm host connectivity
- Review firmware or software level

## Upgrade Notes

1. Confirm current version
2. Review vendor compatibility matrix
3. Confirm backups and rollback plan
4. Validate support contract
5. Upgrade during maintenance window
6. Confirm host access and replication after upgrade

## Best Practices

- Keep naming consistent
- Monitor capacity growth
- Document storage mappings
- Validate multipathing
- Test restore and failover procedures
- Review support advisories regularly
