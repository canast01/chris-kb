---
tags:
  - architecture
  - netapp
---
# Superna Eyeglass — Architecture

<div class="kb-summary">
Superna Eyeglass DR orchestration for NetApp PowerScale — automates SyncIQ failover, SMB/NFS share reconfiguration, quota migration, and DNS cutover in 5–15 minutes.

*Applies to: Superna Eyeglass*
</div>

```text
┌─────────────────────── Superna Eyeglass — ONTAP DR Orchestration Architecture ────────────────────────┐
│                                                                                                       │
│  Third-party DR automation for NetApp ONTAP SVM DR; replicates configuration changes,                 │
│  automates failover, and updates DNS — replacing manual SVM DR failover steps.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                Key Functions                │   │
│   │        Linux VM (Eyeglass appliance)         │  │          SVM DR config replication          │   │
│   │         Connects to both ONTAP sites         │  │              Export policy sync             │   │
│   │         REST + ZAPI for ONTAP access         │  │           Share + ACL replication           │   │
│   │           HA: active-passive pair            │  │           DNS failover automation           │   │
│   │         Monitor: config drift alerts         │  │          Failover in minutes, not h         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Without Eyeglass, SVM DR failover requires 20+ manual steps; Eyeglass reduces to 1.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Failover Process               │  │                  Monitoring                 │   │
│   │         Detect: SnapMirror lag alert         │  │            Config drift detection           │   │
│   │            Decide: manual or auto            │  │           Replication lag tracking          │   │
│   │           Break SnapMirror mirrors           │  │              DR readiness score             │   │
│   │           Activate SVM at DR site            │  │          Compliance report: config          │   │
│   │           Update DNS: new IPs live           │  │             Alerts: email + SNMP            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Eyeglass VM (4 vCPU, 16 GB RAM) on vSphere; management network access to both                        │
│  ONTAP cluster-mgmt LIFs; DNS server access for automatic record updates.                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Eyeglass       = Superna product; automates ONTAP SVM DR failover and config sync                    │
│  SVM DR         = Storage Virtual Machine Disaster Recovery; ONTAP native feature                     │
│  Config replication= Eyeglass copies export policies, shares, ACLs to DR site SVM                     │
│  Config drift   = production SVM config changed but DR SVM not updated; Eyeglass alerts               │
│  Export policy  = NFS access rule; Eyeglass replicates so NFS works after failover                    │
│  SnapMirror lag = time between last successful transfer; Eyeglass monitors and alerts                 │
│  DNS failover   = Eyeglass updates DNS records to point to DR SVM IPs post-failover                   │
│  DR readiness score= Eyeglass composite score; 0-100; low score = failover risk                       │
│  Break mirror   = convert SnapMirror secondary to read-write; Eyeglass automates                      │
│  Failback       = reverse replication back to primary after DR event is resolved                      │
│  ZAPI           = legacy NetApp ONTAP management API; Eyeglass uses alongside REST                    │
│  ACL            = Access Control List; file share permissions replicated to DR                        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Superna Eyeglass Architecture](../../../../assets/superna-eyeglass-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Failover execution flow, DR readiness scoring, CLI commands, sizing, and RPO tiers.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>PowerScale SyncIQ, Active Directory DNS, and SNMP/email alerting.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Policy naming, RPO tier assignments, readiness thresholds, and test schedule.</span></a>
</div>

| Component | Role | Location |
|---|---|---|
| Eyeglass Primary Appliance | Monitors SyncIQ; syncs share/quota config; DR orchestration control | Primary site |
| Eyeglass DR Appliance | Standby node; activates when primary site unavailable | DR site |
| PowerScale SyncIQ | Underlying data replication engine | Both sites |
| DNS Integration | Automated SmartConnect zone cutover during failover | Primary / DR DNS |

