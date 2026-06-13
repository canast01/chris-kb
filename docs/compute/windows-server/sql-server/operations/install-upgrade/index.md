---
tags:
  - operations
  - windows
---
# SQL Server — Install & Upgrade

<div class="kb-summary">
SQL Server upgrade procedures — in-place upgrade, side-by-side upgrade, compatibility level, upgrade advisor, and post-upgrade validation.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌─────────────────────────────────── SQL Server — Install & Upgrade ────────────────────────────────────┐
│                                                                                                       │
│   Supports in-place upgrade from up to two prior major versions; cannot skip versions                 │
│   Keep databases on previous compatibility level immediately after upgrade; raise after testing       │
│   Always backup all databases (master, msdb, user DBs) before starting upgrade                        │
│                                                                                                       │
│   Upgrade path                                                                                        │
│   SQL 2016 → 2019, SQL 2017 → 2019, SQL 2019 → 2022 (one major version at a time)                     │
│   Cannot skip: SQL 2014 → 2022 is not a supported direct in-place upgrade path                        │
│                                                                                                       │
│   Pre-upgrade steps                                                                                   │
│   Check version: SELECT @@VERSION; check compat levels: SELECT name, compatibility_level              │
│   Run Database Experimentation Assistant (DEA) to identify compatibility issues                       │
│   Check deprecated features: sys.dm_os_performance_counters WHERE counter_name = 'Deprecated'         │
│   Backup all: BACKUP DATABASE [master/msdb/user DBs] WITH COMPRESSION                                 │
│                                                                                                       │
│   In-place upgrade                                                                                    │
│   Mount SQL Server ISO; run setup.exe → Installation → Upgrade from previous version                  │
│   Select features; point to existing instance; SQL Setup upgrades system DBs and restarts             │
│                                                                                                       │
│   Post-upgrade                                                                                        │
│   Raise compat level after testing: ALTER DATABASE MyDB SET COMPATIBILITY_LEVEL = 160                 │
│   Update statistics: EXEC sp_updatestats; verify SQL Agent jobs; verify AG health                     │
│                                                                                                       │
│   Key terms:                                                                                          │
│   compatibility_level = database-level setting; controls query optimizer behaviour version            │
│   DEA            = Database Experimentation Assistant; analyses workload against new version          │
│   DBCC UPDATEUSAGE = corrects inaccuracies in page and row counts in system catalog tables            │
│   sp_updatestats = updates statistics for all objects in all user databases                           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Local Administrator or Domain Admin on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Upgrade Path

SQL Server supports in-place upgrade from two prior major versions:
- `SQL 2016 → 2019`, `SQL 2017 → 2019`, `SQL 2019 → 2022`
- Cannot skip more than one major version

## Pre-Upgrade Steps

```sql
-- 1. Check current version and compatibility level
SELECT @@VERSION;
SELECT name, compatibility_level FROM sys.databases;

-- 2. Run Upgrade Advisor / Database Experimentation Assistant (DEA)
-- Download from Microsoft; analyse compatibility issues

-- 3. Check deprecated features in use
SELECT * FROM sys.dm_os_performance_counters
WHERE counter_name = 'Deprecated features';

-- 4. Backup all databases
BACKUP DATABASE [master] TO DISK = 'D:\Backup\master.bak' WITH COMPRESSION;
BACKUP DATABASE [msdb]   TO DISK = 'D:\Backup\msdb.bak'   WITH COMPRESSION;
BACKUP DATABASE [MyDB]   TO DISK = 'D:\Backup\MyDB.bak'   WITH COMPRESSION;
```

## In-Place Upgrade

1. Mount SQL Server installation media
2. Run `setup.exe` → **Maintenance** → **Edition Upgrade** or directly **Installation** → **Upgrade**
3. Select features to upgrade; point to existing instance
4. SQL Setup upgrades system databases and restarts service

## Post-Upgrade Steps

```sql
-- 1. Update compatibility level to new version (after testing)
ALTER DATABASE MyDB SET COMPATIBILITY_LEVEL = 160;   -- SQL 2022

-- 2. Update statistics
EXEC sp_updatestats;

-- 3. Rebuild system indexes
DBCC UPDATEUSAGE(0);

-- 4. Verify SQL Agent jobs running
SELECT name, enabled, date_modified FROM msdb.dbo.sysjobs ORDER BY name;

-- 5. Verify AG health (if applicable)
SELECT ag.name, rs.role_desc, rs.synchronization_health_desc
FROM sys.dm_hadr_availability_replica_states rs
JOIN sys.availability_replicas ar ON rs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id;
```

## Compatibility Level Strategy

Keep databases on previous compatibility level immediately after upgrade. Test application, then raise level. This allows rollback of query plan regression without downgrading SQL Server.
