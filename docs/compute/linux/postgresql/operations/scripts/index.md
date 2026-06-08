# PostgreSQL — Scripts

<div class="kb-summary">
PostgreSQL automation scripts — base backup, WAL archiving, replication lag monitor, bloat report, long-running transaction alert, and connection trend logging.
</div>

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
