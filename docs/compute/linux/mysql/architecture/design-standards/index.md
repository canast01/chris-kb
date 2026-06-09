# MySQL / MariaDB — Design Standards

<div class="kb-summary">
MySQL design standards — HA topology choices, replication sizing, InnoDB tuning baselines, naming conventions, and backup strategy requirements.
</div>

```text
┌────────────────────────────────────── MySQL — Design Standards ───────────────────────────────────────┐
│                                                                                                       │
│   Design decisions made before deployment define reliability, recovery time, and operational cost     │
│   Minimum production standard: semi-sync replication + automated failover + nightly backup            │
│   InnoDB Cluster (Group Replication + MySQL Router) for zero-manual-failover HA                       │
│                                                                                                       │
│   HA topology selection                                                                               │
│   Async 1+1: primary + one replica; manual failover; use for dev/test or low RPO tolerance            │
│   Semi-sync 1+1: primary ACKs replica before commit; no data loss on primary crash                    │
│   Group Replication: multi-primary or single-primary; auto-failover; high write availability          │
│   InnoDB Cluster: Group Replication + MySQL Router + MySQL Shell; fully managed HA                    │
│   ProxySQL: connection proxy; read/write split; app-transparent failover routing                      │
│                                                                                                       │
│   InnoDB tuning baselines                                                                             │
│   innodb_buffer_pool_size: 60-80% of total RAM; single most impactful setting                         │
│   innodb_log_file_size: 1-4 GB for write-heavy workloads; larger = faster writes, slower recovery     │
│   innodb_flush_log_at_trx_commit=1: full ACID; set to 2 for write performance if durability permits   │
│   max_connections: set to expected peak concurrency; each connection uses ~1 MB RAM                   │
│                                                                                                       │
│   Naming conventions                                                                                  │
│   Database: lowercase_underscore (app_db, reporting_db); no spaces, no uppercase                      │
│   Tables: plural nouns (users, orders, audit_log); prefix with schema if multi-tenant                 │
│   Service accounts: svc_<app>_rw (read-write) and svc_<app>_ro (read-only) per application            │
│                                                                                                       │
│   Key terms:                                                                                          │
│   RPO           = Recovery Point Objective; max acceptable data loss (semi-sync = near zero)          │
│   RTO           = Recovery Time Objective; max acceptable downtime (InnoDB Cluster = seconds)         │
│   innodb_buffer_pool = in-memory InnoDB page cache; sizing directly controls I/O load                 │
│   MySQL Router  = lightweight proxy included with InnoDB Cluster; routes to current primary           │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## High-Availability Topologies

| Pattern | Description | Use case |
|---|---|---|
| Async replication (1+1) | Primary + 1 replica; manual failover | Dev/test; low RPO tolerance |
| Semi-sync (1+1) | Primary ACKs replica before commit | Production where data loss is unacceptable |
| Group Replication | Multi-primary or single-primary cluster; auto-failover | High write availability |
| InnoDB Cluster | Group Replication + MySQL Router + MySQL Shell | Fully managed HA with automatic routing |
| ProxySQL | Connection proxy; routes read/write split automatically | Any topology where app must not change on failover |

## Sizing Guidelines

| Resource | Baseline |
|---|---|
| `innodb_buffer_pool_size` | 70–80% of dedicated DB server RAM |
| CPU | 4+ cores; InnoDB scales well to 16 cores |
| Storage | IOPS-optimised disk; SSD required for production |
| Log volume | Separate mount for `/var/lib/mysql`; avoid sharing with OS |

## Naming Conventions

- Schema names: lowercase, underscores — `app_prod`, `reporting_dw`
- Tables: lowercase singular nouns — `user`, `order_line`
- Indexes: `idx_<table>_<columns>` — `idx_user_email`
- Users: `<app>_rw` (read-write), `<app>_ro` (read-only), `<app>_admin`

## Backup Strategy Requirements

| Tier | Method | RTO | RPO |
|---|---|---|---|
| Daily full | `mysqldump` or Percona XtraBackup | Hours | 24 h |
| Hourly logical | Binlog backup | Minutes | 1 h |
| Point-in-time | Binlog + full restore | Variable | Seconds |

Always test restores quarterly. Store backups off the DB host.

## Schema Design Rules

- Every table must have a primary key (use `AUTO_INCREMENT BIGINT UNSIGNED`)
- Avoid `TEXT`/`BLOB` in frequently joined tables; store in separate table or object storage
- Use `DATETIME` not `TIMESTAMP` for dates beyond 2038
- Enable `innodb_strict_mode` to catch row size violations at DDL time
