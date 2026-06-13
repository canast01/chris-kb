---
tags:
  - linux
  - troubleshooting
---
# PostgreSQL — Diagnostics

<div class="kb-summary">
PostgreSQL diagnostics — reading pg_stat_activity, lock contention queries, autovacuum analysis, WAL lag, slow query identification, and log analysis.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌────────────────────────────────────── PostgreSQL — Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│   Primary diagnostic sources: error log, pg_stat_activity, pg_stat_replication, pg_locks              │
│   Lock contention: use pg_blocking_pids() to find which session is blocking another                   │
│   Slow queries: pg_stat_statements tracks cumulative execution stats per query fingerprint            │
│                                                                                                       │
│   Error log locations                                                                                 │
│   Ubuntu: /var/log/postgresql/postgresql-16-main.log                                                  │
│   RHEL: /var/lib/pgsql/16/data/log/postgresql-*.log                                                   │
│   Systemd: journalctl -u postgresql-16 --since "1 hour ago"                                           │
│                                                                                                       │
│   Active queries and blocking                                                                         │
│   pg_stat_activity: shows pid, user, state, wait_event, duration, query text per session              │
│   pg_blocking_pids(pid): returns array of PIDs blocking the given session                             │
│   Cancel: pg_cancel_backend(<pid>); terminate: pg_terminate_backend(<pid>)                            │
│                                                                                                       │
│   Replication and autovacuum                                                                          │
│   pg_stat_replication: shows sent/write/flush/replay LSN and lag_bytes per replica                    │
│   pg_last_xact_replay_timestamp(): seconds since last WAL replay on standby replica                   │
│   pg_stat_user_tables: last_autovacuum, n_dead_tup per table; find tables with bloat                  │
│                                                                                                       │
│   Key terms:                                                                                          │
│   pg_stat_activity = live view of all backend processes and their current query state                 │
│   pg_blocking_pids = returns PIDs that hold locks blocking a given session PID                        │
│   pg_stat_statements = extension tracking top queries by total and mean execution time                │
│   LSN          = Log Sequence Number; WAL position; used to calculate replication lag bytes           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Error Log

```bash
sudo tail -100 /var/log/postgresql/postgresql-16-main.log   # Ubuntu
sudo tail -100 /var/lib/pgsql/16/data/log/postgresql-*.log  # RHEL
sudo journalctl -u postgresql-16 --since "1 hour ago"
```

## Active Queries and Blocking

```sql
-- All non-idle sessions
SELECT pid, usename, state, wait_event_type, wait_event,
       now() - query_start AS duration,
       left(query, 100) AS query
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY duration DESC;

-- Lock contention: who is blocking whom
SELECT blocked.pid AS blocked_pid,
       blocking.pid AS blocking_pid,
       blocked.query AS blocked_query,
       blocking.query AS blocking_query
FROM pg_stat_activity blocked
JOIN pg_stat_activity blocking
  ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE cardinality(pg_blocking_pids(blocked.pid)) > 0;

-- Kill a blocking query
SELECT pg_cancel_backend(<pid>);   -- graceful
SELECT pg_terminate_backend(<pid>); -- force
```

## Autovacuum Analysis

```sql
-- Tables that haven't been vacuumed recently
SELECT relname, last_autovacuum, last_autoanalyze, n_dead_tup
FROM pg_stat_user_tables
WHERE last_autovacuum IS NULL OR last_autovacuum < now() - interval '24 hours'
ORDER BY n_dead_tup DESC;

-- Force vacuum on a specific table
VACUUM ANALYZE schema.tablename;
```

## WAL and Replication Diagnostics

```sql
-- On primary: replica connections and lag
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn,
       (sent_lsn - replay_lsn) AS lag_bytes
FROM pg_stat_replication;

-- On replica: lag in seconds
SELECT now() - pg_last_xact_replay_timestamp() AS replay_lag;
SELECT pg_is_in_recovery() AS is_standby;
```

## Slow Query Identification

```sql
-- Top queries by total time (requires pg_stat_statements)
SELECT query, calls, total_exec_time/1000 AS total_sec,
       mean_exec_time/1000 AS mean_sec, rows
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
