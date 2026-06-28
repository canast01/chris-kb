---
tags:
  - operations
  - san
---
# Nexus Dashboard: Endpoint Tracking, Flow Visibility, and Topology View

<div class="kb-summary">
Nexus Dashboard: Endpoint Tracking, Flow Visibility, and Topology View reference covering Flow Visibility, Topology View, Path Trace for Troubleshooting, Common Visibility Issues.

*Applies to: Cisco MDS · Nexus*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Common Visibility Issues

| Issue | Likely Cause | Fix |
|---|---|---|
| Endpoint not found | Not yet learned or aged out | Check on leaf: `show endpoint ip <ip>` |
| Flow data missing | Telemetry not enabled on leaf | Verify ERSPAN/sFlow config on fabric switches |
| Path trace shows "No path" | Policy contract missing | Check ACI contracts between source and destination EPGs |
| Topology not loading | NDI not connected to APIC | Re-check fabric connection in NDI settings |
| Latency values all zero | Latency telemetry requires specific hardware | Verify leaf hardware supports latency reporting |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Nexus Dashboard: Fabric Alerts, Severity, Acknowledgement, and Notification Policies](alerts.md)
- [Cisco Nexus Dashboard — Operations Backup & Restore](backup-restore.md)
- [Cisco Nexus Dashboard — Operations CLI Reference](cli-reference.md)
- [Nexus Dashboard — Operations](index.md)
- [Nexus Dashboard — Architecture](../architecture/)
- [Nexus Dashboard — Initial Deployment](../deploy/)
- [Nexus Dashboard — Security](../security/)
- [Cisco Nexus Dashboard — Troubleshooting](../troubleshooting/)
