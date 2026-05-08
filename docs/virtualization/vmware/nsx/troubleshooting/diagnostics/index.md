# NSX — Diagnostics

## Technical Deep Dive

NSX is part of the virtualization platform. This section covers technical operations, troubleshooting, upgrade planning, and support handoff.

### Platform Role

NSX provides software-defined networking, security, routing, distributed firewalling, segmentation, and edge services for VMware environments.

### Core Components

- NSX Manager cluster
- Transport nodes
- Edge nodes
- Edge clusters
- Segments
- Tier-0 gateways
- Tier-1 gateways
- Distributed firewall
- Overlay transport zones
- TEP networking

### Main Dependencies

- DNS resolution
- NTP/time sync
- Authentication source
- Management network
- Storage access
- Certificate trust
- Monitoring
- Backup/recovery process
- Vendor support access

### Ports and Protocols

| Use | Protocol | Port |
|-----|----------|------|
| NSX Manager UI/API | HTTPS | 443 |
| Geneve overlay | UDP | 6081 |
| BGP | TCP | 179 |
| DNS | TCP/UDP | 53 |
| NTP | UDP | 123 |
| Syslog | UDP/TCP | 514 |

### Key Logs

- NSX Manager appliance logs
- Edge node logs
- ESXi host transport node logs
- Distributed firewall logs
- Syslog destination logs

### Health Checks

- Confirm management access.
- Review current alarms.
- Review recent failed tasks.
- Validate DNS and NTP.
- Confirm certificate status.
- Check service health.
- Check capacity and performance.
- Confirm monitoring data is current.
- Review recent changes.

### Useful Commands

```bash
get cluster status
get managers
get transport-nodes status
get logical-switches
get edge-clusters
get bgp neighbor
get firewall sections
```

### Common Failure Points

- Manager cluster health issue
- Edge node failure
- TEP connectivity issue
- BGP adjacency down
- DFW rule order issue
- Certificate issue
- Transport node prep failure
- Overlay/VLAN mismatch

### Troubleshooting Workflow

1. Confirm the impact and scope.
2. Check recent changes.
3. Review alerts, tasks, and events.
4. Validate DNS, NTP, authentication, and certificates.
5. Check service status.
6. Check storage and network dependencies.
7. Review logs.
8. Capture screenshots, timestamps, errors, and task IDs.
9. Escalate with clean evidence if needed.

### Upgrade and Compatibility Notes

- Check product interoperability before upgrades.
- Confirm supported version path.
- Confirm backup or rollback method.
- Confirm maintenance window.
- Run pre-checks before change work.
- Validate health after the change.
- Document version before and after.

### Best Practices

| Recommendation | Detail |
|---|---|
| Keep versions aligned. | Keep versions aligned. |
| Keep certificates tracked. | Keep certificates tracked. |
| Keep DNS and NTP clean. | Keep DNS and NTP clean. |
| Keep alerting actionable. | Keep alerting actionable. |
| Document support ownership. | Document support ownership. |
| Avoid undocumented changes. | Avoid undocumented changes. |

---

## Edge Health

Use this section to review NSX edge node health, routing, transport, and service impact.

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
