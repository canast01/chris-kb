---
tags:
  - architecture
  - netapp
---
# SnapCenter — Architecture

<div class="kb-summary">
SnapCenter architecture reference — topology, HA options, components, connectivity ports, plugin model, and sizing guidelines.

*Applies to: SnapCenter 5.x*
</div>

```text
┌───────────────────────── NetApp SnapCenter — Centralized Backup Architecture ─────────────────────────┐
│                                                                                                       │
│  Windows-based backup orchestration for app-aware ONTAP Snapshots; plugins for SQL,                   │
│  Oracle, SAP HANA, VMware, Exchange; SnapVault for DR copies; REST API for automation.                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │            Supported Applications           │   │
│   │          SnapCenter Server: Windows          │  │           SQL Server: VSS quiesce           │   │
│   │           Plugins: per-app agents            │  │           Oracle: RMAN integration          │   │
│   │         MySQL: internal metadata DB          │  │            SAP HANA: Backint API            │   │
│   │            Web UI: browser-based             │  │            VMware: VADP snapshots           │   │
│   │                REST API: 4.6+                │  │             Exchange: VSS-aware             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Snapshots are instant and zero-impact; SnapVault fans out to secondary ONTAP for DR.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Backup Flow                  │  │                Cloning and DR               │   │
│   │             Plugin quiesces app              │  │         Clone from Snapshot: instant        │   │
│   │            ONTAP Snapshot created            │  │             Dev/test: thin clone            │   │
│   │        SnapVault: vault to secondary         │  │           SnapMirror: DR failover           │   │
│   │           Catalog: metadata stored           │  │           Restore: volume or file           │   │
│   │           Retention: policy-based            │  │          SMSQL: SQL-aware failover          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Windows Server VM for SnapCenter; ONTAP primary + secondary HA pairs; management                     │
│  network access from SnapCenter to ONTAP cluster-mgmt LIF on HTTPS.                                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SnapCenter     = NetApp centralized backup and clone management server                               │
│  Plugin         = per-application agent; installed on app server; quiesces app                        │
│  VSS            = Windows Volume Shadow Service; quiescence for SQL and Exchange                      │
│  Snapshot       = instant ONTAP point-in-time copy; no IO impact; basis for backup                    │
│  SnapVault      = vault-mode replication; keeps long-term backup copies on secondary                  │
│  SnapMirror     = DR replication; failover brings secondary ONTAP to primary role                     │
│  Clone          = writable thin copy from Snapshot; used for dev/test instantly                       │
│  Backint API    = SAP HANA backup interface; SnapCenter speaks Backint natively                       │
│  RMAN           = Oracle recovery manager; SnapCenter plugin coordinates with it                      │
│  Retention policy= defines how many Snapshot copies to keep and for how long                          │
│  Catalog        = SnapCenter database of all backups; needed for restore operations                   │
│  SMSQL          = SnapManager for SQL; legacy tool; replaced by SnapCenter plugin                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TB
  SCW["SnapCenter Server\n(Windows / Linux VM)"]
  SCW --> PL1["Plug-in for SQL Server"]
  SCW --> PL2["Plug-in for Oracle"]
  SCW --> PL3["Plug-in for VMware"]
  PL1 & PL2 & PL3 --> ONTAP["NetApp ONTAP\nSnapshot · SnapMirror · SnapVault"]
  ADMIN(["DBA / Storage Admin"]) -->|"web UI / REST API"| SCW
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class SCW,PL1,PL2,PL3 ctrl
  class ONTAP store
  class ADMIN host
```
![SnapCenter Architecture](../../../../assets/snapcenter-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Topology, HA options, components, connectivity ports, plugins, and sizing guidelines.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with ONTAP, VMware, Active Directory, and external systems.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
</div>

| Component | Platform | Notes |
|---|---|---|
| SnapCenter Server | Windows Server 2019/2022 VM | Web GUI (8146), REST API, scheduler; 4 vCPU/8GB min |
| Repository Database | MySQL (local or HA cluster) | Stores job history, policies, resource groups, RBAC |
| SnapCenter Agent | Windows or Linux service | Port 8145; installed on each protected host |
| Plug-in for VMware | OVA appliance (per vCenter) | VM and datastore backup without in-guest agents |


