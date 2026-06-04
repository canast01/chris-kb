# Database — Replication Check

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
