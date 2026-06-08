# SQL Server — Backup Restore

<div class="kb-summary">
SQL Server backup restore reference.
</div>

## Database — Backup Validation

```bash
# pgBackRest — check latest backup info
pgbackrest --stanza=<stanza-name> info

# List backup files
pgbackrest --stanza=<stanza-name> info --output=json | jq '.[] | .backup[-1]'

# Check WAL archiving is current
psql -U postgres -c "SELECT last_archived_wal, last_archived_time, last_failed_wal FROM pg_stat_archiver;"
```
```text
┌──────────────────────────────────── Database — Backup Validation ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Confirm database backups are completing successfully and restores work before needed     │   │
│   │          PostgreSQL: pgBackRest info + WAL archiving; MySQL: mysqldump + binary logs          │   │
│   │         SQL Server: RESTORE VERIFYONLY; Oracle: RMAN validate; check agent job history        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Backup Status Checks             │  │             Restore Verification            │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │           pgBackRest: stanza info            │  │           Restore to test instance          │   │
│   │         Check last backup timestamp          │  │         Run row count + key queries         │   │
│   │         Verify WAL archiving current         │  │          RESTORE VERIFYONLY (MSSQL)         │   │
│   │            SQL Agent job history             │  │           RMAN validate backupset           │   │
│   │             Alert on missed jobs             │  │             Document test result            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │     Platform     │  Check command   │   Restore verify  │    Frequency     │     Alert on     │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    PostgreSQL    │ pgbackrest info  │  pg_restore test  │      Daily       │     WAL gap      │   │
│   │    SQL Server    │Agent job history │    VERIFY ONLY    │      Daily       │   Job failure    │   │
│   │      MySQL       │    mysqlcheck    │  Restore + query  │      Daily       │    Binlog gap    │   │
│   │      Oracle      │    RMAN list     │   RMAN validate   │      Daily       │   RMAN failure   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    pgBackRest   = PostgreSQL backup tool; stanza = named backup config for a cluster                  │
│    WAL archiving= PostgreSQL ships WAL segments to archive; gap = missing logs; PITR broken           │
│    VERIFY ONLY  = SQL Server command; reads backup and validates checksums without restoring          │
│    RMAN validate= Oracle checks backup set integrity; reports any corrupt blocks found                │
│    Binary log   = MySQL changelog of every committed transaction; needed for PITR                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# PostgreSQL — verify backup with pgBackRest
pgbackrest --stanza=<stanza-name> check

# MySQL — verify xtrabackup integrity
xtrabackup --prepare --target-dir=/backup/mysql/latest/

# SQL Server — verify backup file checksum
RESTORE VERIFYONLY FROM DISK = '/backup/mssql/mydb_full.bak' WITH CHECKSUM;
```
```bash
# Restore to test instance
pgbackrest --stanza=<stanza-name> --pg1-path=/var/lib/pgsql/test-restore restore
# Start test instance and verify
pg_ctl -D /var/lib/pgsql/test-restore start
psql -p 5433 -U postgres -c "SELECT count(*) FROM pg_stat_user_tables;"
```
```bash
# Copy backup to test directory
xtrabackup --prepare --target-dir=/restore/mysql-test/
rsync -a /restore/mysql-test/ /var/lib/mysql-test/
chown -R mysql: /var/lib/mysql-test/
mysqld_safe --datadir=/var/lib/mysql-test --socket=/tmp/mysql-test.sock &
mysql -S /tmp/mysql-test.sock -e "SHOW DATABASES;"
```
```sql
RESTORE DATABASE [TestRestore] FROM DISK = '/backup/mssql/prod_full.bak'
WITH MOVE 'proddb' TO '/var/opt/mssql/data/TestRestore.mdf',
     MOVE 'proddb_log' TO '/var/opt/mssql/data/TestRestore_log.ldf',
     REPLACE, STATS = 10;
-- Verify table counts match expected
USE TestRestore;
SELECT COUNT(*) FROM important_table;
```
