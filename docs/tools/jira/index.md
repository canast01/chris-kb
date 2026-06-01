# Jira

<div class="kb-summary">
Jira knowledge base covering Data Center cluster architecture, issue management, workflow configuration, security, and troubleshooting.
</div>

```
┌────────────────────────────────────── Jira — Platform Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Atlassian Jira — Issue and Project Tracking                          │   │
│   │         Projects: Software (Scrum/Kanban), Business, Service Management project types         │   │
│   │          App tier: Tomcat on port 8080; behind reverse proxy on 443; JVM heap 4-8 GB          │   │
│   │           Data tier: PostgreSQL or Oracle DB; Lucene search index on shared NFS home          │   │
│   │           Integrations: Confluence app link, Bitbucket, CI/CD webhooks, REST API v3           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Jira is the central issue registry linking development, operations, and support                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │       Tomcat app tier       │  │       Install/Upgrade       │  │        LDAP/SAML auth       │   │
│   │        PostgreSQL DB        │  │        Backup/Restore       │  │      Permission schemes     │   │
│   │        Lucene search        │  │        Health checks        │  │        TLS encryption       │   │
│   │         REST API v3         │  │           Scripts           │  │       Hardening guide       │   │
│   │         Integrations        │  │        CLI reference        │  │        Access control       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere VMs for app nodes · PostgreSQL DB VM · NFS shared home · load balancer                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Project      = Jira container for issues; has type (Software/Business/SM), key, and scheme           │
│  Issue        = unit of work: Bug, Story, Task, Epic, Sub-task; tracked across workflow               │
│  JQL          = Jira Query Language; SQL-like filter syntax (project = TEAM AND status = Open)        │
│  Workflow     = state machine for issues; Statuses and Transitions defined per project                │
│  Screen       = field layout shown on create/edit/view; configured per issue type                     │
│  Permission scheme = project-level ACL; maps project roles to operations (create, edit, etc.)         │
│  Notification scheme = email rules for issue events; per project configuration                        │
│  Component    = sub-category within a project; assigned to issues for grouping                        │
│  Sprint       = Scrum time-box; issues committed to a 1-4 week iteration                              │
│  Kanban board = continuous flow board; WIP limits; no fixed sprint iterations                         │
│  Epic         = large user story grouping multiple stories; tracked across sprints                    │
│  Velocity     = average story points completed per sprint; sprint planning metric                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌────────────────────────────────────── Jira — Platform Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                          Atlassian Jira — Issue and Project Tracking                          │   │
│   │         Projects: Software (Scrum/Kanban), Business, Service Management project types         │   │
│   │          App tier: Tomcat on port 8080; behind reverse proxy on 443; JVM heap 4-8 GB          │   │
│   │           Data tier: PostgreSQL or Oracle DB; Lucene search index on shared NFS home          │   │
│   │           Integrations: Confluence app link, Bitbucket, CI/CD webhooks, REST API v3           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Jira is the central issue registry linking development, operations, and support                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │           Security          │   │
│   │       Tomcat app tier       │  │       Install/Upgrade       │  │        LDAP/SAML auth       │   │
│   │        PostgreSQL DB        │  │        Backup/Restore       │  │      Permission schemes     │   │
│   │        Lucene search        │  │        Health checks        │  │        TLS encryption       │   │
│   │         REST API v3         │  │           Scripts           │  │       Hardening guide       │   │
│   │         Integrations        │  │        CLI reference        │  │        Access control       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere VMs for app nodes · PostgreSQL DB VM · NFS shared home · load balancer                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Project      = Jira container for issues; has type (Software/Business/SM), key, and scheme           │
│  Issue        = unit of work: Bug, Story, Task, Epic, Sub-task; tracked across workflow               │
│  JQL          = Jira Query Language; SQL-like filter syntax (project = TEAM AND status = Open)        │
│  Workflow     = state machine for issues; Statuses and Transitions defined per project                │
│  Screen       = field layout shown on create/edit/view; configured per issue type                     │
│  Permission scheme = project-level ACL; maps project roles to operations (create, edit, etc.)         │
│  Notification scheme = email rules for issue events; per project configuration                        │
│  Component    = sub-category within a project; assigned to issues for grouping                        │
│  Sprint       = Scrum time-box; issues committed to a 1-4 week iteration                              │
│  Kanban board = continuous flow board; WIP limits; no fixed sprint iterations                         │
│  Epic         = large user story grouping multiple stories; tracked across sprints                    │
│  Velocity     = average story points completed per sprint; sprint planning metric                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Issue management, reporting, and workflow procedures.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, permissions, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
