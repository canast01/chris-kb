---
tags:
  - linux
  - operations
---
# MySQL / MariaDB — Health Checks

<div class="kb-summary">
MySQL / MariaDB health checks reference.

*Applies to: RHEL / Ubuntu LTS*
</div>

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Database — Daily Health Check

```bash
# PostgreSQL
systemctl status postgresql
psql -U postgres -c "SELECT version();"
psql -U postgres -c "SELECT pg_is_in_recovery();"  # true = standby

# MySQL / MariaDB
systemctl status mysqld
mysql -u root -e "SHOW STATUS LIKE 'Uptime';"
mysql -u root -e "SHOW STATUS LIKE 'Threads_connected';"

# SQL Server
systemctl status mssql-server   # Linux
# Windows:
Get-Service -Name MSSQLSERVER
```
```text
┌──────────────────────────────────── Database — Daily Health Check ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Daily DB health: connections, blocking queries, long-running txns, replication, logs     │   │
│   │       Run each morning; alert on blocking > 5 min, connections > 80%, error log entries       │   │
│   │      Document anomalies; escalate blocking chains that cannot be cleared within threshold     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Health Check Items              │  │               Alert Thresholds              │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          Active connections vs max           │  │         >80% connection pool = alert        │   │
│   │        Blocking chains (head/waiters)        │  │           >5 min block = page DBA           │   │
│   │          Long-running transactions           │  │          >30 min txn = investigate          │   │
│   │         Error log: ORA-/FATAL/ERROR          │  │            Any ORA-600/4031 = P1            │   │
│   │            Replication lag check             │  │            >30s lag = investigate           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Blocking chain  = Series of queries waiting on each other; head blocker holds the lock             │
│    pg_stat_activity= PostgreSQL view; shows all active connections, state, and wait events            │
│    sys.dm_exec_reqs= SQL Server DMV; lists active requests with wait type and blocking session        │
│    INFORMATION_SCHEMA= Standard SQL views for connection and schema metadata                          │
│    ORA-600         = Oracle internal error; always escalate; indicates potential corruption           │
│    Wait event      = Reason a session is not running; categorised by type (I/O, lock, CPU, etc.)      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```sql
-- Instance uptime
SELECT sqlserver_start_time FROM sys.dm_os_sys_info;

-- Active sessions and blocking
SELECT session_id, status, blocking_session_id, wait_type, wait_time/1000 AS wait_sec, text
FROM sys.dm_exec_requests
CROSS APPLY sys.dm_exec_sql_text(sql_handle)
WHERE status != 'background'
ORDER BY wait_time DESC;

-- Database file sizes and free space
SELECT DB_NAME(database_id) AS db_name, name, type_desc,
       size * 8 / 1024 AS size_mb,
       fileproperty(name, 'SpaceUsed') * 8 / 1024 AS used_mb
FROM sys.master_files;

-- AG replica health (Always On)
SELECT ag.name, ar.replica_server_name, rs.synchronization_state_desc, rs.synchronization_health_desc
FROM sys.dm_hadr_availability_replica_states rs
JOIN sys.availability_replicas ar ON rs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id;
```
```bash
# PostgreSQL
psql -h <host> -U <user> -d <dbname> -c "SELECT 1 AS alive;"

# MySQL
mysql -h <host> -u <user> -p<pass> -e "SELECT 1 AS alive;"

# SQL Server
sqlcmd -S <host> -U <user> -P <pass> -Q "SELECT 1 AS alive"

# Port reachability
nc -zv <db-host> 5432    # PostgreSQL
nc -zv <db-host> 3306    # MySQL
nc -zv <db-host> 1433    # SQL Server
```

Database — Capacity Monitoring

```sql
-- Database sizes
SELECT datname AS database,
       pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database ORDER BY pg_database_size(datname) DESC;

-- Table sizes (top 20)
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;

-- Index sizes
SELECT indexname,
       pg_size_pretty(pg_relation_size(indexname::regclass)) AS index_size
