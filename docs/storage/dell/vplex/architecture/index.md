---
tags:
  - architecture
  - dell
---
# VPLEX — Architecture

<div class="kb-summary">
Dell VPLEX is a storage federation and virtualisation platform that decouples physical storage from the host view, presenting virtual volumes regardless of which back-end array holds the data. VPLEX Metro provides zero-RPO active-active stretched storage across two sites with a ≤5ms RTT ICL.

*Applies to: VPLEX*
</div>

```text
┌────────────────────────── Dell VPLEX — Storage Virtualization Architecture ───────────────────────────┐
│                                                                                                       │
│  Storage virtualization appliance between hosts and arrays; presents virtual volumes                  │
│  abstracting underlying LUNs; Metro active-active stretch; non-disruptive migration.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Function                   │  │            Deployment Topologies            │   │
│   │         Storage virtualization layer         │  │         Local: single site; migrate         │   │
│   │         Sits between hosts + arrays          │  │         Metro: active-active 2-site         │   │
│   │           Presents virtual volumes           │  │           Geo: async distant sites          │   │
│   │          Abstracts underlying LUNs           │  │        Cluster: 2 directors per site        │   │
│   │         Cache coherency: distributed         │  │            FC: only connectivity            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  VPLEX Metro enables VMware vMSC (Metro Storage Cluster) for cross-site vMotion.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Key Use Cases                 │  │                  Management                 │   │
│   │           Non-disruptive migration           │  │           VPLEX Management Console          │   │
│   │         Heterogeneous array support          │  │             vscli: command line             │   │
│   │         Active-active Metro stretch          │  │             REST API: automation            │   │
│   │          Host transparent migration          │  │          VPLEX Witness: tiebreaker          │   │
│   │        vMSC: VMware stretched cluster        │  │           vCenter plugin optional           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VPLEX VS2 appliance (2U rackmount); FC fabric connections to both hosts and arrays;                  │
│  Inter-cluster link (ICL): FC between VPLEX clusters at both Metro sites.                             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VPLEX          = Dell storage virtualization appliance; brand name                                   │
│  Virtual volume = logical volume presented to hosts; maps to one or more LUNs                         │
│  Virtual device = internal VPLEX construct mapping virtual vol to storage extents                     │
│  Metro          = synchronous active-active VPLEX across 2 sites; shared volume                       │
│  Local          = single-site VPLEX; non-disruptive migration use case                                │
│  Cache coherency= VPLEX distributed cache ensures consistency across both copies                      │
│  ICL            = Inter-Cluster Link; FC link between the two VPLEX clusters                          │
│  Director       = VPLEX compute module; two per cluster for HA                                        │
│  vMSC           = vSphere Metro Storage Cluster; VMware validated with VPLEX Metro                    │
│  Witness        = VPLEX tiebreaker VM; determines surviving site on network partition                 │
│  Non-disruptive migration= move LUNs between arrays while host IO continues                           │
│  Heterogeneous  = VPLEX virtualizes LUNs from any vendor (PowerMax, NetApp, Pure)                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  W(["Witness VM\nSite C — 3rd domain"])
  subgraph "Site A"
    HA(["Hosts A"]) --> DIR_A["VPLEX Cluster-1\nDirector Pair A"]
    DIR_A --> STG_A[("Array A\nPowerMax / Unity")]
  end
  subgraph "Site B"
    HB(["Hosts B"]) --> DIR_B["VPLEX Cluster-2\nDirector Pair B"]
    DIR_B --> STG_B[("Array B\nPowerMax / Unity")]
  end
  DIR_A <-->|"ICL — 10/25GbE\n≤5ms RTT"| DIR_B
  W -. "Quorum" .- DIR_A
  W -. "Quorum" .- DIR_B
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef wit fill:#b45309,stroke:#92400e,color:#fff
  class DIR_A,DIR_B ctrl
  class STG_A,STG_B store
  class HA,HB host
  class W wit
```
![VPLEX Architecture](../../../../assets/vplex-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">How It Works</div>
    <div class="kb-card-desc">Storage object hierarchy, Metro write path, Witness quorum arbitration, ICL requirements, and vplexcli reference.</div>
  </a>
  <a class="kb-card" href="integrations/">
    <div class="kb-card-icon">🔗</div>
    <div class="kb-card-title">Integrations</div>
    <div class="kb-card-desc">VMware Metro Storage Cluster (vMSC), RecoverPoint (Geo), PowerMax and Unity back-end arrays.</div>
  </a>
  <a class="kb-card" href="design-standards/">
    <div class="kb-card-icon">📐</div>
    <div class="kb-card-title">Design Standards</div>
    <div class="kb-card-desc">Model selection (Local / Metro / Geo), ICL bandwidth sizing, Witness placement, and storage view zoning standards.</div>
  </a>
</div>

## Deployment Models

| Model | Sites | Replication | RTT Limit | Active-Active | Use Case |
|---|---|---|---|---|---|
| VPLEX Local | 1 | Synchronous (within engine) | N/A | Yes (within site) | LUN virtualisation, data mobility |
| VPLEX Metro | 2 | Synchronous (ICL) | ≤5ms | Yes (both sites) | Zero-RPO stretched cluster for VMware HA |
| VPLEX Geo | 2+ | Asynchronous (RecoverPoint) | Any | No | Long-distance DR beyond Metro RTT limits |

## Topology


