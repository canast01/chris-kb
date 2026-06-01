# Unity — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Architecture, HA and Write Cache Mirroring, Hardware Models, Storage Pool Architecture and 3 more sections.
</div>
```text
┌──────────────────────────────────── Dell Unity XT — How It Works ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Unity XT operational flow: request → controller → data service → host acknowledgement     │   │
│   │          Data path: host I/O → Unity XT controller → storage media → persistent write         │   │
│   │     Management: Unisphere / UEMCLI provides unified control for all operational functions     │   │
│   │           Protection: snapshots, replication, and redundancy ensure data durability           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Host I/O → Unity XT controller → storage media → acknowledge → replicate                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Ctrl            │  │         SP-A + SP-B         │  │        Cache mirrored       │   │
│   │             Pool            │  │       Dynamic FAST VP       │  │         Auto-tiering        │   │
│   │          NAS server         │  │        File protocols       │  │          Per-tenant         │   │
│   │           Snapshot          │  │        Writable snaps       │  │        Thin PiT copy        │   │
│   │         Replication         │  │         Async/Metro         │  │       Native or RP4VM       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    Unisphere     │  GUI / REST API  │       HTTPS       │    LDAP/local    │    SP-hosted     │   │
│   │      UEMCLI      │  CLI management  │    SSH / HTTPS    │   Local admin    │  All operations  │   │
│   │    NAS server    │  File services   │      NFS/SMB      │  Kerberos/NTLM   │ Virtual file se  │   │
│   │   RecoverPoint   │ Continuous prote │   Encrypted TCP   │   Certificate    │   Journal CDP    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Unity XT 380F/480F/680F/880F · dual SPs · DPE/DAE expansion · 10/25 GbE                  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Unity XT           = Dell unified mid-range array; block LUNs, file NAS, and VMware vVols          │
│    Unisphere          = HTML5 GUI and REST API for Unity XT management; SP-hosted management portal   │
│    UEMCLI             = CLI for Unity XT; uemcli -d <ip> -u admin -p <pw> /show commands              │
│    Storage pool       = collection of drives forming a usable pool; FAST VP tiers data automatically  │
│    FAST VP            = Fully Automated Storage Tiering VP; moves hot and cold data between tiers     │
│    NAS server         = virtual file server on Unity; each has its own IP, DNS, and CIFS/NFS shares   │
│    Data Mover         = older EMC term for NAS server; used in VNX and early Unity documentation      │
│    SP-A / SP-B        = storage processors; active-active HA pair with mirrored cache                 │
│    Snapshot           = space-efficient PiT copy of LUN or FS; writable snapshots supported           │
│    RecoverPoint       = RP4VM; journal-based continuous data protection for Unity volumes             │
│    Metro              = synchronous replication between two Unity XT sites; active-active zero RPO    │
│    vVols              = Virtual Volumes; VASA provider exposes per-VM storage objects to vCenter      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Overview

Dell Unity XT is a mid-range unified storage platform delivering block (FC, iSCSI) and file (NFS, SMB) from a single system. It uses a dual storage processor (SP A / SP B) active-active architecture with write-cache mirroring. Administration is via Unisphere for Unity (GUI) or `uemcli` (CLI).

## Architecture

```mermaid
graph TB
  SPA["Storage Processor A\n(active for owned LUNs/NAS)"] <-->|"write cache mirror\n+ HA heartbeat"| SPB["Storage Processor B"]
  SPA & SPB --> POOL[("Drive Pool\nRAID-5 / RAID-10 / NL-SAS")]
  SPA --> NAS["NFS · SMB · FTP\nData Mover"]
  SPA --> SAN["iSCSI · FC\nBlock LUNs"]
  SPB --> NAS & SAN
  NAS --> NH(["NAS Clients"])
  SAN --> SH(["SAN Hosts"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class SPA,SPB ctrl
  class POOL store
  class NH,SH host
```

## HA and Write Cache Mirroring

Unity XT uses an active-active dual-SP model:

- LUN and NAS server ownership is distributed across SP A and SP B
- Each resource is owned by exactly one SP at a time; resources can be rebalanced or fail over automatically
- Write cache is **continuously mirrored** between SPs over a dedicated internal interconnect — no acknowledged write is lost on SP failure
- Battery-backed units (BBUs) on each SP protect write cache during power loss
- On SP failure, the surviving SP takes ownership of all resources within ~30 seconds; host multipath drivers (PowerPath, MPIO) redirect automatically

## Hardware Models

| Model | Max Raw Capacity | Notes |
|---|---|---|
| Unity XT 380 | ~2 PB | Entry mid-range; hybrid or all-flash |
| Unity XT 480 | ~4 PB | Mid-range; higher SP performance |
| Unity XT 680 | ~8 PB | High-end mid-range |
| Unity XT 880 | ~12 PB | Maximum scale for mid-range |
| Unity All-Flash (F-series) | Varies | No spinning disk; optimised for low latency |
| UnityVSA | Software-defined | ESXi-hosted; dev/test and small environments only |

## Storage Pool Architecture

```mermaid
graph TD
  subgraph "Unity Array"
    subgraph "Storage Pool"
      DG1["Disk Group 1\nRAID-5 · SAS SSD"]
      DG2["Disk Group 2\nRAID-5 · NL-SAS"]
      DG3["Disk Group 3\nRAID-10 · NVMe"]
    end
    LUN["Block LUN\n(thin-provisioned)"]
    FS["File System\n(NFS / SMB)"]
  end
  DG1 & DG2 & DG3 --> LUN
  DG1 & DG2 & DG3 --> FS
  classDef dg fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef res fill:#2563eb,stroke:#1d4ed8,color:#fff
  class DG1,DG2,DG3 dg
  class LUN,FS res
```

| Drive Type | Tier | Use |
|---|---|---|
| NVMe SSD | Tier 0 | Ultra-low latency; FAST VP performance tier |
| SAS SSD | Tier 1 | High IOPS; performance tier in hybrid pools |
| NL-SAS | Tier 3 | High capacity; archive and backup targets |

## Data Services

| Service | Description |
|---|---|
| Inline deduplication + compression | All-flash pools only; reduces effective capacity consumption |
| FAST VP | Automated sub-LUN tiering between drive tiers in a pool |
| FAST Cache | Dedicated SAS Flash drives as read/write cache for hybrid pools |
| Snapshots | Space-efficient redirect-on-write at LUN and filesystem level |
| Thin provisioning | Pool space consumed only as data is written |
| Consistency groups | Group LUNs for crash-consistent snapshots |
| Replication | Async or sync to a remote Unity or PowerStore |

## Networking

| Network | Protocol | Interface |
|---|---|---|
| Host block (FC) | Fibre Channel | 8/16/32 Gb FC HBAs |
| Host block (iSCSI) | iSCSI | 10/25 GbE Ethernet |
| Host file (NAS) | NFS / SMB | 10/25 GbE Ethernet |
| Management | HTTPS / SSH | Dedicated 1 GbE port per SP |

## Key CLI Commands

```bash
uemcli /env/health show -filter "health.value ne OK"  # health check
uemcli /stor/pool show -detail                         # pool capacity + FAST Cache
uemcli /sys/alert show                                 # active alerts
uemcli /rep/session show                               # replication session state
uemcli /sys/sw show                                    # installed OE version
uemcli /stor/snap show                                 # snapshot inventory
```
