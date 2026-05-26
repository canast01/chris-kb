# Jira — Troubleshooting


```
┌─────────────────────────────────── Jira — Troubleshooting Overview ───────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                 Jira Troubleshooting Framework                                │   │
│   │            Triage by symptom: slow, down, search broken, workflow stuck, auth fail            │   │
│   │            First check: GET /status, heap usage, catalina.out, and DB connectivity            │   │
│   │           Escalate to Atlassian Support with support-zip; attach thread + heap dumps          │   │
│   │             Known issues: search jira.atlassian.com before opening support ticket             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Systematic triage reduces mean time to resolution for common Jira issues                           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Diagnostics         │  │        Common Issues        │  │          Escalation         │   │
│   │      GET /status check      │  │       OOM / heap full       │  │      Atlassian Support      │   │
│   │         Thread dump         │  │       Slow page loads       │  │      support-zip bundle     │   │
│   │       Heap dump (OOM)       │  │        Search broken        │  │        Thread dump x3       │   │
│   │      DB query analysis      │  │        Workflow stuck       │  │      jira.atlassian.com     │   │
│   │         Log analysis        │  │        Auth failures        │  │        Hotfix / patch       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Jira VMs · PostgreSQL · NFS · monitoring (Prometheus/Zabbix) · log aggregator                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  support-zip    = Admin > System > Troubleshooting > Create Support Zip                               │
│  Thread dump    = kill -3 <pid>; take 3 at 10-second intervals for deadlock analysis                  │
│  Heap dump      = jmap -dump:format=b,file=jira.hprof <pid>; analyse with MAT                         │
│  Workflow stuck = issue cannot transition; check conditions/validators in workflow                    │
│  OOM            = OutOfMemoryError; increase -Xmx in setenv.sh                                        │
│  Reindex        = Admin > System > Indexing > Full Re-Index; fixes stale search                       │
│  catalina.out   = primary startup and exception log; check first on any issue                         │
│  pg_stat_activity = PostgreSQL active queries; find long-running blocking queries                     │
│  MAT            = Eclipse Memory Analyser Tool; heap dump analysis                                    │
│  Safe mode      = start Jira without plugins; diagnose plugin-related issues                          │
│  jira.atlassian.com = Atlassian public bug tracker for known Jira issues                              │
│  Hotfix         = patch JAR from Atlassian for critical CVEs between releases                         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="common-issues/">
  <strong>Common Issues</strong>
  <span>Frequently encountered problems and fixes.</span>
</a>

<a class="kb-card" href="diagnostics/">
  <strong>Diagnostics</strong>
  <span>Diagnostic commands and log analysis.</span>
</a>

<a class="kb-card" href="escalation/">
  <strong>Escalation</strong>
  <span>Escalation paths and vendor support procedures.</span>
</a>

</div>
