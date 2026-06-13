---
tags:
  - servicenow
---
# Release Management


<div class="kb-summary">
Coordinates planning, scheduling, and execution of software and infrastructure releases to minimise risk and ensure controlled delivery.
</div>

## Release Types

| Type | Description | Cadence | Approval |
|---|---|---|---|
| Major release | New features, architectural changes | Quarterly / planned | Full CAB |
| Minor release | Bug fixes, minor enhancements | Monthly | Team lead + service owner |
| Patch / hotfix | Security patch, critical bug fix | As needed | Emergency CAB or team lead |
| Configuration release | Config-only changes (no code) | Weekly or ad hoc | Standard change |

## Release Lifecycle

```text
┌───────────────────────────────────────── Release Management ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Release management: package, schedule, and coordinate multi-change deployments        │   │
│   │         Release calendar: scheduled windows, freeze periods, and dependency sequencing        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Planning          │  │          Execution          │  │          Close-out          │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │      Release packaging      │  │       Sequenced deploy      │  │        Release review       │   │
│   │        Dependency map       │  │         Gate checks         │  │       Lessons learned       │   │
│   │      Go/No-Go criteria      │  │       Rollback trigger      │  │        Metrics review       │   │
│   │        Freeze periods       │  │        Communication        │  │        Backlog update       │   │
│   │      Stakeholder comms      │  │        Live dashboard       │  │         RFC closure         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   │      Phase       │     Timeline     │        Gate       │      Owner       │     Artefact     │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │     Planning     │      T-14d       │    Release plan   │   Release mgr    │   Release doc    │   │
│   │      Freeze      │       T-7d       │    No new items   │    Change mgr    │  Freeze notice   │   │
│   │     Go/No-Go     │       T-1h       │  All checks pass  │   Release mgr    │   Decision log   │   │
│   │      Review      │       T+2d       │   Success verify  │   Release mgr    │  Review report   │   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Release package= Group of related changes deployed together in a coordinated window                │
│    Freeze period  = No new changes added to release after freeze date; scope locked                   │
│    Dependency map = Which changes must complete before others can start; sequence critical            │
│    Go/No-Go call  = Release decision meeting T-1h; all dependencies and pre-checks confirmed          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Go / No-Go Decision

At the start of the change window, explicitly confirm go/no-go:

| Check | Go Condition |
|---|---|
| Source environment healthy | All services green in staging |
| Target environment healthy | No active incidents in prod |
| Team available | Implementer + approver + on-call present |
| Rollback confirmed available | Rollback steps validated < 4h ago |
| Stakeholders notified | Notification acknowledged |

If any check fails: defer the release; communicate delay to stakeholders.

## Post-Release Actions

- Monitor for 30–60 min (production soak)
- Publish release notes to internal wiki / changelog
- Update CMDB with new software versions
- Close all linked change and release tickets
- Schedule post-release review for major releases (within 1 week)
