---
tags:
  - architecture
  - netbackup
---
# NetBackup — Architecture

<div class="kb-summary">
Veritas NetBackup three-tier architecture — Primary Server catalog and scheduling, Media Servers for data movement, and Clients with backup agents.

*Applies to: NetBackup 10.x*
</div>

```text
┌──────────────────────────── Backup Netbackup Architecture — Architecture ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │            Netbackup architecture overview: Backup Netbackup Architecture platform            │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │       Key components: Backup Netbackup Architecture, Management, Monitoring, Automation       │   │
│   │          Design principles: HA, scalability, non-disruptive operations, and security          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Design → deploy → configure → validate → monitor → optimise                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Backup Netbackup Architecture infrastructure · management network · monitoring           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Netbackup          = Backup Netbackup Architecture platform overview and core concepts             │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


![NetBackup Architecture](../../../assets/netbackup-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Three-tier topology, key processes, storage units, catalog backup, and sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware VADP, Oracle RMAN, NDMP, and cloud storage integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Policy naming, retention schedules, MSDP standards, and media server placement.</span></a>
</div>

| Component | Role |
|---|---|
| Primary Server | Central scheduler, catalog DB (PostgreSQL), EMM device database |
| Media Server | Data mover; writes to storage units; runs deduplication (MSDP) |
| Client | Backup agent on protected host; sends data to Media Server via TCP 13724 |
| MSDP | Media Server Deduplication Pool; inline dedup; supports AIR image replication |
| Catalog | Most critical component — tracks all backup images; must be protected separately |

