---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
---
# MySQL / MariaDB — Diagnostics

<div class="kb-summary">
MySQL diagnostics — reading the error log, SHOW PROCESSLIST, slow query log analysis, InnoDB status, and performance_schema queries for locking and I/O bottlenecks.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌───────────────────────────────────────── MySQL — Diagnostics ─────────────────────────────────────────┐
│                                                                                                       │
│   Diagnostic sequence: error log → SHOW PROCESSLIST → InnoDB status → performance_schema              │
│   Error log is the first stop for crashes, plugin failures, and replication errors                    │
│   InnoDB engine status shows deadlocks, lock waits, and buffer pool state in one command              │
│                                                                                                       │
│   Error log                                                                                           │
│   Location: /var/log/mysql/error.log (Debian) or /var/log/mysqld.log (RHEL)                           │
│   journalctl -u mysqld -n 100: systemd journal for recent service events                              │
│   Look for: [ERROR], InnoDB startup messages, and crash recovery messages                             │
│                                                                                                       │
│   Process and lock analysis                                                                           │
│   SHOW FULL PROCESSLIST: all sessions with full query text and wait state                             │
│   SHOW ENGINE INNODB STATUS: deadlocks, lock waits, active trx, buffer pool hit rate                  │
│   SELECT * FROM information_schema.INNODB_TRX: transactions holding locks > 60 seconds                │
│   SELECT * FROM performance_schema.events_waits_current: current wait events per thread               │
│                                                                                                       │
│   Slow query analysis                                                                                 │
│   SET GLOBAL slow_query_log=ON; SET GLOBAL long_query_time=1: enable without restart                  │
│   pt-query-digest /var/log/mysql/slow.log: top queries ranked by total execution time                 │
│   EXPLAIN SELECT ...: shows index usage, join type, and estimated rows for a query                    │
│                                                                                                       │
│   Key terms:                                                                                          │
│   SHOW ENGINE INNODB STATUS = InnoDB internal diagnostic dump; includes deadlock history              │
│   EXPLAIN     = query plan analyser; shows which indexes MySQL will use for a SELECT                  │
│   long_query_time = threshold in seconds; queries exceeding it are written to slow_query_log          │
│   INNODB_TRX  = information_schema table listing all currently running InnoDB transactions            │
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
# Default location
sudo tail -100 /var/log/mysqld.log        # RHEL
sudo tail -100 /var/log/mysql/error.log   # Ubuntu

# Watch in real time
sudo tail -f /var/log/mysqld.log | grep -i 'error\|warning\|crash'
```

## Active Connections and Blocking

```sql
-- All active queries
SHOW FULL PROCESSLIST;

-- Blocking queries only (performance_schema)
SELECT r.trx_id waiting_trx, r.trx_mysql_thread_id waiting_thread,
       b.trx_id blocking_trx, b.trx_mysql_thread_id blocking_thread,
       r.trx_query waiting_query
FROM information_schema.innodb_lock_waits w
JOIN information_schema.innodb_trx b ON b.trx_id = w.blocking_trx_id
JOIN information_schema.innodb_trx r ON r.trx_id = w.requesting_trx_id;

-- Kill blocking query
KILL QUERY <thread_id>;
```

## InnoDB Status

```sql
-- Full InnoDB status (look for LATEST DETECTED DEADLOCK and TRANSACTIONS)
SHOW ENGINE INNODB STATUS\G

-- Buffer pool hit rate (should be > 99%)
SHOW STATUS LIKE 'Innodb_buffer_pool_read%';
-- hit_rate = Innodb_buffer_pool_read_requests / (read_requests + reads)
```

## Slow Query Log

```bash
# Enable temporarily for diagnosis
mysql -u root -p -e "SET GLOBAL slow_query_log=ON; SET GLOBAL long_query_time=1;"

# Analyse with pt-query-digest
pt-query-digest /var/log/mysql/slow.log | head -100
```

## Performance Schema Queries

```sql
-- Top queries by total execution time
SELECT DIGEST_TEXT, COUNT_STAR, SUM_TIMER_WAIT/1e12 AS total_sec
FROM performance_schema.events_statements_summary_by_digest
ORDER BY SUM_TIMER_WAIT DESC LIMIT 10;

-- Table I/O waits
SELECT OBJECT_NAME, COUNT_READ, COUNT_WRITE,
       SUM_TIMER_READ/1e12 AS read_sec, SUM_TIMER_WRITE/1e12 AS write_sec
FROM performance_schema.table_io_waits_summary_by_table
WHERE OBJECT_SCHEMA NOT IN ('mysql','sys')
ORDER BY SUM_TIMER_READ+SUM_TIMER_WRITE DESC LIMIT 10;
```

## Replication Diagnostics

```sql
SHOW REPLICA STATUS\G
-- Check: Replica_IO_Running, Replica_SQL_Running (both must be Yes)
--        Seconds_Behind_Source (lag in seconds)
--        Last_IO_Error, Last_SQL_Error
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
