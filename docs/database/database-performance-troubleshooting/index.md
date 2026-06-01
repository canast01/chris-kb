# Database Performance Troubleshooting


<div class="kb-summary">
Systematic approach to identifying and resolving database performance bottlenecks — from slow queries to I/O saturation and locking.
</div>

## Triage — Identify the Bottleneck

```bash
# OS resource view
top -b -n 1 | head -20
vmstat 1 5        # check wa (I/O wait) column
iostat -xz 1 5    # %util, await, r/s, w/s on DB disk
free -h           # check swap usage — DB paging = critical
```
┌─────────────────────────────── Database — Performance Troubleshooting ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Diagnose DB performance: slow queries, blocking chains, lock contention, I/O saturation    │   │
│   │    Start with wait events to identify bottleneck type before looking at individual queries    │   │
│   │    Use EXPLAIN ANALYZE to confirm query plan; index changes need testing before production    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Diagnose                   │  │                   Resolve                   │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           Identify wait event type           │  │           Kill blocking head query          │   │
│   │           Find top CPU/IO queries            │  │          Add/rebuild missing index          │   │
│   │          EXPLAIN ANALYZE slow query          │  │          Rewrite query (avoid N+1)          │   │
│   │          Check index usage/missing           │  │          Increase work_mem / buffer         │   │
│   │          Review I/O wait on storage          │  │          Partition or archive data          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │     Symptom      │   Likely cause   │   Diagnose with   │    Resolution    │     Validate     │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │   Slow SELECT    │  Missing index   │  EXPLAIN ANALYZE  │   CREATE INDEX   │ Query time drop  │   │
│   │    High wait     │ Lock contention  │    pg_locks/DMV   │   Kill blocker   │   Wait clears    │   │
│   │    I/O spike     │ Full table scan  │  iostat + EXPLAIN │Index + partition │  I/O normalises  │   │
│   │    CPU spike     │  Bad query plan  │   AWR / top SQLs  │   Stats update   │    CPU drops     │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Wait event    = Reason a DB session is idle; lock/IO/CPU waits indicate bottleneck type            │
│    EXPLAIN ANALYZE= PostgreSQL; shows actual execution plan with row counts and timings               │
│    N+1 problem   = Loop issuing one query per item instead of one bulk query; kills DB                │
│    work_mem      = PostgreSQL per-sort memory; increase to avoid temp file disk spills                │
│    DMV           = SQL Server Dynamic Management View; real-time query and session stats              │
│    Seq scan      = Full table scan; normal for small tables; bad for large + OLTP queries             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

```text
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
