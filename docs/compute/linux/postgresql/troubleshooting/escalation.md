---
tags:
  - linux
  - troubleshooting
search:
  boost: 1.5
---
# PostgreSQL — Escalation

<div class="kb-summary">
How to escalate PostgreSQL issues to vendor support (EDB, Percona, or Crunchy Data): what data to collect, how to capture pg_stat_activity and WAL state, step-by-step case creation, and the escalation path when progress stalls.

*Applies to: PostgreSQL 14 / 15 / 16 on RHEL / Ubuntu LTS*
</div>

```text
┌───────────────────────────────── PostgreSQL — Escalation ─────────────────────────────────────────────┐
│                                                                                                       │
│  Escalate PostgreSQL issues to vendor support or DBA on-call when the postmaster is completely        │
│  down, a PANIC entry appears in the log (data corruption), a lock wait chain exceeds 10 minutes,      │
│  disk on the data directory or WAL volume exceeds 90%, or XID wraparound is imminent.                 │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 1 — Collect Data               │  │          Step 2 — Open the Case             │   │
│   │  Save error log (last 500 lines)             │  │  EDB: support.enterprisedb.com              │   │
│   │  Capture pg_stat_activity + pg_locks         │  │  Percona: customers.percona.com             │   │
│   │  Run pg_stat_replication (if primary)        │  │  Crunchy: access.crunchydata.com            │   │
│   │  Check disk on PGDATA and WAL volume         │  │  Severity: P1 (down) / P2 (degraded)        │   │
│   │  Write timeline: last good → first failure   │  │  Attach error log + pg_stat_activity output │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  For P1: engage DBA on-call immediately AND open vendor support case.                                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Step 3 — Escalation Path            │  │         What NOT to Do                      │   │
│   │  T1: triage + confirm log received           │  │  Do not restart on PANIC without DBA        │   │
│   │  T2: PG SE assigned; deep log analysis       │  │  Do not cancel active long-running txns     │   │
│   │  DBA: involve for schema or data issues      │  │  Do not delete WAL files manually           │   │
│   │  P1 wraparound: emergency VACUUM FREEZE now  │  │  Do not run VACUUM FULL on large tables     │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  postmaster     = master PostgreSQL daemon; runs as postgres OS user; owns all backends               │
│  PANIC          = PostgreSQL log level for unrecoverable error; indicates corruption risk             │
│  WAL            = Write-Ahead Log; transaction journal; loss of WAL = data loss or unrecoverable      │
│  wraparound     = XID (transaction ID) exhaustion; PG shuts down DB at limit; requires VACUUM         │
│  VACUUM FREEZE  = forces visibility update on all rows; prevents XID wraparound shutdown              │
│  pg_blocking_pids = function returning PIDs holding locks that block a given session                  │
│  PGDATA         = PostgreSQL data directory; contains cluster config, data, and WAL by default        │
│  pg_stat_activity = system view; shows all active connections and their current query/state           │
│  pg_locks       = system view; shows all current lock requests; NOT granted = waiting                 │
│  autovacuum     = background daemon; automatically vacuums tables; critical for XID wraparound        │
│  EDB            = EnterpriseDB; provides PostgreSQL enterprise support and extensions                 │
│  replication slot = WAL retention mechanism for streaming replicas; can cause disk fill if stuck      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Before you begin

- **Access required:** `postgres` OS user or `sudo` access; PostgreSQL superuser role; vendor support account at your PostgreSQL support provider (EDB, Percona, or Crunchy Data)
- **Do NOT restart the postmaster** when a PANIC entry is in the log without DBA guidance — a restart may overwrite shared memory state that is needed to diagnose the corruption
- **Do NOT delete WAL files** manually — WAL files are the transaction journal; deleting them causes data loss and makes the cluster unrecoverable without a full restore
- **Do NOT cancel long-running transactions** during a lock wait incident without DBA review — the blocking transaction may be in a state where cancellation causes a partial rollback that takes longer than the original transaction

---

## When to Escalate Immediately

Escalate to DBA on-call and open a vendor support case without delay for any of these:

- **Postmaster down** — `systemctl status postgresql` shows failed; `pg_isready` returns error
- **PANIC in error log** — indicates data corruption or unrecoverable error; do not restart without DBA
- **Lock wait chain > 10 minutes** with application impact; applications timing out
- **Disk > 90%** on PGDATA directory or WAL volume — writes failing or about to fail
- **XID wraparound imminent** — log message: `database with OID XXXXX must be vacuumed within X transactions`
- **Replication slot lag > 10 GB** — slot is retaining WAL and filling the disk
- **Connection exhaustion** — `FATAL: remaining connection slots are reserved for non-replication superuser connections`

---

## Pre-Escalation Self-Check

Run these before opening the case.

| Check | Command | Expected result |
|---|---|---|
| PostgreSQL version | `psql -c "SELECT version();"` | Note full version |
| Service status | `systemctl status postgresql` or `pg_isready` | Running / accepting connections |
| Active connections | `psql -c "SELECT count(*) FROM pg_stat_activity;"` | Below `max_connections` |
| Lock waits | `psql -c "SELECT count(*) FROM pg_locks WHERE NOT granted;"` | Zero |
| Replication lag | `psql -c "SELECT * FROM pg_stat_replication;"` | `sent_lsn` close to `write_lsn` |
| Disk space | `df -h $PGDATA` | Below 80% used |
| WAL volume | `df -h` on pg_wal or pg_xlog partition | Below 80% used |
| Autovacuum running | `psql -c "SELECT count(*) FROM pg_stat_activity WHERE query LIKE 'autovacuum%';"` | > 0 (autovacuum active) |
| Error log recent | `tail -50 /var/log/postgresql/postgresql-*.log` | No PANIC or FATAL entries |

---

## Step-by-Step Data Collection

### 1. Get the PostgreSQL version and configuration

```bash
# Version
psql -U postgres -c "SELECT version();"

