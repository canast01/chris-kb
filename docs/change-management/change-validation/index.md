# Change Validation


<div class="kb-summary">
Post-implementation checks to confirm a change achieved its intent, introduced no regressions, and the system is in a known-good state.
</div>

## Validation Phases

| Phase | Timing | Purpose |
|---|---|---|
| Immediate validation | During change window | Confirm core function restored |
| Smoke tests | First 15 min post-change | Catch obvious regressions |
| Monitoring soak | 30–60 min post-change | Detect latent issues before closing |
| Closure validation | End of window | Sign-off criteria met |

## Service Validation — Linux

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

## Monitoring Verification

```bash
# Check no active alerts after change
# In Prometheus / Alertmanager:
curl -s http://alertmanager:9093/api/v2/alerts | jq '[.[] | select(.status.state=="firing")]'

# Check dashboard shows no anomalies — look for:
# - Error rate spike
# - Latency increase > 20% above baseline
# - Resource utilisation jump (CPU, memory, disk I/O)
```

## Validation Checklist

- [ ] Target service/application is responding correctly
- [ ] All dependent services confirmed healthy
- [ ] No new errors in application logs since change
- [ ] No new alerts firing in monitoring system
- [ ] Performance metrics within normal baseline (CPU, latency, error rate)
- [ ] Replication/HA status healthy (if applicable)
- [ ] User acceptance confirmed (if user-facing change)
- [ ] Rollback criteria: change stays implemented (not rolled back)

## Failure Criteria — Trigger Rollback If

| Condition | Threshold |
|---|---|
| Service fails health check | Immediate |
| Error rate above baseline | > 3× sustained for 5 min |
| Critical alert fires | Any P1/P2 alert |
| Key metric degraded | CPU > 95% / latency > 3× SLO / disk full |
| Replication broken | Replica lag > 5 min or stopped |

## Closure Requirements

Before closing the ITSM change ticket:

1. All validation checklist items ticked
2. Monitoring soak period completed (min 30 min for Normal changes)
3. Stakeholders notified of completion
4. Change outcome recorded: `Success / Partial success / Rolled back`
5. Lessons learned noted (for High-risk or rolled-back changes)
