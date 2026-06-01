# Reliability Engineering


<div class="kb-summary">
Reliability Engineering reference covering Core Principles, Redundancy Patterns, Reliability Metrics, Incident Review (Postmortem) Process, Toil Reduction and 1 more sections.
</div>

```
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
