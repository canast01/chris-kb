---
tags:
  - troubleshooting
  - windows
search:
  boost: 1.5
---
# SQL Server — Diagnostics

<div class="kb-summary">
SQL Server diagnostics — error log, Activity Monitor equivalent via DMVs, blocking chain analysis, AG health, tempdb contention, and Query Store.

*Applies to: Windows Server 2019 / 2022*
</div>

```text
┌────────────────────────────────────── SQL Server — Diagnostics ───────────────────────────────────────┐
│                                                                                                       │
│   Primary diagnostic sources: error log (sp_readerrorlog), DMVs, Windows Event Log                    │
│   Blocking: sys.dm_exec_requests WHERE blocking_session_id > 0; KILL head blocker to unblock          │
│   AG health: sys.dm_hadr_availability_replica_states; log_send_queue_size = bytes not sent            │
│                                                                                                       │
│   Error log                                                                                           │
│   EXEC sp_readerrorlog; filter: EXEC sp_readerrorlog 0, 1, 'Login failed'                             │
│   Windows Event Log: Get-EventLog -LogName Application -Source MSSQLSERVER -Newest 50                 │
│                                                                                                       │
│   Active requests and blocking                                                                        │
│   sys.dm_exec_requests: session_id, status, blocking_session_id, wait_type, wait_time                 │
│   CROSS APPLY sys.dm_exec_sql_text(sql_handle): gets query text per request                           │
│   KILL <session_id>: terminates a session; use to release blocking locks                              │
│                                                                                                       │
│   AG and tempdb                                                                                       │
│   sys.dm_hadr_availability_replica_states: role, sync state, health per replica                       │
│   sys.dm_hadr_database_replica_states: log_send_queue_size, redo_queue_size                           │
│   tempdb contention: sys.dm_os_wait_stats WHERE wait_type LIKE 'PAGELATCH%'                           │
│                                                                                                       │
│   Query Store (SQL 2016+)                                                                             │
│   ALTER DATABASE app_prod SET QUERY_STORE = ON; captures plan history per query                       │
│   sys.query_store_runtime_stats: avg_duration, count_executions per plan                              │
│                                                                                                       │
│   Key terms:                                                                                          │
│   sp_readerrorlog = reads SQL Server error log; ERRORLOG file on disk                                 │
│   DMV            = Dynamic Management View; sys.dm_* views exposing live SQL Server state             │
│   PAGELATCH      = wait for in-memory data page access; high counts = tempdb contention               │
│   Query Store    = built-in workload tracking; captures execution plans and regressions               │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Local Administrator or Domain Admin on target hosts
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## Error Log

```sql
-- Current error log
EXEC sp_readerrorlog;

-- Filter for errors and warnings
EXEC sp_readerrorlog 0, 1, 'error';
EXEC sp_readerrorlog 0, 1, 'Login failed';
```

```powershell
# Windows Event Log — Application
Get-EventLog -LogName Application -Source "MSSQLSERVER" -Newest 50 |
  Format-Table TimeGenerated, EntryType, Message -Wrap
```

## Active Requests and Blocking

```sql
-- All active non-background requests
SELECT r.session_id, r.status, r.blocking_session_id,
       r.wait_type, r.wait_time/1000 AS wait_sec,
       r.open_transaction_count, DB_NAME(r.database_id) AS db,
       left(t.text, 100) AS query
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.session_id > 50
ORDER BY r.wait_time DESC;

-- Identify head blocker
SELECT session_id, blocking_session_id, wait_type, wait_time/1000 AS wait_sec
FROM sys.dm_exec_requests
WHERE blocking_session_id > 0;

-- Kill a session
KILL <session_id>;
```

## AG Availability Group Health

```sql
SELECT ag.name, ar.replica_server_name, rs.role_desc,
       rs.synchronization_state_desc, rs.synchronization_health_desc,
       drs.log_send_queue_size, drs.redo_queue_size, rs.last_commit_time
FROM sys.dm_hadr_availability_replica_states rs
JOIN sys.availability_replicas ar ON rs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
LEFT JOIN sys.dm_hadr_database_replica_states drs ON drs.replica_id = rs.replica_id;
```

## tempdb Contention

```sql
-- Check for page latch contention (2:1:1, 2:1:3)
SELECT wait_type, waiting_tasks_count, wait_time_ms
FROM sys.dm_os_wait_stats
WHERE wait_type LIKE 'PAGELATCH%'
ORDER BY wait_time_ms DESC;
```

## Query Store (SQL 2016+)

```sql
-- Enable Query Store
ALTER DATABASE app_prod SET QUERY_STORE = ON;

-- Top regressed queries
SELECT TOP 10 q.query_id, qt.query_sql_text,
       rs.avg_duration/1000 AS avg_ms, rs.count_executions
FROM sys.query_store_query q
JOIN sys.query_store_query_text qt ON qt.query_text_id = q.query_text_id
JOIN sys.query_store_plan p ON p.query_id = q.query_id
JOIN sys.query_store_runtime_stats rs ON rs.plan_id = p.plan_id
ORDER BY rs.avg_duration DESC;
```

---

## Verify resolution

- Confirm the original symptom no longer occurs
- Check logs for any residual errors related to the issue
- Monitor for 10–15 minutes to confirm the fix is stable
