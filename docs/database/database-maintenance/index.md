# Database Maintenance Procedure


<div class="kb-summary">
Routine maintenance tasks to keep databases healthy: index optimisation, statistics refresh, log cleanup, and integrity checks.
</div>

## PostgreSQL Maintenance

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

-- Check table status
SHOW TABLE STATUS FROM <database>;

-- Purge old binary logs (retain 7 days)
PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 7 DAY);

-- Update InnoDB statistics
mysql -u root -e "CALL sys.ps_setup_enable_consumer('events_statements_history_long');"
ANALYZE TABLE <table>;
```text

## SQL Server Maintenance

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

### SQL Server — Integrity Check

```sql
-- DBCC CHECKDB — run weekly on non-peak window; can take hours on large DBs
DBCC CHECKDB ('<dbname>') WITH NO_INFOMSGS, ALL_ERRORMSGS;

-- Faster: check allocation structures only
DBCC CHECKDB ('<dbname>') WITH PHYSICAL_ONLY, NO_INFOMSGS;
```

## Maintenance Schedule

| Task | PostgreSQL | MySQL | SQL Server | Frequency |
|---|---|---|---|---|
| Update statistics | `ANALYZE` | `ANALYZE TABLE` | `UPDATE STATISTICS` | Daily (autovacuum/auto-stats) |
| Index maintenance | `REINDEX CONCURRENTLY` | `OPTIMIZE TABLE` | `REORGANIZE` / `REBUILD` | Weekly |
| Log / WAL cleanup | Auto + check pg_wal | `PURGE BINARY LOGS` | Log backup + shrink | Weekly |
| Integrity check | `VACUUM FULL` (if needed) | `mysqlcheck --check` | `DBCC CHECKDB` | Weekly |
| Dead tuple cleanup | `VACUUM ANALYZE` | N/A (InnoDB purge) | N/A | Daily (autovacuum) |

## Maintenance Checklist

- [ ] Autovacuum / auto-stats are enabled and not falling behind
- [ ] Index fragmentation reviewed — heavily fragmented indexes rebuilt
- [ ] Statistics are current (check last update date)
- [ ] Old logs / WAL / binary logs purged per retention policy
- [ ] Integrity check (`DBCC CHECKDB` / `VACUUM`) completed without errors
- [ ] Maintenance task duration logged (flag if significantly longer than baseline)
- [ ] No blocking during maintenance tasks (schedule during low-traffic window)

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| VACUUM FULL blocking production | Long-running transaction holding lock | Identify and terminate blocker: `SELECT pid, query FROM pg_stat_activity WHERE state='idle in transaction';` |
| OPTIMIZE TABLE takes too long | Large table / high traffic | Run during maintenance window; consider `pt-online-schema-change` |
| DBCC CHECKDB reports corruption | Disk error? | Restore from last known-good backup; run `DBCC CHECKDB WITH REPAIR_ALLOW_DATA_LOSS` as last resort |
| Autovacuum not running | `autovacuum=off`? | Check `SHOW autovacuum;`; enable if off |
