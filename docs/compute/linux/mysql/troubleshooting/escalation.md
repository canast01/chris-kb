---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
---
# MySQL / MariaDB — Escalation

<div class="kb-summary">
How to escalate MySQL and MariaDB issues to Oracle MySQL support or Percona support: what data to collect, how to capture InnoDB status and replication state, step-by-step case creation, and the escalation path when progress stalls.

*Applies to: MySQL 8.x / MariaDB 10.x on RHEL / Ubuntu LTS*
</div>

```text
┌──────────────────────────────── MySQL / MariaDB — Escalation ─────────────────────────────────────────┐
│                                                                                                       │
│  Escalate MySQL/MariaDB issues to vendor support (Oracle or Percona) when the instance is             │
│  completely unreachable, InnoDB crash recovery is looping, replication is stopped with an             │
│  error that cannot be skipped safely, or data loss or corruption is suspected.                        │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 1 — Collect Data               │  │          Step 2 — Open the Case             │   │
│   │  Save error log (last 500 lines)             │  │  Oracle MySQL: support.oracle.com (MOS)     │   │
│   │  Run SHOW ENGINE INNODB STATUS               │  │  Percona: percona.com/services              │   │
│   │  Run SHOW REPLICA STATUS \G                  │  │  Severity: P1 (down) / P2 (degraded)        │   │
│   │  Run SHOW FULL PROCESSLIST                   │  │  Attach error log + InnoDB status + replic  │   │
│   │  Write timeline: last good → first failure   │  │  For P1: also call vendor phone support     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  For P1: do not restart mysqld repeatedly on crash recovery loop; take data dir snapshot first.       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 3 — Escalation Path            │  │         What NOT to Do                      │   │
│   │  T1: triage + confirm logs received          │  │  Do not run innodb_force_recovery > 3       │   │
│   │  T2: MySQL/MariaDB SE assigned; deep review  │  │  Do not flush binary logs before capture    │   │
│   │  DBA: involve DBA for schema or data issues  │  │  Do not delete corrupted .ibd files         │   │
│   │  P1 data loss: snapshot data dir before ops  │  │  Do not repeatedly restart on InnoDB loop   │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  InnoDB         = MySQL/MariaDB default storage engine; transactional; ACID-compliant                 │
│  REPLICA STATUS = SHOW REPLICA STATUS \G; shows replication position, lag, and errors                 │
│  Last_Error     = replication SQL thread error; error code + message; core for escalation             │
│  innodb_force_recovery = startup option 1-6; allows MySQL to start with InnoDB damage; dangerous      │
│  crash recovery = InnoDB automatic repair process on startup after unclean shutdown                   │
│  OOM kill       = Linux out-of-memory killer terminates mysqld; check with `dmesg`                    │
│  binlog         = binary log; records all changes for replication and point-in-time recovery          │
│  Errno          = OS-level error code in replication status; 0 = no error                             │
│  pt-query-digest = Percona tool; analyzes slow query log; install from percona-toolkit                │
│  ibdata1        = InnoDB shared tablespace file; corruption here is catastrophic                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access required:** MySQL `root` user or an account with `SUPER`, `REPLICATION CLIENT`, and `PROCESS` privileges; root or `sudo` on the Linux host; Oracle My Oracle Support (MOS) account (for Oracle MySQL Enterprise) or Percona account (for Percona support)
- **Do NOT restart mysqld repeatedly** when InnoDB crash recovery is looping — each failed restart attempt may make corruption worse; take a filesystem snapshot or `rsync` of the data directory first
- **Do NOT set `innodb_force_recovery` above 3** without explicit DBA or vendor guidance — levels 4–6 permanently disable redo log processing and can destroy data
- **Do NOT delete `.ibd` files** during a crash recovery — InnoDB tablespace files contain the actual table data; deleting them causes permanent data loss

---

## When to Escalate Immediately

Escalate to the DBA or vendor support without delay for any of these:

- **MySQL unreachable** — `systemctl status mysqld` shows failed; all connections refused
- **InnoDB crash recovery loop** — mysqld restarts repeatedly with InnoDB recovery errors
- **Replication stopped with `Errno != 0`** and the error cannot be skipped safely (data mismatch)
- **Disk full on data or log directory** — writes failing; data directory at 100%
- **OOM kill** — `dmesg | grep -i "Out of memory"` shows mysqld killed
- **Data corruption suspected** — `SHOW ENGINE INNODB STATUS` shows corruption errors; tables return incomplete data
- **`Seconds_Behind_Source` > 1 hour sustained** with no long-running transactions to explain it

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| MySQL service status | `systemctl status mysqld` or `mysqld_safe` | Active (running) |
| MySQL version | `mysqld --version` or `SELECT version()` | Note full version |
| Replication status | `SHOW REPLICA STATUS\G` | `Slave_SQL_Running: Yes`; `Last_Errno: 0` |
| Replication lag | `SHOW REPLICA STATUS\G` → `Seconds_Behind_Source` | Close to 0 |
| InnoDB status | `SHOW ENGINE INNODB STATUS\G` | No deadlock section; no corruption messages |
| Disk space | `df -h /var/lib/mysql` | Below 80% used |
| Active connections | `SHOW PROCESSLIST` | No sessions stuck in `Waiting for lock` > 60 sec |
| Error log recent | `tail -50 /var/log/mysqld.log` | No `[ERROR]` entries in the last hour |

---

## Step-by-Step Data Collection

### 1. Get the MySQL version and configuration

```bash
# MySQL/MariaDB version
mysqld --version
mysql -u root -p -e "SELECT VERSION(), @@datadir, @@innodb_buffer_pool_size, @@max_connections;"

