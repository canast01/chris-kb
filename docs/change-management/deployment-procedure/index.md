```bash
# Snapshot / backup before change (example: VM snapshot)
# Azure
az snapshot create -g <rg> -n <snapshot-name> --source <disk-id>

# AWS
aws ec2 create-snapshot --volume-id <vol-id> --description "pre-change-ITSM-XXXX"

# Linux — configuration backup
tar czf /root/pre-change-config-$(date +%Y%m%d).tar.gz /etc/<service>/

# Verify service is healthy before starting
systemctl status <service>
curl -sf http://localhost:<port>/health
```

```text
┌──────────────────────────────────────── Deployment Procedure ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Deployment: execute change per approved RFC; document each step and outcome          │   │
│   │         No deviation from approved steps without ECAB approval; call out any variance         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Deployment Steps               │  │                Documentation                │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │          1. Go/No-Go decision call           │  │                Log start time               │   │
│   │        2. Confirm attendees on bridge        │  │           Capture each step output          │   │
│   │        3. Execute RFC steps in order         │  │             Note any deviations             │   │
│   │        4. Checkpoint after each tier         │  │            Screenshot key states            │   │
│   │           5. Run validation checks           │  │            Log end time + outcome           │   │
│   │          6. Go/No-Go for next phase          │  │             Notify stakeholders             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│   │    Checkpoint    │     Trigger      │      Decision     │     If pass      │     If fail      │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Go/No-Go     │   Before exec    │     Team vote     │     Proceed      │   Defer change   │   │
│   │    Mid-change    │ After each tier  │    Lead decides   │    Next step     │     Rollback     │   │
│   │    Validation    │ After last step  │    Test results   │   Close change   │     Rollback     │   │
│   │   Time overrun   │  Beyond window   │    Lead decides   │   Brief extend   │     Rollback     │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Go/No-Go   = Explicit decision call before proceeding; requires confirmation from lead             │
│    Deviation   = Any step that differs from approved RFC; document and get verbal ECAB approval       │
│    Time overrun= Execution exceeds approved window; decision: extend (if safe) or rollback            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Remove temporary files and pre-change backups (after soak period)
rm /etc/<service>.conf.pre-<date>   # only after validation passes

# Update ITSM ticket: outcome, duration, any deviations
```
```text
Validation fails?
  ├─ Immediate: service down / error rate > 3×baseline
  │     → Roll back now; notify stakeholders
  └─ Degraded: latency elevated / some errors
        → Investigate for 10 min
              ├─ Improving → continue soak
              └─ Not improving → roll back
```
```bash
# Restore config from backup
cp /etc/<service>.conf.pre-<date> /etc/<service>.conf
systemctl restart <service>

# Rollback package to previous version
apt-get install <package>=<prev-version>

# Rollback DB migration
psql -U <user> -d <db> -f migration_XXXX_down.sql

# Re-validate after rollback (same checks as Phase 3)
```
```markdown
Change:        ITSM-XXXX
Date/Time:     2026-05-06 22:00 UTC
Implementer:   <name>
Window:        22:00 – 23:00 UTC

Pre-change backup: Snapshot snap-abc123 created 21:55 UTC
Implementation:    Deployed package nginx=1.24.0-2 at 22:04 UTC
Restart:           Service restarted 22:05 UTC; came up in 8 seconds
Validation:        Health check OK; error rate 0%; latency normal
Monitoring soak:   22:05 – 22:40 UTC — no alerts fired
Outcome:           Success
Ticket closed:     22:42 UTC
```
