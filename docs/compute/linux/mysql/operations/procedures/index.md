---
tags:
  - linux
  - operations
---
# MySQL / MariaDB — Procedures

<div class="kb-summary">
MySQL / MariaDB procedures reference.

*Applies to: RHEL / Ubuntu LTS*
</div>

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Database — Maintenance Procedures

```sql
-- Update statistics (safe at any time)
ANALYZE;
ANALYZE <schema>.<table>;

-- Vacuum dead tuples (non-blocking)
VACUUM ANALYZE;
VACUUM ANALYZE <schema>.<table>;

-- Full vacuum — reclaims disk space (acquires exclusive lock — use off-peak)
VACUUM FULL <schema>.<table>;

-- Check autovacuum status per table
SELECT relname, last_autovacuum, last_autoanalyze, n_dead_tup, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Rebuild bloated indexes
REINDEX TABLE <schema>.<table>;
-- Online (PG12+, no locking)
REINDEX TABLE CONCURRENTLY <schema>.<table>;

-- Check index bloat
SELECT indexname, pg_size_pretty(pg_relation_size(indexname::regclass)) AS index_size,
       idx_scan AS scans
FROM pg_stat_user_indexes ORDER BY pg_relation_size(indexname::regclass) DESC LIMIT 20;
```
```text
┌────────────────────────────────── Database — Maintenance Procedures ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Scheduled DB maintenance keeps performance stable and prevents space exhaustion        │   │
│   │      Index maintenance: rebuild (>30% fragmentation) or reorganise (10-30% fragmentation)     │   │
│   │       Run during low-traffic maintenance windows; monitor impact on production workloads      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Index Maintenance      │  │      Statistics Update      │  │        Log Management       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      PG: REINDEX TABLE      │  │      PG: ANALYZE / auto     │  │      PG: WAL truncation     │   │
│   │       PG: VACUUM FULL       │  │     MSSQL: UPDATE STATS     │  │      MSSQL: DBCC SHRINK     │   │
│   │      MSSQL: ALTER INDEX     │  │     MySQL: ANALYZE TABLE    │  │     MySQL: PURGE BINARY     │   │
│   │     Check fragmentation     │  │    Stale stats = bad plan   │  │       Log backup first      │   │
│   │      Online vs offline      │  │   Trigger after bulk load   │  │      Monitor VLF count      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    VACUUM        = PostgreSQL process; reclaims dead row space; VACUUM FULL rewrites table            │
│    autovacuum    = PostgreSQL background process; runs VACUUM/ANALYZE automatically                   │
│    Fragmentation = Index leaf pages out of order; > 30% triggers REBUILD (full rewrite)               │
│    REORGANIZE    = Online defrag (SQL Server); moves leaf pages in-place; low-impact                  │
│    Statistics    = Histogram of data distribution; query planner uses them for plan selection         │
│    VLF           = Virtual Log File (SQL Server); many small VLFs slow log operations                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text

## SQL Server Maintenance

```

```sql
-- Rebuild fragmented indexes (> 30% fragmentation)
SELECT OBJECT_NAME(ips.object_id) AS table_name, i.name AS index_name,
       ips.avg_fragmentation_in_percent
FROM sys.dm_db_index_physical_stats(DB_ID(), NULL, NULL, NULL, 'LIMITED') ips
JOIN sys.indexes i ON ips.object_id = i.object_id AND ips.index_id = i.index_id
WHERE ips.avg_fragmentation_in_percent > 30
ORDER BY ips.avg_fragmentation_in_percent DESC;

-- Rebuild index
ALTER INDEX [IX_TableName_Column] ON dbo.TableName REBUILD;
-- Online rebuild (Enterprise edition)
ALTER INDEX ALL ON dbo.TableName REBUILD WITH (ONLINE = ON);

-- Reorganise (< 30% fragmentation — online, low-impact)
ALTER INDEX ALL ON dbo.TableName REORGANIZE;

-- Update statistics
UPDATE STATISTICS dbo.TableName;
UPDATE STATISTICS dbo.TableName WITH FULLSCAN;

-- Shrink log file (use sparingly — only after log backup, not routine)
USE <dbname>;
BACKUP LOG <dbname> TO DISK = '/backup/mssql/<dbname>_log.bak';
DBCC SHRINKFILE (<dbname>_log, 256);  -- shrink to 256 MB
```
```sql
-- DBCC CHECKDB — run weekly on non-peak window; can take hours on large DBs
DBCC CHECKDB ('<dbname>') WITH NO_INFOMSGS, ALL_ERRORMSGS;

-- Faster: check allocation structures only
DBCC CHECKDB ('<dbname>') WITH PHYSICAL_ONLY, NO_INFOMSGS;
```

