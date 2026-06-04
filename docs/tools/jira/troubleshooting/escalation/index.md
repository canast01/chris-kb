# Jira — Escalation


<div class="kb-summary">
Escalation reference covering Escalation Matrix, Emergency Contacts, Escalation Communication Template, Post-Incident Review (PIR) Checklist.
</div>

## Escalation Matrix

```mermaid
flowchart TD
    ISSUE([Issue Reported]) --> L1[L1 — Operations / Service Desk\nFirst response, known issues,\npassword resets, basic config]

    L1 --> L1_RESOLVE{Resolved\nat L1?}
    L1_RESOLVE -- Yes --> DONE([Resolved])
    L1_RESOLVE -- No --> L1_TIME{Within\nL1 SLA?}
    L1_TIME -- No --> L2_ESC[Escalate to L2]
    L1_TIME -- Yes --> L1

    L2_ESC --> L2[L2 — Jira Administrator\nAdvanced config, integrations,\nlog analysis, plugin issues,\nperformance troubleshooting]

    L2 --> L2_RESOLVE{Resolved\nat L2?}
    L2_RESOLVE -- Yes --> DONE
    L2_RESOLVE -- No --> L2_TIME{Within\nL2 SLA?}
    L2_TIME -- No --> L3_ESC[Escalate to L3]
    L2_TIME -- Yes --> L2

    L3_ESC --> L3[L3 — Senior Engineer / Atlassian Support\nData corruption, code-level bugs,\nDB schema issues, cluster failures,\nAtlassian vendor engagement]

    L3 --> L3_RESOLVE{Resolved\nat L3?}
    L3_RESOLVE -- Yes --> DONE
    L3_RESOLVE -- No --> VENDOR[Escalate to Atlassian\nSupport / Emergency Hotline]

    VENDOR --> DONE

    style DONE fill:#2d8a4e,color:#fff
    style VENDOR fill:#c0392b,color:#fff
```text
┌──────────────────────────────────── Jira — Escalation Procedures ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                     Jira Escalation Tiers                                     │   │
│   │                Tier 1: Ops — restart, reindex, check logs, restore from backup                │   │
│   │           Tier 2: Senior engineer — JVM tuning, DB query analysis, plugin isolation           │   │
│   │            Tier 3: Atlassian Support — ticket with support-zip; thread + heap dumps           │   │
│   │              Tier 4: Atlassian escalation — P1 production down; 24x7 critical SLA             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Escalate: T1 > 30 min no resolution; T2 > 2 hr; T3 > 4 hr production down                          │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Escalation Criteria              │  │             Artifacts to Gather             │   │
│   │             Service down >30 min             │  │              support-zip bundle             │   │
│   │             Data loss suspected              │  │               Thread dumps x3               │   │
│   │              Security incident               │  │               Heap dump (OOM)               │   │
│   │              Repeated OOM crash              │  │              catalina.out tail              │   │
│   │             Corruption suspected             │  │              DB slow query log              │   │
│   │            Plugin breaks upgrade             │  │             Version + patch info            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Jira VMs · PostgreSQL DB · monitoring/alerting · Atlassian Support portal                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  support-zip    = Admin > System > Troubleshooting > Create Support Zip                               │
│  Thread dump    = 3 dumps 10 seconds apart; detect deadlocks in worker threads                        │
│  Heap dump      = full JVM memory; jmap -dump:format=b,file=jira.hprof <pid>                          │
│  P1 incident    = production down; page on-call; escalate within 30 minutes                           │
│  Atlassian Support = support.atlassian.com; valid license required                                    │
│  Safe mode      = start without plugins; -Djira.startup.options=safe-mode                             │
│  Plugin isolate = disable plugins one by one until issue resolves                                     │
│  DB slow query  = set log_min_duration_statement=1000 in postgresql.conf                              │
│  Corruption     = DB row count vs index count mismatch; reindex if different                          │
│  Data loss      = check jiraissue table; deleted issues have DELETED status                           │
│  SLA            = P1 1hr response, P2 4hr, P3/P4 next business day                                    │
│  Critical escalation = request via Atlassian account team for P1 outages                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### Resolution Notification

```text
[JIRA RESOLVED] — HH:MM UTC

ISSUE: [Brief description]
RESOLVED AT: HH:MM UTC (Duration: Xh Ym)
ROOT CAUSE: [One sentence]
FIX APPLIED: [What was done]
PREVENTIVE ACTION: [What will be done to prevent recurrence]

Post-mortem scheduled: [Date/time or "within 5 business days"]
```

---

## Post-Incident Review (PIR) Checklist

Complete within 5 business days for all P1 and P2 incidents.

- [ ] Incident timeline documented (minute by minute for P1)
- [ ] Root cause identified and confirmed
- [ ] Contributing factors listed
- [ ] Immediate fix documented
- [ ] Preventive actions agreed with owners and due dates set
- [ ] Monitoring gaps identified and addressed
- [ ] Documentation updated (runbooks, KB articles)
- [ ] SLA breach assessed — did response and resolution meet targets?
- [ ] PIR document published to Confluence incident space
- [ ] PIR shared with stakeholders
