# NetBackup — Architecture

<div class="kb-summary">
Veritas NetBackup three-tier architecture — Primary Server catalog and scheduling, Media Servers for data movement, and Clients with backup agents.
</div>

```
┌────────────────────────────────────── NetBackup — Architecture ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               NetBackup — Component Architecture                              │   │
│   │             Master Server     — scheduler, catalog, policy engine, job controller             │   │
│   │             Media Server      — data mover, dedup engine, storage unit management             │   │
│   │          Client Agent      — installed on protected host; sends data to media server          │   │
│   │                       Ports: 443 (Web UI) · 1556 (vnetd) · 13724 (bprd)                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Three-tier component model — control plane, data plane, and management                             │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Control Plane        │  │          Data Plane         │  │          Management         │   │
│   │ Master Server     — schedule│  │ Media Server      — data mov│  │ NetBackup Web UI  — browser │   │
│   │          Scheduling         │  │      Replication/Backup     │  │         443 (Web UI)        │   │
│   │         Policy mgmt         │  │        Data movement        │  │           REST API          │   │
│   │          Catalog/DB         │  │        Dedup/compress       │  │             RBAC            │   │
│   │          Job engine         │  │         1556 (vnetd)        │  │           Alerting          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection             │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master Server = central controller: scheduler, catalog, job manager, policy engine                   │
│  Media Server  = data mover between client and storage; can be co-located with master                 │
│  MSDP          = Media Server Deduplication Pool; inline variable-length block dedup                  │
│  Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot                    │
│  Policy        = defines what, when, and where to back up; contains schedules and clients             │
│  Schedule      = full / differential-incremental / cumulative-incremental timing within policy        │
│  Retention     = how long an image is kept; set per schedule, enforced by catalog expiry              │
│  Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config             │
│  NBU CA        = auto-issued certificate authority; signs host IDs for secure comms                   │
│  vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556           │
│  bpdbjobs      = CLI to query job history: status, duration, exit code, errors                        │
│  bplist        = CLI to list available backup images for a client, policy, or date range              │
│  KMS           = Key Management Service for encryption keys used in backup data encryption            │
│  NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── NetBackup — Architecture ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               NetBackup — Component Architecture                              │   │
│   │             Master Server     — scheduler, catalog, policy engine, job controller             │   │
│   │             Media Server      — data mover, dedup engine, storage unit management             │   │
│   │          Client Agent      — installed on protected host; sends data to media server          │   │
│   │                       Ports: 443 (Web UI) · 1556 (vnetd) · 13724 (bprd)                       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Three-tier component model — control plane, data plane, and management                             │
│                                                                                                       │
│                          ▼                        ▼                        ▼                          │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Control Plane        │  │          Data Plane         │  │          Management         │   │
│   │ Master Server     — schedule│  │ Media Server      — data mov│  │ NetBackup Web UI  — browser │   │
│   │          Scheduling         │  │      Replication/Backup     │  │         443 (Web UI)        │   │
│   │         Policy mgmt         │  │        Data movement        │  │           REST API          │   │
│   │          Catalog/DB         │  │        Dedup/compress       │  │             RBAC            │   │
│   │          Job engine         │  │         1556 (vnetd)        │  │           Alerting          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Linux/Windows rack servers · SAN HBAs for tape · 10 GbE NIC · SCSI tape robot connection             │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Master Server = central controller: scheduler, catalog, job manager, policy engine                   │
│  Media Server  = data mover between client and storage; can be co-located with master                 │
│  MSDP          = Media Server Deduplication Pool; inline variable-length block dedup                  │
│  Storage Unit  = logical target: AdvancedDisk, MSDP pool, cloud LSU, or tape robot                    │
│  Policy        = defines what, when, and where to back up; contains schedules and clients             │
│  Schedule      = full / differential-incremental / cumulative-incremental timing within policy        │
│  Retention     = how long an image is kept; set per schedule, enforced by catalog expiry              │
│  Catalog       = internal PostgreSQL DB tracking all image metadata, host IDs, and config             │
│  NBU CA        = auto-issued certificate authority; signs host IDs for secure comms                   │
│  vnetd         = NetBackup network daemon; multiplexes all client-master-media on port 1556           │
│  bpdbjobs      = CLI to query job history: status, duration, exit code, errors                        │
│  bplist        = CLI to list available backup images for a client, policy, or date range              │
│  KMS           = Key Management Service for encryption keys used in backup data encryption            │
│  NDMP          = Network Data Management Protocol; direct NAS-to-storage backup path                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![NetBackup Architecture](../../../assets/netbackup-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Three-tier topology, key processes, storage units, catalog backup, and sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware VADP, Oracle RMAN, NDMP, and cloud storage integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Policy naming, retention schedules, MSDP standards, and media server placement.</span></a>
</div>

| Component | Role |
|---|---|
| Primary Server | Central scheduler, catalog DB (PostgreSQL), EMM device database |
| Media Server | Data mover; writes to storage units; runs deduplication (MSDP) |
| Client | Backup agent on protected host; sends data to Media Server via TCP 13724 |
| MSDP | Media Server Deduplication Pool; inline dedup; supports AIR image replication |
| Catalog | Most critical component — tracks all backup images; must be protected separately |