```bash
# Database — Failover Procedure

```
```bash
# On STANDBY — check replication lag before promoting
psql -U postgres -c "SELECT now() - pg_last_xact_replay_timestamp() AS replication_lag;"

# Promote standby to primary
pg_ctl promote -D /var/lib/postgresql/data
# or PostgreSQL 12+:
touch /var/lib/postgresql/data/promote_standby

# Verify promotion
psql -U postgres -c "SELECT pg_is_in_recovery();"  # should return 'f' (false)
psql -U postgres -c "SELECT now() AS current_time;"

# Update application connection string / DNS to point at new primary
```
```text
┌──────────────────────────────────── Database — Failover Procedure ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Promote standby to primary when primary becomes unavailable or for planned maintenance    │   │
│   │    Pre-check: confirm failure (not network partition); check replication lag; notify teams    │   │
│   │     Post-failover: update DNS/VIP; rebuild old primary as new standby; monitor replication    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Pre-Failover        │  │       Promote Standby       │  │        Post-Failover        │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │     Confirm primary down    │  │      PG: pg_ctl promote     │  │       Update DNS / VIP      │   │
│   │      Check repl lag/RPO     │  │      MSSQL: AG failover     │  │       Notify app teams      │   │
│   │      Notify: DBA + app      │  │     MySQL: STOP REPLICA     │  │      Validate app login     │   │
│   │   Identify failover method  │  │      CHANGE REPL SOURCE     │  │      Rebuild as standby     │   │
│   │      Open change ticket     │  │    Oracle: DG switchover    │  │     Monitor replication     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │     Platform     │   Promote cmd    │     DNS update    │   Rebuild cmd    │   RTO estimate   │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    PostgreSQL    │  pg_ctl promote  │  pg_hba + reload  │    pg_rewind     │     5-15 min     │   │
│   │    SQL Server    │ AG failover wiz  │   Listener auto   │  Resync replica  │  < 30s auto AG   │   │
│   │      MySQL       │   STOP REPLICA   │   Update app DSN  │  CHANGE SOURCE   │     5-30 min     │   │
│   │      Oracle      │  DG switchover   │  TNS alias update │    reinstate     │   DG: < 1 min    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    pg_ctl promote = Promotes PostgreSQL standby to primary; creates recovery.signal removal           │
│    pg_rewind      = Resync old primary to new primary using WAL; avoids full re-base copy             │
│    Always On AG   = SQL Server availability group; listener DNS auto-redirects after failover         │
│    GTID           = MySQL Global Transaction Identifier; simplifies replica reconnect after failover  │
│    Data Guard     = Oracle HA/DR product; synchronous/async standby; switchover/failover modes        │
│    Split-brain    = Two nodes both believe they are primary; never promote without fencing            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Automatic failover — check MHA status
masterha_check_repl --conf=/etc/mha/app.conf

# Manual failover
masterha_master_switch --conf=/etc/mha/app.conf --master_state=dead --new_master_host=<replica-host>
```
```sql
-- Check AG health before failover
SELECT ag.name, ar.replica_server_name, rs.role_desc, rs.synchronization_health_desc
FROM sys.dm_hadr_availability_replica_states rs
JOIN sys.availability_replicas ar ON rs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id;

-- Manual failover to synchronous replica (no data loss)
ALTER AVAILABILITY GROUP [AG_Name] FAILOVER;

-- Forced failover (async replica — possible data loss; only if synchronous unavailable)
ALTER AVAILABILITY GROUP [AG_Name] FORCE_FAILOVER_ALLOW_DATA_LOSS;
```
```powershell
# Check cluster node status
Get-ClusterNode

# Move SQL Server resource group to another node
Move-ClusterGroup -Name "SQL Server (MSSQLSERVER)" -Node <target-node>

# Verify
Get-ClusterGroup -Name "SQL Server (MSSQLSERVER)" | Select-Object Name, OwnerNode, State
```
```bash
# Verify new primary accepting writes
psql -h <new-primary> -U appuser -c "INSERT INTO health_check(ts) VALUES (now());"
mysql -h <new-primary> -u appuser -e "INSERT INTO health_check(ts) VALUES(now());"

# Application connectivity
curl -sf https://<app-endpoint>/health && echo "OK"

# Check for open transactions / locks
# PostgreSQL
psql -c "SELECT pid, state, wait_event_type, query FROM pg_stat_activity WHERE state != 'idle';"
# SQL Server
SELECT session_id, blocking_session_id, wait_type, wait_time FROM sys.dm_exec_requests WHERE blocking_session_id != 0;
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
