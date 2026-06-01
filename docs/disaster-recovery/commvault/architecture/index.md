# Commvault — Architecture

<div class="kb-summary">
Commvault architecture reference — CommServe topology, MediaAgent deduplication, storage library types, multi-site design, and port requirements.
</div>

```
┌───────────────────────────── Commvault Architecture — Component Topology ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     CommCell Architecture                                     │   │
│   │          Three-tier: CommServe (control) → MediaAgent (data plane) → Client (source)          │   │
│   │              All communications encrypted TLS 1.2+; certificate-based mutual auth             │   │
│   │        CommCell ID uniquely identifies the deployment; required for cross-CommCell ops        │   │
│   │             Firewall tunnels: clients connect outbound to CommServe 8400 / MA 8403            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Control plane (CS) and data plane (MA) are separated for independent scaling                       │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Control Plane (CommServe)           │  │           Data Plane (MediaAgents)          │   │
│   │        SQL Server CommCell DB (CSDB)         │  │         Deduplication Database (DDB)        │   │
│   │      Job Manager: schedule/queue/retry       │  │          Chunk-based data pipeline          │   │
│   │        Event Manager: alerts and SNMP        │  │        Compression + encryption at MA       │   │
│   │         CommServe Cache: DR metadata         │  │     Mount paths: disk/tape/cloud targets    │   │
│   │        HA: active/passive CS failover        │  │      MA groups: load-balance across MAs     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Data flows from Client iDA → MediaAgent → Storage Library (bypassing CommServe)                    │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Data Flow: Backup Job                                     │   │
│   │         1. CS Job Manager fires job → sends instructions to Client iDA and MediaAgent         │   │
│   │            2. Client iDA reads source data (VSS snapshot, DB quiesce, or live read)           │   │
│   │               3. Data stream transferred Client → MA over TCP (port 8403 tunnel)              │   │
│   │            4. MA deduplicates (DDB lookup), compresses, encrypts, writes to library           │   │
│   │                5. MA reports chunk metadata to CS; CSDB records job completion                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CommServe: 2U rack server · 32-64 GB RAM · SQL Server on NVMe RAID-10 · 10 GbE NIC                   │
│  MediaAgent: 2U server · 16-32 GB RAM · FC HBA 8/16 Gb for tape · 10/25 GbE NIC                       │
│  Disk Library: NAS/SAN target · FC or iSCSI LUNs · WORM-capable for compliance                        │
│  Tape Library: FC-attached autoloader or enterprise tape library (LTO-8/9)                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CommCell DB    = SQL Server database holding all job history, policies, and metadata                 │
│  Job Manager    = CommServe service that schedules, launches, and monitors backup jobs                │
│  iDA            = Intelligent Data Agent; client-side component that reads/writes data                │
│  VSS            = Volume Shadow Copy Service; Windows quiesce mechanism used by iDA                   │
│  Chunk          = Fixed-size data block written to library; unit of dedup and tracking                │
│  Silo           = Isolated MA group for multi-tenant or compliance storage separation                 │
│  MA Group       = Named set of MediaAgents used for load balancing backup streams                     │
│  Firewall Proxy = CV Tunnel Service enabling outbound-only client connectivity                        │
│  CommCell DR    = Warm standby CommServe; CSDB replicated via SQL log shipping                        │
│  CSDB Backup    = Automated backup of CommServe DB; critical for disaster recovery                    │
│  Library        = Logical storage target: disk path, tape drive, or cloud container                   │
│  Retention      = Policy defining how many days/cycles backup data is kept on each copy               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌───────────────────────────── Commvault Architecture — Component Topology ─────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     CommCell Architecture                                     │   │
│   │          Three-tier: CommServe (control) → MediaAgent (data plane) → Client (source)          │   │
│   │              All communications encrypted TLS 1.2+; certificate-based mutual auth             │   │
│   │        CommCell ID uniquely identifies the deployment; required for cross-CommCell ops        │   │
│   │             Firewall tunnels: clients connect outbound to CommServe 8400 / MA 8403            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Control plane (CS) and data plane (MA) are separated for independent scaling                       │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Control Plane (CommServe)           │  │           Data Plane (MediaAgents)          │   │
│   │        SQL Server CommCell DB (CSDB)         │  │         Deduplication Database (DDB)        │   │
│   │      Job Manager: schedule/queue/retry       │  │          Chunk-based data pipeline          │   │
│   │        Event Manager: alerts and SNMP        │  │        Compression + encryption at MA       │   │
│   │         CommServe Cache: DR metadata         │  │     Mount paths: disk/tape/cloud targets    │   │
│   │        HA: active/passive CS failover        │  │      MA groups: load-balance across MAs     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Data flows from Client iDA → MediaAgent → Storage Library (bypassing CommServe)                    │
│                                                                                                       │
│                                                   ▼                                                   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Data Flow: Backup Job                                     │   │
│   │         1. CS Job Manager fires job → sends instructions to Client iDA and MediaAgent         │   │
│   │            2. Client iDA reads source data (VSS snapshot, DB quiesce, or live read)           │   │
│   │               3. Data stream transferred Client → MA over TCP (port 8403 tunnel)              │   │
│   │            4. MA deduplicates (DDB lookup), compresses, encrypts, writes to library           │   │
│   │                5. MA reports chunk metadata to CS; CSDB records job completion                │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  CommServe: 2U rack server · 32-64 GB RAM · SQL Server on NVMe RAID-10 · 10 GbE NIC                   │
│  MediaAgent: 2U server · 16-32 GB RAM · FC HBA 8/16 Gb for tape · 10/25 GbE NIC                       │
│  Disk Library: NAS/SAN target · FC or iSCSI LUNs · WORM-capable for compliance                        │
│  Tape Library: FC-attached autoloader or enterprise tape library (LTO-8/9)                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  CommCell DB    = SQL Server database holding all job history, policies, and metadata                 │
│  Job Manager    = CommServe service that schedules, launches, and monitors backup jobs                │
│  iDA            = Intelligent Data Agent; client-side component that reads/writes data                │
│  VSS            = Volume Shadow Copy Service; Windows quiesce mechanism used by iDA                   │
│  Chunk          = Fixed-size data block written to library; unit of dedup and tracking                │
│  Silo           = Isolated MA group for multi-tenant or compliance storage separation                 │
│  MA Group       = Named set of MediaAgents used for load balancing backup streams                     │
│  Firewall Proxy = CV Tunnel Service enabling outbound-only client connectivity                        │
│  CommCell DR    = Warm standby CommServe; CSDB replicated via SQL log shipping                        │
│  CSDB Backup    = Automated backup of CommServe DB; critical for disaster recovery                    │
│  Library        = Logical storage target: disk path, tape drive, or cloud container                   │
│  Retention      = Policy defining how many days/cycles backup data is kept on each copy               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Commvault Architecture](../../../assets/commvault-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>CommServe topology, MediaAgent dedup, storage library types, multi-site design, and port requirements.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware, cloud storage, NDMP, and third-party integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, retention schedule, DDB standards, and VMware backup settings.</span></a>
</div>

| Component | Role |
|---|---|
| CommServe | Command and control; SQL DB; HA pair for critical environments |
| MediaAgent | Data movement and deduplication (DDB); one DDB per storage pool |
| Client | Backup agent (Windows, Linux, VSA for VMware vSphere) |
| Command Center | Web UI (port 443); replaces legacy Java GUI in FR32+ |


