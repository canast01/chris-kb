---
tags:
  - architecture
  - dell
---
# PowerScale — Architecture

<div class="kb-summary">
Dell PowerScale (formerly Isilon) is a scale-out NAS platform running the OneFS distributed operating system. All nodes are peers sharing a single global namespace under <code>/ifs</code>. Clusters scale from 3 to 252 nodes across NFS, SMB, HDFS, and S3 protocols.

*Applies to: PowerScale (Isilon) 9.x*
</div>

```text
┌───────────────────────── Dell PowerScale — OneFS Scale-Out NAS Architecture ──────────────────────────┐
│                                                                                                       │
│  Single filesystem namespace across all nodes; horizontal scale by adding nodes;                      │
│  NFS/SMB/HDFS/S3 protocols; SyncIQ async replication; SmartConnect DNS load balance.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              OneFS Architecture              │  │                  Protocols                  │   │
│   │         Single filesystem namespace          │  │           NFS v3/v4.1: Linux/Unix           │   │
│   │            H-series: HDD capacity            │  │             SMB 2.1/3.0: Windows            │   │
│   │          F-series: NVMe performance          │  │            HDFS: Hadoop workloads           │   │
│   │             A-series: AFA nodes              │  │              S3: via S3 gateway             │   │
│   │        No LUN abstraction: files only        │  │          Multi-protocol: same data          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SmartConnect assigns DNS names per access zone; clients distributed across nodes.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Data Protection                │  │                  Management                 │   │
│   │          N+M FEC: RAID across nodes          │  │           OneFS CLI: isi commands           │   │
│   │          SyncIQ: async replication           │  │            OneFS web UI: browser            │   │
│   │          SnapshotIQ: point-in-time           │  │                REST API: v12+               │   │
│   │          SmartLock: WORM compliance          │  │             InsightIQ: analytics            │   │
│   │           CloudPools: S3 cold tier           │  │             SmartConnect: DNS LB            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  PowerScale nodes in rack; InfiniBand or 25GbE backend between nodes; dual-port                       │
│  front-end Ethernet to client network; dedicated management Ethernet port.                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PowerScale     = Dell scale-out NAS; formerly Isilon; runs OneFS OS                                  │
│  OneFS          = PowerScale operating system; presents single namespace across nodes                 │
│  FEC            = Forward Error Correction; like RAID 5/6 but across multiple nodes                   │
│  SyncIQ         = async policy-based replication between PowerScale clusters                          │
│  SnapshotIQ     = point-in-time snapshot; no performance impact; schedule-based                       │
│  SmartLock      = WORM (Write Once Read Many) compliance; object immutability                         │
│  CloudPools     = auto-tier cold data to S3 (AWS, Azure, or ECS)                                      │
│  SmartConnect   = DNS-based client distribution across OneFS front-end nodes                          │
│  Access zone    = logical tenant partition; own auth, protocols, IP range                             │
│  H-series       = HDD-based capacity nodes; high density, moderate performance                        │
│  HDFS           = Hadoop Distributed Filesystem; PowerScale presents as HDFS                          │
│  isi commands   = OneFS CLI; isi status, isi volumes, isi sync policies                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TB
  N1["Node 1"] & N2["Node 2"] & N3["Node 3"] & NN["Node N…"] --> INT["InfiniBand / 100GbE\nInternal Cluster Network"]
  INT --> SC["SmartConnect\n(DNS-based load balancing)"]
  SC --> NFS(["NFS v3/v4 Clients"])
  SC --> SMB(["SMB / CIFS Clients"])
  SC --> HDFS(["HDFS / S3 Clients"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2,N3,NN ctrl
  class INT,SC net
  class NFS,SMB,HDFS host
```
![PowerScale Architecture](../../../../assets/powerscale-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">How It Works</div>
    <div class="kb-card-desc">OneFS distributed FS, SmartConnect DNS load balancing, SmartPools tiering, SyncIQ replication, and protection levels.</div>
  </a>
  <a class="kb-card" href="integrations/">
    <div class="kb-card-icon">🔗</div>
    <div class="kb-card-title">Integrations</div>
    <div class="kb-card-desc">Hadoop/HDFS, VMware NFS datastores, S3 object API, CloudPools cold tiering, and Active Directory auth.</div>
  </a>
  <a class="kb-card" href="design-standards/">
    <div class="kb-card-icon">📐</div>
    <div class="kb-card-title">Design Standards</div>
    <div class="kb-card-desc">Access zone layout, SmartConnect zone design, protection level selection, and SyncIQ policy standards.</div>
  </a>
</div>

## Node Families

| Family | Models | Storage Type | Primary Use Case |
|---|---|---|---|
| F-series | F600, F900 | All-NVMe SSD | High-IOPS: EDA, genomics, databases |
| H-series | H700, H7000 | NVMe + SAS HDD hybrid | Mixed: home directories, general NAS |
| A-series | A300, A3000 | NL-SAS high-density | Archive and cold data retention |

## Topology


