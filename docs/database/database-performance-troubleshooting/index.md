# Database Performance Troubleshooting

Systematic approach to identifying and resolving database performance bottlenecks — from slow queries to I/O saturation and locking.

## Triage — Identify the Bottleneck

```bash
# OS resource view
top -b -n 1 | head -20
vmstat 1 5        # check wa (I/O wait) column
iostat -xz 1 5    # %util, await, r/s, w/s on DB disk
free -h           # check swap usage — DB paging = critical
```

| Symptom | Likely Cause |
|---|---|
| High CPU on DB server | Missing index / full table scan / too many connections |
| High I/O wait | Buffer pool too small / no indexes / HDD not SSD |
| High swap usage | Insufficient RAM for buffer pool |
| Many blocked/waiting sessions | Table locks / long transactions |
| Queries slow for specific tables | Table bloat / stale statistics / fragmented indexes |

## PostgreSQL — Slow Query Analysis

```sql
-- Currently running queries (sorted by duration)
SELECT pid, now() - query_start AS duration, state, wait_event_type, wait_event, left(query,100)
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Kill a long-running query
SELECT pg_cancel_backend(<pid>);    -- sends SIGINT (graceful)
SELECT pg_terminate_backend(<pid>); -- sends SIGTERM (immediate)

-- Top queries by total time (requires pg_stat_statements)
SELECT left(query,80), calls, total_exec_time/1000 AS total_sec,
       mean_exec_time AS mean_ms, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 20;

-- Missing indexes — sequential scans on large tables
SELECT relname, seq_scan, idx_scan, n_live_tup
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan AND n_live_tup > 10000
ORDER BY seq_scan DESC;

-- Explain a slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT) SELECT ...;
```

## MySQL / MariaDB — Slow Query Analysis

```sql
-- Show currently running queries
SHOW FULL PROCESSLIST;
-- Kill a query
KILL QUERY <process_id>;

-- Slow query log (enable if not on)
SHOW VARIABLES LIKE 'slow_query_log%';
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 1;  -- log queries > 1 second

-- Top slow queries
mysqldumpslow -s t -t 20 /var/log/mysql/mysql-slow.log

-- Query execution plan
EXPLAIN SELECT ...;
EXPLAIN FORMAT=JSON SELECT ...;

-- Check for table locks
SHOW OPEN TABLES WHERE In_use > 0;
SELECT * FROM information_schema.innodb_trx\G
SELECT * FROM information_schema.innodb_locks\G
```

## SQL Server — Slow Query Analysis

```sql
-- Currently executing requests sorted by CPU
SELECT r.session_id, r.status, r.cpu_time, r.total_elapsed_time/1000 AS elapsed_sec,
       r.wait_type, r.blocking_session_id, LEFT(t.text, 100) AS query_text
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.status != 'background'
ORDER BY r.cpu_time DESC;

-- Top queries by total CPU (Query Store — SQL Server 2016+)
SELECT TOP 20 qt.query_sql_text, rs.avg_cpu_time/1000 AS avg_cpu_ms,
       rs.avg_logical_io_reads, rs.count_executions
FROM sys.query_store_query_text qt
JOIN sys.query_store_query q ON qt.query_text_id = q.query_text_id
JOIN sys.query_store_plan p ON q.query_id = p.query_id
JOIN sys.query_store_runtime_stats rs ON p.plan_id = rs.plan_id
ORDER BY rs.avg_cpu_time DESC;

-- Missing index recommendations
SELECT mig.equality_columns, mig.inequality_columns, mig.included_columns,
       mid.statement AS table_name, migs.avg_user_impact
FROM sys.dm_db_missing_index_details mid
JOIN sys.dm_db_missing_index_groups mig ON mid.index_handle = mig.index_handle
JOIN sys.dm_db_missing_index_group_stats migs ON mig.index_group_handle = migs.group_handle
ORDER BY migs.avg_user_impact DESC;

-- Blocking chains
SELECT blocking_session_id, session_id, wait_type, wait_time/1000 AS wait_sec
FROM sys.dm_exec_requests WHERE blocking_session_id != 0;
```

## Buffer Pool / Cache Efficiency

```sql
-- PostgreSQL: cache hit ratio (target > 99%)
SELECT sum(heap_blks_hit) / NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0) * 100 AS cache_hit_pct
FROM pg_statio_user_tables;

-- MySQL: InnoDB buffer pool hit ratio
SHOW STATUS LIKE 'Innodb_buffer_pool_read%';
-- Formula: (read_requests - disk_reads) / read_requests * 100

-- SQL Server: page life expectancy (target > 300s per 4GB RAM)
SELECT object_name, counter_name, cntr_value
FROM sys.dm_os_performance_counters
WHERE counter_name = 'Page life expectancy';
```

## Connection Pool Issues

```bash
# Too many connections exhausting max_connections (PostgreSQL)
psql -c "SELECT count(*), state FROM pg_stat_activity GROUP BY state;"
psql -c "SHOW max_connections;"

# MySQL threads_connected approaching max_connections
mysql -e "SHOW STATUS LIKE 'Threads_connected';"
mysql -e "SHOW VARIABLES LIKE 'max_connections';"
```

## Troubleshooting Decision Tree

```
Query slow?
  ├─ EXPLAIN shows Seq Scan on large table → add index
  ├─ EXPLAIN shows correct index but slow → stale statistics → ANALYZE
  ├─ Waiting on lock → find blocker; kill if necessary
  ├─ High I/O wait → buffer pool too small → increase shared_buffers / innodb_buffer_pool_size
  └─ CPU spiking → too many connections or parallel queries → check pool; tune work_mem
```

## Immediate Remediation

| Problem | Action |
|---|---|
| Long-running query blocking others | `pg_terminate_backend(pid)` / `KILL QUERY` |
| Missing index causing full scan | `CREATE INDEX CONCURRENTLY` (PG) / `CREATE INDEX` (MySQL/MSSQL) |
| Stale statistics | `ANALYZE` (PG) / `UPDATE STATISTICS` (MSSQL) |
| Buffer pool too small | Increase `shared_buffers` (PG) / `innodb_buffer_pool_size` (MySQL) |
| Connection pool exhausted | Restart app pool; lower `max_connections` per app |