# Key variables
mysql -u root -p -e "SHOW GLOBAL VARIABLES LIKE 'innodb%';" > /tmp/innodb-vars.txt
mysql -u root -p -e "SHOW GLOBAL STATUS;" > /tmp/global-status.txt
```

### 2. Save the error log

```bash
# Error log path varies by distribution
# RHEL/CentOS: /var/log/mysqld.log
# Ubuntu/Debian: /var/log/mysql/error.log
# or check: mysql -u root -p -e "SHOW VARIABLES LIKE 'log_error';"

sudo tail -500 /var/log/mysqld.log > /tmp/mysql-error-$(date +%Y%m%d%H%M).log

# Check for OOM kill in system log
sudo dmesg | grep -i "out of memory\|kill process\|mysqld" > /tmp/dmesg-mysql.txt
sudo grep -i "mysqld\|mysql\|oom" /var/log/messages 2>/dev/null | tail -100 >> /tmp/dmesg-mysql.txt
```

### 3. Capture InnoDB status (critical for crash and lock issues)

```bash
mysql -u root -p -e "SHOW ENGINE INNODB STATUS\G" > /tmp/innodb-status-$(date +%Y%m%d%H%M).txt

# Look for:
# - LATEST DETECTED DEADLOCK section
# - FILE I/O section for errors
# - BUFFER POOL AND MEMORY section
# - TRANSACTIONS section for long-running transactions
```

### 4. Capture replication status (if replica)

```bash
# On the replica server
mysql -u root -p -e "SHOW REPLICA STATUS\G" > /tmp/replica-status-$(date +%Y%m%d%H%M).txt

# On the primary: check binary log position
mysql -u root -p -e "SHOW MASTER STATUS\G" > /tmp/master-status.txt

# Binary log list
mysql -u root -p -e "SHOW BINARY LOGS;" > /tmp/binlog-list.txt
```

### 5. Capture active process list and blocking

```bash
# Full process list
mysql -u root -p -e "SHOW FULL PROCESSLIST;" > /tmp/processlist.txt

# Sessions waiting for locks
mysql -u root -p << 'SQL' > /tmp/lock-waits.txt
SELECT r.trx_id AS waiting_trx,
       r.trx_query AS waiting_query,
       b.trx_id AS blocking_trx,
       b.trx_query AS blocking_query,
       b.trx_started
FROM information_schema.INNODB_TRX b
JOIN information_schema.INNODB_TRX r
  ON r.trx_wait_started IS NOT NULL;
SQL
```

### 6. Write the timeline

```text
MySQL version: 8.0.36 (Community) / MariaDB 10.11.7 (Enterprise)
Host: db-prod-01.corp.local (RHEL 8.9, 32 GB RAM)
Role: Primary (db-prod-01) with 2 replicas (db-prod-02, db-prod-03)
Issue first observed: 2026-06-14 07:00 UTC
Last confirmed replication sync: 2026-06-14 06:30 UTC
Changes in 24h before the issue:
  - 06:00: MySQL 8.0.35 to 8.0.36 upgrade applied; service restarted
  - 06:30: db-prod-02 replica: Seconds_Behind_Source starts increasing
  - 07:00: db-prod-02: SHOW REPLICA STATUS shows Last_Errno 1062 (duplicate key)
  - 07:05: db-prod-02 SQL thread stopped; Seconds_Behind_Source: NULL
Steps already taken:
  - SHOW REPLICA STATUS: Last_Error = "Duplicate entry '12345' for key 'orders.PRIMARY'"
  - Did NOT run SET GLOBAL SQL_SLAVE_SKIP_COUNTER or SKIP (data integrity risk)
  - Did NOT restart mysqld on primary
Blast radius: db-prod-02 out of sync since 06:30 UTC; RPO window: 30 minutes if primary fails
```

---

## How to Open the Case

### Oracle MySQL Enterprise Support (My Oracle Support)

1. Go to **support.oracle.com** and sign in with your Oracle account linked to your MySQL Enterprise support contract.

2. Click **Create Service Request**.

3. Under **Product**, select **MySQL Server** and your version.

4. Under **Severity**, select:
   - **Severity 1**: MySQL completely down; data loss occurring; crash recovery looping; no workaround
   - **Severity 2**: Replication stopped; significant performance degradation; partial availability
   - **Severity 3**: Non-critical issue; workaround exists
   - **Severity 4**: How-to, pre-upgrade planning, non-urgent question

5. In the **Summary** field: symptom + scope. Example: `MySQL 8.0.36 — replica stopped with errno 1062 after upgrade 8.0.35→8.0.36, 30-minute RPO gap, primary still running`.

6. Under **Attachments**, upload: error log, InnoDB status output, replication status output.

7. Click **Submit**. **Sev 1**: also call Oracle Support — phone number listed in your MOS account.

### Percona Support (MySQL / MariaDB / Percona Server)

1. Go to **customers.percona.com** and sign in with your Percona customer account.

2. Click **Open a Ticket**.

3. Select the product (MySQL / MariaDB / Percona Server) and version.

4. Set severity (P1/P2/P3) based on production impact.

5. Attach: error log, InnoDB status, replication status, slow query log.

6. Submit. For P1, Percona provides 24×7 response.

---

## Escalation Path

```text
Step 1 — Engage DBA immediately for any P1 condition
         ↓
