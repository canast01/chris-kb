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
```text
┌────────────────────────────────────────── NetApp Operations ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     NetApp Ops: NetApp storage platform operational support and administration procedures     │   │
│   │                     Protocols: HTTPS · SSH · SNMP · AutoSupport · REST API                    │   │
│   │                          Management: ActiveIQ / mysupport.netapp.com                          │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │          Monitoring         │  │           ActiveIQ          │  │       Risk assessment       │   │
│   │          Telemetry          │  │         AutoSupport         │  │       Call-home relay       │   │
│   │         Health check        │  │        Config Advisor       │  │        Best practice        │   │
│   │           Support           │  │     mysupport.netapp.com    │  │        SR management        │   │
│   │           Upgrade           │  │         NDO rolling         │  │        Non-disruptive       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │       Access      │       Auth       │      Notes       │   │
│   │     ActiveIQ     │  Health portal   │       HTTPS       │    NetApp SSO    │       SaaS       │   │
│   │   AutoSupport    │    Call-home     │    HTTPS/email    │   Certificate    │  Daily reports   │   │
│   │  Config Advisor  │  Best practice   │     Local tool    │   Local admin    │  Point-in-time   │   │
│   │  ONTAP Upgrade   │   Version mgmt   │   System Manager  │    Admin role    │   Rolling NDO    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: NetApp AFF/FAS clusters · ActiveIQ SaaS · mysupport.netapp.com support portal            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ActiveIQ           = NetApp SaaS health portal; risk assessment, upgrade advisor, capacity planning│
│    AutoSupport        = ONTAP telemetry; sends daily health reports and call-home bundles to NetApp   │
│    Config Advisor     = NetApp best-practice checker; validates cabling, config, and firmware         │
│    NDO                = Non-Disruptive Operations; rolling upgrades without host I/O service disrup...│
│    Takeover           = HA failover; one node takes over partner storage on node failure event        │
│    Giveback           = return storage to original node after failover; completes HA pair recovery    │
│    Aggregate relocation = move aggregate between HA pair nodes without service disruption             │
│    LIF migration      = move logical interface to different node port during planned maintenance      │
│    System Manager     = ONTAP web GUI; unified management for cluster, SVMs, volumes, policies        │
│    ONTAP CLI          = SSH to cluster management IP; diag privilege required for low-level commands  │
│    mysupport          = mysupport.netapp.com; open SRs, download firmware, and access knowledge base  │
│    ASUP bundle        = AutoSupport bundle with logs, config, and core files for TAC case analysis    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
