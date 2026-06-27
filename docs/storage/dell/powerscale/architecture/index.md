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

![PowerScale — Architecture — Diagram](../../../../assets/storage-dell-powerscale-architecture-diagram.svg)

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


