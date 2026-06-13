---
tags:
  - architecture
  - linux
---
# PostgreSQL — Integrations

<div class="kb-summary">
PostgreSQL integration points — application connectors (JDBC, psycopg2, asyncpg), PgBouncer, monitoring exporters, logical replication targets, and backup tools.

*Applies to: PostgreSQL 15.x / 16.x*
</div>

```text
┌────────────────────────────────────── PostgreSQL — Integrations ──────────────────────────────────────┐
│                                                                                                       │
│   PostgreSQL integrates with application connectors, connection poolers, monitoring, and backup tools │
│   PgBouncer sits between app and PostgreSQL; reduces connection overhead significantly                │
│   Prometheus postgres_exporter exposes 40+ metrics; used with Grafana for dashboards                  │
│                                                                                                       │
│   Application connectors                                                                              │
│   JDBC (Java): postgresql JDBC driver; standard URL: jdbc:postgresql://host/db                        │
│   psycopg2 (Python 2/3): most common Python adapter; supports async via asyncpg                       │
│   asyncpg (Python): high-performance async driver; 3-10× faster than psycopg2 for bulk ops            │
│   libpq (C): native PostgreSQL client library; basis for most language adapters                       │
│                                                                                                       │
│   Connection pooling                                                                                  │
│   PgBouncer: session/transaction/statement pooling modes; configure in pgbouncer.ini                  │
│   pgpool-II: pooling + load balancing + replication management; more complex than PgBouncer           │
│                                                                                                       │
│   Monitoring                                                                                          │
│   postgres_exporter: exposes pg_stat_* views as Prometheus metrics                                    │
│   Key metrics: pg_stat_activity (active queries), pg_stat_replication (lag), pg_stat_bgwriter         │
│   pgBadger: log analyser; generates HTML reports from PostgreSQL log files                            │
│                                                                                                       │
│   Backup tools                                                                                        │
│   pgBackRest: parallel backup and restore; supports differential and incremental backups              │
│   pg_dump / pg_basebackup: logical (per-DB) and physical (whole cluster) backup utilities             │
│   Barman: backup and recovery manager; enterprise-grade WAL archiving and PITR                        │
│                                                                                                       │
│   Key terms:                                                                                          │
│   asyncpg      = high-performance async Python driver using PostgreSQL binary protocol                │
│   postgres_exporter = Prometheus exporter; exposes PostgreSQL metrics for Grafana dashboards          │
│   pgBackRest   = backup tool with parallel WAL archiving, delta restore, and encryption support       │
│   pg_stat_replication = system view showing streaming replication lag per standby                     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

---

## See also

- [Postgresql — How It Works](how-it-works/)
- [Postgresql — Design Standards](design-standards/)
