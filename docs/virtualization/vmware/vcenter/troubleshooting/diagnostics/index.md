# vCenter — Diagnostics

## Service Health

### Appliance Management Interface

- Log into the VCSA Appliance Management Interface (VAMI) at `https://<vcenter>:5480`
- Check CPU, memory, and disk usage
- Confirm all services are shown as healthy

### Checking Service Status

```bash
# SSH to vCenter, then:
service-control --status
```

### Disk Partition Usage

```bash
df -h
```

Key partitions to monitor:
- `/storage/log` — fills quickly during issues
- `/storage/db` — vCenter database
- `/storage/core` — core appliance data

### SSO and Lookup Service Health

- Confirm SSO is running: `service-control --status vmware-sts`
- Confirm Lookup Service: `service-control --status vmware-lookupsvc`
- Confirm Identity Management: `service-control --status vmware-eam`

### Certificate-Related Failures

- Browser certificate warning usually means the machine SSL cert is expired
- Login failures with SSO errors often point to the STS certificate
- Check certificate expiration in VAMI → Certificate Management

### DNS and NTP Validation

```bash
# Check DNS from vCenter appliance shell
nslookup <vcenter-fqdn>
dig <vcenter-fqdn>

# Check NTP status
timedatectl
```

### Restarting Services Safely

Only restart services after checking disk space and reviewing recent changes.

```bash
service-control --restart --all
```

> Restart one service at a time where possible. A full restart causes brief vCenter unavailability.

### When to Restore from Backup

- Corrupt database
- STS certificate failure that cannot be resolved in place
- Multi-service failure with no clear root cause
- Disk partition full with no recovery path

### Evidence to Collect Before Escalation

- `df -h` output
- `service-control --status` output
- Screenshots of VAMI health
- Recent vCenter events and tasks
- Support bundle from VAMI

## Tasks and Failures

### Overview

Failed tasks, stuck tasks, event review, job ownership, and first-pass triage.

### Daily Checks

| Check | Command | Notes |
|---|---|---|
| Review active alarms. |  |  |
| Check recent failed tasks. |  |  |
| Confirm service health. |  |  |
| Confirm capacity and performance are normal. |  |  |
| Check recent changes. |  |  |

### Health Commands

```bash
# Add environment-specific commands here
```

### Common Issues

- Failed or stuck tasks.
- Certificate, DNS, or authentication issues.
- Capacity pressure.
- Service health warnings.
- Version mismatch after maintenance.
- Monitoring gaps.

### Operational Tasks

| Task | Command |
|---|---|
| Review alarms and events. |  |
| Confirm ownership and support notes. |  |
| Validate dependencies. |  |
| Document changes. |  |
| Confirm monitoring coverage. |  |

### Upgrade Notes

- Confirm compatibility.
- Review known issues.
- Confirm rollback plan.
- Validate health before and after the change.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Keep versions aligned. | Keep versions aligned. |
| Avoid unsupported version combinations. | Avoid unsupported version combinations. |
| Document exceptions. | Document exceptions. |
| Validate after every change. | Validate after every change. |

## Certificate Checks

### Overview

Use this section to check vCenter certificate health, expiration risk, and renewal readiness.

### Pre-Checks

- Confirm scope.
- Confirm maintenance window if changes are planned.
- Confirm current health.
- Check recent alerts and tasks.
- Confirm access to management tools.
- Confirm rollback path if configuration changes are made.

### Steps

1. Identify the affected object.
2. Capture current state.
3. Review alarms, logs, and recent changes.
4. Apply the planned action.
5. Validate service health.
6. Record notes and follow-up items.

### Validation

- Confirm the object is healthy.
- Confirm no new critical alarms.
- Confirm monitoring reflects the expected state.
- Confirm related systems still have access.
- Document the result.

### Rollback

- Revert the changed setting if possible.
- Restore prior configuration from documented state.
- Escalate if rollback requires vendor support.

### Notes

