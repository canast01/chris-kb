# Dell PowerMax — How It Works


<div class="kb-summary">
Internal architecture and data-path reference: Director architecture, Global Cache, SRDF replication, storage resource management, host connectivity, and Unisphere management.
</div>

## Architecture Overview

PowerMax is Dell's flagship enterprise all-NVMe storage array, purpose-built for mission-critical tier-1 workloads including mainframe, OLTP databases, ERP platforms, and financial transaction systems. It uses a massively parallel director-based architecture: multiple independent processing boards (Directors) share access to a large global DRAM cache and back-end NVMe flash drives.

Two models are available:

| Model | Max Engines | Max Raw Capacity | Target Workload |
|---|---|---|---|
| PowerMax 2500 | 2 engines | ~4 PB | Mid-enterprise; tier-1 databases |
| PowerMax 8500 | 8 engines | ~9 PB | Large enterprise; SRDF metro clusters, mainframe |

The Hypermax OS runs on all director boards simultaneously. There is no single master controller — every director is a fully active processing node sharing the same global state through the crossbar interconnect and global cache. This architecture delivers millions of IOPS at sub-millisecond latency without creating bottlenecks at a centralised controller.

## Director Architecture

Directors are the compute and I/O processing units inside a PowerMax engine. Each engine contains at least two director boards, and all directors share a common crossbar interconnect to reach global cache and the back-end NVMe drives.

There are three classes of directors, each with a distinct role:

**Front-End (FA) Directors**

Front-end directors face the host network. They terminate host I/O sessions and pass data into global cache.

- Connect to hosts via FC (32 Gb/s), iSCSI (25 GbE), NVMe/FC, or FICON (mainframe)
- Each FA director hosts multiple host-facing ports; zoning and masking views are applied here
- ALUA path states are managed per FA director port — preferred and non-preferred paths are defined in Masking Views

**Back-End (DA) Directors**

Back-end directors face the NVMe flash drives. They move data between global cache and the physical flash media.

- Connect to NVMe drive bays via a direct PCIe fabric
- Manage RAID protection (RAID-5 3+1, RAID-6 6+2 or 8+2) across NVMe drives
- Execute destage operations — moving dirty write data from global cache to NVMe drives during idle periods and continuously under load

**RDF Directors (RA)**

RDF directors handle SRDF replication traffic between PowerMax arrays.

- Connect to remote PowerMax arrays via dedicated FC or IP links
- All SRDF replication traffic is isolated to RA director ports — it does not compete with host I/O on FA director ports
- Each SRDF group (RDF group) is bound to a specific pair of RA directors at source and target

## Global Cache

The global cache is a large DRAM memory pool shared by all directors in the array. It acts as the staging area for all reads and writes.

Key properties:

- Size ranges from tens of GB to over 2 TB depending on model and configuration
- All host writes land in global cache first; the host ACK is returned after the write is in cache and mirrored to the peer director's cache — not after it is written to NVMe drives
- All reads are checked in global cache first; a cache hit avoids a back-end NVMe read entirely, reducing latency to DRAM speeds (microseconds)
- Write data in global cache is destaged to NVMe drives by back-end directors asynchronously; destage policy is managed by the Dynamic Cache Management (DCM) subsystem
- Cache is RAID-1 mirrored across directors within the same engine — a single director failure does not cause data loss

**Vault protection:** In the event of a power failure, PowerMax uses battery-backed NVRAM to safely flush the contents of global cache to a dedicated vault area on the NVMe drives. On power restoration, the array replays the vault log and restores the cache to its pre-failure state before accepting new host I/O.

## Mermaid Diagram: I/O Architecture

