# SQL Server — Escalation

<div class="kb-summary">
SQL Server escalation criteria — P1/P2 indicators, evidence bundle before engaging Microsoft CSS or DBA team, and AG failover decision criteria.
</div>

## Escalation Thresholds

| Condition | Severity | Action |
|---|---|---|
| SQL Server service down / unreachable | P1 | Page DBA on-call immediately |
| AG primary down; no automatic failover | P1 | Manual failover; page DBA |
| Blocking chain > 10 min; app impact | P1 | KILL head blocker; page DBA |
| Transaction log full; writes failing | P1 | Backup log; investigate log growth |
| Corruption detected (suspect database) | P1 | Stop writes; do not restore without DBA |
| Disk > 90% on data or log volume | P1 | Emergency cleanup; page DBA |
| AG sync degraded; RPO at risk | P2 | Alert DBA; investigate log send queue |
| Repeated deadlocks | P2 | Capture deadlock graph; alert DBA |

## Evidence to Collect

```sql
-- 1. Error log (last 200 entries)
EXEC sp_readerrorlog;

-- 2. Active requests and blocking
SELECT r.session_id, r.blocking_session_id, r.wait_type, r.wait_time,
       left(t.text, 100) AS query
FROM sys.dm_exec_requests r
CROSS APPLY sys.dm_exec_sql_text(r.sql_handle) t
WHERE r.session_id > 50;

-- 3. AG health
SELECT ag.name, rs.role_desc, rs.synchronization_health_desc,
       drs.log_send_queue_size, drs.redo_queue_size
FROM sys.dm_hadr_availability_replica_states rs
JOIN sys.availability_replicas ar ON rs.replica_id = ar.replica_id
JOIN sys.availability_groups ag ON ar.group_id = ag.group_id
LEFT JOIN sys.dm_hadr_database_replica_states drs ON drs.replica_id = rs.replica_id;

-- 4. Disk usage
EXEC xp_fixeddrives;

-- 5. Log space usage
DBCC SQLPERF(LOGSPACE);
```

## AG Manual Failover

```sql
-- On the target secondary:
ALTER AVAILABILITY GROUP [AG_Name] FAILOVER;

-- Forced failover (data loss possible — use only when primary is completely lost)
ALTER AVAILABILITY GROUP [AG_Name] FORCE_FAILOVER_ALLOW_DATA_LOSS;
```

## Information for Microsoft CSS

- SQL Server version and edition (`SELECT @@VERSION`)
- Error log (from `sp_readerrorlog` or Event Viewer)
- Windows System/Application event logs around the time of incident
- AG topology diagram and database list
- Recent changes (patches, schema changes, load spikes)
