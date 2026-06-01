# PowerScale — Architecture

<div class="kb-summary">
Dell PowerScale (formerly Isilon) is a scale-out NAS platform running the OneFS distributed operating system. All nodes are peers sharing a single global namespace under <code>/ifs</code>. Clusters scale from 3 to 252 nodes across NFS, SMB, HDFS, and S3 protocols.
</div>
```text
┌─────────────────────────────────── Dell PowerScale — Architecture ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ PowerScale architecture overview: scale-out NAS platform (Isilon) for unstructured and file w │   │
│   │                     Protocols: NFS v3/v4.1 · SMB · HDFS · S3 · Swift · FTP                    │   │
│   │                    Key components: OneFS OS, SmartPools, SyncIQ, SnapshotIQ                   │   │
│   │          Design principles: HA, scalability, non-disruptive operations, and security          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Design → deploy → configure → validate → monitor → optimise                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │              OS             │  │            OneFS            │  │        Distributed FS       │   │
│   │           Tiering           │  │          SmartPools         │  │        Auto data move       │   │
│   │         Replication         │  │            SyncIQ           │  │        Async DR copy        │   │
│   │          Snapshots          │  │          SnapshotIQ         │  │       Space-efficient       │   │
│   │         Load balance        │  │         SmartConnect        │  │       DNS client dist.      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │      OneFS       │ Distributed file │  NFS/SMB/S3/HDFS  │  Kerberos/NTLM   │ Single namespac  │   │
│   │    SmartPools    │  Tiering policy  │      Internal     │    Admin role    │  Auto data move  │   │
│   │      SyncIQ      │ Async replicatio │   Encrypted TCP   │   Certificate    │   Policy-based   │   │
│   │    SnapshotIQ    │    Snapshots     │      Internal     │    Admin role    │  Per directory   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerScale nodes (All-Flash/Hybrid) · InfiniBand backend · 25/100 GbE frontend           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    OneFS              = Dell PowerScale distributed filesystem OS; all nodes share a single namespace │
│    SmartPools         = tiering engine; moves files between All-Flash, Hybrid, and Archive tiers      │
│    SyncIQ             = async replication to DR cluster; RPO-based schedule; failover in minutes      │
│    SnapshotIQ         = space-efficient snapshots; accessed via .snapshot directory in each share     │
│    SmartConnect       = DNS-based load balancing; distributes NFS/SMB client connections across nodes │
│    Access zone        = logical container with separate authentication and export namespace per tenant│
│    Quota              = directory or user quota; hard/soft/advisory limits enforced by OneFS QuotaIQ  │
│    CloudPools         = tiering to cloud object storage (S3/Blob); data remains accessible locally    │
│    isi CLI            = OneFS command-line interface; all management operations available via isi c...│
│    Node pool          = group of same-model nodes sharing protection domain for data distribution     │
│    Protection level   = N+2:1, N+3:1 etc.; defines how many node or drive failures are tolerated      │
│    File pool policy   = rule-based policy assigning files to specific node pools or storage tiers     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
