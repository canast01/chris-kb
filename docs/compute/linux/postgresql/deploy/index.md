---
tags:
  - deployment
  - linux
---
# PostgreSQL — Initial Deployment

<div class="kb-summary">
PostgreSQL initial deployment — installation on RHEL/Ubuntu, postgresql.conf baseline tuning, pg_hba.conf access control, firewall, and first-connection validation.

*Applies to: RHEL / Ubuntu LTS*
</div>

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

## Install on Ubuntu

```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable --now postgresql
```

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
