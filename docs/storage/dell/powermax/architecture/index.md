# PowerMax — Architecture

<div class="kb-summary">
Dell PowerMax is an enterprise all-flash NVMe-oF array with an active-active director-pair architecture and global memory mirroring. It supports SRDF synchronous (zero RPO) and asynchronous replication for metro and long-distance DR.
</div>
```
┌──────────────────────────────────── Dell PowerMax — Architecture ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ PowerMax architecture overview: high-end enterprise NVMe all-flash array for mission-critical │   │
│   │                      Protocols: FC · iSCSI · NVMe-oF · SRDF (replication)                     │   │
│   │             Key components: Unisphere, Solutions Enabler, SRDF, TimeFinder SnapVX             │   │
│   │          Design principles: HA, scalability, non-disruptive operations, and security          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Design → deploy → configure → validate → monitor → optimise                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │           Function          │   │
│   │            Cache            │  │          DRAM 2 TB+         │  │        Sub-ms latency       │   │
│   │         FE director         │  │        FC/iSCSI ports       │  │         Host facing         │   │
│   │         BE director         │  │         NVMe drives         │  │        Storage facing       │   │
│   │             SRDF            │  │         RDF director        │  │       Metro/remote DR       │   │
│   │          TimeFinder         │  │         SnapVX/Clone        │  │       Local protection      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    SRDF Sync     │   Zero-RPO DR    │    RDF protocol   │   Certificate    │   Metro <200ms   │   │
│   │    SRDF Async    │  Near-zero RPO   │    RDF protocol   │   Certificate    │   Any distance   │   │
│   │    TimeFinder    │ Local snapshots  │      Internal     │ Solutions Enabl  │   256 snaps/SG   │   │
│   │Solutions Enabler │   CLI/API mgmt   │    HTTPS/symcli   │   Certificate    │     Symm CLI     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerMax 2500/8500 engine · FE/BE/RDF directors · DRAM cache · expansion bays            │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerMax           = Dell flagship NVMe all-flash array; millions of IOPS at sub-millisecond lat...│
│    SRDF               = Symmetrix Remote Data Facility; sync/async metro and remote site replication  │
│    TimeFinder SnapVX  = space-efficient snapshot technology; up to 256 snapshots per storage group    │
│    Storage group      = logical container for volumes sharing service level and host access policy    │
│    Service level      = performance target for a storage group: Diamond, Platinum, Gold, Silver       │
│    FE director        = front-end director providing FC or iSCSI host-facing ports on the engine      │
│    BE director        = back-end director connecting engine cache to NVMe flash drive bays            │
│    RDF director       = SRDF director providing dedicated bandwidth for replication traffic           │
│    Solutions Enabler  = CLI and API toolkit; symcli commands cover all PowerMax management            │
│    Unisphere          = web GUI and REST API server for PowerMax; unified management interface        │
│    DCM                = Dynamic Cache Management; auto-balances workloads across available cache re...│
│    Service level obj. = workload performance class assigned to storage group; enforced by DPTM        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


![PowerMax Architecture](../../../../assets/powermax-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">How It Works</div>
    <div class="kb-card-desc">Director-pair HA, SRDF replication modes, NVMe-oF fabric, SnapVX snapshots, and SYMCLI reference.</div>
  </a>
  <a class="kb-card" href="integrations/">
    <div class="kb-card-icon">🔗</div>
    <div class="kb-card-title">Integrations</div>
    <div class="kb-card-desc">VMware VASA/vVols, Oracle RMAN, SQL Server, VPLEX back-end, and Solutions Enabler scripting.</div>
  </a>
  <a class="kb-card" href="design-standards/">
    <div class="kb-card-icon">📐</div>
    <div class="kb-card-title">Design Standards</div>
    <div class="kb-card-desc">SRDF topology decisions, director layout, zoning standards, and host connectivity design rules.</div>
  </a>
</div>

## Models

| Model | Engines | Max Raw Capacity | Primary Use Case |
|---|---|---|---|
| PowerMax 2000 | 1–4 | ~4.5 PB | Mid-enterprise; tier-1 databases |
| PowerMax 8000 | 1–8 | ~9 PB | Large enterprise; SRDF/S metro clusters |

Both models share the same PowerMaxOS, SRDF feature set, and NVMe-oF architecture. The 8000 supports more engines and higher drive counts.

## Topology

```mermaid
graph TB
  SAN(["FC / NVMe-oF Hosts"])
  subgraph "PowerMax Engine"
    DA["Director A\n(FE + BE + RDF)"] <-->|"Global Memory\n(mirrored)"| DB["Director B\n(FE + BE + RDF)"]
  end
  NVMe[("NVMe SSDs\nRAID-5 / RAID-6")]
  SRDF["Remote PowerMax\n(SRDF partner)"]
  SAN --> DA & DB
  DA & DB --> NVMe
  DA & DB -->|"SRDF/S or SRDF/A\nFC / GigE"| SRDF
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class DA,DB ctrl
  class NVMe store
  class SAN host
  class SRDF dr
```
