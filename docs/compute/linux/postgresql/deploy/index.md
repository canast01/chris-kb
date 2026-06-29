---
tags:
  - deployment
  - linux
search:
  boost: 1.5
---
# PostgreSQL — Initial Deployment

<div class="kb-summary">
PostgreSQL initial deployment — installation on RHEL/Ubuntu, postgresql.conf baseline tuning, pg_hba.conf access control, firewall, and first-connection validation.

*Applies to: RHEL / Ubuntu LTS*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
install_on_rhel_rocky: "Install on RHEL / Rocky" {shape: rectangle}
install_on_ubuntu: "Install on Ubuntu" {shape: rectangle}
initial_configuration_postgresqlconf: "Initial Configuration (`postgresql.conf`)" {shape: rectangle}
pghbaconf_access_control: "`pg_hba.conf` Access Control" {shape: rectangle}
firewall: "Firewall" {shape: rectangle}
create_application_user_and_database: "Create Application User and Database" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> install_on_rhel_rocky
install_on_rhel_rocky -> install_on_ubuntu
install_on_ubuntu -> initial_configuration_postgresqlconf
initial_configuration_postgresqlconf -> pghbaconf_access_control
pghbaconf_access_control -> firewall
firewall -> create_application_user_and_database
create_application_user_and_database -> validate
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Install on RHEL / Rocky

```bash
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm
sudo dnf -qy module disable postgresql
sudo dnf install -y postgresql16-server
sudo /usr/pgsql-16/bin/postgresql-16-setup initdb
sudo systemctl enable --now postgresql-16
```


```text title="Expected output"
PostgreSQL 16 Repository Setup
Last metadata expiration check: 0:00:42 ago on Thu 19 Dec 2024 02:15:33 PM UTC.
Dependencies resolved.
================================================================================
 Package                    Arch      Version           Repository       Size
================================================================================
Installing:
 pgdg-redhat-repo           noarch    latest-1          @commandline    9.2 kB

Transaction Summary
================================================================================
Install  1 Package

Complete!
Resetting modules for package postgresql:16-devel
Disabling module postgresql:16-devel
Disabling module postgresql:16
Dependencies resolved.
================================================================================
 Package                    Arch      Version           Repository       Size
================================================================================
Installing:
 postgresql16-server        x86_64    16.1-1PGDG.rhel9  pgdg16           4.8 MB
 postgresql16-contrib       x86_64    16.1-1PGDG.rhel9  pgdg16           652 kB
 postgresql16-libs          x86_64    16.1-1PGDG.rhel9  pgdg16           412 kB

Transaction Summary
================================================================================
Install  3 Packages

Complete!
Initializing database ... ok
Created symlink /etc/systemd/system/multi-user.target.wants/postgresql-16.service → /usr/lib/systemd/system/postgresql-16.service.
```

!!! warning "Common errors"
    **`Error: Failed to download repository metadata`** — Verify internet connectivity and ensure the PostgreSQL repository URL is accessible from your network.
    **`Error: Package postgresql16-server not found`** — Confirm the module disable command completed successfully and that the pgdg repository was installed without errors.
## Install on Ubuntu

```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql
```


```text title="Expected output"
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  postgresql postgresql-contrib postgresql-client postgresql-common libpq5
Setting up postgresql-common (15+248~deb12u1) ...
Setting up postgresql-15 (15.6-1.pgdg120+1) ...
Creating new PostgreSQL cluster 15/main ...
  /usr/lib/postgresql/15/bin/initdb -D /var/lib/postgresql/15/main --auth-local peer --auth-host md5
  Initializing database ... ok
Created symlink /etc/systemd/system/multi-user.target.wants/postgresql.service → /etc/systemd/system/postgresql.service.
postgresql.service enabled and set to start at system boot.
postgresql.service started successfully.
```

!!! warning "Common errors"
    **`E: Unable to locate package postgresql`** — Run `sudo apt update` before installing to refresh the package index.
    **`Job for postgresql.service failed because the start code exited with error code 1.`** — Check `/var/log/postgresql/postgresql-15-main.log` for initialization errors, often caused by insufficient disk space or permission issues on `/var/lib/postgresql`.
## Initial Configuration (`postgresql.conf`)

```ini
listen_addresses = 'localhost'
max_connections = 100
shared_buffers = 2GB
effective_cache_size = 6GB
maintenance_work_mem = 512MB
work_mem = 16MB
wal_level = replica
archive_mode = on
archive_command = 'cp %p /backup/wal/%f'
log_min_duration_statement = 1000
```

## `pg_hba.conf` Access Control

```text
# TYPE  DATABASE  USER      ADDRESS          METHOD
local   all       postgres                   peer
host    app_prod  appuser   10.0.1.0/24      scram-sha-256
host    all       all       127.0.0.1/32     scram-sha-256
```

After editing: `sudo systemctl reload postgresql-16`

## Firewall

```bash
sudo firewall-cmd --add-rich-rule='rule family=ipv4 source address=10.0.1.0/24 port port=5432 protocol=tcp accept' --permanent
sudo firewall-cmd --reload
```


```text title="Expected output"
success
success
```

!!! warning "Common errors"
    **`Error: INVALID_RULE: rule family=ipv4 source address=10.0.1.0/24 port port=5432 protocol=tcp accept: bad attribute port`** — Remove the duplicate "port" keyword; the correct syntax is `port protocol=tcp port=5432`.
    **`Error: COMMAND_FAILED: '/usr/bin/firewall-cmd --reload' failed: org.fedoraproject.FirewallD1.Exception: INVALID_RULE`** — Verify the rich rule syntax is valid before running `--reload`, as malformed rules will prevent the daemon from reloading.
## Create Application User and Database

```sql
CREATE USER appuser WITH ENCRYPTED PASSWORD 'StrongPass1!';
CREATE DATABASE app_prod OWNER appuser;
GRANT ALL ON DATABASE app_prod TO appuser;
```

## Validation

```bash
psql -U postgres -c "SELECT version(); SHOW shared_buffers;"
psql -U appuser -h 127.0.0.1 -d app_prod -c "SELECT 1 AS alive;"
```


```text title="Expected output"
version                                                  
────────────────────────────────────────────────────────────────────────────────────────────────────────
 PostgreSQL 14.8 on x86_64-pc-linux-gnu, compiled by gcc (GCC) 9.4.0, 64-bit
(1 row)

 shared_buffers 
────────────────
 256MB
(1 row)

 alive 
───────
     1
(1 row)
```

!!! warning "Common errors"
    **`psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL: Ident authentication failed for user "postgres"`** — Ensure the postgres system user exists and pg_hba.conf allows local socket connections with trust or peer authentication.
    **`psql: error: FATAL: password authentication failed for user "appuser"`** — Verify appuser exists in PostgreSQL and the password is correct, or configure .pgpass file with credentials for non-interactive connections.
---

## Verify

- `systemctl status postgresql` shows `active (running)`
- `psql -U postgres -c "SELECT version();"` returns the expected PostgreSQL version
- Application user can connect: `psql -U appuser -h 127.0.0.1 -d app_prod -c "SELECT 1 AS alive;"`
- `pg_lsclusters` shows the cluster as `online`

---

## See also

- [Postgresql — Procedures](../operations/procedures/)
- [Postgresql — Common Issues](../troubleshooting/common-issues/)
- [Postgresql — How It Works](../architecture/how-it-works/)
