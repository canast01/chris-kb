---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
---
# PostgreSQL — Diagnostics

<div class="kb-summary">
PostgreSQL diagnostic commands: read the error log, query pg_stat_activity for blocking sessions, identify slow queries with pg_stat_statements, check WAL replication lag, diagnose autovacuum bloat, and collect a diagnostic snapshot for escalation.

*Applies to: PostgreSQL 14–17 on RHEL / Ubuntu LTS*
</div>
![PostgreSQL — Diagnostics](../../../../assets/compute-linux-postgresql-troubleshooting-diagnostics.svg)




```mermaid
graph TD
    A([PostgreSQL Issue]) --> B{What type of problem?}
    B -->|Queries hanging / slow| C[Check pg_stat_activity\nWhere state != idle]
    B -->|High CPU or I/O| D[Check pg_stat_statements\nTop queries by total_exec_time]
    B -->|Replication lag| E[Check pg_stat_replication\nlag_bytes on primary]
    B -->|Table bloat / disk full| F[Check pg_stat_user_tables\nn_dead_tup per table]
    B -->|Crash or restart| G[Check error log\ntail /var/log/postgresql/...]
    C --> H{Blocked sessions?}
    H -->|Yes| I[pg_blocking_pids pid\nFind blocking session]
    H -->|No, just slow| D
    I --> J[pg_cancel_backend or\npg_terminate_backend]
    D --> K[EXPLAIN query\nCheck index usage]
    E --> L{Lag increasing?}
    L -->|Yes| M[Check network\nand WAL send rate]
    L -->|High but stable| N[Monitor; may be acceptable]
    F --> O[VACUUM ANALYZE table\nMonitor n_dead_tup]
    G --> P[Check for OOM or\ndisk full in log]
    J --> Q[Collect pg_dump diag\nfor escalation]
    K --> Q
    M --> Q
    O --> Q
    P --> Q

    classDef dark fill:#1e3a5f,color:#fff
    classDef action fill:#78350f,color:#fff
    classDef escalate fill:#991b1b,color:#fff
    class A,B,H,L dark
    class C,D,E,F,G,I,J,K,M,N,O,P action
    class Q escalate
```

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
step_1_check_the_error_log: "Step 1 — Check the error log" {shape: rectangle}
step_2_check_active_sessions_and_blo: "Step 2 — Check active sessions and blocking" {shape: rectangle}
step_3_find_and_resolve_lock_content: "Step 3 — Find and resolve lock contention" {shape: rectangle}
step_4_identify_slow_queries: "Step 4 — Identify slow queries" {shape: rectangle}
step_5_check_autovacuum_and_table_bl: "Step 5 — Check autovacuum and table bloat" {shape: rectangle}
step_6_check_wal_replication_and_lag: "Step 6 — Check WAL replication and lag" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> step_1_check_the_error_log: investigate
symptom -> step_2_check_active_sessions_and_blo: investigate
symptom -> step_3_find_and_resolve_lock_content: investigate
symptom -> step_4_identify_slow_queries: investigate
symptom -> step_5_check_autovacuum_and_table_bl: investigate
symptom -> step_6_check_wal_replication_and_lag: investigate
step_1_check_the_error_log -> resolution
step_2_check_active_sessions_and_blo -> resolution
step_3_find_and_resolve_lock_content -> resolution
step_4_identify_slow_queries -> resolution
step_5_check_autovacuum_and_table_bl -> resolution
step_6_check_wal_replication_and_lag -> resolution
```

## Before you begin

- **Access:** `postgres` superuser or a role with `pg_monitor` privileges for diagnostic queries; root/sudo on the OS for log access
- **Gather first:** the exact error message, affected database name, approximate time of the issue, and whether it affects one query, one user, or all connections
- **Scope:** confirm whether the issue is a single slow query, a blocked transaction, a replication lag event, or a service crash
- **Extensions:** `pg_stat_statements` must be enabled in `postgresql.conf` (`shared_preload_libraries = 'pg_stat_statements'`) for slow query data — verify before relying on it

---

## Step 1 — Check the error log

```bash
# Ubuntu (default log location)
sudo tail -100 /var/log/postgresql/postgresql-16-main.log