```mermaid
flowchart LR
    subgraph HOSTS["Host Layer"]
        H1["Production Hosts\nOracle / SQL / SAP\nFC / iSCSI / FICON"]
    end

    subgraph FEDIR["Front-End Directors"]
        FA1["FA Director A\nFC / iSCSI ports\nMasking Views"]
        FA2["FA Director B\nFC / iSCSI ports\nMasking Views"]
    end

    subgraph CACHE["Global Cache"]
        GC["DRAM Cache\nTens–hundreds of GB\nRAID-1 across directors\nVault on power loss"]
    end

    subgraph BEDIR["Back-End Directors"]
        DA1["DA Director A\nNVMe drive control\nRAID-5/6 protection"]
        DA2["DA Director B\nNVMe drive control\nRAID-5/6 protection"]
    end

    subgraph NVME["NVMe Flash"]
        DRV["NVMe Drive Bays\neTLC / SCM\nRAID protected"]
    end

    subgraph SRDF["SRDF Replication"]
        RA1["RA Director A\nRDF Group links"]
        RA2["RA Director B\nRDF Group links"]
    end

    REMOTE["Remote PowerMax\nSRDF/S or SRDF/A target"]

    H1 -->|"FC / iSCSI host I/O"| FA1
    H1 -->|"FC / iSCSI host I/O"| FA2
    FA1 --> GC
    FA2 --> GC
    GC --> DA1
    GC --> DA2
    DA1 --> DRV
    DA2 --> DRV
    GC --> RA1
    GC --> RA2
    RA1 -->|"SRDF/S or SRDF/A\nRDF protocol over FC or IP"| REMOTE
    RA2 -->|"SRDF/S or SRDF/A"| REMOTE

    classDef host fill:#1d4ed8,stroke:#1e3a8a,color:#fff
    classDef dir fill:#15803d,stroke:#14532d,color:#fff
    classDef cache fill:#15803d,stroke:#14532d,color:#fff
    classDef nvme fill:#b45309,stroke:#92400e,color:#fff
    classDef srdf fill:#7c3aed,stroke:#5b21b6,color:#fff

    class H1 host
    class FA1,FA2,DA1,DA2 dir
    class GC cache
    class DRV nvme
    class RA1,RA2,REMOTE srdf
```

## SRDF Replication

SRDF (Symmetrix Remote Data Facility) is PowerMax's native replication protocol, used for disaster recovery and metro high availability. SRDF operates at the volume (device) level — individual devices or groups of devices are paired between a source (R1) and a target (R2) PowerMax.

**SRDF/S — Synchronous**

- Every host write to an R1 device is immediately mirrored to the R2 device on the remote PowerMax before the ACK is returned to the host
- RPO = 0 — no data can be lost at the R2 site if the R1 site fails
- RTO depends on the failover procedure, but R2 data is always fully current
- Requires low-latency network between sites — typically <10 ms RTT; higher latency degrades host write response time directly
- Best suited for metro distances (same city or campus)

**SRDF/A — Asynchronous**

- Writes are buffered at the R1 site and transmitted to R2 in periodic delta sets (typically every 15–30 seconds)
- RPO = the delta set cycle time — typically less than 30 seconds for configured workloads
- R2 data lags R1 by one delta set; the lag is consistent and monitored
- No latency impact on host writes — the host ACK does not wait for R2 confirmation
- Suitable for any network distance, including intercontinental replication

**SRDF pair states:**

| State | Meaning |
|---|---|
| Synchronized | Normal SRDF/S state — R1 and R2 are in sync |
| Consistent | Normal SRDF/A state — R2 consistent, receiving delta sets |
| Synchronizing | Data transfer in progress — catching up after a pause |
| Suspended | SRDF link paused; writes queuing on R1 |
| Partitioned | Network connectivity lost between R1 and R2 |
| Failed Over | R2 is read-write; R1 is not ready — post-failover state |

## Storage Resource Management

PowerMax organises storage through a hierarchy of logical constructs:

```text
Physical NVMe Drives
    └── Storage Resource Pool (SRP)
          └── Storage Group (SG)
                └── Thin Devices (TDEVs)
                      └── Masking View → Host
```

**Thin Devices (TDEVs):** The logical block devices presented to hosts. TDEVs are thin-provisioned — physical capacity is allocated from the SRP only as data is written. A TDEV can be presented as much larger than the physical capacity available.

**Storage Groups (SGs):** A named container grouping one or more TDEVs together. Service Levels (Diamond, Platinum, Gold, Silver, Bronze) are applied at the SG level to set performance expectations enforced by DPTM (Dynamic Performance and Tiering Management).

