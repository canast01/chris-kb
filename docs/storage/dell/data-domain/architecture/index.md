# Data Domain — Architecture
## Overview

Dell PowerProtect DD (Data Domain) is a purpose-built backup appliance built around inline global deduplication. All data is deduplicated as it is written — not in post-processing — using the SISL (Stream-Informed Segment Layout) deduplication engine. The result is a highly space-efficient backup target that typically achieves 20:1 or greater reduction ratios across mixed workloads.


## Deduplication Pipeline

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                  Data Domain (PowerProtect DD) Architecture              │
  │                                                                          │
  │  Ingest                                                                  │
  │  ┌──────────────────────────────────────────────────────────────────┐   │
  │  │  Backup clients / media servers                                  │   │
  │  │  Veeam  NetBackup  CommVault  TSM  Oracle RMAN  NFS / CIFS / VTL│   │
  │  └────────────────────────────────┬─────────────────────────────── ┘   │
  │                                   │  data stream                       │
  │  ┌────────────────────────────────▼─────────────────────────────────┐  │
  │  │  SISL Inline Deduplication Engine                                │  │
  │  │  1. Segment stream into variable-length chunks                   │  │
  │  │  2. Fingerprint each chunk (SHA)                                 │  │
  │  │  3. Lookup FP in dedup index (DRAM + SSD cache)                  │  │
  │  │  4. If match: store reference only (no write to disk)            │  │
  │  │  5. If new: compress + write to active tier                      │  │
  │  └───────────────────────────────┬──────────────────────────────── ┘  │
  │                                  │  deduplicated + compressed data     │
  │  ┌─────────────────────────────── ▼────────────────────────────────┐   │
  │  │  Storage Tiers                                                   │   │
  │  │  ┌──────────────────┐  ┌───────────────────┐  ┌──────────────┐  │   │
  │  │  │  Active Tier     │  │  Retention Tier   │  │  Cloud Tier  │  │   │
  │  │  │  (SSD / NL-SAS)  │  │  (NL-SAS archive) │  │  (S3 / Azure)│  │   │
  │  │  └──────────────────┘  └───────────────────┘  └──────────────┘  │   │
  │  └──────────────────────────────────────────────────────────────────┘  │
  │  Typical dedupe ratio: 20:1 across mixed backup workloads               │
  └──────────────────────────────────────────────────────────────────────────┘
```

## Core Components

| Component | Description |
|---|---|
| DDOS | Data Domain Operating System — the purpose-built OS managing the filesystem, dedup engine, protocols, and services |
| DDFS | Data Domain Filesystem — the underlying deduplicated storage layer; manages segments, containers, and references |
| SISL Engine | Stream-Informed Segment Layout — determines which segments are unique vs. duplicates using locality-based filtering before writing to disk |
| MTree | Logical namespace partition within DDFS; provides per-tenant or per-application capacity isolation, quotas, replication, and retention lock scope |
| DD Boost | Application-aware deduplication protocol; moves dedup processing partially to the backup client, reducing network traffic by 50% or more |
| VTL | Virtual Tape Library — emulates physical tape drives and libraries over Fibre Channel for backup software expecting tape |
| DD Encryption (D@RE) | Data at Rest Encryption — encrypts all on-disk data; integrates with RSA DPM or KMIP key managers |
| Cloud Tier | Extends DDFS to cloud object storage (AWS S3, Azure Blob, ECS) for long-term retention without a separate archive tier |
| NVRAM | Non-volatile write cache — absorbs incoming writes to protect against data loss during power failure |

## Filesystem Architecture

```
DDFS (Data Domain Filesystem)
├── Namespace layer (MTrees: /data/col1/<name>)
│   ├── MTree A (e.g., mtree-veeam-prod)
│   ├── MTree B (e.g., mtree-netbackup-ora)
│   └── MTree C (e.g., mtree-commvault-dev)
├── Segment store (deduplicated data containers)
├── Index (segment fingerprint lookup table)
└── Cleaning layer (garbage collection of unreferenced segments)
```

Each MTree is a logical view; all data physically shares the same dedup pool. Quotas are enforced per MTree, but deduplication operates globally across all MTrees.

## HA Topology

### Single Node (Standard)

The most common deployment. A single DD appliance with internal or external shelf expansion. No automatic failover — HA is achieved through MTree replication to a secondary DD at a remote site.

```
[Backup Clients]
      |
  [Data Domain]  ←── DDBoost / NFS / CIFS / VTL
      |
  [Disk Shelves]  (internal or external SAS expansion)
      |
  [Replication target DD] (remote site — DR)
