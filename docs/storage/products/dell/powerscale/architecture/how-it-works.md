---
tags:
  - architecture
  - dell
description: "How It Works reference covering Overview, Architecture, OneFS Distributed File System, HA and Protection Levels, Node Pool and Tier Architecture and 4..."
---
# PowerScale — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Architecture, OneFS Distributed File System, HA and Protection Levels, Node Pool and Tier Architecture and 4 more sections.

*Applies to: PowerScale (Isilon) 9.x*
</div>
![PowerScale — How It Works](../../../../../assets/storage-dell-powerscale-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "NFS / SMB Client" as CLT
participant "SmartConnect\n(DNS round-robin / zone)" as SC
participant "Chosen Node\n(OneFS)" as NODE
participant "OneFS Distributed\nFile System" as DFS
participant "Backend Disks\n(SSD / HDD)" as DISK
participant "SyncIQ\n(replication)" as SYNC

== 1. Client file read (live, per-request) ==
CLT -> SC: DNS lookup for cluster FQDN
SC --> CLT: IP of least-loaded node
CLT -> NODE: NFS mount / SMB connect
NODE -> DFS: Coordinate with peer nodes
DFS -> DISK: Stripe data across nodes (N+2/N+3)
DISK --> DFS: Data
DFS --> NODE: Serve
NODE --> CLT: File data

== 2. SyncIQ replication (scheduled independently, not triggered by the read above) ==
NODE -> SYNC: Policy-based replication job
SYNC -> NODE: Delta to target cluster
@enduml
```

## Overview

Dell PowerScale (formerly Isilon) is a scale-out NAS platform running the **OneFS** distributed operating system. All nodes in a cluster are peers — there is no dedicated metadata controller. The entire cluster presents a single namespace rooted at `/ifs` across all protocols (NFS, SMB, HDFS, S3, FTP). Clusters scale from a minimum of 3 nodes to 252 nodes.

## Architecture

```d2
direction: right

N1: "Node 1" {shape: rectangle}
N2: "Node 2" {shape: rectangle}
N3: "Node 3" {shape: rectangle}
NN: "Node N…" {shape: rectangle}
INT: "InfiniBand / 100GbE\nInternal Cluster Network" {shape: rectangle}
SC: "SmartConnect\n(DNS-based load balancing" {shape: rectangle}
NFS: "NFS v3/v4 Clients" {shape: rectangle}
SMB: "SMB / CIFS Clients" {shape: rectangle}
HDFS: "HDFS / S3 Clients" {shape: rectangle}

N1 -> N2
N2 -> N3
N3 -> NN
NN -> INT
INT -> SC
SC -> NFS
SC -> SMB
SC -> HDFS
```

## OneFS Distributed File System

OneFS runs identically on every node. There is no primary node or metadata controller — all nodes share metadata, data, and client I/O.

- **Single global namespace**: All data lives under `/ifs`. No volumes, LUNs, or mount points.
- **Distributed metadata**: File metadata (inodes, block maps, directory entries) is erasure-coded and distributed across all nodes — no metadata bottleneck.
- **Distributed locking**: Coherence is maintained via per-I/O node ownership; NFS write caching and SMB oplocks operate within this framework.

## HA and Protection Levels

| Level | Survives | Recommended Use |
|---|---|---|
| N+1 | 1 node or drive failure | Minimum for any production cluster |
| N+2 | 2 simultaneous failures | Standard recommendation for production |
| N+3 | 3 simultaneous failures | High-value data; archive clusters |
| 2x (mirroring) | Any 1 full copy lost | Small clusters or metadata-heavy workloads |

Losing a node triggers **SMARTFAIL** — OneFS rebalances data to remaining nodes. Quorum (strict majority) is required for write operations.

## Node Pool and Tier Architecture

```d2
direction: right

cluster: "OneFS Cluster\n(single /ifs namespace" {shape: rectangle}
poolNVMe: "Node Pool: F-series NVMe\n(all-flash — performance tier" {shape: rectangle}
poolSAS: "Node Pool: H-series Hybrid\n(NVMe + SAS — capacity tier" {shape: rectangle}
poolNLSAS: "Node Pool: A-series NL-SAS\n(high-density — archive tier" {shape: rectangle}
fp: "SmartPools File Policy\n(age / path / type rules" {shape: rectangle}

cluster -> poolNVMe
cluster -> poolSAS
cluster -> poolNLSAS
fp -> poolNVMe
fp -> poolSAS
fp -> poolNLSAS
```

## Components

| Component | Description |
|---|---|
| OneFS Node | Individual server unit with CPU, RAM, and NVMe/SSD/HDD. Every node runs OneFS. |
| SmartPools | Policy-based data tiering; migrates files between node pools based on access time or custom criteria. |
| Access Zones | Virtual NAS partitions; each zone has its own IP pool, auth provider, and share namespace. |
| SmartConnect | DNS-based load balancing; distributes client connections across node IPs within a zone. |
| SyncIQ | Asynchronous replication engine; replicates directories to a remote PowerScale cluster. |
| SnapshotIQ | Per-directory point-in-time snapshots stored within `/ifs/.snapshot/`. |
| SmartQuotas | Per-directory or per-user capacity quotas with advisory, soft, and hard thresholds. |
| CloudPools | Tiers cold data to object stores (AWS S3, Azure Blob, ECS) as a transparent extension of `/ifs`. |

## Connectivity

| Protocol | Port | Notes |
|---|---|---|
| NFS v3/v4 | TCP/UDP 2049 | Primary Unix/Linux protocol; per access zone |
| SMB 2.x/3.x | TCP 445 | Windows file sharing; per access zone |
| S3 | TCP 9020/9021 | Object API; per access zone |
| HDFS | TCP 8020 | Hadoop; maps `/ifs` paths as HDFS volumes |
| Management API (PAPI) | TCP 8080/8081 | REST API for automation |
| SyncIQ replication | TCP 7722 | Cluster-to-cluster replication traffic |
| SSH | TCP 22 | CLI access; restrict to management VLAN |

## Node Hardware Families

| Family | Storage Type | Primary Use Case |
|---|---|---|
| F-series (F600, F900) | All-NVMe SSD | High-IOPS workloads: EDA, genomics, databases |
| H-series (H700, H7000) | NVMe + SAS HDD hybrid | Mixed workloads: home directories, general NAS |
| A-series (A300, A3000) | NL-SAS (high-density) | Archive and cold data; long-term retention |

## Key CLI Commands

```bash
isi status                    # cluster node and drive health
isi event list                # active events — filter for CRITICAL
isi storagepool list          # capacity per tier
isi sync policies list        # SyncIQ policy status
isi quota list                # quota violations
isi network pools list        # SmartConnect zone config
isi job list                  # background jobs (Restripe, FlexProtect)
```


```text title="Expected output"
Cluster Status:
  Nodes: 6 (all online)
  Drives: 48 (47 healthy, 1 rebuilding)
  CPU: 45% | Memory: 62% | Network: 12%

Events (Last 24h):
  WARNING: Node-3 disk temperature elevated (52°C)
  INFO: SyncIQ policy 'DR-Chicago' completed 2.3TB in 4h 22m

Storage Pools:
  Tier: SSD-NVMe    Capacity: 12.4TB / 15TB (82%)
  Tier: SAS-7.2k    Capacity: 287TB / 320TB (89%)
  Tier: NL-SAS      Capacity: 1.2PB / 1.4PB (86%)

SyncIQ Policies:
  dr-chicago       RUNNING    Last: 2024-01-15 03:22:14    Next: 2024-01-16 03:00:00
  backup-denver    IDLE       Last: 2024-01-14 22:15:03    Next: 2024-01-15 22:00:00

Quotas:
  /ifs/projects/media    EXCEEDED (1.2TB / 1TB)
  /ifs/home/jsmith       WARNING (890GB / 1TB)

Network Pools:
  zone-prod-east    10.42.1.0/24    SmartConnect: enabled
  zone-prod-west    10.42.2.0/24    SmartConnect: enabled

Jobs:
  FlexProtect-Node2    RUNNING    45% complete    ETA: 2h 18m
  Restripe-Tier2       IDLE       Last: 2024-01-14 18:30:00
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `isi: command not found` | Ensure you are logged into the PowerScale cluster via SSH or the OneFS CLI is installed in your PATH. |
    | `Error: Permission denied` | Verify your user account has cluster administrator or read-only admin privileges via `isi auth roles view`. |
    | `Connection refused on port 8080` | Confirm the cluster management interface is accessible and OneFS services are running with `isi_services_status`. |
---

## See also

- [Powerscale — Design Standards](../design-standards/)
- [Powerscale — Integrations](../integrations/)
- [Powerscale — Deploy](../../deploy/)
