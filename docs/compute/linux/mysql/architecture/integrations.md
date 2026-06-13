---
tags:
  - architecture
  - linux
---
# MySQL / MariaDB — Integrations

<div class="kb-summary">
MySQL integration points — application connectors (JDBC, ODBC, Python, PHP), ProxySQL, Percona Monitoring, replication to replica sets, and backup tool integration.
</div>

## Application Connectors

| Language | Connector | Notes |
|---|---|---|
| Java | `mysql-connector-j` | Use `autoReconnect=false`; handle `SQLTransientConnectionException` |
| Python | `mysql-connector-python` or `PyMySQL` | Use connection pooling; `mysql.connector.pooling.MySQLConnectionPool` |
| PHP | `mysqli` or PDO with `pdo_mysql` | Prefer PDO for portability |
| .NET | `MySql.Data` (Oracle) or `MySqlConnector` | Use `MySqlConnector` for async support |
| Go | `go-sql-driver/mysql` | Set `parseTime=true` in DSN |

**Connection string pattern:**
```text
mysql://<user>:<password>@<host>:<port>/<database>?charset=utf8mb4
```

## ProxySQL Integration

ProxySQL sits between application and MySQL:
- Routes `SELECT` to read replicas, `INSERT`/`UPDATE`/`DELETE` to primary
- Handles failover transparently without app changes
- Connection multiplexing reduces per-connection overhead

Key tables: `mysql_servers`, `mysql_replication_hostgroups`, `mysql_query_rules`

## Monitoring Integration

| Tool | Integration |
|---|---|
| Prometheus | `mysqld_exporter` — exposes `/metrics`; scrape port 9104 |
| Percona PMM | Agent installed on DB host; connects to PMM Server |
| Nagios/Icinga | `check_mysql` / `check_mysql_query` plugins |
| Datadog | MySQL integration via DD agent; auto-discovers metrics |

Key metrics to export: `Threads_connected`, `Queries`, `Innodb_buffer_pool_read_requests`, `Slave_SQL_Running_State`

## Backup Tool Integration

| Tool | Type | Notes |
|---|---|---|
| `mysqldump` | Logical | Portable; slow for large DBs; use `--single-transaction` for InnoDB |
| Percona XtraBackup | Physical hot backup | No table locks; incremental supported; faster restore |
| MySQL Enterprise Backup | Physical | Oracle commercial; streaming to S3 supported |
| `mysqlbinlog` | Binlog backup | Used for PITR; replicate binlogs to backup host continuously |