# Key configuration parameters
psql -U postgres -c "SHOW ALL;" > /tmp/pg-config-$(date +%Y%m%d).txt

# Data directory and log path
psql -U postgres -c "SHOW data_directory; SHOW log_directory;"
```

### 2. Save the PostgreSQL error log

```bash
# Log directory (varies by distribution)
# RHEL: /var/lib/pgsql/<version>/data/log/ or /var/log/postgresql/
# Ubuntu: /var/log/postgresql/postgresql-<version>-main.log

# Save last 500 lines
sudo tail -500 /var/log/postgresql/postgresql-*.log > /tmp/pg-error-$(date +%Y%m%d%H%M).log

# Search for PANIC and FATAL entries (the critical ones)
grep -E "PANIC|FATAL|ERROR" /tmp/pg-error-$(date +%Y%m%d%H%M).log | tail -100
```

### 3. Capture active sessions and lock waits

```bash
# Active sessions with duration and query
psql -U postgres << 'SQL' > /tmp/pg-activity-$(date +%Y%m%d%H%M).txt
SELECT pid, usename, application_name, client_addr, state,
       now() - query_start AS query_duration,
       wait_event_type, wait_event,
       LEFT(query, 200) AS query_text
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_duration DESC NULLS LAST;
SQL

# Lock waits (sessions blocked waiting for a lock)
psql -U postgres << 'SQL' >> /tmp/pg-activity-$(date +%Y%m%d%H%M).txt
SELECT blocked.pid AS blocked_pid,
       blocked.query AS blocked_query,
       blocking.pid AS blocking_pid,
       blocking.query AS blocking_query,
       now() - blocked.query_start AS wait_duration
FROM pg_stat_activity AS blocked
JOIN pg_stat_activity AS blocking
  ON blocking.pid = ANY(pg_blocking_pids(blocked.pid))
WHERE NOT blocked.granted;
SQL
```

### 4. Capture replication state (if primary with replicas)

```bash
# On the primary server
psql -U postgres << 'SQL' > /tmp/pg-replication-$(date +%Y%m%d%H%M).txt
SELECT client_addr, state, sent_lsn, write_lsn, flush_lsn, replay_lsn,
       pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes,
       sync_state
FROM pg_stat_replication;

-- Replication slots (check for stuck slots filling WAL)
SELECT slot_name, plugin, slot_type, active, restart_lsn,
       pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) AS lag_bytes
FROM pg_replication_slots;
SQL
```

### 5. Capture disk usage and vacuum state

```bash
# Disk space on PGDATA and WAL
df -h $PGDATA
df -h  # full disk picture

