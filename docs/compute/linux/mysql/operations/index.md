# MySQL / MariaDB — Operations

<div class="kb-summary">
Health checks, procedures, CLI, backup/restore, upgrades, and scripts.
</div>

```text
┌──────────────────────────────────── MySQL — Operations Reference ─────────────────────────────────────┐
│                                                                                                       │
│   Six operational sub-sections: health checks, procedures, CLI reference, backup/restore, upgrades    │
│   Daily operations: monitor replication lag, slow queries, connection count, and buffer pool hit rate │
│   Backup strategy must cover: nightly full + binlog retention for PITR                                │
│                                                                                                       │
│   Health checks                                                                                       │
│   Replication lag: SHOW REPLICA STATUS; Seconds_Behind_Source should be 0 or near 0                   │
│   Buffer pool hit rate: (1 - innodb_buffer_pool_reads/innodb_buffer_pool_read_requests) * 100         │
│   Connection pressure: Threads_connected vs max_connections; alert at 80%                             │
│   Slow query log: set long_query_time=1; review with mysqldumpslow or pt-query-digest                 │
│                                                                                                       │
│   Backup and restore                                                                                  │
│   Logical: mysqldump --single-transaction --routines --triggers; slow on large databases              │
│   Physical hot backup: xtrabackup --backup; faster restore; requires Percona XtraBackup tool          │
│   PITR: restore full backup + replay binlogs up to the recovery point time                            │
│                                                                                                       │
│   Procedures                                                                                          │
│   Promote replica: STOP REPLICA; check lag = 0; set read_only=OFF; redirect app connections           │
│   Add replica: xtrabackup + binlog position or GTID; START REPLICA; verify lag catches up             │
│   Schema change: use pt-online-schema-change or gh-ost for non-blocking ALTER on live tables          │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Seconds_Behind_Source = replication lag metric; seconds replica is behind primary                   │
│   xtrabackup   = Percona tool for online physical hot backup without locking tables                   │
│   PITR         = Point-In-Time Recovery; restore backup then replay binlogs to target time            │
│   pt-query-digest = Percona toolkit tool; analyses slow query log and ranks by total time             │
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
