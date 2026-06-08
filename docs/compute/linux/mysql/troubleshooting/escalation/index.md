# MySQL / MariaDB — Escalation

<div class="kb-summary">
MySQL escalation criteria — P1/P2 indicators, what to collect before engaging DBA or vendor support, and support bundle checklist.
</div>

## Escalation Thresholds

| Condition | Severity | Action |
|---|---|---|
| Database unreachable | P1 | Page DBA on-call immediately |
| Replica SQL thread stopped with error | P2 | Alert DBA; begin lag triage |
| Blocking chain > 10 min; app impact | P1 | Kill head blocker; page DBA |
| Disk > 90% full (datadir or log) | P1 | Emergency cleanup or resize |
| Corruption detected (InnoDB crash) | P1 | Stop writes; page DBA; do not restart arbitrarily |
| Replication lag > 5 min | P2 | Alert DBA; identify cause |
| Connection exhaustion (`max_connections`) | P1 | Kill idle sessions; page DBA |

## Evidence to Collect Before Escalating

```bash
# 1. Error log (last 200 lines)
sudo tail -200 /var/log/mysqld.log > /tmp/mysql-error.log

# 2. Process list
mysql -u root -p -e "SHOW FULL PROCESSLIST;" > /tmp/processlist.txt

# 3. InnoDB status
mysql -u root -p -e "SHOW ENGINE INNODB STATUS\G" > /tmp/innodb-status.txt

# 4. Replica status (if applicable)
mysql -u root -p -e "SHOW REPLICA STATUS\G" > /tmp/replica-status.txt

# 5. Disk usage
df -h /var/lib/mysql > /tmp/disk-usage.txt

# 6. Key variables
mysql -u root -p -e "SHOW GLOBAL STATUS; SHOW GLOBAL VARIABLES;" > /tmp/global-status.txt
```

## InnoDB Crash Recovery

```bash
# Safe restart attempt (innodb_force_recovery = 0 is default)
sudo systemctl restart mysqld

# If data directory corrupted, try increasing recovery level incrementally
# Add to /etc/mysql/mysqld.cnf, restart after each:
# innodb_force_recovery = 1  → skip corrupt pages
# innodb_force_recovery = 2  → skip background threads
# innodb_force_recovery = 3  → do not roll back transactions
# WARNING: Only use with DBA guidance. Always backup first.
```

## Vendor / DBA Support Information

Provide for any escalation:
- MySQL version (`SELECT version()`)
- OS version (`uname -a`, `cat /etc/os-release`)
- Storage engine (`SELECT engine FROM information_schema.TABLES LIMIT 5`)
- Replication topology (primary/replica count, GTID mode)
- Recent changes (upgrades, schema changes, load spike)
- Timeline of when symptoms started
