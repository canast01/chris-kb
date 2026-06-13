---
tags:
  - architecture
  - linux
---
# PostgreSQL — Design Standards

<div class="kb-summary">
PostgreSQL design standards — HA patterns (streaming + Patroni), connection pooling, sizing guidelines, schema conventions, and backup requirements.
</div>

```text
┌──────────────────────────────────── PostgreSQL — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│   Production minimum: streaming replication + Patroni for HA + PgBouncer for connection pooling       │
│   Patroni automates failover via etcd/Consul/ZooKeeper consensus; eliminates split-brain              │
│   Connection pooling is mandatory for applications with >50 concurrent connections                    │
│                                                                                                       │
│   HA topologies                                                                                       │
│   Streaming replication (sync): primary waits for standby WAL write before commit; zero data loss     │
│   Streaming replication (async): primary commits without waiting; standby may lag                     │
│   Patroni + etcd: 3-node DCS for leader election; auto-promotes standby on primary failure            │
│   pgpool-II: connection pooling + replication management; heavier than PgBouncer                      │
│                                                                                                       │
│   Connection pooling                                                                                  │
│   PgBouncer: lightweight; modes = session (default), transaction, statement                           │
│   Transaction mode: connection returned to pool after each transaction; most efficient                │
│   max_client_conn: total clients PgBouncer accepts; default_pool_size: connections to PostgreSQL      │
│                                                                                                       │
│   Sizing guidelines                                                                                   │
│   shared_buffers: 25% of RAM (PostgreSQL caches here first)                                           │
│   effective_cache_size: 75% of RAM (hint to planner for index scan cost estimation)                   │
│   max_connections: set low (100-200); rely on PgBouncer for client multiplexing                       │
│   work_mem: per sort/hash operation; RAM usage = max_connections × work_mem at peak                   │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Patroni      = Python HA template; uses DCS for leader election and failover automation             │
│   WAL          = Write-Ahead Log; stream of change records; base for replication and PITR             │
│   PgBouncer    = lightweight connection pooler; sits between app and PostgreSQL                       │
│   shared_buffers = PostgreSQL shared memory for caching table and index pages                         │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## High-Availability Topologies

| Pattern | Description | Use case |
|---|---|---|
| Streaming replication (1+1) | Primary + hot standby; manual failover with `pg_promote` | Simple HA; minimal tooling |
| Patroni | Streaming + etcd/ZooKeeper; automatic failover; leader election | Production HA; cloud-native |
| Pgpool-II | Connection proxy; read splitting; failover | Simpler proxy; less common now |
| Citus | Distributed PostgreSQL; sharding | Large-scale analytics |

## Connection Pooling (Required in Production)

PgBouncer between app and PostgreSQL:
- `transaction` mode: best performance; connection returned after each transaction
- `session` mode: safer; connection held for full client session
- Typical: 20–100 PgBouncer connections per PostgreSQL max_connections

## Sizing Guidelines

| Resource | Baseline |
|---|---|
| `shared_buffers` | 25% of RAM |
| `effective_cache_size` | 75% of RAM |
| `work_mem` | RAM × 0.25 ÷ max_connections |
| `max_connections` | 100–200; use PgBouncer to serve more app threads |

## Naming Conventions

- Databases: lowercase, underscores — `app_prod`, `reporting`
- Schemas: separate per app — `app`, `audit`, `reporting`
- Tables: lowercase plural — `users`, `order_lines`
- Indexes: `ix_<table>_<columns>` — `ix_users_email`

## Backup Requirements

| Tier | Method | RPO |
|---|---|---|
| Continuous WAL archiving | `archive_command` → S3/NFS | Seconds |
| Daily base backup | `pg_basebackup` | 24 h |
| PITR capability | WAL + base backup together | Any point |

Test restore to separate instance monthly. `pg_restore` time must be < RTO.
