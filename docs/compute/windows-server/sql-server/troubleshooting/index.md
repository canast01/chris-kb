---
tags:
  - troubleshooting
  - windows
---
# SQL Server — Troubleshooting

<div class="kb-summary">
Common issues, diagnostics, and escalation.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌──────────────────────────────────── SQL Server — Troubleshooting ─────────────────────────────────────┐
│                                                                                                       │
│   Three sub-sections: common issues (quick fixes), diagnostics (deep analysis), escalation            │
│   Start with error log (sp_readerrorlog) and sys.dm_exec_requests before deeper investigation         │
│   Escalate when: service down, AG primary lost, log full, corruption, or blocking > 10 min            │
│                                                                                                       │
│   Common issues                                                                                       │
│   Blocking: sys.dm_exec_requests WHERE blocking_session_id > 0; KILL head blocker                     │
│   Log full: BACKUP LOG db; then investigate log growth cause (long transaction, no log backups)       │
│   AG not synchronising: check log_send_queue and network between replicas                             │
│   Slow queries: enable Query Store; find regressions in sys.query_store_runtime_stats                 │
│                                                                                                       │
│   Diagnostics entry points                                                                            │
│   Error log: sp_readerrorlog; Windows Application Event Log for service crashes                       │
│   sys.dm_exec_requests: all active requests with blocking chains and wait types                       │
│   sys.dm_hadr_availability_replica_states: AG health, sync state, log send queue                      │
│   sys.dm_os_wait_stats: top wait types reveal system-wide bottlenecks                                 │
│                                                                                                       │
│   Key terms:                                                                                          │
│   sp_readerrorlog = reads SQL Server ERRORLOG file; filterable by keyword and log number              │
│   wait_type       = identifies what a session is waiting for; PAGEIOLATCH_SH = disk I/O               │
│   log_send_queue  = bytes of transaction log not yet sent to AG secondary replica                     │
│   Query Store     = built-in query performance tracking; catches plan regressions                     │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">
  <a class="kb-card" href="common-issues/">Common Issues</a>
  <a class="kb-card" href="diagnostics/">Diagnostics</a>
  <a class="kb-card" href="escalation/">Escalation</a>
</div>

