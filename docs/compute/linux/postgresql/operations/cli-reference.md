---
tags:
  - linux
  - operations
description: "PostgreSQL CLI reference — psql meta-commands, pg_dump/pg_restore, pg_basebackup, pg_upgrade, vacuumdb, and reindexdb quick reference."
---
# PostgreSQL — CLI Reference

<div class="kb-summary">
PostgreSQL CLI reference — psql meta-commands, pg_dump/pg_restore, pg_basebackup, pg_upgrade, vacuumdb, and reindexdb quick reference.

*Applies to: RHEL / Ubuntu LTS*
</div>
![PostgreSQL — CLI Reference](../../../../assets/compute-linux-postgresql-operations-cli-reference.svg)

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## psql

```bash
# Connect
psql -h <host> -U <user> -d <database>
psql -U postgres                           # local socket
psql -U appuser -h 10.0.1.10 -d app_prod
psql -U postgres -c "SELECT version();"    # one-liner
psql -U postgres -Atc "SELECT count(*) FROM pg_stat_activity;"  # -A no align, -t tuples only
```


```text title="Expected output"
psql (15.2 (Debian 15.2-1.pgdg120+1), server 15.2)
Type "help" for help.

postgres=# 

PostgreSQL 15.2 on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit

42
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `psql: error: could not translate host name "10.0.1.10" to address: Name or service not known` | Verify the hostname/IP is correct and the PostgreSQL server is running and accessible from your network. |
    | `psql: error: FATAL: Ident authentication failed for user "appuser"` | Check that the pg_hba.conf file permits the authentication method for this user/host combination, or switch to md5/scram-sha-256 authentication. |
    | `psql: error: FATAL: password authentication failed for user "postgres"` | Ensure the password is correct, or use `sudo -u postgres psql` for local socket connections without a password prompt. |
**Meta-commands inside psql:**

| Command | Action |
|---|---|
| `\l` | List databases |
| `\c <db>` | Connect to database |
| `\dt` | List tables in current schema |
| `\d <table>` | Describe table |
| `\du` | List roles/users |
| `\i <file.sql>` | Execute SQL file |
| `\timing` | Toggle query execution time |
| `\x` | Toggle expanded output |
| `\q` | Quit |

## pg_dump / pg_restore

```bash
# Dump single DB (custom format)
pg_dump -U postgres -Fc app_prod > app_prod_$(date +%F).dump

# Dump all databases
pg_dumpall -U postgres > all-$(date +%F).sql

# Restore custom format (parallel)
pg_restore -U postgres -d app_prod -j 4 app_prod.dump

# Restore with create
pg_restore -U postgres -C -d postgres app_prod.dump
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `pg_dump: error: connection to database "app_prod" failed: FATAL: role "postgres" does not exist` | Verify the PostgreSQL superuser exists and the `-U` parameter matches an actual role in your cluster. |
    | `pg_restore: [archiver] could not open input file "app_prod.dump": No such file or directory` | Ensure the dump file path is correct and the file exists in the current directory or provide the full path. |
    | `pg_restore: error: could not execute query: ERROR: database "app_prod" already exists` | Either drop the target database first with `dropdb -U postgres app_prod`, or omit the `-C` flag if the database already exists. |
## pg_basebackup

```bash
pg_basebackup -h localhost -U replication -D /backup/base -P -Xs -R
# -Xs = include WAL; -R = write standby.signal
```


```text title="Expected output"
pg_basebackup: initiating base backup, waiting for checkpoint to complete
pg_basebackup: checkpoint completed
24601/24601 kB (100%), 1/1 tablespace
pg_basebackup: write-ahead log start point: 0/2000028 on timeline 1
pg_basebackup: write-ahead log end point: 0/2000100 on timeline 1
pg_basebackup: base backup completed
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `pg_basebackup: could not connect to server: FATAL: role "replication" does not exist` | Create the replication role with `CREATE ROLE replication WITH REPLICATION LOGIN;` on the primary server. |
    | `pg_basebackup: could not create directory "/backup/base": Permission denied` | Ensure the backup directory exists and is writable by the PostgreSQL system user with `mkdir -p /backup/base && chown postgres:postgres /backup/base`. |
    | `pg_basebackup: could not receive data from WAL stream: ERROR: replication slot "pg_basebackup_slot" does not exist` | Create a replication slot on the primary with `SELECT pg_create_physical_replication_slot('pg_basebackup_slot');` or use `-C` flag to auto-create it. |
## vacuumdb / reindexdb

```bash
vacuumdb -U postgres --analyze -d app_prod
vacuumdb -U postgres --full -d app_prod --table orders   # full; locks table
reindexdb -U postgres -d app_prod
```


```text title="Expected output"
ANALYZE
VACUUM
REINDEX INDEX pg_toast.pg_toast_2619_index
REINDEX INDEX pg_toast.pg_toast_2620_index
REINDEX INDEX orders_pkey
REINDEX INDEX orders_user_id_idx
REINDEX INDEX orders_created_at_idx
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `vacuumdb: error: could not connect to database server: FATAL: role "postgres" does not exist` | Create the postgres superuser role with `createuser -s postgres` or use an existing superuser name with `-U`. |
    | `vacuumdb: error: database "app_prod" does not exist` | Verify the database name is correct and exists by running `psql -U postgres -l` to list all databases. |
    | `ERROR: relation "orders" does not exist` | Confirm the table name and schema; if in a non-public schema, use `--table schema_name.orders`. |
## pg_upgrade

```bash
pg_upgrade \
  --old-datadir /var/lib/pgsql/15/data \
  --new-datadir /var/lib/pgsql/16/data \
  --old-bindir /usr/pgsql-15/bin \
  --new-bindir /usr/pgsql-16/bin \
  --check   # dry-run; remove --check for actual upgrade
```


```text title="Expected output"
Performing Consistency Checks
-----------------------------
Checking cluster versions                                   ok
Checking database user is a superuser                       ok
Checking database connection settings                       ok
Checking for prepared transactions                          ok
Checking for reg* data types                                ok
Checking for contrib/isn with bigint-passing mismatch       ok
Checking for tables WITH OIDS                               ok
Checking for invalid "sql" aggregate functions              ok
Checking for presence of required libraries                 ok
Checking database user is a superuser                       ok
Checking for prepared transactions                          ok

*Clusters are compatible*
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `could not connect to database server: could not translate host name "localhost" to address: Name or service not known` | Ensure PostgreSQL 15 is running and accepting connections on the default socket before running pg_upgrade. |
    | `pg_upgrade: error: old cluster data and binary directories are not from the same server` | Verify that the --old-bindir points to the PostgreSQL 15 installation that created the data in --old-datadir (check version with `/usr/pgsql-15/bin/postgres --version`). |
    | `pg_upgrade: error: could not find a "pg_dump" executable` | Confirm both PostgreSQL 15 and 16 are installed and their bin directories exist at the specified paths. |
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Postgresql — Procedures](../procedures/)
- [Postgresql — Scripts](../scripts/)
- [Postgresql — Health Checks](../health-checks/)