FROM pg_indexes
ORDER BY pg_relation_size(indexname::regclass) DESC LIMIT 20;
```
```text
┌─────────────────────────────────── Database — Capacity Monitoring ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Track database growth, tablespace usage, log space, and forecast expansion needs       │   │
│   │     Alert at 75% usage; plan expansion at 85%; emergency at 90%; autogrow is a safety net     │   │
│   │     Monitor: data files, log files, temp/undo space, index fragmentation, row growth rate     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Current Capacity               │  │              Growth Forecasting             │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │            PG: pg_database_size()            │  │          Trend: 30/60/90 day growth         │   │
│   │         MSSQL: sys.dm_db_file_space          │  │          Forecast to 90% threshold          │   │
│   │          MySQL: information_schema           │  │         Alert: % full + growth rate         │   │
│   │          Log space: VLF / undo seg           │  │          Capacity request lead time         │   │
│   │          Temp: active session usage          │  │         Archive + partition old data        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Tablespace   = Named storage container for database objects; monitored per datafile                │
│    VLF          = Virtual Log File (SQL Server); fragmented log slows backup and recovery             │
│    Autogrow     = Auto-expand datafile; emergency safety net — not a capacity management plan         │
│    Undo segment = Oracle/MySQL space for rolled-back transactions; ORA-01555 on shortage              │
│    pg_database_size= PostgreSQL function returning total size of named database in bytes              │
│    Partitioning = Split large tables by range/list/hash; move old partitions to cheaper storage       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Database data directories
df -h /var/lib/postgresql /var/lib/mysql /var/opt/mssql

# inode usage (log files can exhaust inodes before disk is full)
df -i /var/lib/postgresql

