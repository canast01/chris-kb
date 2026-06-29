---
tags:
  - architecture
  - dell
---
# Dell ECS — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Scale-Out Object Storage Topology, Erasure Coding, Virtual Data Centers (VDC), Replication Groups and Geo-Distribution and 3 more sections.

*Applies to: ECS 3.x*
</div>
![Dell ECS — How It Works](../../../../assets/storage-dell-ecs-architecture-how-it-works.svg)

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

actor "S3 / Swift Client" as CLT
participant "ECS Data Node\n(object API)" as DN
participant "Chunk Manager\n(erasure coding)" as CM
participant "Disk\n(local storage)" as DISK
participant "Remote ECS Site\n(geo-replication)" as REMOTE
participant "ECS Portal\n(management)" as MGR

CLT -> DN: PUT object (S3 / Swift)
DN -> CM: Chunk + erasure-code (12+4)
CM -> DISK: Write coded chunks across nodes
DISK --> CM: Confirmed
CM --> DN: Object stored
DN --> CLT: 200 OK + ETag

DN -> REMOTE: Async geo-replication
REMOTE --> DN: Replicated

MGR -> DN: Policy + quota management
@enduml
```

## Overview

Dell ECS (Enterprise Content Storage) is a scale-out, software-defined object storage platform built on commodity x86 nodes. It exposes S3, Swift, Atmos, and CAS APIs over HTTPS. The software stack runs entirely on commodity hardware and provides geo-distribution across sites via Virtual Data Centers (VDCs) linked into replication groups.

## Scale-Out Object Storage Topology

```d2
direction: right

CLT: "S3 / Swift / Atmos Clients" {shape: rectangle}
GW: "Load Balancer\n(optional" {shape: rectangle}
N1: "ECS Node 1" {shape: rectangle}
N2: "ECS Node 2" {shape: rectangle}
N3: "ECS Node 3" {shape: rectangle}
NN: "Node N…" {shape: rectangle}
RING: "Object Ring\ndistributed erasure coding" {shape: rectangle}

CLT -> GW
GW -> N1
N1 -> N2
N2 -> N3
N3 -> NN
NN -> RING
```

## Erasure Coding

ECS uses erasure coding (EC) rather than replication for within-VDC data protection. Objects are broken into data fragments and parity fragments; the cluster reconstructs the original object when a defined number of fragments are lost.

| EC Scheme | Data Fragments | Parity Fragments | Min Nodes | Tolerated Failures |
|---|---|---|---|---|
| 12+4 (default) | 12 | 4 | 16 | Up to 4 simultaneous node/disk failures |
| 10+2 | 10 | 2 | 12 | Up to 2 simultaneous failures |
| 4+2 (small cluster) | 4 | 2 | 6 | Up to 2 simultaneous failures |

The EC scheme is selected automatically based on VDC node count. A 12+4 scheme has a 1.33× raw-to-usable overhead ratio. ECS also reserves ~30% overhead for metadata, journals, and rebuild workspace.

## Virtual Data Centers (VDC)

| Concept | Description |
|---|---|
| VDC | Single-site logical cluster of ECS nodes; independently manageable; serves S3 requests autonomously |
| VDC Quorum | Requires majority of VDC nodes online — `(n/2)+1` for even node counts |
| Temporary Site Failure (TSF) | VDC continues accepting writes locally; queues replication backlog; replays on reconnection |
| VDC Federation | Multiple VDCs peered into one management domain via ECS Portal for cross-VDC replication |

## Replication Groups and Geo-Distribution

Replication groups define which VDCs participate in geo-replication. Every namespace is assigned to a replication group.

| Mode | Consistency | RPO | Use Case |
|---|---|---|---|
| Synchronous | Strong — write confirmed on all VDCs | Near-zero | Compliance, financial records |
| Asynchronous | Eventual — write acknowledged locally; replicated in background | Minutes | General workloads, backup targets |
| Metered | Async with WAN bandwidth throttling | Longer | WAN-constrained environments |

## Namespace and Bucket Hierarchy

![Dell ECS — How It Works — Diagram](../../../../assets/storage-dell-ecs-architecture-how-it-works-diagram.svg)

## Supported API Protocols

| Protocol | Port | Use Case |
|---|---|---|
| S3 | HTTPS 443 / 9021 | General-purpose; primary API; widest client support |
| Swift | HTTPS 9024 | OpenStack integration |
| CAS (Centera) | HTTPS | Fixed-content WORM compliance (legacy EMC Centera migration) |
| HDFS | TCP 9003 | Hadoop/Spark via ECS HDFS connector JAR |
| NFS (ECS 3.8+) | TCP 2049 | POSIX namespace access via NFS gateway |
| Management REST API | HTTPS 4443 | Administration and automation |

## Data Write Path

1. Client sends S3 PUT to the ECS load balancer (or directly to a node)
2. Receiving node acts as the request coordinator
3. Coordinator chunks the object, applies erasure coding, distributes fragments across data nodes
4. Once local write completes, coordinator acknowledges write to client
5. Geo-replication journal records the new object; replication service transmits to peer VDCs

---

## See also

- [Ecs — Design Standards](../design-standards/)
- [Ecs — Integrations](../integrations/)
