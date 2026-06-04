# Database — Maintenance Procedures

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
