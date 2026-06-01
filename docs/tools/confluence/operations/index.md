# Confluence — Operations



<div class="kb-summary">
Confluence — Operations reference.
</div>

```text
┌────────────────────────────────── Confluence — Operations Overview ───────────────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Daily Checks        │  │         Weekly Tasks        │  │        Monthly Tasks        │   │
│   │        Service status       │  │         Space health        │  │        License audit        │   │
│   │        Backup verify        │  │          User audit         │  │        Plugin updates       │   │
│   │          Disk usage         │  │          Check logs         │  │      Performance review     │   │
│   │         Alert triage        │  │       Reindex if slow       │  │       Security review       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Confluence server/DC VMs · PostgreSQL or Oracle DB · file system for attachments                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Service status = Confluence app server running; check via systemctl or process monitor               │
│  Backup verify = Confirm backup job completed; test restore quarterly                                 │
│  Disk usage = Monitor home directory and attachments; alert at 80%                                    │
│  Reindex = Rebuilding Confluence search index; needed after bulk import or corruption                 │
│  Plugin = Confluence app/add-on; update via UPM (Universal Plugin Manager)                            │
│  UPM = Universal Plugin Manager; Confluence built-in app marketplace management                       │
│  Space = Confluence top-level container for pages; each team typically has a space                    │
│  License audit = Verifying active user count against licensed seats                                   │
│  PostgreSQL = Recommended database for Confluence Server/DC deployments                               │
│  Home directory = CONFLUENCE_HOME; stores attachments, backups, and indexes                           │
│  Performance review = Monthly check of heap usage, GC pauses, and page load times                     │
│  Security review = Monthly check of admin accounts, anonymous access, and HTTPS config                │
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
  <span>Page management, cleanup, and search procedures.</span>
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
