---
tags:
  - architecture
  - pure
---
# FlashBlade — Architecture

<div class="kb-summary">
Architecture reference for Pure Storage FlashBlade. Covers the scale-out blade model, Purity//FB data services, NFS/SMB/S3/HDFS protocol support, HA through blade redundancy, ActiveDR and ActiveCluster replication, and design standards.

*Applies to: FlashBlade Purity//FB 4.x*
</div>

![FlashBlade Architecture](../../../../assets/flashblade-architecture-overview.svg)

```text
┌──────────────────── Pure FlashBlade — Scale-Out Unstructured Storage Architecture ────────────────────┐
│                                                                                                       │
│  Scale-out all-flash for unstructured data; blade-based architecture; NFS, SMB, S3;                   │
│  target: AI/ML datasets, genomics, media workflows, backup targets.                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                  Protocols                  │   │
│   │           FlashBlade chassis (4U)            │  │            NFS v3/v4.1: Linux/AI            │   │
│   │          Blades: capacity + compute          │  │           SMB 2/3: Windows shares           │   │
│   │          Scale: add blades for perf          │  │          S3: object; AI data lakes          │   │
│   │         //S: storage blade (current)         │  │            HDFS: Hadoop connector           │   │
│   │           Fabric: 40GbE or 100GbE            │  │          Multi-protocol: same data          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Performance scales linearly: each blade adds both capacity and throughput.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Data Services                 │  │                  Management                 │   │
│   │         Snapshots: instant, no-cost          │  │          Purity//FB UI: web browser         │   │
│   │         Replication: async to remote         │  │           REST API v2: automation           │   │
│   │         Pure Object Store: S3 compat         │  │            Pure1: multi-site SaaS           │   │
│   │          SafeMode: immutable snaps           │  │            CLI: purectl commands            │   │
│   │         File system: directory-based         │  │          NFS exports: per-FS share          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashBlade chassis in rack; 40GbE or 100GbE data ports per blade; management                         │
│  port (Eth); blades share chassis backplane for internal communication.                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FlashBlade     = Pure scale-out all-flash for file and object workloads                              │
│  //S blade      = current FlashBlade generation; each blade = storage + compute                       │
│  Scale-out      = add blades to grow capacity and performance simultaneously                          │
│  Purity//FB     = FlashBlade OS; manages filesystem, S3, snapshots                                    │
│  NFS export     = directory shared over NFS; each filesystem can have one export                      │
│  Pure Object Store= S3-compatible object store built into FlashBlade //S                              │
│  SafeMode       = immutable Snapshot; admin cannot delete; ransomware protection                      │
│  HDFS           = Hadoop filesystem; FlashBlade presents as HDFS target                               │
│  AI/ML workload = high-throughput random read; FlashBlade optimized for this                          │
│  Replication    = async policy-based; replicates filesystems to remote FlashBlade                     │
│  Multi-protocol = same data accessible via NFS, SMB, and S3 simultaneously                            │
│  Blade          = hot-plug module; each adds storage capacity + bandwidth + IOPS                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