**Storage Resource Pools (SRPs):** Aggregate the physical NVMe drive capacity. All TDEVs draw physical capacity from an SRP. In models with mixed media (NVMe + SCM), FAST (Fully Automated Storage Tiering) automatically migrates hot data to the faster tier and cold data to the denser tier.

**Masking Views:** Define the access relationship between a host, a port group (set of FA director ports), and a storage group. A Masking View is what causes a TDEV to appear as a block device on a specific host — without a Masking View, no host can see any device, regardless of zoning.

## Host Connectivity

PowerMax supports a wide range of host protocols, all serviced through Front-End Directors.

| Protocol | Speed | Notes |
|---|---|---|
| Fibre Channel | 32 Gb/s | Standard for enterprise block; dual-fabric zoning required |
| iSCSI | 25 GbE | IP SAN; requires dedicated network or VLAN |
| NVMe/FC | 32 Gb/s | NVMe over FC; lowest host-visible latency |
| NVMe/TCP | 25 GbE+ | NVMe over TCP; supported on PowerMax 2500/8500 |
| FICON | Mainframe | IBM z-series channel attachment; dedicated FA director cards |

**PowerPath** is Dell's multipathing software, installed on hosts. It aggregates multiple paths (from different FA directors) into a single virtual device, provides automatic path failover on director or port failure, and applies intelligent load balancing across active paths. PowerPath/VE is the VMware-specific variant.

Cross-director zoning is the recommended practice — each host HBA should be zoned to ports on both FA Director A and FA Director B. This ensures that a director failure leaves at least one active path per host without requiring manual intervention.

## Unisphere for PowerMax

Unisphere is the browser-based management interface for PowerMax. It runs as a virtual appliance (vApp) on a vCenter environment and exposes both a GUI and a REST API.

- REST API base: `https://<unisphere-host>:8443/univmax/restapi/`
- All operations available in the GUI are also available via REST — array configuration, storage group management, masking, SRDF management, snapshot management, and performance metrics
- Multiple PowerMax arrays can be managed from a single Unisphere instance

**Solutions Enabler (SYMCLI)** is the host-based command-line toolkit for PowerMax management. It communicates with the array directly over a gatekeeper device (a small SCSI device presented to the Solutions Enabler host).

Commonly used SYMCLI command families:

| Command Prefix | Scope |
|---|---|
| `symcfg` | Array-level configuration and status |
| `symsg` | Storage group management |
| `sympd` | Physical drive status |
| `symrdf` | SRDF pair management and failover |
| `symsnap` | TimeFinder SnapVX snapshot management |
| `symmaskdb` | Masking view and initiator group management |

## Key Terms Glossary

| Term | Definition |
|---|---|
| Director | An independent processing board inside a PowerMax engine; comes in FA (front-end), DA (back-end), and RA (RDF/replication) variants |
| Global Cache | A large DRAM pool shared by all directors; all reads and writes pass through it; RAID-1 protected across director pairs |
| SRDF/S | SRDF Synchronous — writes are mirrored to the remote R2 array before host ACK; RPO=0; suitable for metro distances |
| SRDF/A | SRDF Asynchronous — writes are batched into delta sets and sent to R2 periodically; configurable RPO (~30 seconds); suitable for any distance |
| TDEV | Thin Device — the thin-provisioned logical block volume presented to a host; physical capacity allocated from an SRP on write |
| SRP | Storage Resource Pool — the aggregate of physical NVMe drives from which TDEVs draw capacity |
| FAST | Fully Automated Storage Tiering — automatically migrates data between NVMe tiers (e.g., SCM for hot, eTLC for warm) based on access frequency |
| Masking View | The access-control object that binds a host initiator group, a port group, and a storage group — determines which devices a host can see |
| PowerPath | Dell multipathing software installed on hosts; aggregates multiple FA director paths, provides failover and load balancing |
| Hypermax OS | The operating system running on all PowerMax director boards; manages cache, scheduling, SRDF, and data services |
| RDF Group | A numbered replication group on PowerMax; binds R1 and R2 devices together for SRDF replication on specific RA director ports |
| Solutions Enabler | Dell's host-based CLI toolkit (SYMCLI) for PowerMax; required for scripted and advanced management operations |
