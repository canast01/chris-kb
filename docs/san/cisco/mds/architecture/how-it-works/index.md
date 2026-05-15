# Cisco MDS — How It Works

## Overview

Cisco MDS 9000 series switches run NX-OS and provide scalable SAN fabric services supporting Fibre Channel (FC). The core isolation mechanism is the **VSAN (Virtual SAN)** — multiple logical fabrics share physical infrastructure while maintaining separate name servers, zoning databases, and fabric login tables. Each VSAN operates as an independent fabric.

## SAN Fabric Topology

```mermaid
graph TB
  H1A(["esxi-01 HBA0"]) --> MDSA["MDS-9710 Director A\n2× 48p 32Gb FC"]
  H2A(["esxi-02 HBA0"]) --> MDSA
  H1B(["esxi-01 HBA1"]) --> MDSB["MDS-9710 Director B\n2× 48p 32Gb FC"]
  H2B(["esxi-02 HBA1"]) --> MDSB
  MDSA <-->|"4× 100G ISL"| MDSB
  MDSA --> FA_CT0[("FlashArray CT0")]
  MDSA --> PM_A[("PowerMax Dir A")]
  MDSB --> FA_CT1[("FlashArray CT1")]
  MDSB --> PM_B[("PowerMax Dir B")]
  classDef switch fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef storage fill:#7c3aed,stroke:#6d28d9,color:#fff
  class MDSA,MDSB switch
  class H1A,H2A,H1B,H2B host
  class FA_CT0,PM_A,FA_CT1,PM_B storage
```

## Platform Reference

| Model | Type | Max FC Ports | Notes |
|---|---|---|---|
| MDS 9132T | Fixed | 32× 32G FC | Entry/mid-range |
| MDS 9148T | Fixed | 48× 32G FC | Mid-range |
| MDS 9396T | Fixed | 96× 32G FC | High-density fixed |
| MDS 9706 | Director | Up to 384 FC | Modular director |
| MDS 9710 | Director | Up to 576 FC | Large-scale director |

Directors (9706/9710) support ISSU (In-Service Software Upgrade) — preferred for zero-downtime maintenance.

## VSAN Design

VSANs segment the fabric logically. Each VSAN has its own FC Name Server, domain ID space, zone database, and FLOGI/PLOGI table.

| VSAN | Purpose | Fabric A | Fabric B |
|---|---|---|---|
| Production | ESXi hosts → storage | 10 | 11 |
| Replication | SRDF/A or SnapMirror | 20 | 21 |
| Management | Out-of-band fabric management | 99 | 99 |

VSAN 1 is the default — do not use VSAN 1 for production; all production traffic must use dedicated VSANs.

## FC Services

| Service | Function |
|---|---|
| FCNS (Name Server) | Registers all devices (hosts and storage) that FLOGI into the fabric |
| FSPF | Fabric Shortest Path First — routing protocol for FC fabrics |
| FLOGI DB | Records all fabric login events (WWN, FCID, port) |
| Zoning | Controls which initiators can communicate with which targets |

## Fabric Login Sequence

When a host HBA connects:
1. HBA sends **FLOGI** → switch assigns FCID (3-byte address)
2. HBA sends **PLOGI** to Name Server (0xFFFFFC) → registers WWPN and FCID
3. HBA queries **GNN_FT / GID_FT** → Name Server returns list of target FCIDs
4. HBA sends **PLOGI** to each target → establishes session
5. HBA sends **PRLI** → negotiates SCSI/NVMe service — I/O ready

## Key Commands

```bash
show fcns database vsan 10    # all devices logged into VSAN 10
show flogi database           # all FLOGI entries
show fspf database vsan 10    # fabric shortest path
show interface fc1/1          # port status
```
