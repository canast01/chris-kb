---
tags:
  - architecture
  - windows
---
# SQL Server — Architecture

<div class="kb-summary">
Architecture overview, design standards, and integrations.

*Applies to: SQL Server 2019 / 2022*
</div>

```text
┌───────────────────────────── SQL Server — Enterprise RDBMS Architecture ──────────────────────────────┐
│                                                                                                       │
│  Microsoft SQL Server; Always On Availability Groups for HA/DR; FCI for local HA;                     │
│  buffer pool as main memory cache; tempdb performance critical for concurrency.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Engine Architecture              │  │              Memory Components              │   │
│   │          SQL Server Database Engine          │  │           Buffer pool: data cache           │   │
│   │            SQL Server Agent: jobs            │  │           Plan cache: query plans           │   │
│   │             SSRS: report server              │  │           Column store: in-memory           │   │
│   │           SSAS: analysis services            │  │              tempdb: work area              │   │
│   │            SSIS: ETL integration             │  │         Max server memory: required         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  tempdb contention is the #1 performance issue; use multiple data files (1 per CPU).                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               HA: Always On AG               │  │          HA: Failover Cluster (FCI)         │   │
│   │           Primary: reads + writes            │  │           Shared storage: SAN LUN           │   │
│   │          Secondaries: read replicas          │  │            WSFC: Windows cluster            │   │
│   │          Listener: virtual IP/name           │  │            One instance at a time           │   │
│   │         Sync or async per secondary          │  │           AG+FCI: combine for best          │   │
│   │           Auto-failover: sync only           │  │             DTC: distributed tx             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Windows Server VMs (min 4 vCPU, 16 GB RAM); local NVMe for tempdb; SAN LUN for                       │
│  user DBs (FCI) or local/SAN per replica (AG); WSFC quorum disk or cloud witness.                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Always On AG   = Availability Group; HA/DR for user databases; most common SQL HA                    │
│  FCI            = Failover Cluster Instance; WSFC + shared storage; HA for instance                   │
│  Listener       = virtual network name for AG; clients connect here                                   │
│  Buffer pool    = SQL Server memory cache for data pages; largest memory consumer                     │
│  tempdb         = system DB for temp tables, sort spills; shared across all sessions                  │
│  SSMS           = SQL Server Management Studio; primary admin GUI                                     │
│  SQL Agent      = job scheduler; runs maintenance plans, SSIS packages, backups                       │
│  WSFC           = Windows Server Failover Cluster; required for both AG and FCI                       │
│  Max server memory= set to leave 10-15% RAM for OS; prevents OOM                                      │
│  Sync replica   = AG secondary in sync mode; 0 RPO; auto-failover eligible                            │
│  Async replica  = AG secondary with lag; lower network cost; manual failover only                     │
│  Quorum         = WSFC vote mechanism; need majority to operate; use cloud witness                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![SQL Server Architecture Overview](../../../../assets/sql-server-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="how-it-works/">How It Works</a>
  <a class="kb-card" href="design-standards/">Design Standards</a>
  <a class="kb-card" href="integrations/">Integrations</a>
</div>
