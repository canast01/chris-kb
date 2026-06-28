---
tags:
  - netapp
  - operations
---
# NetApp Operations — Alerts

<div class="kb-summary">
Alerts reference covering ONTAP EMS Alerts, AutoSupport Notifications, SNMP Alerting, BlueXP Alerts (Keystone / Cloud Manager), Alert Triage Priority and 2 more sections.

*Applies to: ONTAP 9.x*
</div>
![NetApp Operations — Alerts](../../../../assets/storage-netapp-operations-alerts-index.svg)




```d2
direction: right

center: "Alerts" {shape: hexagon}
ontap_ems_alerts: "ONTAP EMS Alerts" {shape: rectangle}
autosupport_notifications: "AutoSupport Notifications" {shape: rectangle}
snmp_alerting: "SNMP Alerting" {shape: rectangle}
bluexp_alerts_keystone_cloud_manager: "BlueXP Alerts (Keystone / Cloud Manager)" {shape: rectangle}
alert_triage_priority: "Alert Triage Priority" {shape: rectangle}
resolving_health_alerts: "Resolving Health Alerts" {shape: rectangle}

center -> ontap_ems_alerts
center -> autosupport_notifications
center -> snmp_alerting
center -> bluexp_alerts_keystone_cloud_manager
center -> alert_triage_priority
center -> resolving_health_alerts
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## ONTAP EMS Alerts

```bash
# Show active health alerts
system health alert show

# Show recent critical/error events
event log show -severity critical
event log show -severity error -time ">24h"

# Show subsystem health
system health subsystem show
```

## AutoSupport Notifications

AutoSupport triggers automatic case creation with NetApp support for critical events. Verify it is configured:

```bash
system node autosupport show -fields state,support,transport,mail-hosts
```

Expected: `state: enable`, `support: true`.

## SNMP Alerting

```bash
# Show SNMP communities and trap hosts
system snmp show
system snmp traphost show
```

Verify trap destinations are configured to route to your monitoring platform (SCOM, Zabbix, etc.).

## BlueXP Alerts (Keystone / Cloud Manager)

For Keystone subscriptions and Cloud Volumes ONTAP, alerts are surfaced in:
- **BlueXP → Notifications** — capacity, health, and service alerts
- **BlueXP → Digital Wallet** — burst capacity warnings

## Alert Triage Priority

| Severity | Example | Action |
|---|---|---|
| Emergency | Aggregate offline | Immediate — page on-call |
| Alert | Disk failed, HA link down | Same business day |
| Error | LIF down, volume near full | Investigate within 24h |
| Warning | Efficiency below threshold | Review at next available |

## Resolving Health Alerts

```bash
# View active alerts with detail
system health alert show

# Acknowledge an alert (after resolution)
system health alert modify -node <node> -alert-id <id> -acknowledge true

# Clear alert after fixing underlying issue
system health alert delete -node <node> -alert-id <id>
```

## Common Alerts

| Alert | Cause | Resolution |
|---|---|---|
| Volume full | Data growth | Resize or enable autosize |
| Disk failed | Hardware failure | Replace disk, verify RAID rebuild |
| HA interconnect down | Cable/port failure | Investigate HA link |
| AutoSupport failure | Proxy or network | Verify outbound connectivity |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [NetApp — Health Checks](../health-checks/)