# RHEL (logs in data directory)
sudo tail -100 /var/lib/pgsql/16/data/log/postgresql-*.log

# systemd journal (works on both distros)
sudo journalctl -u postgresql-16 --since "1 hour ago" | tail -100

# Filter for errors only
sudo grep -E "FATAL|ERROR|PANIC" /var/log/postgresql/postgresql-16-main.log | tail -50

# Common error patterns:
#   FATAL: max_connections exceeded — too many clients
#   FATAL: password authentication failed — credential or pg_hba.conf issue
#   PANIC: could not write to file — disk full or permissions
#   LOG: autovacuum: found X pages with Y dead row versions — normal autovacuum
```

---

## Step 2 — Check active sessions and blocking

```sql
-- All non-idle sessions with duration
SELECT pid, usename, datname, state, wait_event_type, wait_event,
       now() - query_start AS duration,
       left(query, 120) AS query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC NULLS LAST;

-- Sessions in "idle in transaction" (holding locks without active query)
SELECT pid, usename, state, now() - state_change AS idle_duration,
       left(query, 80) AS last_query
FROM pg_stat_activity
WHERE state = 'idle in transaction'
ORDER BY idle_duration DESC;
-- "idle in transaction" for > 30 seconds = common lock holder; consider terminating
```

---

## Step 3 — Find and resolve lock contention

```sql
-- Who is blocking whom
SELECT blocked.pid   AS blocked_pid,
       blocked.usename AS blocked_user,
       blocking.pid  AS blocking_pid,
       blocking.usename AS blocking_user,
       left(blocked.query, 80)  AS blocked_query,
       left(blocking.query, 80) AS blocking_query,
       now() - blocked.query_start AS blocked_duration
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
  ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;

-- Identify the root blocker (chain of blocking)
SELECT pg_blocking_pids(<blocked_pid>);
-- Returns array of PIDs; recurse up the chain to find the root

-- Cancel the blocking query (sends SIGINT — graceful; waits for safe point)
SELECT pg_cancel_backend(<blocking_pid>);

-- Terminate the blocking connection (sends SIGTERM — forces disconnect)
SELECT pg_terminate_backend(<blocking_pid>);
-- Use terminate only if cancel does not resolve within 30 seconds
```

---

## Step 4 — Identify slow queries

```sql
-- Top 10 queries by total execution time (requires pg_stat_statements)
SELECT left(query, 100) AS query,
       calls,
       total_exec_time / 1000   AS total_sec,
       mean_exec_time  / 1000   AS mean_sec,
       rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Reset stats after a fix to measure improvement
SELECT pg_stat_statements_reset();

-- Get query plan for a slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
  SELECT * FROM my_table WHERE some_column = 'value';
-- Look for: Seq Scan on large tables (should be Index Scan), high Rows Removed by Filter
-- High "Buffers: hit=X read=Y" with large Y = heavy I/O

-- Enable slow query log temporarily without restart
SET log_min_duration_statement = 1000;  -- log queries > 1 second in current session
-- Or globally (requires reload, not restart):
-- ALTER SYSTEM SET log_min_duration_statement = 1000;
-- SELECT pg_reload_conf();
```

---

## Step 5 — Check autovacuum and table bloat

```sql
-- Tables with the most dead tuples (candidates for bloat)
SELECT schemaname, relname, last_autovacuum, last_autoanalyze, n_dead_tup,
       n_live_tup,
       round(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 1) AS dead_pct
FROM pg_stat_user_tables
WHERE n_dead_tup > 10000
ORDER BY n_dead_tup DESC
LIMIT 20;
-- dead_pct > 20% = table needs VACUUM; autovacuum may not be keeping up

-- Force vacuum on a specific table (non-blocking VACUUM; FULL is disruptive)
VACUUM ANALYZE <schema>.<tablename>;

