# Tools

<div class="kb-summary">
Operational tooling reference covering version control, project tracking, documentation, and ITSM — Git, Jira, Confluence, and ServiceNow.
</div>

```
┌─────────────────────────────────────── Tools Platform Overview ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   Enterprise Tools Platform                                   │   │
│   │               Collaboration, version control, issue tracking, and ITSM services               │   │
│   │     Atlassian DC stack: Confluence + Jira on PostgreSQL, shared NFS home, Tomcat app tier     │   │
│   │        Git: distributed VCS hosted on GitHub/GitLab/Bitbucket with SSH and HTTPS access       │   │
│   │       ServiceNow: SaaS ITSM — Incident, Change, CMDB, ITOM with MID Server on-prem link       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Four tools cover the full DevOps lifecycle from code to production to incident                     │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Confluence                  │  │                     Git                     │   │
│   │         Team wiki and knowledge base         │  │         Distributed version control         │   │
│   │          Spaces · Pages · Templates          │  │          Branches · Commits · Tags          │   │
│   │        Macros · Page tree · REST API         │  │         Pull requests · Hooks · LFS         │   │
│   │             LDAP / SAML SSO auth             │  │             SSH keys / PAT auth             │   │
│   │          Lucene search · XML backup          │  │         GitHub · GitLab · Bitbucket         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                     Jira                     │  │                  ServiceNow                 │   │
│   │          Issue and project tracking          │  │              SaaS ITSM platform             │   │
│   │             Scrum · Kanban · JQL             │  │           Incident · Change · CMDB          │   │
│   │          Epics · Stories · Sprints           │  │          MID Server: on-prem bridge         │   │
│   │         Workflows · Screens · Fields         │  │          Integration Hub REST flows         │   │
│   │            REST API v3 · Webhooks            │  │            SAML SSO · GlideScript           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Atlassian DC on vSphere VMs · NFS shared home · PostgreSQL DB VMs · ServiceNow MID Server VM         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Confluence   = Atlassian wiki platform; Data Center edition on Tomcat + PostgreSQL/Oracle            │
│  Jira         = Atlassian issue tracker; Scrum/Kanban/SM projects with JQL query language             │
│  Git          = distributed VCS; every clone is a full repo with local commit history                 │
│  ServiceNow   = SaaS ITSM; Incident, Problem, Change, Request, CMDB on Now Platform                   │
│  MID Server   = Management/Instrumentation/Discovery; on-prem Java agent for ServiceNow               │
│  LDAP         = Lightweight Directory Access Protocol; centralised user auth directory                │
│  SAML SSO     = Security Assertion Markup Language; federated single sign-on standard                 │
│  PAT          = Personal Access Token; scoped credential replacing password for Git/API               │
│  JQL          = Jira Query Language; SQL-like syntax for filtering and searching issues               │
│  Lucene       = Apache full-text search engine embedded in Confluence and Jira                        │
│  Tomcat       = Apache Tomcat; Java servlet container hosting Confluence/Jira web apps                │
│  Integration  = ServiceNow Integration Hub; low-code REST/SOAP/scripted integrations                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Main Areas

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="servicenow/">
  <strong>ServiceNow</strong>
  <span>Incidents, changes, requests, CMDB, and work notes.</span>
</a>
<a class="kb-card" href="jira/">
  <strong>Jira</strong>
  <span>Projects, stories, tasks, boards, and reporting.</span>
</a>
<a class="kb-card" href="confluence/">
  <strong>Confluence</strong>
  <span>Spaces, pages, templates, search, and cleanup.</span>
</a>
<a class="kb-card" href="git/">
  <strong>Git</strong>
  <span>Repos, branches, commits, tags, and recovery.</span>
</a>
</div>