# Autovacuum status (tables with high dead tuple counts)
psql -U postgres << 'SQL' > /tmp/pg-vacuum-$(date +%Y%m%d).txt
SELECT schemaname, relname, n_live_tup, n_dead_tup,
       round(n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100, 1) AS dead_pct,
       last_autovacuum, last_autoanalyze
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC
LIMIT 20;
SQL

# XID wraparound distance (tables needing freeze)
psql -U postgres << 'SQL' >> /tmp/pg-vacuum-$(date +%Y%m%d).txt
SELECT datname, age(datfrozenxid) AS xid_age,
       2147483647 - age(datfrozenxid) AS xids_remaining
FROM pg_database
ORDER BY age(datfrozenxid) DESC;
SQL
```

### 6. Write the timeline

```text
PostgreSQL version: 16.2 (Ubuntu 16.2-1.pgdg22.04+1)
Host: db-prod-01.corp.local (Ubuntu 22.04, 64 GB RAM)
Role: Primary; 2 streaming replicas (db-prod-02 standby, db-prod-03 standby)
PGDATA: /var/lib/postgresql/16/main/
Issue first observed: 2026-06-14 12:00 UTC
Last confirmed healthy: 2026-06-14 10:00 UTC
Changes in 24h before the issue:
  - 10:00: nightly maintenance job ran; included ALTER TABLE orders ADD COLUMN
  - 12:00: application reports connection timeouts from app servers
  - 12:05: pg_stat_activity: 150 sessions in state "idle in transaction" for > 30 min
  - 12:10: pg_locks: 80 sessions blocked waiting for lock on "orders" table
Steps already taken:
  - Identified head blocker: PID 12345, idle in transaction since 10:00 UTC
  - Did NOT cancel the blocking session (awaiting DBA review)
  - Did NOT restart PostgreSQL
Blast radius: All writes to "orders" table blocked; e-commerce checkout halted; 500 users affected
```

---

## How to Open the Case

### EDB (EnterpriseDB) — EDB Postgres Advanced Server / EDB community support

1. Go to **support.enterprisedb.com** and sign in with your EDB customer account.
2. Click **Open a Case** → select **PostgreSQL** or **EDB Postgres Advanced Server**.
3. Set severity based on impact (Critical/High/Medium/Low).
4. Attach: error log, pg_stat_activity output, replication state, timeline.
5. For Critical: call EDB support — phone number is in your contract portal.

### Percona — PostgreSQL support

1. Go to **customers.percona.com** and sign in.
2. Click **Open a Ticket** → select **PostgreSQL**.
3. Set severity: P1 (down), P2 (degraded), P3 (non-critical).
4. Attach: error log, pg_stat_activity output, replication state, timeline.
5. For P1: Percona provides 24×7 response.

### Crunchy Data — PostgreSQL support

1. Go to **access.crunchydata.com** and sign in with your Crunchy customer account.
2. Open a support ticket under **PostgreSQL**.
3. Attach diagnostic data and timeline.

In all cases, include in the description:
- Full `SELECT version()` output
- OS version (`uname -a`, `cat /etc/os-release`)
- Replication topology (primary/replica count, streaming vs. logical)
- Disk state (df -h output)
- Recent changes (schema changes, upgrades, load spikes)

---

## Escalation Path

```text
Step 1 — Engage DBA on-call immediately for any P1 condition
         ↓
Step 2 — Open vendor support case with error log + pg_stat_activity + replication state
         ↓
Step 3 — T1 engineer acknowledges and reviews diagnostic data
         ↓
Step 4 — If no meaningful progress (P1: < 1 hr; P2: < 4 hr):
         → Reply: "Requesting escalation to PostgreSQL Senior Engineer"
         → State: "[postmaster down / PANIC in log / lock chain / wraparound imminent]"
         ↓
Step 5 — Senior engineer assigned; may request SSH access to the PostgreSQL host
         → Have OS-level access and PostgreSQL superuser credentials ready
         → Confirm a file-level backup or snapshot exists before allowing recovery steps
         ↓
Step 6 — If issue involves a confirmed PostgreSQL bug:
         → Vendor escalates to engineering; may provide a patch or specific workaround
