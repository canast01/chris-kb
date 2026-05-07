# FlashArray Architecture
## ActiveCluster Topology

```mermaid
graph LR
  H1(["ESXi-01"]) & H2(["ESXi-02"]) --> FabA["FC Fabric A"] & FabB["FC Fabric B"]
  H3(["ESXi-03"]) & H4(["ESXi-04"]) --> FabA & FabB
  FabA & FabB --> FA_A["FlashArray Site A\nCT0 · CT1"]
  FabA & FabB --> FA_B["FlashArray Site B\nCT0 · CT1"]
  FA_A <-->|"ActiveCluster\nsync replication"| FA_B
  FA_A & FA_B -.->|"heartbeat"| MED(["Purity Mediator"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef med fill:#b45309,stroke:#92400e,color:#fff
  class FA_A,FA_B ctrl
  class FabA,FabB net
  class H1,H2,H3,H4 host
  class MED med
```

## Overview

Pure Storage FlashArray is an all-flash block storage platform running Purity//FA OS. It is purpose-built for block workloads — databases, virtualisation, and latency-sensitive applications — and is designed around three core principles: all-flash always (no spinning disk tiering), active-active dual-controller high availability with no single point of failure, and non-disruptive operations including upgrades, hardware replacement, and capacity expansion.

FlashArray ships in three product lines:

- **//X series** — NVMe-based, highest performance; targets Tier-1 databases and NVMe/FC or NVMe/RoCE workloads
- **//C series** — QLC NAND, capacity-optimised; targets secondary workloads, backup staging, and dev/test at lower cost per TB
- **//E series** — Maximum density with high-capacity QLC drives; targets large-scale consolidation at the lowest $/TB

All models share the same Purity//FA OS, the same CLI and REST API surface, and the same operational model.

## Components

