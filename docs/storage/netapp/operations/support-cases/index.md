---
tags:
  - netapp
  - operations
---
# NetApp Operations — Support Cases

<div class="kb-summary">
Support Cases reference covering Opening a Support Case, Case Severity Levels, Generating a Support Bundle, Information to Include in a Case, Keystone-Specific Cases and 2 more sections.
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


## Opening a Support Case

**Via NetApp Support Portal (mysupport.netapp.com):**
1. Log in and navigate to **My AutoSupport → Cases → Create Case**
2. Select the affected system (by serial number or site)
3. Provide a detailed description, symptom timeline, and impact
4. Attach relevant logs or AutoSupport bundles
5. Select severity and submit

**Via Phone:**
NetApp provides 24/7 phone support for P1 and P2 cases.

## Case Severity Levels

| Severity | Definition | Target Response |
|---|---|---|
| P1 — Critical | Production system down, data loss risk | 15–30 minutes (24/7) |
| P2 — High | Degraded operation, redundancy lost | 1–2 hours (24/7) |
| P3 — Medium | Non-critical issue, workaround available | 4 business hours |
| P4 — Low | Question, guidance, feature request | Next business day |

## Generating a Support Bundle

Before opening a case, collect an AutoSupport:

```bash
# Generate a manual AutoSupport (sends to NetApp automatically)
system node autosupport invoke -node * -type all -message "Opening case for <issue>"

# Confirm AutoSupport delivery
system node autosupport history show | head -20
```

## Information to Include in a Case

- Array serial number and system name
- ONTAP version (`system node image show`)
- Symptom description with timestamps
- Affected volumes, SVMs, or nodes
- Recent changes (upgrades, configuration, cabling)
- Output of:
  - `cluster show`
  - `system health status show`
  - `event log show -severity error -time ">24h"`
  - `storage failover show`

## Keystone-Specific Cases

For Keystone subscription issues, engage via:
- NetApp Support Portal — select subscription
- Keystone Success Manager — for billing and capacity disputes
- BlueXP → Support → Create Case — for BlueXP-managed services

## Escalating a Case

If a case is not progressing:
1. Request escalation directly within the case
2. Contact your NetApp TAM (Technical Account Manager)
3. For P1: call NetApp support directly — do not rely on email

## Tracking Open Cases

All open and closed cases are visible at **mysupport.netapp.com → Cases**.

AutoSupport also generates case numbers automatically when critical EMS events are triggered — check **My AutoSupport → Cases** for system-initiated cases.
