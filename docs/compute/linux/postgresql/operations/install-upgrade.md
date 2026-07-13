---
tags:
  - linux
  - operations
description: "PostgreSQL upgrade procedures — minor version (in-place), major version (pg_upgrade), upgrade path, pre-upgrade checks, and post-upgrade validation."
---
# PostgreSQL — Install & Upgrade

<div class="kb-summary">
PostgreSQL upgrade procedures — minor version (in-place), major version (pg_upgrade), upgrade path, pre-upgrade checks, and post-upgrade validation.

*Applies to: RHEL / Ubuntu LTS*
</div>
![PostgreSQL — Install & Upgrade](../../../../assets/compute-linux-postgresql-operations-install-upgrade.svg)

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Version Upgrade Path

Minor versions (15.x → 15.y): in-place, same data directory.
Major versions (15 → 16): requires `pg_upgrade` or logical replication migration.
Always upgrade one major version at a time.

## Minor Version Upgrade (RHEL)

```bash
sudo systemctl stop postgresql-15
sudo dnf upgrade postgresql15-server
sudo systemctl start postgresql-15
psql -U postgres -c "SELECT version();"
```


```text title="Expected output"
psql (15.2, server 15.2)
 version
─────────────────────────────────────────────────────────────────────────────────
 PostgreSQL 15.2 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 11.4.0, 64-bit
(1 row)
```

!!! warning "Common errors"
    **`Job for postgresql-15.service failed because the control process exited with error code.`** — Check `/var/log/postgresql/postgresql-15-main.log` for startup errors, likely due to incompatible configuration parameters in `postgresql.conf` after the upgrade.
    **`psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory`** — Verify PostgreSQL is running with `sudo systemctl status postgresql-15` and check that the socket directory exists and has correct permissions.
## Major Version Upgrade with `pg_upgrade`

```bash
# Install new version
sudo dnf install -y postgresql16-server
sudo /usr/pgsql-16/bin/postgresql-16-setup initdb

# Copy config files
sudo cp /var/lib/pgsql/15/data/postgresql.conf /var/lib/pgsql/16/data/
sudo cp /var/lib/pgsql/15/data/pg_hba.conf /var/lib/pgsql/16/data/

# Stop old instance
sudo systemctl stop postgresql-15

# Dry-run check
sudo -u postgres pg_upgrade \
  --old-datadir /var/lib/pgsql/15/data \
  --new-datadir /var/lib/pgsql/16/data \
  --old-bindir /usr/pgsql-15/bin \
  --new-bindir /usr/pgsql-16/bin \
  --check

# Actual upgrade
sudo -u postgres pg_upgrade \
  --old-datadir /var/lib/pgsql/15/data \
  --new-datadir /var/lib/pgsql/16/data \
  --old-bindir /usr/pgsql-15/bin \
  --new-bindir /usr/pgsql-16/bin \
  --jobs 4

sudo systemctl start postgresql-16
```


```text title="Expected output"
Last metadata expiration check: 0:12:34 ago on Thu 14 Dec 2024 09:47:22 AM UTC.
Dependencies resolved.
================================================================================
 Package                    Architecture    Version         Repository    Size
================================================================================
Installing:
 postgresql16-server        x86_64          16.1-1.rhel9    pgdg16       4.2 M

Transaction Summary:
================================================================================
Install  1 Package

Total download size: 4.2 M
Installed size: 18 M
Downloading Packages:
[100%] postgresql16-server-16.1-1.rhel9.x86_64.rpm
Running transaction
Installed: postgresql16-server-16.1-1.rhel9.x86_64

Data directory is not empty, initdb is skipped
Performing Consistency Checks
-----------------------------
Checking cluster versions                                 ok
Checking database user is the install user                ok
Checking database connection settings                      ok
Checking for prepared transactions                        ok
Checking for reg* data types                              ok
Checking for contrib/isn with bigint-passing mismatch     ok
Checking for tables WITH OIDS                             ok
Checking for invalid "sql_identifier" user columns        ok
Checking for extension updates                            ok
pg_upgrade check ok
Upgrade Complete
================================================================================
Unit postgresql-15.service stopped.
Upgrade Complete
Data successfully upgraded.
Optimizer statistics have not been updated, because
'analyze_new_cluster.sh' has not been run on the new cluster.
Please run:
    /var/lib/pgsql/analyze_new_cluster.sh
Unit postgresql-16.service started.
```

!!! warning "Common errors"
    **`pg_upgrade: error: could not connect to compatible PostgreSQL server (libpq version 16, server version 15.0)`** — Ensure the old PostgreSQL 15 instance is stopped before running pg_upgrade.
    **`permission denied while trying to open version file "/var/lib/pgsql/16/data/PG_VERSION"`** — Run the initdb step with proper permissions or ensure /var/lib/pgsql/16/data is owned by the postgres user.
    **`FATAL: could not create shared memory segment: No space left on device`** — Increase shared_buffers in postgresql.conf or reduce the value before starting the new cluster.
## Post-Upgrade Steps

```bash
# Update statistics (required after pg_upgrade)
sudo -u postgres /usr/pgsql-16/bin/vacuumdb --all --analyze-in-stages

# Verify all databases accessible
psql -U postgres -l

# Update extensions
psql -U postgres -d app_prod -c "ALTER EXTENSION pg_stat_statements UPDATE;"
```


```text title="Expected output"
vacuumdb: vacuuming database "postgres"
vacuumdb: vacuuming database "app_prod"
vacuumdb: vacuuming database "app_staging"
vacuumdb: vacuuming database "monitoring"
vacuumdb: analyzing database "postgres"
vacuumdb: analyzing database "app_prod"
vacuumdb: analyzing database "app_staging"
vacuumdb: analyzing database "monitoring"
                                   List of databases
        Name        |  Owner   | Encoding |   Collate   |    Ctype    |   Access privileges
--------------------+----------+----------+-------------+-------------+-----------------------
 app_prod           | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 app_staging        | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 monitoring         | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 postgres           | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 |
 template0          | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres
 template1          | postgres | UTF8     | en_US.UTF-8 | en_US.UTF-8 | =c/postgres
(6 rows)
ALTER EXTENSION
```

!!! warning "Common errors"
    **`psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: No such file or directory`** — Verify PostgreSQL is running with `sudo systemctl status postgresql-16` and check socket location in postgresql.conf.
    **`ERROR: extension "pg_stat_statements" does not exist`** — Create the extension first with `psql -U postgres -d app_prod -c "CREATE EXTENSION IF NOT EXISTS pg_stat_statements;"` before attempting to update it.
    **`ERROR: permission denied for schema public`** — Ensure the postgres user has proper ownership of databases with `ALTER DATABASE app_prod OWNER TO postgres;`.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Postgresql — Procedures](../procedures/)
- [Postgresql — Health Checks](../health-checks/)
- [Postgresql — Deploy](../../deploy/)
