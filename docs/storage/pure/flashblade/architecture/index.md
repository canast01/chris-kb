---
tags:
  - architecture
  - pure
---
# FlashBlade — Architecture

<div class="kb-summary">
Architecture reference for Pure Storage FlashBlade. Covers the scale-out blade model, Purity//FB data services, NFS/SMB/S3/HDFS protocol support, HA through blade redundancy, ActiveDR and ActiveCluster replication, and design standards.
</div>

![FlashBlade Architecture](../../../../assets/flashblade-architecture-overview.svg)

```text
FlashBlade Architecture — Component Relationships
  Storage Blades ──────────────────────────────────────
  (each blade: NVMe flash + CPU + RAM — independent node)
          │
          ▼  NVMe-oF internal fabric
  Fabric Module (FM)
  ├── Aggregates blade capacity and compute
  ├── Routes client requests to owning blade
  └── Provides unified namespace (NFS / SMB / S3)
          │
          ▼  10/25/100 GbE
  Client Network
  ├── NFS v3/v4.1 (pNFS for parallel AI/ML reads)
  ├── SMB 2/3 (Windows file shares)
  ├── S3 (object — analytics pipelines, backup targets)
  └── HDFS (Hadoop/Spark without separate cluster)

  HA: blade failure → remaining blades absorb capacity
  Replication: ActiveDR (async) to remote FlashBlade
```

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Scale-out architecture, HA topology, protocols, file and object services.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware, backup tools, Pure1, authentication, and REST API.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, sizing, build baseline, and configuration checklist.</span></a>
</div>

| Protocol | Use Case |
|---|---|
| NFS v3 / v4.1 | Linux clients, HPC workloads, AI/ML training data (pNFS for parallel access) |
| SMB 2.0 / 3.0 | Windows file sharing; SMB 3.0 encryption and multichannel |
| S3 object | Analytics pipelines, backup targets, object storage; compatible with AWS S3 SDK |
| HDFS | Hadoop/Spark workloads without a dedicated Hadoop cluster |

```mermaid
graph TB
  FMM["Fabric Management Module\n(NVMe-oF internal fabric)"]
  B1["Blade 1"] & B2["Blade 2"] & B3["Blade 3"] & BN["Blade N…"] --> FMM
  FMM --> ETH["10 / 25 / 100 GbE\nData Ports"]
  ETH --> NFS(["NFS v3/v4.1 Clients"])
  ETH --> S3(["S3 / Object Clients"])
  ETH --> SMB(["SMB Clients"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class FMM,B1,B2,B3,BN ctrl
  class ETH net
  class NFS,S3,SMB host
```
