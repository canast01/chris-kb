---
tags:
  - linux
  - operations
---
# MySQL / MariaDB — Scripts

<div class="kb-summary">
MySQL automation scripts — nightly backup, slow query report, replication lag alert, connection count monitoring, and table size report.

*Applies to: RHEL / Ubuntu LTS*
</div>
![MySQL / MariaDB — Scripts](../../../../assets/compute-linux-mysql-operations-scripts.svg)

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Nightly Backup Script

```bash
#!/bin/bash
# /opt/scripts/mysql-backup.sh
BACKUP_DIR="/backup/mysql/$(date +%F)"
PASS="$(cat /etc/mysql-backup.pass)"
mkdir -p "$BACKUP_DIR"

mysqldump -u backup_user -p"$PASS" \
  --single-transaction --routines --triggers \
  --all-databases | gzip > "$BACKUP_DIR/full.sql.gz"

# Retain 14 days
find /backup/mysql/ -maxdepth 1 -type d -mtime +14 -exec rm -rf {} +
echo "Backup complete: $BACKUP_DIR"
```


```text title="Expected output"
Backup complete: /backup/mysql/2024-01-15
```

!!! warning "Common errors"
    **`mysqldump: [Warning] Using a password on the command line interface can be insecure.`** — This is a warning, not an error; suppress it by ensuring the password file has restricted permissions (chmod 600 /etc/mysql-backup.pass) and the script runs with appropriate privileges.
    **`mysqldump: Got error: 1045 "Access denied for user 'backup_user'@'localhost'"`** — Verify the backup_user credentials in /etc/mysql-backup.pass match the MySQL user permissions, and confirm the user has RELOAD and LOCK TABLES privileges.
    **`mkdir: cannot create directory '/backup/mysql/2024-01-15': Permission denied`** — Ensure the script runs with sufficient privileges (sudo or as root) and that the /backup/mysql parent directory is writable by the executing user.
## Replication Lag Monitor

```bash
#!/bin/bash
# Alert if replica lag > 30 seconds
LAG=$(mysql -u monitor -p"$PASS" -Nse \
  "SHOW REPLICA STATUS" 2>/dev/null | awk '{print $43}')
if [ -n "$LAG" ] && [ "$LAG" -gt 30 ]; then
  echo "CRITICAL: Replication lag ${LAG}s on $(hostname)" | \
    mail -s "MySQL Replication Alert" dba@example.com
fi
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ERROR 1227 (42000) at line 1: Access denied; you need (at least one of) the REPLICATION CLIENT privilege(s) for this operation`** — Grant the monitor user REPLICATION CLIENT privilege with `GRANT REPLICATION CLIENT ON *.* TO 'monitor'@'localhost';`
    **`awk: fatal: not enough fields (NF=0)`** — The SHOW REPLICA STATUS output format differs between MySQL versions; use `SHOW REPLICA STATUS\G` and parse with grep instead of awk positional fields.
    **`sh: mail: command not found`** — Install mailutils with `apt-get install mailutils` or replace mail command with your monitoring system's alert mechanism.
## Connection Count Report

```bash
#!/bin/bash
# Log connection counts to CSV for trending
mysql -u monitor -p"$PASS" -Nse \
  "SELECT NOW(), VARIABLE_VALUE FROM performance_schema.global_status
   WHERE VARIABLE_NAME='Threads_connected';" \
  >> /var/log/mysql-connections.csv
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`ERROR 1045 (28000): Access denied for user 'monitor'@'localhost' (using password: YES)`** — Verify the monitor user exists and the password in `$PASS` is correct by testing `mysql -u monitor -p"$PASS" -e "SELECT 1;"`.
    **`ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)`** — Ensure MySQL is running with `systemctl status mysql` and the socket path matches your installation (check `my.cnf` for `socket=` setting).
    **`Permission denied` when writing to `/var/log/mysql-connections.csv`** — Verify the mysql system user has write permissions on `/var/log/` with `ls -ld /var/log/` and adjust ownership or create the file with `touch /var/log/mysql-connections.csv && chown mysql:mysql /var/log/mysql-connections.csv`.
## Table Size Report

```sql
-- Top 20 largest tables with row counts
SELECT
  TABLE_SCHEMA AS db,
  TABLE_NAME AS tbl,
  ROUND((DATA_LENGTH + INDEX_LENGTH) / 1024 / 1024, 1) AS size_mb,
  TABLE_ROWS AS approx_rows
FROM information_schema.TABLES
WHERE TABLE_SCHEMA NOT IN ('information_schema','mysql','performance_schema','sys')
ORDER BY (DATA_LENGTH + INDEX_LENGTH) DESC
LIMIT 20;
```

## Slow Query Report

```bash
# Weekly summary from slow query log
pt-query-digest \
  --since "$(date -d '7 days ago' +'%F %T')" \
  /var/log/mysql/slow.log \
  > /var/log/mysql-slow-report-$(date +%F).txt
```


```text title="Expected output"
# Query_time distribution
  1us
 10us
 100us
   1ms
  10ms
 100ms
    1s
  10s
 100s
1000s
# 95th percentile all queries
    1s

# Tables
    SHOW TABLE STATUS FROM `production`\G
    SHOW CREATE TABLE `production`.`orders`\G
    SHOW CREATE TABLE `production`.`users`\G

# Top 10 ignored queries
    0.0s user time,   0.0s system time,  45.23M rss max used
    0 pages short lived,     0 swapped,   0 non-resident

Report saved to /var/log/mysql-slow-report-2024-01-15.txt
```

!!! warning "Common errors"
    **`Can't open /var/log/mysql/slow.log: No such file or directory`** — Enable slow query logging in MySQL with `slow_query_log = ON` and verify the log_slow_queries_file path matches the one specified.
    **`pt-query-digest: command not found`** — Install Percona Toolkit with `apt-get install percona-toolkit` or `yum install percona-toolkit`.
    **`Permission denied`** — Run the command with `sudo` or ensure the MySQL system user has read permissions on /var/log/mysql/slow.log.
## Index Usage Report

```sql
-- Find unused indexes (zero scans since last restart)
SELECT OBJECT_SCHEMA, OBJECT_NAME, INDEX_NAME
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE INDEX_NAME IS NOT NULL
  AND COUNT_STAR = 0
  AND OBJECT_SCHEMA NOT IN ('mysql','sys')
ORDER BY OBJECT_SCHEMA, OBJECT_NAME;
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Mysql — Procedures](../procedures/)
- [Mysql — CLI Reference](../cli-reference/)
- [Mysql — Health Checks](../health-checks/)
