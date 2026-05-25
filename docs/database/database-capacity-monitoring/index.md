# Database Capacity Monitoring

Track database storage growth, identify capacity risks early, and plan expansion before thresholds are breached.

```text
┌─────────────────────────────────────────────────────┐
│             Database Storage Components             │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ Data     │  │   Log /  │  │   Temp / Sort    │   │
│  │ files    │  │ WAL/binlog│  │   tablespace     │  │
│  └────┬─────┘  └────┬─────┘  └────────┬─────────┘   │
└───────┼─────────────┼─────────────────┼────────────┘
        └─────────────┴─────────────────┘
                          │
                          ▼
             ┌────────────────────────┐
             │    Growth Trending     │
             │  weekly size snapshot  │
             │  → growth rate/month   │
             └────────────┬───────────┘
                          │
         ┌────────────────┼────────────────┐
         ▼                ▼                ▼
┌──────────────┐  ┌─────────────┐  ┌──────────────────┐
│  >70% → Alert│  │ >80% → Escal│  │ >90% → Emergency │
│  plan capac. │  │ expand 2wks │  │ expand or archive│
└──────────────┘  └─────────────┘  └──────────────────┘
```

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

### MySQL / MariaDB

```sql
-- Database sizes
SELECT table_schema AS `database`,
       ROUND(SUM(data_length + index_length) / 1024 / 1024, 1) AS size_mb
FROM information_schema.tables
GROUP BY table_schema ORDER BY size_mb DESC;

-- Largest tables
SELECT table_schema, table_name,
       ROUND((data_length + index_length) / 1024 / 1024, 1) AS size_mb,
       ROUND(data_free / 1024 / 1024, 1) AS free_mb
FROM information_schema.tables
ORDER BY (data_length + index_length) DESC LIMIT 20;
```

### SQL Server

```sql
-- Database file sizes and usage
SELECT DB_NAME(vfs.database_id) AS database_name,
       mf.name AS logical_name,
       mf.type_desc,
       ROUND(vfs.size_on_disk_bytes / 1048576.0, 1) AS size_mb,
       ROUND(vfs.io_stall_read_ms, 0) AS read_stall_ms
FROM sys.dm_io_virtual_file_stats(NULL, NULL) vfs
JOIN sys.master_files mf ON vfs.database_id = mf.database_id AND vfs.file_id = mf.file_id
ORDER BY vfs.size_on_disk_bytes DESC;

-- Top 20 tables by size
SELECT TOP 20 t.name AS table_name,
       SUM(a.total_pages) * 8 / 1024 AS total_size_mb,
       SUM(a.used_pages) * 8 / 1024 AS used_size_mb
FROM sys.tables t
JOIN sys.indexes i ON t.object_id = i.object_id
JOIN sys.partitions p ON i.object_id = p.object_id AND i.index_id = p.index_id
JOIN sys.allocation_units a ON p.partition_id = a.container_id
GROUP BY t.name ORDER BY total_size_mb DESC;
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
