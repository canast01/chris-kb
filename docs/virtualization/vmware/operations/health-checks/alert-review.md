---
tags:
  - operations
---
# Alert Health Check


<div class="kb-summary">
Alert Health Check reference covering Active Alerts Review, Aria Operations Alerts, Hardware Alerts, Backup Alerts, Repeat Alerts and 2 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌────────────────────────────────── Alert Health Check — Review Flow ───────────────────────────────────┐
│                                                                                                       │
│    Review all active alerts every morning; triage by priority; assign or suppress                     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Alert Sources        │  │       Priority Triage       │  │       Response Actions      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        vCenter alarms       │  │      P1 = red critical      │  │        P1 → immediate       │   │
│   │       Aria Operations       │  │       P2 = yellow warn      │  │      P2 → assign owner      │   │
│   │        Pure1 / iDRAC        │  │        P3 = blue info       │  │      P3 → log + weekly      │   │
│   │       Monitoring tools      │  │                             │  │       False pos → tune      │   │
│   │        Manual reports       │  │                             │  │       Repeat → RCA req      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    P1           = Critical; immediate action; escalate if not resolved within 30 min                  │
│    P2           = Warning; assign an owner; resolve within business hours                             │
│    P3           = Informational; log and review weekly; no immediate action required                  │
│    False positive = Alert fires incorrectly; tune threshold or suppress after RCA                     │
│    Repeat alert  = Same alert fires repeatedly; trigger RCA to find root cause                        │
│    Aria Ops      = VMware Aria Operations; collects metrics and fires perf alerts                     │
│    Pure1         = Pure Storage cloud portal; array health, capacity, and alerts                      │
│    iDRAC         = Dell integrated remote access; hardware alerts: temp, disk, PSU                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Active Alerts Review

- Review all critical alerts in vCenter — confirm each has an owner or action
- Review warning alerts — identify any that have been open longer than expected
- Check for alerts that triggered during a recent maintenance window

## Aria Operations Alerts

- Review Aria Operations alert dashboard
- Identify any critical or high-severity alerts
- Confirm alerts are not suppressed unnecessarily outside maintenance windows

## Hardware Alerts

- Review iDRAC alerts for all VxRail nodes and other servers
- Confirm no outstanding disk, memory, NIC, or PSU alerts

## Backup Alerts

- Review backup platform for failed or missed jobs
- Confirm all critical VMs and systems have a successful recent backup

## Repeat Alerts

- Identify alerts that fire repeatedly without resolution
- Review repeat alerts for tuning or permanent fixes
- Suppress intentionally only with a documented reason and expiry

## False Positives and Stale Alerts

- Remove or disable alerts that no longer apply
- Review alert thresholds — adjust if consistently firing below the meaningful threshold

## Alert Owner and Next Action

For each open critical alert, confirm:
- Owner assigned
- Next action documented
- Escalation path clear if not resolved within SLA

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Capacity Review](capacity-review.md)
- [Daily Health Check](daily-health-check.md)
- [Management Access Check](management-access-check.md)
- [Virtualization Health Checks](index.md)