```

---

## What NOT to Do

| Do NOT do this | Why | What to do instead |
|---|---|---|
| Restart the postmaster when PANIC is in the log without DBA | PANIC indicates an unrecoverable state; a restart may overwrite shared memory state needed to diagnose the corruption | Preserve the current state; take a filesystem snapshot if possible; contact DBA before restart |
| Delete WAL files manually | WAL files are the transaction journal; manual deletion causes data loss and leaves the cluster unrecoverable without a full restore from backup | If WAL is filling the disk due to a stuck replication slot, drop the unused slot instead: `SELECT pg_drop_replication_slot('<slot>');` |
| Cancel long-running transactions without DBA review | The blocking transaction may be managing a large batch operation; cancellation triggers a partial rollback that could take longer than the original transaction | Report the PID to DBA; wait for DBA direction before running `SELECT pg_cancel_backend(<pid>)` |
| Run `VACUUM FULL` on large tables during a live incident | VACUUM FULL acquires an exclusive lock and rewrites the table; on large tables it can take hours and blocks all writes | For dead tuple cleanup, use regular `VACUUM ANALYZE` which is non-blocking; only use VACUUM FULL with DBA guidance |
| Manually modify files in PGDATA | PGDATA is a tightly controlled binary format; any file-level modification corrupts the cluster | All recovery operations must go through PostgreSQL tools (`pg_resetwal`, `pg_filedump`) with vendor guidance |
| Set `maintenance_work_mem` very high for VACUUM FREEZE without DBA | Can cause OOM if multiple autovacuum workers are running simultaneously | Let autovacuum manage the freeze; only manually tune with DBA review of memory constraints |

---

## Useful Commands for Case Updates

```bash
# Paste these into every case update (as postgres user or with sudo)

# Service status
systemctl status postgresql

# Active session count and states
psql -U postgres -c "SELECT state, count(*) FROM pg_stat_activity GROUP BY state;"

# Lock waits (non-zero = blocking occurring)
psql -U postgres -c "SELECT count(*) FROM pg_locks WHERE NOT granted;"

# Replication lag (run on primary)
psql -U postgres -c "SELECT client_addr, state, pg_wal_lsn_diff(sent_lsn, replay_lsn) AS lag_bytes FROM pg_stat_replication;"

# XID wraparound distance (run on each DB)
psql -U postgres -c "SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY age DESC;"

# Disk space on PGDATA and WAL
df -h $PGDATA

# Error log recent entries
tail -100 /var/log/postgresql/postgresql-*.log | grep -E "PANIC|FATAL|ERROR"
```

---

## Wraparound Emergency Procedure

If the PostgreSQL log shows "must be vacuumed within X transactions":

```bash
# Emergency VACUUM FREEZE to prevent wraparound shutdown
# Run on the AFFECTED DATABASE as postgres superuser
vacuumdb --all --freeze --analyze --echo 2>&1 | tee /tmp/vacuum-freeze-$(date +%Y%m%d).log

# Or targeted at a specific database
vacuumdb --dbname=app_prod --freeze --analyze --echo

# Monitor progress
psql -U postgres -c "SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY age DESC;"
```

---

## Support SLA Reference

| Severity | Definition | Initial Response SLA |
|---|---|---|
| P1 / Critical | Postmaster down; PANIC in log; data loss; wraparound imminent | EDB/Percona: < 1 hr (24×7) |
| P2 / High | Replication broken; lock chain; disk > 90%; partial availability | EDB/Percona: < 4 hr (24×7) |
| P3 / Medium | Non-critical issue; performance degradation; workaround available | Business hours |
| P4 / Low | How-to, planning, non-urgent configuration review | Next business day |

---

## See also

- [PostgreSQL — Diagnostics](diagnostics/)
- [PostgreSQL — Common Issues](common-issues/)

---

## Verify resolution

- Run `systemctl status postgresql` and confirm the service is `active (running)`
- Run `SELECT count(*) FROM pg_locks WHERE NOT granted;` and confirm zero lock waits
- Run `SELECT state, count(*) FROM pg_stat_activity GROUP BY state;` and confirm no large number of sessions in `idle in transaction`
- Run `SELECT datname, age(datfrozenxid) FROM pg_database ORDER BY age DESC;` and confirm XID age is safely below the wraparound limit
- Run `df -h $PGDATA` and confirm disk usage is below 80%
- On each replica: run `SELECT * FROM pg_stat_replication;` on the primary and confirm lag is near zero
- Test the previously failing application operation and confirm it succeeds
- Monitor `pg_stat_activity` for 15 minutes to confirm lock waits do not re-form
