---
tags:
  - architecture
  - dell
---
# Data Domain — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Architecture, Data Path, Components, HA Options and 2 more sections.

*Applies to: Data Domain DD OS 7.x*
</div>
![Data Domain — How It Works](../../../../assets/storage-dell-data-domain-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "Backup Client\n(Veeam / NetBackup)" as CLT
participant "DD Boost\nLibrary (client-side)" as DDB
participant "Data Domain\nOS (DDOS)" as DD
participant "SISL Dedup Engine" as SISL
participant "Local Disks\n(RAID-6)" as DISK
participant "Remote DD\n(replication target)" as REMO

CLT -> DDB: Backup stream
DDB -> DD: Segmented + fingerprinted chunks
DD -> SISL: Deduplicate against index
SISL --> DD: Unique chunks only
DD -> DISK: Write unique segments
DD --> CLT: Backup complete (dedup ratio reported)

DD -> REMO: DD Replication (unique chunks delta)
REMO --> DD: Replication confirmed
@enduml
```

## Overview

Dell PowerProtect DD (Data Domain) is a purpose-built backup appliance built around **inline global deduplication**. All data is deduplicated as it is written using the SISL (Stream-Informed Segment Layout) engine — not in post-processing. Typical deduplication ratios: 20:1 or greater across mixed workloads.

## Architecture

```mermaid
graph TB
  BU(["Backup Servers\nNetBackup / Commvault / Veeam"]) -->|"DDBoost / NFS / CIFS / VTL"| DD["Dell Data Domain\n(dedup + compression)"]
  DD -->|"DD Replicator\nTCP 2051"| DDDR["Remote Data Domain\n(DR copy)"]
  DD --> CLOUD["Cloud Tier\nS3 / Azure Blob — long-term"]
  DD --> VTL["Virtual Tape Library\n(optional — FC)"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  class DD ctrl
  class BU host
  class CLOUD cloud
  class DDDR dr
```

DDBoost reduces network traffic by ~50% via source-side deduplication — only unique segments are sent to the DD appliance.

## Components

| Component | Description |
|---|---|
| DDBoost | Protocol allowing backup software to perform source-side dedup filtering; integrates with NetBackup, Commvault, Veeam |
| SISL Engine | Stream-Informed Segment Layout; fingerprints segments and matches against global index; new unique segments go to NVRAM |
| NVRAM | Power-safe write buffer; writes acknowledged to backup software after NVRAM landing |
| MTree | Logical namespace partition (`/data/col1/<name>`); quotas, retention locks, and replication policies set per MTree |
| DD Replicator | Asynchronous delta replication between DD systems; replicates only new unique segments (TCP 2051) |
| Cloud Tier | Lifecycle policy to offload aged segments to S3-compatible or Azure Blob object storage |
| VTL | Virtual Tape Library interface via FC for tape-based backup software integration |

## HA Options

| Model | HA Type | Description |
|---|---|---|
| DD2200–DD9400 | Single node | No controller failover; HA via MTree replication to remote DD |
| DD9900 | Active-Standby pair | Two DD heads sharing SAS disk shelves; standby monitors active; automatic failover |

## Protocol Access

| Protocol | Port | Use Case |
|---|---|---|
| DDBoost over IP | TCP 2052 (HTTP) / 2053 (HTTPS) | Primary — backup software integration |
| NFS v3 | TCP/UDP 2049 | Unix/Linux backup clients |
| CIFS/SMB | TCP 445 | Windows backup clients |
| VTL | FC | Tape-emulation for legacy backup software |
| DD Replicator | TCP 2051 | DD-to-DD replication |
| Management (CLI/UI) | TCP 22 (SSH) / 443 (HTTPS) | Administration |

## Key CLI Commands

```bash
filesys status                    # filesystem enabled/disabled state
filesys show space                # pre/post-compression capacity
filesys show compression          # global dedup ratio (healthy = 20:1+)
replication show                  # replication context states
ddboost show clients              # connected backup servers
alerts show current               # active hardware/software alerts
system show                       # hardware health (fans, PSUs, disks)
mtree list                        # all MTrees and their quota status
```

---

## See also

- [Data Domain — Design Standards](design-standards/)
- [Data Domain — Integrations](integrations/)
