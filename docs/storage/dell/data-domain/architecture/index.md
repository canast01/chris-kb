---
tags:
  - architecture
  - dell
---
# Data Domain — Architecture

<div class="kb-summary">
Dell PowerProtect DD (Data Domain) is a purpose-built backup appliance with inline global deduplication via the SISL engine. DDBoost integration with backup software reduces network traffic by ~50% via source-side deduplication. Typical dedup ratios: 20:1 or greater.

*Applies to: Data Domain DD OS 7.x*
</div>

```text
┌────────────────────────── Dell Data Domain — Backup Appliance Architecture ───────────────────────────┐
│                                                                                                       │
│  Purpose-built backup appliance (PBBA) with inline global deduplication (65:1 typical);               │
│  DD Boost protocol for direct backup app integration; DD Replicator for AIR.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Core Architecture               │  │                  Data Paths                 │   │
│   │        PBBA: optimized for backup IO         │  │        DD Boost: OST plugin on client       │   │
│   │         Inline dedup: before writing         │  │         NFS/CIFS: legacy backup apps        │   │
│   │         Typical ratio: 20:1 to 65:1          │  │         DD VTL: virtual tape library        │   │
│   │          DDVE: virtual edition (VM)          │  │         Boost FC: FC-attached option        │   │
│   │           DD OS: purpose-built OS            │  │         S3: object interface (DDVE)         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  DD Boost offloads dedup processing to client (backup server) for faster throughput.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Replication (DD Replicator)          │  │                  Management                 │   │
│   │          AIR: Automatic Image Repl           │  │            DD OS CLI: ddsh shell            │   │
│   │         Dir-to-dir or MTree replica          │  │          DD System Manager: web UI          │   │
│   │         Collection replication: full         │  │         DD Mgmt Center: multi-system        │   │
│   │           Cascade: A → B → C chain           │  │          REST API v2.1: automation          │   │
│   │           Cloud tier: S3 cold tier           │  │         SNMP: monitoring integration        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  DD appliance (DD6300/DD9300/DD9900) or DDVE VM; FC or Ethernet to backup servers;                    │
│  replication link: WAN between primary and DR site DD appliances.                                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  PBBA           = Purpose-Built Backup Appliance; optimized HW + SW for backup                        │
│  DD Boost       = Dell Data Domain Boost; dedup-aware backup app protocol                             │
│  OST            = OpenStorage Technology; Veritas API that DD Boost uses                              │
│  Deduplication  = removing duplicate data; write once, reference many times                           │
│  MTree          = logical partition on Data Domain; like a volume; each client uses one               │
│  AIR            = Automatic Image Replication; replicates backup images to remote DD                  │
│  DDVE           = Data Domain Virtual Edition; runs as VM (VMware or AWS)                             │
│  DD Replicator  = DD feature that performs async replication between DD systems                       │
│  DD VTL         = Virtual Tape Library; presents DD as tape drives to legacy apps                     │
│  Collection replica= full DD system replication; used for DR of the DD itself                         │
│  StreamFusion   = DD technology for parallel stream dedup during backup                               │
│  Cloud tier     = cold tier to S3/Azure Blob; reduces on-prem footprint                               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Data Domain Architecture](../../../../assets/data-domain-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">
    <div class="kb-card-icon">⚙️</div>
    <div class="kb-card-title">How It Works</div>
    <div class="kb-card-desc">SISL dedup engine, DDFS/MTree namespace, DDBoost source-side filtering, DD Replicator, cloud tier, and key CLI commands.</div>
  </a>
  <a class="kb-card" href="integrations/">
    <div class="kb-card-icon">🔗</div>
    <div class="kb-card-title">Integrations</div>
    <div class="kb-card-desc">NetBackup, Commvault, Veeam DDBoost integration, VTL for legacy backup software, and cloud tier object storage.</div>
  </a>
  <a class="kb-card" href="design-standards/">
    <div class="kb-card-icon">📐</div>
    <div class="kb-card-title">Design Standards</div>
    <div class="kb-card-desc">MTree layout, replication topology, DDBoost vs NFS protocol selection, and cloud tier lifecycle policy design.</div>
  </a>
</div>

## Protocol Access

| Protocol | Port | Use Case |
|---|---|---|
| DDBoost over IP | TCP 2052 / 2053 | Primary — backup software integration |
| NFS v3 | TCP/UDP 2049 | Unix/Linux backup clients |
| CIFS/SMB | TCP 445 | Windows backup clients |
| VTL | FC | Tape-emulation for legacy backup software |
| DD Replicator | TCP 2051 | DD-to-DD replication |
| Management | TCP 22 / 443 | SSH CLI and HTTPS UI |

## Topology

