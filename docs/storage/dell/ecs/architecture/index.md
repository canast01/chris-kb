---
tags:
  - architecture
  - dell
---
# Dell ECS — Architecture

<div class="kb-summary">
Scale-out software-defined object storage on commodity x86 nodes. Exposes S3, Swift, Atmos, and CAS APIs; protects data within a site using erasure coding; replicates geo-distributed across Virtual Data Centers linked in replication groups.

*Applies to: ECS 3.x*
</div>

```text
┌──────────────────────────── Dell ECS — Elastic Cloud Storage Architecture ────────────────────────────┐
│                                                                                                       │
│  Software-defined object storage on commodity x86 nodes; S3/Swift/CAS protocols;                      │
│  Reed-Solomon erasure coding across nodes; geo-distribution across multiple sites.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Cluster Architecture             │  │             Supported Protocols             │   │
│   │           3+ nodes minimum per VDC           │  │         S3: primary; widest support         │   │
│   │         RAIN: node-level redundancy          │  │         Swift: OpenStack object API         │   │
│   │        Scale: add nodes horizontally         │  │           CAS: content-addressable          │   │
│   │           VDC: virtual data center           │  │           NFS: via S3-NFS gateway           │   │
│   │          Geo: multiple VDCs linked           │  │            HDFS: Hadoop connector           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Namespace and bucket hierarchy controls access; no traditional filesystem paths.                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Data Protection                │  │                  Management                 │   │
│   │         Erasure coding: 12/4 or 10/4         │  │              ECS Portal: web UI             │   │
│   │          No RAID: node-level coding          │  │           ECS REST API: automation          │   │
│   │         Geo-replication across VDCs          │  │         Namespace + bucket structure        │   │
│   │         WORM: immutable object lock          │  │          S3 ACLs + bucket policies          │   │
│   │         Object versioning supported          │  │          IAM-compatible user model          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ECS commodity x86 nodes (ECS 300/500 series); 25GbE networking between nodes;                        │
│  ECS Appliance or ECS Software on commodity servers; 3-node minimum per VDC.                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ECS            = Elastic Cloud Storage; Dell object storage platform                                 │
│  Object storage = stores data as objects (ID + data + metadata); no file hierarchy                    │
│  S3             = Simple Storage Service; Amazon API now the object storage standard                  │
│  RAIN           = Redundant Array of Independent Nodes; erasure coding at node level                  │
│  Erasure coding = like RAID 6 but across nodes; 12 data + 4 parity = 25% overhead                     │
│  WORM           = Write Once Read Many; immutable object lock for compliance                          │
│  VDC            = Virtual Data Center; an ECS cluster unit; multiple VDCs = geo                       │
│  Namespace      = top-level ECS tenant container; like an S3 account                                  │
│  Bucket         = object container within a namespace; like an S3 bucket                              │
│  CAS            = Content Addressable Storage; Dell Centera-compatible API                            │
│  Swift          = OpenStack object storage API; ECS-supported for OpenStack                           │
│  Geo-distribution= objects replicated across multiple VDCs in different sites                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TB
  CLT(["S3 / Swift / Atmos Clients"]) --> GW["Load Balancer\n(optional)"]
  GW --> N1["ECS Node 1"] & N2["ECS Node 2"] & N3["ECS Node 3"] & NN["Node N…"]
  N1 & N2 & N3 & NN --> RING[("Object Ring\ndistributed erasure coding")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2,N3,NN ctrl
  class GW,RING net
  class CLT host
```
![Dell ECS Architecture](../../../../assets/ecs-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with S3 clients, Hadoop, LDAP/AD, KMS, and backup tools.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>VDC sizing, replication group design, namespace and bucket configuration standards.</span></a>
</div>

## Erasure Coding Schemes

| EC Scheme | Data + Parity | Min Nodes | Tolerated Failures |
|---|---|---|---|
| 12+4 (default) | 12 + 4 | 16 | Up to 4 simultaneous node/disk failures |
| 10+2 | 10 + 2 | 12 | Up to 2 simultaneous failures |
| 4+2 (small cluster) | 4 + 2 | 6 | Up to 2 simultaneous failures |

## Scale-Out Object Storage Topology


