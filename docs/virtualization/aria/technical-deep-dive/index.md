# Aria Suite Technical Deep Dive

## Overview

Aria Suite is part of the virtualization platform. This page is for technical operations, troubleshooting, upgrade planning, and support handoff.

## Platform Role

Aria Suite supports monitoring, logging, automation, lifecycle, dashboards, alerting, capacity analysis, and operational visibility.

## Core Components

- Aria Operations
- Aria Operations for Logs
- Aria Automation
- Aria Suite Lifecycle
- Collectors and adapters
- Dashboards
- Alert policies
- Integrations
- Content management

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
| UI/API | HTTPS | 443 |
| Syslog ingestion | UDP/TCP | 514 |
| Log ingestion SSL | TCP | 6514 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |

## Key Logs

- Product appliance logs
- Collector logs
- Adapter logs
- Workflow execution logs
- Lifecycle operation logs
- Log ingestion diagnostics

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
df -h
systemctl --failed
journalctl -xe
vracli status
kubectl get pods -A
~~~

## Common Failure Points

- Adapter collection failure
- Credential issue
- Stale dashboards
- Alert noise
- Log ingestion issue
- Certificate issue
- Lifecycle upgrade issue
- Automation workflow failure

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
