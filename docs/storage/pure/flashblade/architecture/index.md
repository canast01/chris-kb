# FlashBlade — Architecture

<div class="kb-summary">
Architecture reference for Pure Storage FlashBlade. Covers the scale-out blade model, Purity//FB data services, NFS/SMB/S3/HDFS protocol support, HA through blade redundancy, ActiveDR and ActiveCluster replication, and design standards.
</div>
```
┌─────────────────────────────────── Pure FlashBlade — Architecture ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ FlashBlade architecture overview: massively parallel all-flash NAS and object storage platfor │   │
│   │                      Protocols: NFS v3/v4.1 · SMB · S3 · Swift · REST API                     │   │
│   │             Key components: Purity//FB, File systems, Object buckets, Replication             │   │
│   │          Design principles: HA, scalability, non-disruptive operations, and security          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Design → deploy → configure → validate → monitor → optimise                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Blades           │  │           NVMe+CPU          │  │         Parallel I/O        │   │
│   │             File            │  │           NFS/SMB           │  │        Scale-out NAS        │   │
│   │            Object           │  │           S3/Swift          │  │         Bucket store        │   │
│   │         Replication         │  │            Async            │  │          DR/backup          │   │
│   │           SafeMode          │  │         Locked snaps        │  │      Ransomware resist      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │   File system    │  NAS namespace   │      NFS/SMB      │  Kerberos/NTLM   │   Up to 4 PiB    │   │
│   │  Object bucket   │   S3 namespace   │      S3/Swift     │   S3 keys/IAM    │    Versioning    │   │
│   │   Replication    │     Async DR     │   Encrypted TCP   │   Certificate    │  File or object  │   │
│   │     SafeMode     │ Locked snapshots │      Internal     │   Pure support   │    Immutable     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: FlashBlade//S or //E chassis · storage blades · 100 GbE network · Pure1 SaaS             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FlashBlade         = Pure massively parallel all-flash NAS and object platform; single namespace   │
│    Blade              = individual storage module in FlashBlade chassis; NVMe and CPU per blade       │
│    File system        = FlashBlade NFS/SMB export namespace; up to 4 PiB per file system              │
│    Object store       = S3-compatible bucket store on FlashBlade; versioning and lifecycle rules      │
│    purefb CLI         = REST CLI client for FlashBlade: purefb fs list, purefb array show commands    │
│    Replication        = async file or object replication between FlashBlade systems for DR            │
│    SafeMode           = admin-locked snapshots; protected from deletion even by local array admin     │
│    S3 multitenancy    = per-bucket policy and IAM-style access control for object storage             │
│    NFS Kerberos       = FlashBlade NFS supports krb5, krb5i, and krb5p security flavours              │
│    SMB multichannel   = FlashBlade uses SMB multichannel for improved Windows client performance      │
│    Inline compression = always-on data reduction; typically 2-10x for unstructured data               │
│    ActiveScale        = enterprise geo-distribution and erasure coding for large object workloads     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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

![FlashBlade Architecture](../../../../assets/flashblade-architecture-overview.svg)

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
