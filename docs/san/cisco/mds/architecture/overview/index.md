# MDS — Overview

> Part of the [Cisco MDS](../../) reference.

---

## Cisco MDS Fabric Topology

```mermaid
graph TB
  H1A(["esxi-01  HBA0"]) --> MDSA["MDS-9710 Director A\n2× 48p 32Gb FC"]
  H2A(["esxi-02  HBA0"]) --> MDSA
  H1B(["esxi-01  HBA1"]) --> MDSB["MDS-9710 Director B\n2× 48p 32Gb FC"]
  H2B(["esxi-02  HBA1"]) --> MDSB

  MDSA <-->|"4× 100G ISL"| MDSB

  MDSA --> FA_CT0[("FlashArray CT0")]
  MDSA --> PM_A[("PowerMax Dir A")]
  MDSA --> NA_N1[("NetApp AFF Node 1")]
  MDSB --> FA_CT1[("FlashArray CT1")]
  MDSB --> PM_B[("PowerMax Dir B")]
  MDSB --> NA_N2[("NetApp AFF Node 2")]

  classDef switch fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef storage fill:#7c3aed,stroke:#6d28d9,color:#fff

  class MDSA,MDSB switch
  class H1A,H2A,H1B,H2B host
  class FA_CT0,PM_A,NA_N1,FA_CT1,PM_B,NA_N2 storage
```

## Overview

Cisco MDS 9000 series switches run NX-OS and provide scalable SAN fabric services supporting Fibre Channel (FC) and FCoE. The core isolation mechanism is the **VSAN (Virtual SAN)** — multiple logical fabrics share physical infrastructure while maintaining separate name servers, zoning databases, and fabric login tables. Each VSAN operates as an independent fabric.

---

## Platform Reference

| Model | Type | Max FC Ports | Notes |
|---|---|---|---|
| MDS 9132T | Fixed | 32x 32G FC | Entry/mid-range |
| MDS 9148T | Fixed | 48x 32G FC | Mid-range |
| MDS 9396T | Fixed | 96x 32G FC | High-density fixed |
| MDS 9706 | Director | Up to 384 FC | Modular director |
| MDS 9710 | Director | Up to 576 FC | Large-scale director |

Directors (9706/9710) support ISSU (In-Service Software Upgrade), making them the preferred platform for environments requiring zero-downtime maintenance.

---

## Fabric Design

Typical enterprise deployment uses a **dual-fabric** architecture — each host HBA port connects to a separate switch, with storage targets dual-homed across both fabrics. A failure of one fabric does not impact the other.

Each fabric is completely independent — a failure of one fabric does not impact the other. All hosts and storage targets are connected to both fabrics for redundancy.

**ISLs (Inter-Switch Links):** Used when multiple MDS switches form a fabric. ISLs are configured as port-channel trunks (minimum 2 links). All VSANs allowed on the ISL must be explicitly permitted.

---

## VSAN Design

VSANs segment the fabric logically. Common VSAN allocation:

| VSAN | Purpose | Fabric A | Fabric B |
|---|---|---|---|
| Production | ESXi hosts → storage | 10 | 11 |
| Replication | SRDF/A or SnapMirror | 20 | 21 |
| Management | Out-of-band fabric mgmt | 99 | 99 |

```mermaid
graph TB
  subgraph "Physical MDS Switch"
    subgraph vsan10 ["VSAN 10 — Production (Fabric A)"]
      V10NS["FC Name Server"]
      V10Z["Zone DB"]
      V10D["Domain ID: 1"]
    end
    subgraph vsan20 ["VSAN 20 — Replication (Fabric A)"]
      V20NS["FC Name Server"]
      V20Z["Zone DB"]
      V20D["Domain ID: 2"]
    end
    subgraph vsan99 ["VSAN 99 — Management"]
      V99NS["FC Name Server"]
      V99Z["Zone DB"]
      V99D["Domain ID: 3"]
    end
  end

  H1["ESXi Host\n(HBA0 — fc1/1)"] -->|"VSAN 10"| vsan10
  SA["FlashArray CT0\n(fc1/8)"] -->|"VSAN 10"| vsan10
  SRDF1["PowerMax FA Dir A\n(fc1/9)"] -->|"VSAN 20"| vsan20
  SRDF2["PowerMax FA Dir B\n(fc1/10)"] -->|"VSAN 20"| vsan20

  classDef vsanBox fill:#1e3a5f,stroke:#3b82f6,color:#e0f2fe
  classDef device fill:#15803d,stroke:#166534,color:#fff
  classDef storage fill:#7c3aed,stroke:#6d28d9,color:#fff
  class vsan10,vsan20,vsan99 vsanBox
  class H1 device
  class SA,SRDF1,SRDF2 storage
```

Each VSAN has its own:
- FC Name Server (FCNS)
- Domain ID space
- Zone database
- FLOGI/PLOGI table

VSAN 1 is the default VSAN — do not use VSAN 1 for production; all production traffic should be in dedicated VSANs.

---

## FC Services

| Service | Function |
|---|---|
| FCNS (Name Server) | Registers all devices (hosts and storage) that FLOGI into the fabric |
| FSPF | Fabric Shortest Path First — routing protocol for FC fabrics |
| FLOGI DB | Records all fabric login events (WWN, FCID, port) |
| Zoning | Controls which initiators can communicate with which targets |

```mermaid
sequenceDiagram
  participant HBA as Host HBA
  participant SW as MDS Switch
  participant NS as FC Name Server
  participant TGT as Storage Target

  HBA->>SW: FLOGI (Fabric Login)<br/>sends WWPN + WWNN
  SW-->>HBA: FLOGI Accept<br/>assigns FCID (3-byte address)
  HBA->>NS: PLOGI to Name Server (0xFFFFFC)<br/>registers port type, WWPN, FCID
  NS-->>HBA: LS_ACC (registration accepted)
  HBA->>NS: GNN_FT / GID_FT<br/>query targets in VSAN
  NS-->>HBA: Return list of target FCIDs
  HBA->>TGT: PLOGI (Port Login)<br/>establish session
  TGT-->>HBA: PLOGI Accept
  HBA->>TGT: PRLI (Process Login)<br/>negotiate SCSI / NVMe service
  TGT-->>HBA: PRLI Accept — I/O ready
```

**Key commands:**

```bash
# Show all devices logged into a VSAN
show fcns database vsan 10

# Show all FLOGI entries
show flogi database

# Show fabric shortest path
show fspf database vsan 10

# Show port status
show interface fc1/1
```
