---
tags:
  - linux
  - operations
---
# MySQL / MariaDB — Install & Upgrade

<div class="kb-summary">
MySQL install and upgrade procedures — major version upgrade path, in-place upgrade steps, upgrade checker tool, and post-upgrade validation.

*Applies to: RHEL / Ubuntu LTS*
</div>
![MySQL / MariaDB — Install & Upgrade](../../../../assets/compute-linux-mysql-operations-install-upgrade.svg)

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Version Upgrade Path

Always upgrade one major version at a time: `5.7 → 8.0 → 8.4`

Never skip major versions. Minor versions (8.0.x → 8.0.y) are in-place.

## Pre-Upgrade Checklist

```bash
# Run upgrade compatibility check (MySQL 8.0+)
mysqlcheck -u root -p --all-databases --check-upgrade

# MySQL Shell upgrade checker (8.0 → 8.4)
mysqlsh -- util checkForServerUpgrade root@localhost:3306

# Backup before any upgrade
mysqldump -u root -p --single-transaction --all-databases > pre-upgrade-$(date +%F).sql
```

## In-Place Upgrade (RHEL / Rocky)

```bash
# Stop MySQL
sudo systemctl stop mysqld

# Upgrade package
sudo dnf upgrade mysql-community-server

# Start and run upgrade
sudo systemctl start mysqld
sudo mysql_upgrade -u root -p     # MySQL 5.7 only; 8.0+ auto-upgrades

# Verify
mysql -u root -p -e "SELECT version();"
```

## In-Place Upgrade (Ubuntu)

```bash
sudo systemctl stop mysql
sudo apt-get install -y mysql-server   # upgrades to latest in configured repo
sudo systemctl start mysql
sudo mysql_upgrade -u root -p          # if 5.7 → 8.0
```

## Post-Upgrade Validation

```bash
# Check error log for upgrade warnings
sudo tail -100 /var/log/mysqld.log | grep -i 'error\|warn'

# Verify replication still running
mysql -u root -p -e "SHOW REPLICA STATUS\G" | grep -E 'Running|Error|Lag'

# Check slow query log still active
mysql -u root -p -e "SHOW VARIABLES LIKE 'slow_query%';"

# Run a representative query plan and compare EXPLAIN output
```

## Rolling Upgrade (Replicated Setup)

1. Upgrade replica(s) first; validate replication resumes
2. Promote a replica to primary (failover)
3. Upgrade former primary (now replica)
4. Failover back if needed

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Mysql — Procedures](procedures/)
- [Mysql — Health Checks](health-checks/)
- [Mysql — Deploy](../deploy/)
