---
tags:
  - linux
  - operations
---
# PostgreSQL — Scripts

<div class="kb-summary">
PostgreSQL automation scripts — base backup, WAL archiving, replication lag monitor, bloat report, long-running transaction alert, and connection trend logging.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌────────────────────────────────── PostgreSQL — Operational Scripts ───────────────────────────────────┐
│                                                                                                       │
│   Automation scripts for routine PostgreSQL operational tasks                                         │
│   Replication lag monitor alerts when replica falls more than 30 seconds behind primary               │
│   Bloat report uses pg_stat_user_tables to identify tables with excessive dead tuples                 │
│                                                                                                       │
│   Nightly base backup                                                                                 │
│   pg_basebackup -U replication -D /backup/postgresql/$(date +%F) -Ft -z -P -Xs                        │
│   Rotation: find /backup/postgresql/ -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +                 │
│                                                                                                       │
│   Replication lag monitor                                                                             │
│   Queries pg_last_xact_replay_timestamp() on replica; alerts if lag exceeds 30 seconds                │
│   Sends email alert with hostname; adaptable to PagerDuty or Slack webhook                            │
│                                                                                                       │
│   Bloat report (SQL)                                                                                  │
│   Queries pg_stat_user_tables for n_dead_tup / (n_live_tup + n_dead_tup) ratio per table              │
│   Tables above 20% dead tuple ratio should be scheduled for VACUUM ANALYZE                            │
│                                                                                                       │
│   Other scripts                                                                                       │
│   Long-running transactions: pg_stat_activity WHERE duration > 5 minutes                              │
│   Unused indexes: pg_stat_user_indexes WHERE idx_scan = 0 (excludes primary keys)                     │
│   Connection trend: logs timestamp + connection count to CSV for capacity planning                    │
│                                                                                                       │
│   Key terms:                                                                                          │
│   -Ft           = tar format output; -z gzip compression; -Xs stream WAL during backup                │
│   n_dead_tup    = dead tuple count per table; high values indicate autovacuum falling behind          │
│   pg_last_xact_replay_timestamp = timestamp of last WAL record applied on standby                     │
│   idx_scan      = index usage counter; zero means the index has never been used in queries            │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Nightly Base Backup

```bash
#!/bin/bash
BACKUP_DIR="/backup/postgresql/$(date +%F)"
mkdir -p "$BACKUP_DIR"
pg_basebackup -U replication -D "$BACKUP_DIR" -Ft -z -P -Xs
find /backup/postgresql/ -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +
echo "Base backup complete: $BACKUP_DIR"
```

## Replication Lag Monitor

```bash
#!/bin/bash
LAG=$(psql -U monitor -Atc \
  "SELECT EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))::int;" 2>/dev/null)
if [ -n "$LAG" ] && [ "$LAG" -gt 30 ]; then
  echo "WARN: PG replica lag ${LAG}s on $(hostname)" | \
    mail -s "PostgreSQL Replication Alert" dba@example.com
fi
```

## Bloat Report

```sql
SELECT relname,
       n_dead_tup,
       n_live_tup,
       ROUND(100.0 * n_dead_tup / NULLIF(n_live_tup + n_dead_tup, 0), 1) AS dead_pct,
       last_autovacuum
FROM pg_stat_user_tables
WHERE n_live_tup > 1000
ORDER BY dead_pct DESC NULLS LAST
LIMIT 20;
```

## Long-Running Transaction Alert

```sql
SELECT pid, usename, state, query_start,
       now() - query_start AS duration,
       left(query, 80) AS query_snippet
FROM pg_stat_activity
WHERE state != 'idle'
  AND now() - query_start > interval '5 minutes'
ORDER BY duration DESC;
```

## Index Usage Report

```sql
SELECT schemaname, tablename, indexname, idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0
  AND indexname NOT LIKE '%_pkey'
ORDER BY schemaname, tablename;
```

## Connection Count Trend

```bash
psql -U monitor -Atc "SELECT now(), count(*) FROM pg_stat_activity;" \
  >> /var/log/pg-connections.csv
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Postgresql — Procedures](procedures/)
- [Postgresql — CLI Reference](cli-reference/)
- [Postgresql — Health Checks](health-checks/)
