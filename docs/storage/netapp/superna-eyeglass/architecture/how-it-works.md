---
tags:
  - architecture
  - netapp
---
# Superna Eyeglass — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Component Topology, Connectivity, Key CLI Commands, Sizing and 1 more sections.

*Applies to: Superna Eyeglass*
</div>
![Superna Eyeglass — How It Works](../../../../assets/storage-netapp-superna-eyeglass-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "ONTAP Source\n(primary SVM)" as SRC
participant "SnapMirror\nRelationship" as SM
participant "ONTAP Target\n(DR SVM)" as TGT
participant "Superna Eyeglass\n(DR orchestrator)" as EG
participant "AD / DNS" as AD
actor "Admin" as ADM

EG -> SM: Monitor replication lag
SM --> EG: Lag + relationship state
ADM -> EG: Initiate DR test / failover
EG -> SM: Quiesce source SVM
EG -> TGT: Break SnapMirror + mount volumes
EG -> AD: Update DNS CNAME to target
EG -> AD: Update CIFS shares + exports
AD --> EG: DNS propagated
EG --> ADM: Failover complete — clients reconnecting
@enduml
```

## Overview

Superna Eyeglass is a DR orchestration platform purpose-built for NetApp PowerScale (Isilon). It automates the share, quota, and DNS reconfiguration steps that previously required hours of manual work during a SyncIQ failover. Eyeglass continuously monitors DR readiness and scores it at 100% only when all shares, exports, quotas, and DNS zones are aligned between primary and DR clusters.

## Component Topology

```mermaid
graph LR
  PS_A["PowerScale Cluster A\n(production)"] -->|"SyncIQ policy"| PS_B["PowerScale Cluster B\n(DR)"]
  EG["Superna Eyeglass\nDR Assistant"] -->|"monitors SyncIQ"| PS_A
  EG -->|"orchestrates failover\naccess zone migration"| PS_B
  ADMIN(["Admin"]) -->|"Eyeglass UI"| EG
  DNS(["DNS / AD\naccess zone cutover"]) <--> EG
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PS_A ctrl
  class PS_B dr
  class EG mgmt
  class ADMIN,DNS host
```

## Sizing

| Environment | Eyeglass VM Size |
|---|---|
| < 500 shares | 4 vCPU, 8 GB RAM |
| 500–2,000 shares | 8 vCPU, 16 GB RAM |
| > 2,000 shares | 8 vCPU, 32 GB RAM |

## RPO Tiers

| Data Tier | SyncIQ Schedule | RPO Target | Alert Threshold |
|---|---|---|---|
| Tier 1 (critical file services) | Continuous | < 15 minutes | > 10 minutes lag |
| Tier 2 (departmental shares) | Every 4 hours | < 4 hours | > 3.5 hours lag |
| Tier 3 (archival) | Daily | < 24 hours | > 20 hours lag |

---

## See also

- [Superna Eyeglass — Design Standards](../design-standards/)
- [Superna Eyeglass — Integrations](../integrations/)
- [Superna Eyeglass — Deploy](../deploy/)
