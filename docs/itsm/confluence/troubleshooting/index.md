# Confluence — Troubleshooting



<div class="kb-summary">
Diagnosing Confluence performance issues, indexing failures, login problems, macro errors, and sync failures.
</div>

```text
┌──────────────────────────────── Confluence — Troubleshooting Overview ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                              Confluence Troubleshooting Framework                             │   │
│   │           Triage by symptom: slow, down, data issue, auth failure, or search broken           │   │
│   │            First check: GET /status, heap usage, catalina.out, and DB connectivity            │   │
│   │        Escalate to Atlassian Support with support-zip; include thread dump + heap dump        │   │
│   │         Known issues: check Atlassian JIRA (bugs.atlassian.com) before opening ticket         │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Structured triage prevents escalating issues that can be resolved at Tier 1                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Diagnostics         │  │        Common Issues        │  │          Escalation         │   │
│   │      GET /status check      │  │       OOM / heap full       │  │      Atlassian Support      │   │
│   │         Thread dump         │  │       Slow page loads       │  │      support-zip bundle     │   │
│   │       Heap dump (OOM)       │  │        Search broken        │  │       Thread dump req       │   │
│   │      DB query analysis      │  │        Auth failures        │  │      bugs.atlassian.com     │   │
│   │         Log analysis        │  │        NFS mount lost       │  │        Hotfix / patch       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Confluence VMs · PostgreSQL · NFS · monitoring system (Prometheus/Zabbix) · log aggregator           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  GET /status    = HTTP health endpoint; returns JSON with RUNNING or error state                      │
│  Thread dump    = JVM stack snapshot; generated with kill -3 <pid> or via Admin > Logging             │
│  Heap dump      = JVM memory snapshot; triggered by OOM or via jmap; analysed with MAT                │
│  support-zip    = Admin > Troubleshooting > Create Support Zip; includes logs and config              │
│  OOM            = OutOfMemoryError; heap exhausted; Confluence crash; increase -Xmx                   │
│  Reindex        = rebuild Lucene index from DB; fixes stale or missing search results                 │
│  catalina.out   = Tomcat stdout log; CONFLUENCE_INSTALL/logs/catalina.out                             │
│  NFS mount lost = CONFLUENCE_HOME unmounted; attachments return 404; remount NFS                      │
│  MAT            = Eclipse Memory Analyser Tool; analyses heap dumps for leak suspects                 │
│  DB query       = slow queries visible in pg_stat_activity; check with pg_stat_statements             │
│  bugs.atlassian.com = Atlassian public issue tracker; check for known bugs first                      │
│  Hotfix         = Atlassian-provided patch JAR for critical CVEs between releases                     │
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
