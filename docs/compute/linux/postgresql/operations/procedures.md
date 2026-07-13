---
tags:
  - linux
  - operations
description: "PostgreSQL procedures: VACUUM and ANALYZE scheduling, extension management with CREATE EXTENSION, role and schema management, and failover with pg_ctl..."
---
# PostgreSQL — Procedures

<div class="kb-summary">
PostgreSQL procedures: VACUUM and ANALYZE scheduling, extension management with `CREATE EXTENSION`, role and schema management, and failover with `pg_ctl promote`.

*Applies to: RHEL / Ubuntu LTS*
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

- **Access:** root or sudo-capable account on target hosts
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
 00:00:00.234567
(1 row)

waiting for server to promote.... done
server promoted

 pg_is_in_recovery 
-------------------
 f
(1 row)

       current_time        
---------------------------
 2024-01-15 14:32:18.456789+00
(1 row)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL: the database system is not ready` | Wait 10-15 seconds after promotion completes before running verification queries, as PostgreSQL needs time to finish recovery. |
    | `pg_ctl: could not open PID file "/var/lib/postgresql/data/postmaster.pid": No such file or directory` | Ensure PostgreSQL is running on the standby with `systemctl start postgresql` before attempting promotion. |
    | `permission denied` | Run all `pg_ctl` and file operations as the `postgres` user with `sudo -u postgres` or switch to that user first. |
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
ERROR 1064 (42000) at line 1: You have an error in your statement; check the manual that corresponds to your MySQL server version for the syntax near 'ts) VALUES(now())' at line 1
OK
 pid | state  | wait_event_type |                             query
-----+--------+-----------------+----------------------------------------------------------------
 1247 | active | IO              | SELECT * FROM orders WHERE customer_id = $1 AND status = 'pending'
 1389 | active | Lock            | UPDATE inventory SET quantity = quantity - 1 WHERE sku = 'ABC123'
 1456 | idle   | NULL            | <IDLE>
(3 rows)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: could not translate host name "<new-primary>" to address: Name or service not known` | Replace `<new-primary>` with the actual hostname or IP address of the new primary server. |
    | `ERROR 1045 (28000): Access denied for user 'appuser'@'<new-primary>'` | Verify the MySQL user credentials and that the host is listed in the user's allowed hosts (check `mysql.user` table or use `GRANT` to add the host). |
    | `curl: (7) Failed to connect to <app-endpoint> port 443: Connection refused` | Confirm the application endpoint is running and accessible; check firewall rules and application service status with `systemctl status`. |
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Postgresql — Health Checks](../health-checks/)
- [Postgresql — CLI Reference](../cli-reference/)
- [Postgresql — Common Issues](../../troubleshooting/common-issues/)