Keep screenshots, task IDs, error messages, and timestamps with the change or incident record.

## Service Health Checks

### Overview

Use this section to review core vCenter service health, task failures, and management plane availability.

### Pre-Checks

- Confirm scope.
- Confirm maintenance window if changes are planned.
- Confirm current health.
- Check recent alerts and tasks.
- Confirm access to management tools.
- Confirm rollback path if configuration changes are made.

### Steps

1. Identify the affected object.
2. Capture current state.
3. Review alarms, logs, and recent changes.
4. Apply the planned action.
5. Validate service health.
6. Record notes and follow-up items.

### Validation

- Confirm the object is healthy.
- Confirm no new critical alarms.
- Confirm monitoring reflects the expected state.
- Confirm related systems still have access.
- Document the result.

### Rollback

- Revert the changed setting if possible.
- Restore prior configuration from documented state.
- Escalate if rollback requires vendor support.

### Notes

Keep screenshots, task IDs, error messages, and timestamps with the change or incident record.

## Field Reference

### Overview

vCenter is the main VMware management plane for clusters, hosts, VMs, datastores, networks, permissions, alarms, tasks, and events.

### Where It Fits

This sits in the virtualization stack with compute, storage, networking, monitoring, backup, automation, and security controls. Treat it as a Tier 1 infrastructure area when workloads depend on it.

### Architecture and Components

- vCenter Server Appliance
- vPostgres database
- vSphere Client
- SSO and identity services
- Inventory service
- Task and event system
- Alarm and monitoring framework
- API and automation interfaces

### Dependencies

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

### Ports and Protocols

| Function | Protocol | Typical Port |
|----------|----------|--------------|
| Management | HTTPS | 443 |
| Monitoring | SNMP | 161 |
| Logging | Syslog | 514 |
| API | HTTPS | 443 |

### Daily Operations

- Review vCenter alarms.
- Check failed or stuck tasks.
- Confirm vCenter services are healthy.
- Review backup status.
- Confirm certificate status.
- Validate connectivity to ESXi hosts.
- Review recent permission or inventory changes.

### Health Checks

- vCenter service status
- Appliance CPU and memory
- Appliance disk usage
- Database health
- Certificate expiration
- Host connection state
- Backup job status
- Recent task failures

### Upgrade Workflow

1. Verify compatibility.
2. Confirm backups or recovery point.
3. Validate maintenance window.
4. Check current platform health.
5. Apply the upgrade or patch.
6. Monitor logs and tasks.
7. Validate health after the change.
8. Record results and follow-up items.

### Backup and Recovery Considerations

- Confirm configuration backup coverage.
- Confirm appliance or platform backup status where supported.
- Confirm snapshots are used only when appropriate.
- Confirm restore steps are documented.
- Test recovery periodically.
- Keep backup evidence with change records.

### Common Issues

- vCenter login failure
- Host disconnected
- Certificate expiration
- Failed appliance backup
- Appliance disk full
- Slow inventory loading
- Failed tasks or stuck tasks
- SSO or identity source issue

### Troubleshooting Steps

1. Confirm scope.
2. Review recent changes.
3. Check alarms and events.
4. Review system logs.
5. Validate DNS, NTP, authentication, network, and storage.
6. Check resource utilization.
7. Escalate with timestamps, errors, screenshots, and support bundle if unresolved.

### Root Cause Examples

| Symptom | Possible Cause | Resolution |
|--------|----------------|------------|
| Cannot log in | SSO or identity source issue | Validate identity source and local administrator access |
| Host disconnected | Network, DNS, or host agent issue | Validate management network and host services |
| Appliance warning | Disk or service issue | Check VAMI, service status, and appliance partitions |
| Backup failed | Backup target or credential issue | Validate target path, account, and backup schedule |

### Best Practices

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

### Certification Relevance

Useful certification study areas:

- Architecture design
- High availability
- Performance optimization
- Troubleshooting workflows
- Security controls
- Backup and recovery
- Lifecycle management