```

### HA Active-Standby Pair

Available on high-end DD9000/DD9900 series. Two DD heads share the same disk shelves. The standby monitors the active node and takes over on failure. Failover is automatic and non-disruptive to replication contexts.

```
[Active DD Head] ←──── Heartbeat ────→ [Standby DD Head]
         \                                    /
          └──── Shared SAS Disk Shelves ─────┘
```

### Replication Topologies

| Topology | Use Case |
|---|---|
| MTree replication (point-to-point) | Replicate individual MTrees independently to one or more targets |
| Collection replication | Full filesystem replication — replicates all MTrees as a single stream; used for full site DR |
| Cascaded replication | Source → Intermediate → Remote; useful when remote site is WAN-limited |
| Managed file replication | File-level replication for granular copy workflows |

## Data Path

```
Backup Client
    │
    │  (DDBoost: client-side dedup filter)
    ▼
DD Boost Receiver / NFS / CIFS handler
    │
    ▼
SISL Engine (segment fingerprinting + locality filter)
    │  unique segments only
    ▼
NVRAM write cache
    │
    ▼
DDFS Container Store (on disk)
    │
    ▼ (async)
Replication engine → Remote DD
```

## Protocol Interfaces

| Protocol | Use Case |
|---|---|
| DD Boost (over IP) | Veeam, NetBackup, CommVault, Avamar — application-aware dedup, fastest ingest |
| NFS v3/v4 | Generic Linux/Unix backup servers; NAS backup targets |
| CIFS/SMB | Windows backup clients; generic file-level targets |
| VTL (FC) | Backup software requiring tape emulation (NetBackup, TSM, older CommVault configs) |
| DD Boost (over FC) | High-throughput FC-attached DD Boost for high-performance environments |
| REST API | Programmatic management, automation, and monitoring |
| S3 | Cloud Tier gateway — aged backup data offloaded to cloud object storage |

## Connectivity and Network Design

- **Management network**: Dedicated NIC for DDOS management, System Manager GUI, REST API access. Recommend a separate management VLAN.
- **Data network**: Dedicated 10GbE or 25GbE bonds for backup traffic (DD Boost / NFS / CIFS). Bond with LACP for throughput and redundancy.
- **Replication network**: Separate interface or VLAN for MTree replication. Replication can be throttled per-schedule to protect production bandwidth.
- **FC SAN (VTL)**: HBAs connected to the SAN fabric for VTL tape emulation. Zone only the backup media servers to the VTL ports.

## Sizing Considerations

| Parameter | Guidance |
|---|---|
| Usable capacity | Size for 2–3 weeks of full backups pre-dedup; dedup ratio determines actual footprint |
| Dedup ratio assumption | Conservative estimate: 10:1 for databases, 20:1 for mixed workloads, 50:1 for long-term retention |
| Ingest throughput | Match DD model throughput to peak backup window requirement (e.g., DD9900: up to 68 TB/hr) |
| Head count for HA | HA pair if RTO < 30 minutes; single node with fast replication recovery for RTO > 2 hours |
| Cloud Tier ratio | Keep 10–15% active tier headroom; age data older than 90 days to cloud tier |
| NVRAM | Built-in; not user-configurable — relevant for understanding write latency characteristics |
