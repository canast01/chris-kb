# Database Capacity Monitoring


<div class="kb-summary">
Track database storage growth, identify capacity risks early, and plan expansion before thresholds are breached.
</div>

## Current Capacity — Quick Check

### PostgreSQL

```sql
-- Database sizes
SELECT datname AS database,
       pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database ORDER BY pg_database_size(datname) DESC;

-- Table sizes (top 20)
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;

-- Index sizes
SELECT indexname,
       pg_size_pretty(pg_relation_size(indexname::regclass)) AS index_size
FROM pg_indexes
ORDER BY pg_relation_size(indexname::regclass) DESC LIMIT 20;
```
```text
┌─────────────────────────────────── Database — Capacity Monitoring ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Track database growth, tablespace usage, log space, and forecast expansion needs       │   │
│   │     Alert at 75% usage; plan expansion at 85%; emergency at 90%; autogrow is a safety net     │   │
│   │     Monitor: data files, log files, temp/undo space, index fragmentation, row growth rate     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Current Capacity               │  │              Growth Forecasting             │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │            PG: pg_database_size()            │  │          Trend: 30/60/90 day growth         │   │
│   │         MSSQL: sys.dm_db_file_space          │  │          Forecast to 90% threshold          │   │
│   │          MySQL: information_schema           │  │         Alert: % full + growth rate         │   │
│   │          Log space: VLF / undo seg           │  │          Capacity request lead time         │   │
│   │          Temp: active session usage          │  │         Archive + partition old data        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Tablespace   = Named storage container for database objects; monitored per datafile                │
│    VLF          = Virtual Log File (SQL Server); fragmented log slows backup and recovery             │
│    Autogrow     = Auto-expand datafile; emergency safety net — not a capacity management plan         │
│    Undo segment = Oracle/MySQL space for rolled-back transactions; ORA-01555 on shortage              │
│    pg_database_size= PostgreSQL function returning total size of named database in bytes              │
│    Partitioning = Split large tables by range/list/hash; move old partitions to cheaper storage       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Filesystem / Volume Capacity

```bash
# Database data directories
df -h /var/lib/postgresql /var/lib/mysql /var/opt/mssql

# inode usage (log files can exhaust inodes before disk is full)
df -i /var/lib/postgresql

# Identify large files
du -sh /var/lib/postgresql/data/*
du -sh /var/lib/mysql/*

# WAL / binary log space (PostgreSQL)
du -sh /var/lib/postgresql/data/pg_wal/

# MySQL binary logs
du -sh /var/lib/mysql/mysql-bin.*
mysql -u root -e "SHOW BINARY LOGS;"
```

## Growth Trending (30-day estimate)

```bash
# Weekly snapshots — capture to track growth
psql -U postgres -Atc "SELECT pg_database_size('mydb');" >> /var/log/db-size-mydb.log

# Simple growth rate from log
awk 'NR>1{print ($1-prev)/1024/1024 " MB added since last check"; prev=$1} NR==1{prev=$1}' /var/log/db-size-mydb.log
```

## Capacity Thresholds

| Threshold | Action |
|---|---|
| > 70% volume full | Alert — begin capacity planning |
| > 80% volume full | Escalate — schedule expansion within 2 weeks |
| > 90% volume full | Critical — emergency expansion or archival |
| WAL directory > 10 GB | Review archive lag or max_wal_size |
| MySQL binary logs > 50 GB | Review binlog retention policy |

## Capacity Reduction — Quick Wins

```sql
-- PostgreSQL: reclaim dead tuple space
VACUUM ANALYZE <schema>.<table>;
-- Full reclaim (locks table briefly)
VACUUM FULL <schema>.<table>;

-- PostgreSQL: drop unused indexes
SELECT indexname, idx_scan FROM pg_stat_user_indexes
WHERE idx_scan = 0 ORDER BY pg_relation_size(indexname::regclass) DESC;

-- MySQL: purge old binary logs
PURGE BINARY LOGS BEFORE DATE_SUB(NOW(), INTERVAL 7 DAY);

-- SQL Server: shrink log file (use sparingly — not routine maintenance)
USE mydb;
DBCC SHRINKFILE (mydb_log, 1024);  -- 1024 MB target
```

## Capacity Monitoring Checklist

- [ ] Database volume utilisation checked (< 70% warning, < 80% OK)
- [ ] WAL / binary log directories reviewed
- [ ] Top 10 tables by size reviewed for unexpected growth
- [ ] Growth rate trending updated
- [ ] Backup storage capacity checked
- [ ] Expansion request raised if any threshold breached

## Troubleshooting

| Symptom | Check | Action |
|---|---|---|
| Disk full — DB stopped | WAL or binlogs filling volume | Purge old WAL/binlogs; increase volume |
| Table grew unexpectedly | Bloat from deletes? Missing archival job? | VACUUM FULL; check archival/purge jobs |
| pg_wal growing uncontrolled | Replication slot inactive | Check `pg_replication_slots`; drop inactive slots |
| innodb_data_file_path auto-extend filling disk | Auto-extend enabled without limit | Set `innodb_data_file_path` max size; add data file |
