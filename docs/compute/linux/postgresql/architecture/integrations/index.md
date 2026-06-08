# PostgreSQL — Integrations

<div class="kb-summary">
PostgreSQL integration points — application connectors (JDBC, psycopg2, asyncpg), PgBouncer, monitoring exporters, logical replication targets, and backup tools.
</div>

## Application Connectors

| Language | Library | Notes |
|---|---|---|
| Python | `psycopg2` / `psycopg3` | Synchronous; use `psycopg2.pool.ThreadedConnectionPool` |
| Python async | `asyncpg` | Async; fastest; recommended for FastAPI/asyncio apps |
| Java | `postgresql-jdbc` | Connection URL: `jdbc:postgresql://host/db` |
| Node.js | `pg` / `node-postgres` | Use `Pool` class; avoid single `Client` in production |
| Go | `pgx` | Preferred over `lib/pq`; supports batch queries |
| .NET | `Npgsql` | ADO.NET provider; supports async |

## PgBouncer Integration

```ini
# /etc/pgbouncer/pgbouncer.ini
[databases]
app_prod = host=127.0.0.1 port=5432 dbname=app_prod

[pgbouncer]
listen_port = 6432
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 25
auth_type = scram-sha-256
```

## Monitoring Integration

| Tool | Method |
|---|---|
| Prometheus | `postgres_exporter` on port 9187; scrape `/metrics` |
| pgBadger | Log analyser; parses PostgreSQL log files |
| Datadog | `postgres` integration via DD agent |
| AWS CloudWatch | RDS PostgreSQL publishes metrics natively |

Key metrics: `pg_stat_activity` (connections), replication lag, `pg_database_size`, dead tuples (bloat)

## Logical Replication

```sql
-- Publish a table to downstream consumers
CREATE PUBLICATION my_pub FOR TABLE orders, customers;

-- Subscribe from downstream DB
CREATE SUBSCRIPTION my_sub
  CONNECTION 'host=primary dbname=app_prod user=repl'
  PUBLICATION my_pub;
```

## Backup Tools

| Tool | Type | Notes |
|---|---|---|
| `pg_basebackup` | Physical base backup | Streaming; supports `--checkpoint=fast` |
| `pg_dump` / `pg_restore` | Logical | Portable; table/schema selective |
| `pgBackRest` | Physical + WAL | Incremental; compression; S3 target; PITR |
| `Barman` | Physical + WAL | Central backup server; retention policies |
