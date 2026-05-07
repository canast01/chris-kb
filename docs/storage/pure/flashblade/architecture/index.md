# FlashBlade Architecture
## Overview

Pure Storage FlashBlade is a scale-out all-flash storage platform running Purity//FB OS, purpose-built for unstructured data workloads: AI/ML training data, analytics, high-performance computing, backup repositories, and large-scale file storage. The design philosophy differs fundamentally from FlashArray — rather than a fixed dual-controller appliance, FlashBlade is a disaggregated scale-out architecture where both compute and flash capacity scale together by adding blades to a chassis.

Each FlashBlade blade is an independent storage node containing its own NVMe flash and compute resources. The chassis hosts multiple blades plus Fabric Modules (FMs) that provide the high-speed internal interconnect. This architecture delivers consistently high aggregate throughput regardless of the access pattern — critical for workloads like GPU training jobs that demand tens of GB/s of sustained bandwidth.

FlashBlade serves multiple protocols natively from a single platform without any protocol gateway: NFS v3/v4.1, SMB 2/3, S3 object, and HDFS, all from the same filesystem or object store namespace.


## Scale-Out Blade Architecture

```
  ┌──────────────────────────────────────────────────────────────────────────┐
  │                     FlashBlade Chassis (17U)                             │
  │                                                                          │
  │  ┌─────────────────────────────────────────────────────────────────┐    │
  │  │  Fabric Management Module (FMM)  /  Blade Mgmt Module (BMM)     │    │
  │  │  NVMe-oF internal fabric  |  Out-of-band management plane       │    │
  │  └─────────────────────────────────────────────────────────────────┘    │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
  │  │ Blade 01 │ │ Blade 02 │ │ Blade 03 │ │  ...     │ │ Blade 15 │     │
  │  │ CPU+NVMe │ │ CPU+NVMe │ │ CPU+NVMe │ │          │ │ CPU+NVMe │     │
  │  │ 17 / 52T │ │ 17 / 52T │ │ 17 / 52T │ │          │ │ 17 / 52T │     │
  │  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
  │       └────────────┴────────────┴─────────────┴────────────┘           │
  │                         internal NVMe-oF fabric                        │
  └──────────────────────────────┬──────────────────────────────────────────┘
                                 │  10 / 25 / 100 GbE
               ┌─────────────────▼───────────────────────┐
               │  Ethernet Fabric (leaf-spine)            │
               │  NFS v3/v4.1  |  S3  |  SMB  |  NFS/S3  │
               └────────────────┬────────────────────────┘
                                │
        ┌───────────────────────▼────────────────────────────┐
        │  Clients                                            │
        │  GPU nodes (AI/ML)  Hadoop  Backup  Analytics       │
        └─────────────────────────────────────────────────────┘
  Scale: 1 to 15 blades per chassis, up to 20 chassis in a cluster
```

## Components

| Component | Description |
|---|---|
| Blades | Individual storage nodes within the chassis; each blade contains NVMe flash and dedicated compute; capacity scales by adding blades |
| Fabric Modules (FM) | Internal high-speed interconnect cards in the chassis; redundant FMs provide fault tolerance; all blades communicate through the FMs |
| Chassis | Physical enclosure holding up to 15 blades (//S) or 10 blades (//E series) plus Fabric Modules, power supplies, and management hardware |
| Purity//FB OS | Operating system running across all blades; manages data services including deduplication, compression, snapshots, replication, and protocol serving |
| Pure1 cloud management | SaaS monitoring, capacity forecasting, upgrade scheduling, and AI analytics — same platform as FlashArray |
| ActiveDR | Asynchronous replication for filesystems and object store to a remote FlashBlade for disaster recovery |
| ActiveCluster (FB) | Synchronous replication for filesystems between two FlashBlade arrays for zero-RPO failover (Purity//FB 4.x+) |
| SafeMode snapshots | Immutable, admin-delete-locked snapshots for ransomware protection |

## HA Topology

FlashBlade does not use a dual-controller model. High availability is achieved through blade-level redundancy and Fabric Module redundancy within the chassis:

- **Blade redundancy:** Data is distributed (striped and replicated) across multiple blades within the chassis; a single blade failure causes no data loss and only a proportional reduction in capacity and performance while the array rebalances
- **Fabric Module redundancy:** Two FMs per chassis provide redundant internal connectivity; an FM failure does not interrupt access to data
- **Power and cooling:** Dual redundant power supplies and fan trays; each connects to separate PDUs

**Failover behaviour for blade failure:**

1. Purity//FB detects the blade failure and marks it as unavailable
2. Data striped across the failed blade is reconstructed from parity/replicas on surviving blades (similar to RAID rebuild)
3. Performance and capacity are reduced during rebuild; NFS, SMB, S3, and HDFS client access continues uninterrupted
4. Insert a replacement blade; Purity//FB automatically rebalances data across the new blade

**Protocol service HA:**

- Each FlashBlade presents a virtual IP (VIP) per protocol service; VIPs float across blades automatically if a blade fails
- NFS and SMB clients reconnect automatically to the new VIP host when their session reconnects
- S3 clients use the FlashBlade's S3 endpoint VIP; no client reconfiguration is needed on blade failure

## Connectivity

| Protocol | Standard | Notes |
|---|---|---|
| NFS v3 | NFSv3 over TCP/UDP | Widely supported; suitable for Linux clients and HPC workloads |
| NFS v4.1 | NFSv4.1 over TCP | Stateful; supports pNFS for parallel access from multiple clients; recommended for AI/ML |
| SMB 2.0 / 3.0 | SMB over TCP | Windows file sharing; SMB 3.0 supports encryption and multichannel |
| S3 (object) | S3-compatible REST API | Bucket/object model; compatible with AWS S3 SDK, Boto3, and most S3 clients |
| HDFS | HDFS-over-IP | Compatible with Hadoop/Spark workloads without a dedicated Hadoop cluster |

**Network requirements:**

- Data interfaces: 10 GbE minimum; 25 GbE or 100 GbE recommended for AI/ML and high-throughput workloads
- Replication interface: dedicated 10 GbE or 25 GbE interface on a separate VLAN for ActiveDR/ActiveCluster replication traffic
- Management interface: dedicated 1 GbE; accessible from admin hosts and Pure1 cloud
- Jumbo frames (MTU 9000) are recommended end-to-end for NFS and S3 data networks to maximise throughput
- Pure1 phone-home: outbound HTTPS (port 443) to `*.purestorage.com`

## Sizing Guidelines

| Dimension | Guidance |
|---|---|
| Minimum blades | 3 blades minimum for production redundancy (parity can tolerate 1 blade loss) |
| Scale-out | Add blades in the same chassis up to the chassis maximum; add chassis for larger deployments |
| Per-blade capacity | Varies by blade model: FlashBlade//S 500 = 500 TB usable per blade |
| Aggregate throughput | Scales linearly with blades — each blade adds to the aggregate bandwidth; a 10-blade FlashBlade//S delivers 90+ GB/s aggregate |
| NFS/S3 client count | Hundreds to thousands of concurrent NFS or S3 clients; no hard per-protocol client limit in Purity//FB |
| Maximum filesystem size | Up to 4 PB per filesystem (configuration-dependent) |
| S3 bucket limits | No hard limit on bucket count; object count scales to billions per bucket |
| Data reduction | Inline deduplication and compression; typical backup workloads achieve 2:1–3:1; AI/ML raw data workloads are typically 1:1 (incompressible) |
