```bash
# Service running
systemctl status <service-name>

# Process exists
pgrep -a <process-name>

# Port listening
ss -tlnp | grep <port>

# Recent errors in logs
journalctl -u <service-name> --since "10 minutes ago" | grep -i error

# HTTP endpoint health
curl -sf http://localhost:<port>/health && echo "OK"
```

```text
┌────────────────────────────────────────── Change Validation ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Validation: pre-change baseline + post-change verification against success criteria      │   │
│   │         Document before/after state; define clear pass/fail criteria before execution         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Pre-Change         │  │        During Change        │  │         Post-Change         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │     Screenshot baseline     │  │       Step checkpoints      │  │       Success criteria      │   │
│   │        Config backup        │  │      Rollback triggers      │  │       Service healthy       │   │
│   │        Service state        │  │        Time tracking        │  │       Monitoring clean      │   │
│   │      Capacity baseline      │  │        Comms updates        │  │         Test results        │   │
│   │     Performance metrics     │  │        Decision gate        │  │         Close ticket        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │    Check type    │       What       │       Method      │  Pass criteria   │     If fails     │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Service      │   App response   │  Health endpoint  │   200 OK < 1s    │     Rollback     │   │
│   │    Monitoring    │  No new alerts   │   Alert console   │    All clear     │   Investigate    │   │
│   │   Performance    │  Latency normal  │     Dashboard     │ Within baseline  │     Rollback     │   │
│   │   Replication    │     In sync      │    Rep console    │ Lag < threshold  │   Investigate    │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Success criteria= Defined measurable outcomes that prove the change worked as intended             │
│    Rollback trigger= Specific condition (timeout, error, threshold breach) that activates backout     │
│    Decision gate   = Checkpoint mid-change where team decides: continue, pause, or rollback           │
│    Baseline        = Pre-change metric snapshot; used as comparison target for post-change check      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Check no active alerts after change
# In Prometheus / Alertmanager:
curl -s http://alertmanager:9093/api/v2/alerts | jq '[.[] | select(.status.state=="firing")]'

# Check dashboard shows no anomalies — look for:
# - Error rate spike
# - Latency increase > 20% above baseline
# - Resource utilisation jump (CPU, memory, disk I/O)
```
