# MySQL / MariaDB — Install & Upgrade

<div class="kb-summary">
MySQL install and upgrade procedures — major version upgrade path, in-place upgrade steps, upgrade checker tool, and post-upgrade validation.
</div>

```text
┌───────────────────────────────────── MySQL — Install and Upgrade ─────────────────────────────────────┐
│                                                                                                       │
│   Always upgrade one major version at a time: 5.7 → 8.0 → 8.4; never skip versions                    │
│   Run mysqlcheck and mysql_upgrade_checker before each major upgrade                                  │
│   Take a full physical backup (xtrabackup) before starting any major version upgrade                  │
│                                                                                                       │
│   Pre-upgrade checklist                                                                               │
│   Run mysqlcheck --all-databases: identifies corrupt tables that will block upgrade                   │
│   Run mysql_upgrade_checker (MySQL Shell): flags incompatible config and deprecated syntax            │
│   Document current version: SELECT @@version; and backup all databases                                │
│   Review MySQL release notes for removed features and changed defaults                                │
│                                                                                                       │
│   In-place upgrade (minor version: 8.0.x → 8.0.y)                                                     │
│   Stop service; replace packages (dnf/apt upgrade mysql-community-server)                             │
│   Start service; MySQL auto-runs upgrade scripts on first start                                       │
│   Verify: SELECT @@version; and check error log for warnings                                          │
│                                                                                                       │
│   Major version upgrade (8.0 → 8.4)                                                                   │
│   Step 1: run mysql_upgrade_checker; fix all reported issues before proceeding                        │
│   Step 2: mysqldump full backup; verify backup is complete and restorable                             │
│   Step 3: stop 8.0, install 8.4 packages, start; MySQL runs automatic upgrade scripts                 │
│   Step 4: test app connections; check error log; run mysqlcheck --all-databases                       │
│                                                                                                       │
│   Key terms:                                                                                          │
│   mysql_upgrade_checker = MySQL Shell utility; pre-upgrade compatibility analysis                     │
│   mysqlcheck   = checks, repairs, and optimizes tables; run before and after upgrade                  │
│   in-place upgrade = replacing packages on same host with existing data directory                     │
│   error log    = mysqld log at /var/log/mysql/error.log or /var/log/mysqld.log                        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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
