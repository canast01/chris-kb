---
tags:
  - linux
  - troubleshooting
---
# MySQL / MariaDB — Escalation

<div class="kb-summary">
MySQL escalation criteria — P1/P2 indicators, what to collect before engaging DBA or vendor support, and support bundle checklist.

*Applies to: RHEL / Ubuntu LTS*
</div>

```text
┌───────────────────────────────────────── MySQL — Escalation ──────────────────────────────────────────┐
│                                                                                                       │
│   Escalate when: replication stopped with errors, InnoDB corruption, OOM crash, or data loss risk     │
│   Collect before escalating: error log, InnoDB status, slow log, and replication status output        │
│   P1 (production down): engage DBA immediately; do not attempt self-service recovery on corrupt data  │
│                                                                                                       │
│   Escalation thresholds                                                                               │
│   Replication stopped + Errno != 0: STOP REPLICA; collect Last_Error; escalate to DBA                 │
│   InnoDB crash recovery loop: do not restart repeatedly; take snapshot of data dir first              │
│   Seconds_Behind_Source > 1 hour sustained: check primary for long-running transactions               │
│   OOM kill of mysqld: check innodb_buffer_pool_size vs available RAM before restarting                │
│                                                                                                       │
│   What to collect                                                                                     │
│   SHOW MASTER STATUS / SHOW REPLICA STATUS \G: binlog position and replication state                  │
│   SHOW ENGINE INNODB STATUS \G: deadlocks, lock waits, and crash recovery state                       │
│   pt-query-digest: slow query log from last 24 hours                                                  │
│   dmesg | grep -i mysql: OOM killer messages referencing mysqld                                       │
│   /var/log/mysql/error.log: last 500 lines                                                            │
│                                                                                                       │
│   Support contacts                                                                                    │
│   Oracle MySQL support: support.oracle.com (Enterprise licence required)                              │
│   Percona support: percona.com/services (covers MySQL, MariaDB, and Percona Server)                   │
│   Community: forums.mysql.com, dba.stackexchange.com, #mysql on Libera.Chat IRC                       │
│                                                                                                       │
│   Key terms:                                                                                          │
│   Last_Error    = SHOW REPLICA STATUS field; MySQL error code and message for last failure            │
│   InnoDB crash recovery = automatic repair process on startup after unclean shutdown                  │
│   OOM kill      = Linux out-of-memory killer terminates mysqld to reclaim memory; check dmesg         │
│   Errno         = MySQL/Linux error number in replication status; 0 = no error                        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** root or sudo-capable account on target hosts
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

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
