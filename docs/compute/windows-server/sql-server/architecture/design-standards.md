---
tags:
  - architecture
  - windows
---
# SQL Server — Design Standards

<div class="kb-summary">
SQL Server design standards — HA topology (Always On AG, FCI), edition selection, disk layout, memory sizing, tempdb configuration, and naming conventions.

*Applies to: SQL Server 2019 / 2022*
</div>

```text
┌──────────────────────────────────── SQL Server — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│   Always On AG is the primary HA pattern; log-based replication with automatic failover               │
│   Separate volumes required for data, log, tempdb, and backup; no sharing between workloads           │
│   max server memory must be set; leave 10 GB for OS; default unbounded setting causes OOM             │
│                                                                                                       │
│   HA topologies                                                                                       │
│   Always On AG: log-based replication; automatic failover; readable secondaries; preferred pattern    │
│   Failover Cluster Instance (FCI): shared storage; cluster failover; legacy SAN-based environments    │
│   Log Shipping: async; manual failover; warm standby; used for DR and reporting copies                │
│                                                                                                       │
│   Edition selection                                                                                   │
│   Enterprise: Always On AG (unlimited replicas), partitioning, online operations, analytics           │
│   Standard: limited AG (2 replicas); no online index rebuild on most operations                       │
│   Developer: full Enterprise features; free; non-production only                                      │
│   Express: free; 10 GB database size limit; no SQL Agent                                              │
│                                                                                                       │
│   Disk and memory                                                                                     │
│   Data files (.mdf/.ndf): RAID 10 or SSD; Log (.ldf): sequential writes; dedicated SSD                │
│   tempdb: local NVMe preferred; one file per logical CPU core (cap at 8); equal size                  │
│   max server memory: set to RAM minus 10 GB for OS; use sp_configure to apply                         │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Always On AG   = Availability Group; log-based HA with primary and secondary replicas               │
│   FCI            = Failover Cluster Instance; shared disk; single instance on a Windows cluster       │
│   tempdb         = system database for temporary objects and sort spills; one file per core           │
│   MAXDOP         = max degree of parallelism; cap at 4 for OLTP; 0 for DW/reporting workloads         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## High-Availability Topologies

| Pattern | Description | Use case |
|---|---|---|
| Always On AG | Log-based replication; automatic failover; readable secondaries | Primary HA for production workloads |
| Failover Cluster Instance (FCI) | Shared storage; single database instance; cluster failover | Legacy HA; SAN-based environments |
| Log Shipping | Manual failover; warm standby; async | DR / reporting copies |
| Database Mirroring | Deprecated in SQL 2016; use AG instead | Legacy only |

## Edition Selection

| Edition | Use case |
|---|---|
| Enterprise | Always On AG, partitioning, online operations, advanced analytics |
| Standard | Limited AG (2 replicas); no online index rebuild on most operations |
| Developer | Full Enterprise features; free; non-production only |
| Express | Free; 10 GB limit; no SQL Agent |

## Disk Layout

Separate volumes for:
- **Data files** (`.mdf`, `.ndf`) — RAID 10 / SSD
- **Transaction log** (`.ldf`) — sequential writes; dedicated SSD spindles
- **tempdb** — local NVMe preferred; one file per CPU core (up to 8)
- **Backups** — separate volume or off-host

## Memory Sizing

```sql
-- Set max server memory (leave 10 GB for OS)
EXEC sp_configure 'max server memory (MB)', 51200;   -- 50 GB for SQL
RECONFIGURE WITH OVERRIDE;
```

## tempdb Best Practices

- Equal-sized files: one per logical CPU core (cap at 8)
- Pre-sized to expected workload
- Trace flag 1118 / 1117 built-in from SQL 2016+

## Naming Conventions

- Databases: `AppName_Env` — `CRM_Prod`, `ERP_Dev`
- Logins/users: `app_<name>_<rw|ro>`, `svc_<servicename>`
- AG names: `AG_<DatabaseName>` — `AG_CRM`
