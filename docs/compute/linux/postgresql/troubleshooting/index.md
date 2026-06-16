---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
---
# PostgreSQL — Troubleshooting

<div class="kb-summary">
PostgreSQL troubleshooting hub: replication failures, bloat, lock contention, crash recovery, and escalation path to EnterpriseDB or community support.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌──────────────────────────────────── PostgreSQL — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   Three sub-sections: common issues (quick fixes), diagnostics (deep analysis), escalation            │
│   Start with error log, pg_stat_activity, and replication status before deeper investigation          │
│   Escalate when: replication broken, OOM crash, connection exhaustion, or corruption                  │
│                                                                                                       │
│   Common issues                                                                                       │
│   Too many connections: raise max_connections or add PgBouncer connection pooling layer               │
│   Replication lag: check pg_stat_replication; look for long-running queries on primary                │
│   Slow queries: enable pg_stat_statements; find top queries by total_exec_time                        │
│   Can't connect: check pg_hba.conf, listen_addresses, firewall port 5432, user host scope             │
│                                                                                                       │
│   Diagnostics entry points                                                                            │
│   Error log: first stop for crashes, PANIC entries, and authentication failures                       │
│   pg_stat_activity: live query view; identify blocking sessions and long-running queries              │
│   pg_stat_statements: cumulative stats per query fingerprint; surface expensive queries               │
│   pg_stat_user_tables: dead tuples and autovacuum timestamps; detect table bloat                      │
│                                                                                                       │
│   Key terms:                                                                                          │
│   pg_hba.conf   = authentication rules; wrong entry is a common cause of connection failures          │
│   listen_addresses = controls which interfaces PostgreSQL listens for incoming connections            │
│   pg_stat_statements = query tracking extension; preloaded in shared_preload_libraries                │
│   dead tuples   = old row versions from MVCC; excessive count indicates autovacuum is behind          │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="common-issues/">Common Issues</a>
  <a class="kb-card" href="diagnostics/">Diagnostics</a>
  <a class="kb-card" href="escalation/">Escalation</a>
</div>