-- Check autovacuum activity in real time
SELECT datname, pid, backend_start, now() - backend_start AS runtime,
       left(query, 100) AS query
FROM pg_stat_activity
WHERE query ILIKE '%autovacuum%'
ORDER BY backend_start;
```

---

## Step 6 — Check WAL replication and lag

```sql
-- On the PRIMARY: check replica lag
SELECT client_addr,
       state,
       sent_lsn,
       write_lsn,
       flush_lsn,
       replay_lsn,
       (sent_lsn - replay_lsn) AS lag_bytes
FROM pg_stat_replication;
-- lag_bytes > 100 MB = replica is falling behind; investigate network or replica load

-- On the STANDBY: check lag in seconds
SELECT now() - pg_last_xact_replay_timestamp() AS replay_lag;
-- Expected: < 30 seconds for async streaming; 0 for synchronous replication

-- Confirm this host is a standby
SELECT pg_is_in_recovery() AS is_standby;
```

---

## Step 7 — Collect diagnostic snapshot for escalation

```bash
# All-in-one diagnostic snapshot (run as postgres user or with psql -U postgres)
{
  echo "=== PostgreSQL version ==="
  psql -U postgres -c "SELECT version();"
  echo "=== Active sessions ==="
  psql -U postgres -c "SELECT pid, usename, state, now()-query_start AS dur, left(query,80) FROM pg_stat_activity WHERE state != 'idle' ORDER BY dur DESC NULLS LAST;"
  echo "=== Blocking ==="
  psql -U postgres -c "SELECT blocked.pid, blocking.pid AS blocker, left(blocked.query,60) FROM pg_stat_activity blocked JOIN pg_stat_activity blocking ON blocking.pid = ANY(pg_blocking_pids(blocked.pid)) WHERE cardinality(pg_blocking_pids(blocked.pid))>0;"
  echo "=== Top slow queries ==="
  psql -U postgres -c "SELECT calls, total_exec_time/1000 AS total_sec, left(query,80) FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 10;"
  echo "=== Replication ==="
  psql -U postgres -c "SELECT client_addr, state, (sent_lsn-replay_lsn) AS lag_bytes FROM pg_stat_replication;"
  echo "=== Dead tuple tables ==="
  psql -U postgres -c "SELECT relname, n_dead_tup FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;"
  echo "=== Error log (last 100 lines) ==="
  sudo tail -100 /var/log/postgresql/postgresql-*.log 2>/dev/null || \
    sudo tail -100 /var/lib/pgsql/*/data/log/postgresql-*.log
} > /tmp/pg-diag-$(date +%F-%H%M).txt
```

---

## Log locations

| Source | Path / Command | What to look for |
|---|---|---|
| Error log (Ubuntu) | `/var/log/postgresql/postgresql-16-main.log` | FATAL, PANIC, crash recovery |
| Error log (RHEL) | `/var/lib/pgsql/16/data/log/postgresql-*.log` | Same |
| Slow query log | Configured via `log_min_duration_statement` | Queries exceeding threshold |
| systemd journal | `journalctl -u postgresql-16 --since "1h ago"` | Service start/stop events |
| pg_stat_activity | SQL view — live | Sessions, blocking, wait events |
| pg_stat_statements | SQL view — cumulative | Top queries by total execution time |

---

## See also

- [PostgreSQL — Common Issues](../common-issues/)
- [PostgreSQL — Escalation](../escalation/)
- [PostgreSQL — Health Checks](../../operations/health-checks/)

## Verify resolution

- `pg_stat_activity` shows no sessions in `idle in transaction` for more than 30 seconds
- `pg_stat_replication` shows lag_bytes below 100 MB (or 0 for sync replication)
- The original slow query now runs within expected time; `EXPLAIN ANALYZE` shows Index Scan instead of Seq Scan
- `n_dead_tup` in `pg_stat_user_tables` is decreasing after `VACUUM ANALYZE`
- No new FATAL or PANIC entries in the error log in the last 15 minutes
