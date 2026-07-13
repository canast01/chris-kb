---
tags:
  - operations
  - windows
description: "SQL Server procedures: index rebuild and statistics update, user and role management, linked server configuration, and maintenance plan creation."
---
# SQL Server — Procedures

<div class="kb-summary">
SQL Server procedures: index rebuild and statistics update, user and role management, linked server configuration, and maintenance plan creation.

*Applies to: Windows Server 2019 / 2022*
</div>

```d2
direction: right

database_maintenance_procedures: "Database — Maintenance Procedures" {shape: rectangle}
sql_server_maintenance: "SQL Server Maintenance" {shape: rectangle}
verify: "Verify" {shape: rectangle}

database_maintenance_procedures -> sql_server_maintenance
sql_server_maintenance -> verify
```

## Before you begin

- **Access:** Local Administrator or Domain Admin on target hosts
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


```text title="Expected output"
replication_lag 
-----------------
 00:00:00.342156
(1 row)

waiting for server to promote.... done
server promoted
 pg_is_in_recovery 
-------------------
 f
(1 row)

       current_time        
---------------------------
 2024-01-15 14:32:18.567891+00
(1 row)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory` | Ensure PostgreSQL is running on the standby with `systemctl start postgresql` before executing promotion commands. |
    | `FATAL: the database system is in recovery mode` | Wait for replication to catch up (lag near zero) and ensure the standby is fully synchronized before promoting. |
    | `could not open file "/var/lib/postgresql/data/promote_standby": Permission denied` | Run the touch command as the postgres user with `sudo -u postgres touch /var/lib/postgresql/data/promote_standby`. |
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


```text title="Expected output"
INSERT 0 1
Query OK, 0 rows affected (0.12 sec)
OK
 pid  | state  | wait_event_type |                query
------+--------+-----------------+------------------------------------------
 4521 | active | IO              | INSERT INTO health_check(ts) VALUES (now())
 4523 | active | Lock            | SELECT * FROM orders WHERE id = $1
(2 rows)

session_id | blocking_session_id | wait_type | wait_time
-----------|---------------------|-----------|----------
      52   |          48          | PAGEIOLATCH_SH | 1250
      54   |          0           | WRITELOG  | 0
(2 rows affected)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: FATAL: remaining connection slots are reserved for non-replication superuser connections` | Increase `max_connections` in postgresql.conf or wait for idle connections to close. |
    | `ERROR 1040 (HY000): Too many connections` | Verify MySQL `max_connections` setting and close idle application connections. |
    | `curl: (7) Failed to connect to <app-endpoint> port 443: Connection refused` | Confirm the application service is running on the new primary and network routing is correct. |
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Sql Server — Health Checks](../health-checks/)
- [Sql Server — CLI Reference](../cli-reference/)
- [Sql Server — Common Issues](../../troubleshooting/common-issues/)
