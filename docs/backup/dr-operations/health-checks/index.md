---
tags:
  - dr
---
# Health Checks


<div class="kb-summary">
Health Checks operational notes and deep-dive references.
</div>
```text
┌────────────────────────── Project Management Health Checks — Health Checks ───────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Health Checks health checks: routine verification of operational status and performance    │   │
│   │         Checks include: controller status, drive health, replication lag, and capacity        │   │
│   │         Frequency: daily quick checks; weekly detailed review; monthly capacity report        │   │
│   │        Configure threshold-based alerts for proactive incident prevention and awareness       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Check status → review alerts → verify replication → capacity → log                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Check area    │  How to verify   │   Pass criteria   │    Frequency     │       Tool       │   │
│   │   Controllers    │   show status    │    All healthy    │      Daily       │     CLI/GUI      │   │
│   │      Drives      │   show drives    │  No failed/pred.  │      Daily       │     CLI/GUI      │   │
│   │   Replication    │ show replication │  Lag < threshold  │      Daily       │     CLI/GUI      │   │
│   │     Capacity     │  show capacity   │     < 80% used    │      Daily       │     CLI/GUI      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Project Management Health Checks infrastructure · management network · monitoring        │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Health Checks      = Project Management Health Checks platform overview and core concepts          │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Run This Routine

Run these steps as the standard project management health check sequence — before any change window, after any incident, and at each scheduled review.

1. **Daily checks first** — Open the [Daily Checks](daily-checks/) page and work through every line item. Confirm all indicators are green before proceeding. Log any amber or red items as follow-up actions.
2. **Open change review** — Verify all in-flight changes have an approved ticket and an assigned owner. Confirm no change is past its scheduled end time without a status update.
3. **Incident and risk log review** — Confirm no open P1/P2 incidents are linked to this project. Review the risk register for items that have become active; escalate anything newly triggered.
4. **Pre-change readiness (if applicable)** — If a change is scheduled, open [Pre Change](pre-change/) and complete all readiness checks: rollback plan confirmed, communication sent, maintenance window open.
5. **Post-change validation (if applicable)** — After a change completes, open [Post Change](post-change/) and run all validation steps. Capture evidence in [Evidence](evidence/) before closing the change ticket.
6. **Follow-up action review** — Open [Follow Up](follow-up/) and confirm all outstanding actions have owners and due dates. Escalate any overdue items.
7. **Record and sign off** — Log the date, checks performed, issues found, and actions taken. Confirm the next check-due date is set in the team calendar.

<div class="kb-grid kb-grid-5">

<a class="kb-card" href="daily-checks/">
  <strong>Daily Checks</strong>
  <span>Daily Checks notes, checks, references, and validation.</span>
</a>

<a class="kb-card" href="pre-change/">
  <strong>Pre Change</strong>
  <span>Pre Change notes, checks, references, and validation.</span>
</a>

<a class="kb-card" href="post-change/">
  <strong>Post Change</strong>
  <span>Post Change notes, checks, references, and validation.</span>
</a>

<a class="kb-card" href="evidence/">
  <strong>Evidence</strong>
  <span>Evidence notes, checks, references, and validation.</span>
</a>

<a class="kb-card" href="follow-up/">
  <strong>Follow Up</strong>
  <span>Follow Up notes, checks, references, and validation.</span>
</a>

</div>
