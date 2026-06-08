# PostgreSQL — Escalation

<div class="kb-summary">
PostgreSQL escalation criteria — P1/P2 indicators, evidence bundle to collect before engaging DBA support, and crash recovery guidance.
</div>

## Escalation Thresholds

| Condition | Severity | Action |
|---|---|---|
| Database unreachable / postmaster down | P1 | Page DBA on-call immediately |
| Replica SQL stopped / replication broken | P2 | Alert DBA; begin lag triage |
| Lock wait chain > 10 min with app impact | P1 | Cancel blockers; page DBA |
| Disk > 90% on data dir or WAL | P1 | Emergency cleanup; page DBA |
| Corruption detected (PANIC in log) | P1 | Stop writes; do not restart; page DBA |
| Autovacuum wraparound warning | P2 | Alert DBA; schedule emergency vacuum |
| Connection exhaustion (`FATAL: connection limit exceeded`) | P1 | Kill idle sessions; page DBA |

## Evidence to Collect

```bash
# 1. Last 200 lines of error log
sudo tail -200 /var/log/postgresql/postgresql-*.log > /tmp/pg-error.log

# 2. Active queries
psql -U postgres -c "SELECT pid, state, wait_event_type, now()-query_start AS dur, left(query,80) FROM pg_stat_activity WHERE state != 'idle' ORDER BY dur DESC;" > /tmp/pg-activity.txt

# 3. Lock contention
psql -U postgres -c "SELECT * FROM pg_locks WHERE NOT granted;" > /tmp/pg-locks.txt

# 4. Replication status
psql -U postgres -c "SELECT * FROM pg_stat_replication;" > /tmp/pg-replication.txt

# 5. Disk usage
df -h /var/lib/postgresql > /tmp/disk.txt
du -sh /var/lib/postgresql/*/data/pg_wal/ >> /tmp/disk.txt

# 6. Autovacuum status
psql -U postgres -c "SELECT relname, n_dead_tup, last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 20;" > /tmp/pg-vacuum.txt
```

## Wraparound Emergency

```bash
# If VACUUM FREEZE needed urgently to prevent transaction ID wraparound
sudo -u postgres vacuumdb --all --freeze --analyze
# Or on specific database
psql -U postgres -c "VACUUM FREEZE ANALYZE;" app_prod
```

## Information for Vendor / DBA Support

- PostgreSQL version (`SELECT version()`)
- OS version (`uname -a`)
- Replication topology
- Timeline: when did the issue start?
- Recent changes: upgrades, schema changes, load spikes
- WAL archive status and last successful archive
