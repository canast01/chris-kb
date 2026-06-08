# MySQL / MariaDB — Diagnostics

<div class="kb-summary">
MySQL diagnostics — reading the error log, SHOW PROCESSLIST, slow query log analysis, InnoDB status, and performance_schema queries for locking and I/O bottlenecks.
</div>

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
