# MySQL / MariaDB — CLI Reference

<div class="kb-summary">
MySQL CLI reference — mysql client, mysqladmin, mysqldump, mysqlcheck, mysqlbinlog, and Percona pt-* tool quick reference.
</div>

```text
┌──────────────────────────────────────── MySQL — CLI Reference ────────────────────────────────────────┐
│                                                                                                       │
│   Five core CLI tools: mysql (client), mysqladmin (admin ops), mysqldump, mysqlcheck, mysqlbinlog     │
│   Percona pt-* tools extend the toolkit: pt-query-digest, pt-online-schema-change, pt-heartbeat       │
│   All tools accept -h host -u user -p for connection; use .my.cnf to avoid password on CLI            │
│                                                                                                       │
│   mysql client                                                                                        │
│   mysql -h host -u user -p db: interactive session; -e "SQL" for one-liner execution                  │
│   SHOW PROCESSLIST: active connections and current query; KILL <id> terminates a session              │
│   SHOW REPLICA STATUS\G: replication lag, I/O and SQL thread states, last error                       │
│   SET GLOBAL slow_query_log=ON: enable slow query log without server restart                          │
│                                                                                                       │
│   mysqladmin                                                                                          │
│   mysqladmin status: uptime, threads, questions, and slow queries in one line                         │
│   mysqladmin processlist: running queries; mysqladmin kill <id> terminates by process ID              │
│   mysqladmin flush-logs: rotates general and slow query logs                                          │
│                                                                                                       │
│   mysqldump and mysqlbinlog                                                                           │
│   mysqldump --single-transaction --routines --triggers -A: full logical backup, consistent read       │
│   mysqlbinlog --start-datetime --stop-datetime binlog.*: replay binlogs for PITR restore              │
│   mysqlcheck --all-databases --optimize: reclaim space and update index statistics                    │
│                                                                                                       │
│   Key terms:                                                                                          │
│   .my.cnf      = user-level MySQL config file; stores host/user/pass to avoid CLI prompts             │
│   PROCESSLIST  = live view of all active connections and their current SQL statement                  │
│   --single-transaction = mysqldump option; consistent snapshot without locking tables                 │
│   pt-query-digest = analyses slow log or general log; outputs ranked query report by total time       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## mysql client

```bash
# Connect
mysql -h <host> -u <user> -p<password> <database>
mysql -u root -p                          # interactive, prompt for password
mysql -u root -p -e "SHOW DATABASES;"    # one-liner

# Useful session variables
SET SESSION long_query_time = 0;          # capture all queries in slow log
SHOW PROCESSLIST;                         # active connections
SHOW FULL PROCESSLIST;                    # full query text
KILL <process_id>;                        # kill a blocking query
```

## mysqladmin

```bash
mysqladmin -u root -p status              # uptime, queries/sec, threads
mysqladmin -u root -p extended-status     # all status variables
mysqladmin -u root -p variables           # all config variables
mysqladmin -u root -p flush-logs          # rotate logs
mysqladmin -u root -p processlist         # same as SHOW PROCESSLIST
mysqladmin -u root -p ping                # quick reachability check
```

## mysqldump

```bash
# Full DB dump (InnoDB consistent snapshot)
mysqldump -u root -p --single-transaction --routines --triggers --all-databases > full.sql

# Single database
mysqldump -u root -p --single-transaction mydb > mydb.sql

# Compressed
mysqldump -u root -p --single-transaction mydb | gzip > mydb_$(date +%F).sql.gz

# Restore
mysql -u root -p mydb < mydb.sql
```

## mysqlcheck

```bash
mysqlcheck -u root -p --all-databases     # check all tables
mysqlcheck -u root -p --optimize mydb     # reclaim fragmented space
mysqlcheck -u root -p --repair mydb       # repair MyISAM corruption
```

## mysqlbinlog

```bash
# View binlog events
mysqlbinlog /var/lib/mysql/mysql-bin.000001 | less

# PITR: apply binlog from specific time
mysqlbinlog --start-datetime="2026-06-08 10:00:00" \
            --stop-datetime="2026-06-08 10:30:00" \
            /var/lib/mysql/mysql-bin.000001 | mysql -u root -p
```

## Percona Toolkit

```bash
pt-query-digest /var/log/mysql/slow.log   # analyse slow query log
pt-table-checksum --host=primary --user=root   # verify replica consistency
pt-online-schema-change                   # non-blocking ALTER TABLE
pt-kill --busy-time 300 --kill            # kill queries running > 5 min
```
