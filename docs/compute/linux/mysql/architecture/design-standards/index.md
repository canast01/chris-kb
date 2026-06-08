# MySQL / MariaDB — Design Standards

<div class="kb-summary">
MySQL design standards — HA topology choices, replication sizing, InnoDB tuning baselines, naming conventions, and backup strategy requirements.
</div>

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
