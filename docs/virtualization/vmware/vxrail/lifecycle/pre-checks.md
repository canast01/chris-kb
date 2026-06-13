---
tags:
  - vxrail
---
# VxRail Pre-Change Health Validation


<div class="kb-summary">
VxRail Pre-Change Health Validation reference covering VxRail Manager, vCenter Health, vSAN Health, Hardware Health, Infrastructure and 1 more sections.

*Applies to: VxRail 7.x · 8.x*
</div>

Pre-Upgrade Checklist Flow
```text
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  VxRail Manager         vCenter               vSAN                                                    │
│  ─────────────          ───────────────        ─────                                                  │
│  UI reachable?    →     hosts Connected?  →   Skyline green?                                          │
│  services healthy?      no critical alarms    no resync?                                              │
│  no pending jobs?       DRS/HA healthy        capacity OK?                                            │
│  cert valid?            recent tasks clean    disk groups OK?                                         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                               │
```
```text
                               │
┌────────────────────────────────────────────────── ▼ ──────────────────────────────────────────────────┐
│  Infrastructure + Backup                                                                              │
│  DNS forward/reverse working for all nodes and vCenter                                                │
│  NTP synchronized · vCenter backup current                                                            │
│  critical VM backups done · rollback plan documented                                                  │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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
