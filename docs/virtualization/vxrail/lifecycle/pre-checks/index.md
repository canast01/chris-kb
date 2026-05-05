# VxRail Pre-Change Health Validation

## VxRail Manager

- VxRail Manager VM is powered on and reachable
- VxRail Manager health shows green
- No pending upgrade tasks or failed jobs

## vCenter Health

- All ESXi hosts are Connected
- No critical alarms in vCenter
- Recent tasks show no unexpected failures

## vSAN Health

- vSAN Skyline Health is green — no critical issues
- No active resync (or resync is at an acceptable level)
- Disk groups are healthy
- vSAN capacity is within safe limits

## Hardware Health

- No critical hardware alerts in iDRAC for any node
- Firmware is consistent across nodes
- No disk or memory warnings

## Infrastructure

- DNS forward and reverse resolution working for all nodes
- NTP synchronized across vCenter and ESXi hosts
- Admin access confirmed for both vCenter and VxRail Manager

## Backup and Recovery Readiness

- vCenter file-based backup is current
- Rollback or recovery plan documented
- Dell support contact is available if needed