# Identify large files
du -sh /var/lib/postgresql/data/*
du -sh /var/lib/mysql/*

# WAL / binary log space (PostgreSQL)
du -sh /var/lib/postgresql/data/pg_wal/

# MySQL binary logs
du -sh /var/lib/mysql/mysql-bin.*
mysql -u root -e "SHOW BINARY LOGS;"
```
```bash
# Weekly snapshots — capture to track growth
psql -U postgres -Atc "SELECT pg_database_size('mydb');" >> /var/log/db-size-mydb.log

# Simple growth rate from log
awk 'NR>1{print ($1-prev)/1024/1024 " MB added since last check"; prev=$1} NR==1{prev=$1}' /var/log/db-size-mydb.log
```
```sql
-- PostgreSQL: reclaim dead tuple space
VACUUM ANALYZE <schema>.<table>;
-- Full reclaim (locks table briefly)
VACUUM FULL <schema>.<table>;

-- PostgreSQL: drop unused indexes
SELECT indexname, idx_scan FROM pg_stat_user_indexes
WHERE idx_scan = 0 ORDER BY pg_relation_size(indexname::regclass) DESC;

-- MySQL: purge old binary logs
PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 7 DAY);

-- SQL Server: shrink log file (use sparingly — not routine maintenance)
USE mydb;
DBCC SHRINKFILE (mydb_log, 1024);  -- 1024 MB target
```

Database — Replication Check

```sql
-- On PRIMARY: show connected replicas and lag
SELECT client_addr, application_name, state,
       sent_lsn, write_lsn, flush_lsn, replay_lsn,
       (sent_lsn - replay_lsn) AS replication_lag_bytes,
       sync_state
FROM pg_stat_replication;

-- On STANDBY: confirm it is a replica and check lag
SELECT pg_is_in_recovery() AS is_standby;
SELECT now() - pg_last_xact_replay_timestamp() AS replay_lag;
SELECT pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn();

-- Replication slots — check for inactive slots holding WAL
SELECT slot_name, active, restart_lsn, pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM pg_replication_slots;
```
```text
┌──────────────────────────────────── Database — Replication Check ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Verify replication lag, sync state, and replica health for all HA database pairs       │   │
│   │        PostgreSQL: pg_stat_replication + replication slots; MySQL: SHOW REPLICA STATUS        │   │
│   │            Alert: lag > 30s; replica stopped; WAL slot bloat; disconnected replica            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Replication Status              │  │              Lag Investigation              │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           PG: pg_stat_replication            │  │            Check replica I/O load           │   │
│   │           PG: pg_replication_slots           │  │            WAL slot size growing?           │   │
│   │          MySQL: SHOW REPLICA STATUS          │  │            Seconds_Behind_Source            │   │
│   │           MSSQL: AG sync state DMV           │  │           Log send/redo queue size          │   │
│   │          Oracle: V$DATAGUARD_STATS           │  │             DG apply lag metric             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Replication slot  = PostgreSQL object that tracks WAL position for a replica; prevents WAL purge   │
│    Slot bloat        = Inactive replication slot retaining WAL; can fill disk; drop if unused         │
│    Seconds_Behind_Source= MySQL metric; seconds replica is behind primary; 0 = caught up              │
│    Log send queue    = SQL Server AG: bytes of log not yet sent to replica; measures send lag         │
│    Redo queue        = SQL Server AG: bytes received but not yet applied; measures apply lag          │
│    Synchronous rep   = Primary waits for replica ACK before committing; zero data loss; slower        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Quick one-liner — show lag and thread status
mysql -u root -e "SHOW SLAVE STATUS\G" | grep -E "Slave_(IO|SQL)_Running|Seconds_Behind|Last_(IO|SQL)_Error"
```
```sql
-- Check GTID position on replica vs primary
SHOW VARIABLES LIKE 'gtid_mode';
SELECT @@GLOBAL.gtid_executed;
SELECT @@GLOBAL.gtid_purged;
-- Compare GTID sets between primary and replica to calculate drift
```
```sql
-- Replica synchronization health
SELECT ag.name AS ag_name,
       ar.replica_server_name,
       rs.role_desc,
       rs.synchronization_state_desc,
       rs.synchronization_health_desc,
       rs.last_commit_time
FROM sys.dm_hadr_availability_replica_states rs
JOIN sys.availability_replicas ar ON rs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id;

-- Database-level lag
SELECT drs.database_id, DB_NAME(drs.database_id) AS db_name,
       drs.synchronization_state_desc,
       drs.log_send_queue_size AS send_queue_kb,
       drs.redo_queue_size AS redo_queue_kb,
       drs.last_commit_time
FROM sys.dm_hadr_database_replica_states drs;
```
```bash
# PostgreSQL — compare row counts between primary and replica
psql -h <primary-host> -U postgres -c "SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY relname;" > /tmp/primary-counts.txt
psql -h <standby-host> -U postgres -c "SELECT relname, n_live_tup FROM pg_stat_user_tables ORDER BY relname;" > /tmp/standby-counts.txt
diff /tmp/primary-counts.txt /tmp/standby-counts.txt

# MySQL — pt-table-checksum (Percona Toolkit)
pt-table-checksum --host=<primary> --user=root --password=<pass> --databases=<dbname>
# Then on replica:
pt-table-sync --sync-to-master h=<replica>,u=root,p=<pass> --print  # --execute to fix
```
```sql
-- Check error
SHOW SLAVE STATUS\G
-- If duplicate key / skip error (use with caution)
STOP SLAVE;
SET GLOBAL sql_slave_skip_counter = 1;
START SLAVE;
SHOW SLAVE STATUS\G
```
```bash
# If replay lag is huge and WAL is no longer available on primary,
# rebuild the replica from a fresh base backup
pg_basebackup -h <primary-host> -U replication -D /var/lib/postgresql/data-new -P -R
# -R writes recovery.conf / standby.signal automatically
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Mysql — Procedures](procedures/)
- [Mysql — CLI Reference](cli-reference/)
- [Mysql — Common Issues](../troubleshooting/common-issues/)
