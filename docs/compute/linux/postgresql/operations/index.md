---
tags:
  - linux
  - operations
---
# PostgreSQL — Operations

<div class="kb-summary">
Health checks, procedures, CLI, backup/restore, upgrades, and scripts.
</div>

```text
┌─────────────────────────────────────── PostgreSQL — Operations ───────────────────────────────────────┐
│                                                                                                       │
│   Six operational sub-sections covering the full DBA day-to-day workflow                              │
│   Backup/restore and health checks are the highest-priority regular activities                        │
│   Install/upgrade covers both minor (in-place) and major (pg_upgrade) version changes                 │
│                                                                                                       │
│   Sub-sections                                                                                        │
│   Health Checks: pg_stat_activity, replication lag, autovacuum status, disk usage checks              │
│   Procedures: common DBA procedures — switchover, vacuum, connection resets                           │
│   CLI Reference: psql, pg_dump, pg_restore, pg_basebackup, vacuumdb quick reference                   │
│   Backup/Restore: pg_basebackup, WAL archiving, pgBackRest, PITR restore procedures                   │
│   Install/Upgrade: minor in-place update, major pg_upgrade workflow, post-upgrade steps               │
│   Scripts: automation scripts for backup, replication monitoring, and bloat reporting                 │
│                                                                                                       │
│   Key terms:                                                                                          │
│   pg_basebackup = physical streaming backup of the entire PostgreSQL data directory                   │
│   PITR          = Point-In-Time Recovery; requires WAL archive and a base backup                      │
│   pg_upgrade    = in-place data directory migration between major PostgreSQL versions                 │
│   vacuumdb      = CLI wrapper for VACUUM ANALYZE; used for post-upgrade statistics rebuild            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="health-checks/">Health Checks</a>
  <a class="kb-card" href="procedures/">Procedures</a>
  <a class="kb-card" href="cli-reference/">Cli Reference</a>
  <a class="kb-card" href="backup-restore/">Backup Restore</a>
  <a class="kb-card" href="install-upgrade/">Install Upgrade</a>
  <a class="kb-card" href="scripts/">Scripts</a>
</div>