Step 2 — Open case at Oracle MOS or Percona with error log + InnoDB status + replication status
         ↓
Step 3 — T1 engineer acknowledges; reviews diagnostic data
         ↓
Step 4 — If no meaningful progress (Sev1: < 1 hr; Sev2: < 4 hr):
         → Reply: "Requesting escalation to MySQL/MariaDB Senior Engineer"
         → State: "[crash loop / replica down / data loss risk / production halted]"
         ↓
Step 5 — Senior engineer assigned; may request SSH access via jump host
         → Have root access to MySQL data directory and error log ready
         → Confirm a data directory snapshot exists before allowing any recovery steps
         ↓
Step 6 — If issue involves a confirmed MySQL/MariaDB bug (version regression):
         → Vendor escalates to engineering; may provide a specific build or workaround
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Restart mysqld repeatedly during InnoDB crash recovery loop | Each failed restart attempt may extend the corruption into additional pages | Take a snapshot or `rsync` of the data directory first; contact the DBA; let them guide the recovery |
| Set `innodb_force_recovery` above 3 without DBA/vendor guidance | Levels 4–6 permanently disable redo log processing; redo-based recovery is no longer possible after this | Use levels 1–3 incrementally (1, then 2, then 3) only under DBA supervision; document each attempt |
| Delete `.ibd` files or tablespace files during recovery | `.ibd` files contain the actual table data; deletion = permanent data loss | Never delete `.ibd` files; only rename them as a last resort under vendor guidance |
| Skip replication errors with `SQL_SLAVE_SKIP_COUNTER` for data integrity errors (errno 1062, 1032) | Skipping these errors causes the replica to diverge from the primary; data will differ between servers | Investigate why the duplicate key or missing row error occurred; contact the DBA before skipping any replication error |
| Flush or purge binary logs before capture | Binary logs are needed for point-in-time recovery and to diagnose the replication issue | Copy binary log files to a safe location before any purge operations |
| Run `myisamchk` or `mysqlcheck` on live InnoDB tables | `myisamchk` is for MyISAM only; running it on InnoDB tables can corrupt them | Use `mysqlcheck --innodb-optimize-only` or `OPTIMIZE TABLE` for InnoDB; check with DBA first |

---

## Useful Commands for Case Updates

```bash
# Paste these into every case update (as root on the MySQL host)

# MySQL version
mysql -u root -p -e "SELECT VERSION(), @@hostname;"

# Service status
systemctl status mysqld

# Error log recent entries
sudo tail -100 /var/log/mysqld.log

# InnoDB status (deadlocks, locks, crash info)
mysql -u root -p -e "SHOW ENGINE INNODB STATUS\G"

# Replication status
mysql -u root -p -e "SHOW REPLICA STATUS\G"

# Active sessions (lock waits)
mysql -u root -p -e "SHOW FULL PROCESSLIST;"

# Disk space on data directory
df -h /var/lib/mysql

# OOM kill check
dmesg | grep -i "kill process\|out of memory" | grep -i mysql | tail -20
```

---

## Support SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| Sev 1 / P1 | MySQL down; crash recovery looping; data loss; no workaround | Oracle: < 1 hr (24×7); Percona: < 1 hr (24×7) |
| Sev 2 / P2 | Replication down; performance degraded; partial availability | Oracle: < 4 hr (24×7); Percona: < 4 hr (24×7) |
| Sev 3 / P3 | Non-critical issue; workaround exists | Oracle/Percona: < 24 hr (business hours) |
| Sev 4 / P4 | How-to, planning, non-urgent question | Next business day |

---

## See also

- [MySQL — Diagnostics](diagnostics/)
- [MySQL — Common Issues](common-issues/)

---

## Verify resolution

- Run `systemctl status mysqld` and confirm the service is `active (running)`
- Run `SHOW ENGINE INNODB STATUS\G` and confirm no deadlock or corruption section in the output
- Run `SHOW REPLICA STATUS\G` on each replica and confirm `Slave_SQL_Running: Yes`, `Last_Errno: 0`, and `Seconds_Behind_Source` close to 0
- Run `df -h /var/lib/mysql` and confirm disk usage is below 80%
- Run `SHOW FULL PROCESSLIST` and confirm no sessions stuck in `Waiting for lock` for more than 10 seconds
- Test the previously failing application operation and confirm it succeeds
- Monitor `Seconds_Behind_Source` for 15 minutes on each replica to confirm lag is not growing
