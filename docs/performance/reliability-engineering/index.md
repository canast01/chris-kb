# Reliability Engineering


<div class="kb-summary">
Reliability Engineering reference covering Core Principles, Redundancy Patterns, Reliability Metrics, Incident Review (Postmortem) Process, Toil Reduction and 1 more sections.
</div>

```text
┌──────────────────────────────── Performance — Reliability Engineering ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Reliability engineering: measure, track, and improve system dependability over time      │   │
│   │        MTTR: reduce by improving detection, runbooks, and automation of recovery steps        │   │
│   │       MTBF: improve by eliminating failure causes via root cause analysis and hardening       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Metrics                    │  │             Improvement Actions             │   │
│   │      ─────────────────────────────────       │  │      ─────────────────────────────────      │   │
│   │               MTTR per service               │  │         Automate detection (alerts)         │   │
│   │               MTBF per service               │  │           Improve runbook quality           │   │
│   │                Availability %                │  │           RCA + corrective actions          │   │
│   │              Incident frequency              │  │          Eliminate repeat failures          │   │
│   │             Change failure rate              │  │            Improve test coverage            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    MTTR         = Mean Time To Recover; total incident downtime / number of incidents                 │
│    MTBF         = Mean Time Between Failures; total uptime / number of failures                       │
│    Availability = (MTBF / (MTBF + MTTR)) * 100%; four nines = 99.99% = ~52 min/yr                     │
│    Change fail rate= % of changes causing incidents; target < 5% per DORA metrics                     │
│    FMEA         = Failure Mode and Effects Analysis; proactive failure scenario assessment            │
│    Toil         = Repetitive manual work; automate to reduce MTTR and operator error                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Reliability engineering systematically improves system resilience through redundancy, failure testing, and learning from incidents.

## Core Principles

| Principle | Meaning |
|---|---|
| Embrace failure | Assume components will fail; design for it |
| Measure everything | Reliability without metrics is guesswork |
| Error budgets | Balance reliability investment vs feature velocity |
| Eliminate toil | Automate repetitive operational work |
| Postmortems | Learn from every significant incident |

## Redundancy Patterns

| Layer | Pattern | Example |
|---|---|---|
| Compute | Active/active cluster | HAProxy, Kubernetes, VMware HA |
| Storage | RAID, erasure coding, replication | RAID6, ONTAP SnapMirror, SRDF |
| Network | Bonding/LACP, dual uplinks | Linux bonding mode 4, Cisco LACP |
| Power | Dual PSU, UPS, dual PDU | A+B power feeds per rack |
| Geographic | Multi-site / multi-AZ | ASR, Route 53 failover, SRM |

## Reliability Metrics

| Metric | Formula | Target |
|---|---|---|
| Availability | (Total time − Downtime) / Total time | ≥ 99.9% |
| MTTR (Mean Time to Recover) | Avg time from failure detection to service restore | < 30 min for P1 |
| MTBF (Mean Time Between Failures) | Avg time between incidents | Track trend — improvement over time |
| Change failure rate | % of changes causing incidents | < 5% |
| Error budget consumption | Downtime vs SLO budget | < 100% per month |

## Incident Review (Postmortem) Process

Every P1 and P2 incident should produce a blameless postmortem:

1. **Timeline** — reconstruct events from monitoring, logs, and team recollection
2. **Root cause** — what was the underlying cause? (not just the symptom)
3. **Contributing factors** — what made it worse or harder to detect?
4. **Impact** — duration, affected users/systems, SLO budget consumed
5. **What went well** — detection speed, response, communication
6. **Action items** — specific, owned, time-bounded improvements

```markdown
Postmortem: Database Connection Pool Exhaustion
Date: 2026-05-05
Duration: 44 minutes downtime
Impact: ERP unavailable; ~200 users affected

Timeline:
  14:23 — Monitoring alert: ERP returning 503
  14:25 — On-call acknowledged; investigation started
  14:38 — Root cause identified: connection pool exhausted
  15:07 — Service restored after pool restart and slow query fixed

Root cause: A missing index caused queries to run 40× slower than baseline,
exhausting the 100-connection pool within 5 minutes.

Action items:
  1. Add missing index (DBA — due 2026-05-07) ✓
  2. Add query time alerting in APM (Dev — due 2026-05-15)
  3. Increase connection pool timeout alert threshold from 95% to 80% (Infra — due 2026-05-12)
```

## Toil Reduction

Toil is manual, repetitive, automatable operational work that scales with system size.

Identify toil by asking: "If we doubled our infrastructure, would this task double?"

| Toil Task | Automation Approach |
|---|---|
| Manual certificate renewal | Certbot / Venafi auto-renew |
| Manual backup verification | Automated restore test script |
| Repetitive health check commands | Dashboard; automated alert |
| Manual log review for errors | Log alerting on error patterns |
| VM snapshot cleanup | Automated retention policy |

## Reliability Improvement Checklist

- [ ] All P1/P2 incidents have blameless postmortems within 5 business days
- [ ] Action items from postmortems tracked and completed
- [ ] Failure testing (chaos) run quarterly for critical services
- [ ] Error budget tracked and visible to team each month
- [ ] SLO review completed quarterly
- [ ] Single points of failure identified and have a documented mitigation plan
