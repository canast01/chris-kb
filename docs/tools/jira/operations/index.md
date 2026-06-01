# Jira — Operations



<div class="kb-summary">
Jira — Operations reference.
</div>

```text
┌───────────────────────────────────── Jira — Operations Overview ──────────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Daily Checks        │  │         Weekly Tasks        │  │        Monthly Tasks        │   │
│   │        Service status       │  │        Backup verify        │  │        License audit        │   │
│   │          Heap usage         │  │          User audit         │  │        Plugin updates       │   │
│   │          Disk usage         │  │         Index health        │  │      Performance review     │   │
│   │         Alert triage        │  │          Check logs         │  │       Security review       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Jira app VMs · PostgreSQL DB VM · NFS shared home · monitoring system                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Service status = Jira running state; check via curl http://localhost:8080/status                     │
│  Heap usage     = JVM memory; check Admin > System Info or JMX; alert >80%                            │
│  Disk usage     = monitor JIRA_HOME volume; alert at 80%; attachments grow fast                       │
│  Index health   = Lucene index consistency; reindex if search returns stale results                   │
│  License audit  = active user count vs licensed seats; Admin > License Details                        │
│  Plugin updates = Admin > Manage Apps; update via UPM; test in staging first                          │
│  User audit     = review inactive users and orphan group memberships weekly                           │
│  Backup verify  = confirm pg_dump completed; check JIRA_HOME/export for recent files                  │
│  Performance review = monthly GC log analysis and slow query identification                           │
│  Security review = permission scheme audit and admin account review monthly                           │
│  UPM            = Universal Plugin Manager; built-in app management in Jira admin                     │
│  Alert triage   = review monitoring alerts for Jira service, DB, and NFS health                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>REST API commands and CLI tooling.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Instance health monitoring and validation.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Stories, tasks, and reporting procedures.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation and upgrade procedures.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup strategies and restore procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and utilities.</span>
</a>

</div>
