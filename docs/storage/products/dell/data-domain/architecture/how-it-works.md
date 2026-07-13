---
tags:
  - architecture
  - dell
description: "How It Works reference covering Overview, Architecture, Data Path, Components, HA Options and 2 more sections."
---
# Data Domain — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Architecture, Data Path, Components, HA Options and 2 more sections.

*Applies to: Data Domain DD OS 7.x*
</div>
![Data Domain — How It Works](../../../../../assets/storage-dell-data-domain-architecture-how-it-works.svg)

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

```d2
direction: right

BU: "Backup Servers\nNetBackup / Commvault / Veeam" {shape: rectangle}
DD: "Dell Data Domain\n(dedup + compression" {shape: rectangle}
DDDR: "Remote Data Domain\n(DR copy" {shape: rectangle}
CLOUD: "Cloud Tier\nS3 / Azure Blob — long-term" {shape: rectangle}
VTL: "Virtual Tape Library\n(optional — FC" {shape: rectangle}

BU -> DD
DD -> DDDR
DD -> CLOUD
DD -> VTL
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


```text title="Expected output"
Filesystem Status:
  State: ENABLED

Filesystem Space:
  Pre-compression capacity:  50.2 TB
  Post-compression capacity: 2.4 TB
  Current usage:             1.8 TB

Filesystem Compression:
  Global dedup ratio: 22.1:1
  Compression enabled: yes

Replication Context:
  Context name: dc-repl-01
  State: REPLICATING
  Last sync: 2024-01-15 14:32:18 UTC

DDBoost Clients:
  Host: backup-srv-01.corp.local (10.42.18.55)
  Host: backup-srv-02.corp.local (10.42.18.56)
  Connected clients: 2

Current Alerts:
  CRITICAL: Disk 3.4 predictive failure (SMART threshold exceeded)
  WARNING: Fan module 2 speed degraded to 60%

System Health:
  Fans: 1 of 4 degraded
  Power supplies: OK (2/2 healthy)
  Disks: 1 of 14 at-risk

MTrees:
  mtree1 (quota: 10.0 TB, used: 8.2 TB) - 82% full
  mtree2 (quota: 15.0 TB, used: 3.1 TB) - 21% full
  mtree3 (quota: 8.0 TB, used: 7.9 TB) - 99% full
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: filesystem is DISABLED` | Run `filesys enable` to activate the filesystem before proceeding with replication or backups. |
    | `Error: replication context not found or in FAILED state` | Verify network connectivity between Data Domain systems and check `replication show details` for sync errors. |
    | `Error: MTrees at capacity (quota exceeded)` | Increase MTree quota with `mtree modify <name> -quota <size>` or delete old snapshots to free space. |
---

## See also

- [Data Domain — Design Standards](../design-standards/)
- [Data Domain — Integrations](../integrations/)
