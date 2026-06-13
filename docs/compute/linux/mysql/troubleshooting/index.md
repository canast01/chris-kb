---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
---
# MySQL / MariaDB — Troubleshooting

<div class="kb-summary">
Common issues, diagnostics, and escalation.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌────────────────────────────────── MySQL — Troubleshooting Reference ──────────────────────────────────┐
│                                                                                                       │
│   Three sub-sections: common issues (quick fixes), diagnostics (deep investigation), escalation       │
│   Start with: error log, SHOW PROCESSLIST, SHOW REPLICA STATUS, and InnoDB engine status              │
│   Escalate when: replication is stopped with errors, OOM crashes, or data corruption is suspected     │
│                                                                                                       │
│   Common issues                                                                                       │
│   Too many connections: raise max_connections or add ProxySQL connection pooling                      │
│   Replication lag: check Seconds_Behind_Source; look for long-running queries on primary              │
│   Slow queries: enable slow_query_log; analyse with pt-query-digest; add missing indexes              │
│   Can't connect: check bind-address, firewall port 3306, and user@host account scope                  │
│                                                                                                       │
│   Diagnostics                                                                                         │
│   Error log: /var/log/mysql/error.log or /var/log/mysqld.log — first stop for crashes and errors      │
│   SHOW ENGINE INNODB STATUS: lock waits, deadlocks, buffer pool stats, active transactions            │
│   performance_schema: query events_statements_summary_by_digest for top queries by total time         │
│   processlist: identify blocking queries; KILL <id> to release locks                                  │
│                                                                                                       │
│   Key terms:                                                                                          │
│   SHOW ENGINE INNODB STATUS = prints InnoDB internal state including deadlock and lock wait info      │
│   Seconds_Behind_Source = replica lag in seconds; non-zero means replica is behind primary            │
│   performance_schema = MySQL internal schema with runtime instrumentation and wait events             │
│   deadlock      = two transactions each holding locks the other needs; MySQL auto-resolves            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="common-issues/">Common Issues</a>
  <a class="kb-card" href="diagnostics/">Diagnostics</a>
  <a class="kb-card" href="escalation/">Escalation</a>
</div>