| Component | Description |
|---|---|
| Controllers (CT0, CT1) | Two active-active controllers sharing ownership of all volumes; each runs a full Purity//FA instance |
| NVMe drives / SAS SSDs | Flash media carrying user data and Purity metadata; drives are direct-attached inside the chassis |
| Purity//FA OS | The operating system managing data services: deduplication, compression, thin provisioning, snapshots, and replication |
| Fabric modules (//X) | NVMe-oF fabric connectivity cards in the //X series providing NVMe/FC, NVMe/RoCE, and NVMe/TCP host ports |
| Host interface cards | FC (16/32 Gb), iSCSI (10/25 GbE), or NVMe/TCP (25/100 GbE) adapters in the I/O module bays |
| Replication / management ports | Dedicated 10 GbE ports for inter-array replication, management access, and Pure1 phone-home |
| Pure1 cloud management | SaaS monitoring, AI analytics, capacity planning, and upgrade scheduling; no on-premises management VM required |
| SafeMode snapshots | Immutable, admin-delete-locked snapshot capability for ransomware protection |

## HA Topology

```
  ┌─────────────────────────────────────────────────────────────────────┐
  │                     FlashArray Chassis                              │
  │                                                                     │
  │  ┌────────────────────┐  NVMe fabric  ┌────────────────────┐       │
  │  │     CT0            ├───────────────┤     CT1            │       │
  │  │  (Controller 0)    │  mirror/sync  │  (Controller 1)    │       │
  │  │                    │               │                    │       │
  │  │  FC / iSCSI / NVMe │               │  FC / iSCSI / NVMe │       │
  │  └─────────┬──────────┘               └──────────┬─────────┘       │
  │            │                                     │                 │
  │  ┌─────────▼─────────────────────────────────────▼─────────┐       │
  │  │                    NVMe / SSD Drive Shelf                │       │
  │  └──────────────────────────────────────────────────────────┘       │
  └──────────────┬────────────────────────────────┬────────────────────┘
                 │ FC / NVMe-oF / iSCSI            │ FC / NVMe-oF / iSCSI
        ┌────────▼────────┐                ┌───────▼─────────┐
        │   FC Switch A   │                │   FC Switch B   │
        │  (Fabric A)     │                │  (Fabric B)     │
        └────────┬────────┘                └───────┬─────────┘
                 │                                 │
         ┌───────▼──────────────────────────────────▼──────┐
         │  ESXi-01   ESXi-02   DB-01   DB-02   APP-01     │
         │   HBA0      HBA0     HBA0    HBA0    HBA0       │
         │   HBA1      HBA1     HBA1    HBA1    HBA1       │
         │  (Fabric A) paths ──── (Fabric B) paths         │
         └─────────────────────────────────────────────────┘
                         Host Layer (MPIO / ALUA)
```

FlashArray operates in an active-active dual-controller configuration. Both CT0 and CT1 serve host I/O simultaneously — there is no standby controller. Volume ownership is distributed across both controllers, and load balancing occurs automatically via ALUA (Asymmetric Logical Unit Access).

**Failover behaviour:**

1. If one controller fails (hardware fault, NDU restart, or Purity upgrade), the surviving controller takes ownership of all volumes within seconds.
2. Hosts with proper multipathing (at least two active paths, one to each controller) experience no I/O interruption — the multipath driver promotes the surviving paths immediately.
3. The failed controller reboots automatically and rejoins the active-active pair once healthy; volume ownership rebalances back.
4. There is no manual intervention required for controller failover or rejoin under normal circumstances.

**Requirements for zero-impact failover:**

- Every host must have at least two host bus adapters (HBAs) or NICs connected to the array, one per controller
- Fabric zoning (FC) or iSCSI network design must ensure paths reach both CT0 and CT1
- Host multipath driver (e.g., HPE 3PAR MPIO, native MPIO on Windows, DM-Multipath on Linux) must be active and configured for ALUA

## Connectivity

| Protocol | Media | Port Speed | Notes |
|---|---|---|---|
| FC | Fibre Channel | 16 Gb / 32 Gb | Traditional SAN fabric; requires FC switches and zoning |
| iSCSI | Ethernet | 10 GbE / 25 GbE | IP-SAN; jumbo frames (MTU 9000) recommended |
| NVMe/FC | Fibre Channel | 32 Gb | NVMe-oF over FC fabric; requires NVMe-capable HBAs and FC switches |
| NVMe/RoCE | Ethernet (RoCE v2) | 25 GbE / 100 GbE | NVMe-oF over RDMA-capable Ethernet; requires RoCE-capable NICs and switches |
| NVMe/TCP | Ethernet | 25 GbE / 100 GbE | NVMe-oF over standard TCP/IP; no special fabric requirements |

**Network requirements:**

- Management network: dedicated 1 GbE or 10 GbE; accessible from admin workstations and Pure1 cloud
- Replication network: 10 GbE minimum; dedicated VLAN recommended for ActiveCluster and async replication traffic
- iSCSI data network: MTU 9000 (jumbo frames) end-to-end including host NICs and switch uplinks
- Pure1 phone-home: outbound HTTPS (port 443) to `*.purestorage.com`; can traverse a proxy

## Sizing Guidelines

| Dimension | Guidance |
|---|---|
| Usable capacity | Account for effective capacity after deduplication and compression — Pure1 provides a workload-specific data reduction estimate; typical all-flash workloads achieve 3:1 to 5:1 effective |
| Raw drive capacity | Size raw capacity so that after a single drive failure and rebuild, usable headroom remains above 70% |
| IOPS | FlashArray //X: up to 2M+ IOPS per array depending on model; verify per-model datasheet for your workload block size |
| Latency | Sub-millisecond (typically 100–300 µs) for random 4K reads at normal utilisation; NVMe//X models achieve sub-100 µs |
| Maximum volumes | Up to 500,000 volumes per array depending on model |
| Maximum hosts | Up to 10,000 host entries per array |
| ActiveCluster | Maximum 5 ms round-trip time between arrays for synchronous replication |
| Controller upgrade | Evergreen controller upgrades do not require capacity changes — data stays in place |
