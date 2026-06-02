# Database Health Check


<div class="kb-summary">
Verify database availability, connectivity, replication status, and resource utilization across common platforms.
</div>

## Quick Status — All Platforms

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

## SQL Server Health Checks

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

## Connectivity Test

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

## Health Check Thresholds

| Metric | Warning | Critical |
|---|---|---|
| Active connections | > 80% of max_connections | > 90% of max_connections |
| Replication lag | > 30 seconds | > 5 minutes |
| Long-running queries | > 5 minutes | > 30 minutes |
| Dead tuple ratio (PG) | > 20% | > 50% (vacuum required) |
| Buffer pool hit ratio | < 99% | < 95% |

## Log Locations

| Platform | Log Path |
|---|---|
| PostgreSQL | `/var/log/postgresql/` or `pg_lsclusters` |
| MySQL | `/var/log/mysql/error.log` |
| MariaDB | `/var/log/mariadb/mariadb.log` |
| SQL Server (Linux) | `/var/opt/mssql/log/errorlog` |

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Cannot connect | Port reachable? Service running? | `nc -zv`; `systemctl status` |
| High connection count | Application connection pool leak? | Check app logs; restart connection pool |
| Replication stopped | I/O or SQL thread stopped | `SHOW SLAVE STATUS\G`; check relay log errors |
| Slow queries | Missing indexes? Locking? | Run explain plan; check `pg_stat_activity` / `dm_exec_requests` |
| High dead tuples (PG) | Autovacuum falling behind | Run `VACUUM ANALYZE <table>` manually |
