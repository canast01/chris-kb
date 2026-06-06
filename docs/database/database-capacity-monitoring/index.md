# Database — Capacity Monitoring

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
```bash
# Weekly snapshots — capture to track growth
psql -U postgres -Atc "SELECT pg_database_size('mydb');" >> /var/log/db-size-mydb.log

# Simple growth rate from log
awk 'NR>1{print ($1-prev)/1024/1024 " MB added since last check"; prev=$1} NR==1{prev=$1}' /var/log/db-size-mydb.log
```
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
