---
tags:
  - jira
  - learning-path
---
# Jira — Learning Path

<div class="kb-summary">
Recommended reading order for Atlassian Jira. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌──────────────────────────────────────── Jira — Learning Path ─────────────────────────────────────────┐
│                                                                                                       │
│    5 stages in order: Architecture → Deploy → Operations → Security → Troubleshoot                    │
│                                                                                                       │
│   ┌────────────────┐  ┌────────────────┐  ┌─────────────────┐  ┌────────────────┐  ┌────────────────┐ │
│   │  Architecture  │  │     Deploy     │  │    Operations   │  │    Security    │  │  Troubleshoot  │ │
│   │                │  │                │  │                 │  │                │  │                │ │
│   │  How It Works  │  │ Initial Setup  │  │  Health Checks  │  │ Access Control │  │ Common Issues  │ │
│   │Design Standards│  │Install/Upgrade │  │  CLI Reference  │  │ Authentication │  │  Diagnostics   │ │
│   │  Integrations  │  │                │  │    Procedures   │  │   Encryption   │  │   Escalation   │ │
│   │                │  │                │  │ Backup & Restore│  │   Hardening    │  │                │ │
│   │                │  │                │  │     Scripts     │  │                │  │                │ │
│   └────────────────┘  └────────────────┘  └─────────────────┘  └────────────────┘  └────────────────┘ │
│                                                                                                       │
│    Stage 1 (Architecture) builds understanding. Stage 3 (Operations) is daily work. Troubleshoot last.│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph LR
  S1[Architecture] --> S2[Deploy] --> S3[Operations] --> S4[Security] --> S5[Troubleshoot]
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
| Stage | Focus | Time investment |
|-------|-------|----------------|
| 1 — Architecture | Project types, workflow, scheme model | 3–4 h |
| 2 — Deployment | Installation, DB, upgrade, app compat | 3–4 h |
| 3 — Operations | Admin tasks, REST API, backup cadence | ongoing |
| 4 — Security | Permission schemes, SSO, audit log | 2–3 h |
| 5 — Troubleshooting | Logs, index, workflow conditions, lockouts | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand Jira's project-issue-workflow model and how screens, field configurations, notification schemes, and permission schemes compose into a functioning project.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — project types (Scrum, Kanban, next-gen/team-managed vs company-managed), issue type hierarchy (Epic → Story → Task → Sub-task), workflow states and transitions, and the scheme inheritance model (shared schemes vs project-specific)
- [Design Standards](../architecture/design-standards/) — project template selection criteria, issue type hierarchy design, field configuration standards (required fields, field contexts), and JQL naming conventions for saved filters and dashboards
- [Integrations](../architecture/integrations/) — Confluence page and sprint linking, Bitbucket/GitHub development panel for commit and PR association, Jira Service Management integration, and the REST API for automation and external reporting

**Key concepts before moving on**:

- Company-managed projects share schemes; a change to a shared workflow affects every project using it — test workflow changes on a cloned scheme first
- JQL (`project = X AND status = "In Progress" ORDER BY updated DESC`) is the query language for all searches, filters, boards, and dashboards
- Notifications are driven by notification schemes tied to projects; a change to a shared scheme affects all projects sharing it
- Issue link types are global; adding a new link type is visible to all projects on the instance

**Why first**: Jira's shared scheme model means changes to workflows and fields can cascade across multiple projects. Understanding this before making changes prevents unintended instance-wide impacts.

---

## Stage 2 — Deployment

**Goal**: Install or migrate a Jira Data Center instance, or onboard teams to Jira Cloud, with correct scheme configuration from the start.

**Read**:

- [Deploy](../deploy/) — Data Center installation (application + PostgreSQL/Oracle + shared home for cluster), Jira Cloud site provisioning, and initial global configuration (base URL, SMTP, application links to Confluence)
- [Install & Upgrade](../operations/install-upgrade/) — upgrade wizard pre-check (app compatibility via `upm`), step-by-step upgrade procedure for Data Center, database migration considerations, and zero-downtime upgrade for cluster deployments

**Deployment principles**:

- Create a baseline project template scheme set (workflow, issue types, screens, permissions, notifications) before provisioning any team projects — retrofitting is painful
- Configure application links to Confluence before teams start creating issues to enable two-way page linking from day one
- Always run a full backup before upgrading — Jira Data Center upgrades cannot be rolled back without a DB restore

---

## Stage 3 — Operations

**Goal**: Administer Jira projects and users, maintain performance, and support teams day to day.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; application log errors, index health (`Indexing` in admin), DB connection pool saturation, license seat usage vs remaining, and mail queue depth
- [CLI Reference](../operations/cli-reference/) — REST API patterns for issue creation, bulk status transitions, JQL searches, user account management, project listing, and issue export via `curl` or Python `requests`
- [Procedures](../operations/procedures/) — creating a new company-managed project from a template, modifying a workflow (clone → edit → swap), bulk issue move between projects, and user deprovisioning workflow
- [Backup & Restore](../operations/backup-restore/) — XML backup configuration (schedule, exclusion of attachments for large instances), database dump schedule, attachment backup to object storage, and restore testing on a staging Jira instance
- [Scripts](../operations/scripts/) — JQL-based compliance reports, automation rule export and import, bulk field update via REST API, and stale issue identification scripts

**Daily rhythm**: Application log → index health → DB pool → mail queue → open IT support tickets for admin requests.

---

## Stage 4 — Security

**Goal**: Control who can view, create, and transition issues across projects, and audit all administrative changes.

**Read**:

- [Access Control](../security/access-control/) — permission schemes (Browse Projects, Create Issues, Transition Issues, Assign Issues, Admin), project role assignments (Administrators, Developers, Users), and global permissions (Jira Administrators, Create Shared Objects)
- [Authentication](../security/authentication/) — Atlassian Access SAML 2.0 / OIDC SSO configuration, 2FA enforcement for all users, API token management and expiry policy for service accounts, and session timeout configuration
- [Encryption](../security/encryption/) — TLS at the reverse proxy (port 443 → Tomcat port 8080), database encryption at rest, and attachment storage encryption for Data Center shared home or S3 backend
- [Hardening](../security/hardening/) — disabling public sign-up, restricting project creation to Jira Administrators, audit log retention and export to SIEM, and outbound webhook URL allowlisting to prevent SSRF

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose Jira performance issues, broken workflow transitions, and indexing problems without data loss or service interruption.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — transition button missing (permission scheme or workflow condition blocking), slow board loading (complex JQL or large backlog), search returning wrong results (index out of sync), mail notifications not sent (SMTP auth or mail queue stuck), and bulk move failures
- [Diagnostics](../troubleshooting/diagnostics/) — `atlassian-jira.log` and `atlassian-jira-outgoing-mail.log` analysis, Lucene index rebuild via Admin → Indexing, thread dump analysis with `jstack` for hang diagnosis, workflow condition and validator inspection, and `WorkflowScheme` audit trail
- [Escalation](../troubleshooting/escalation/) — Atlassian Support ticket creation with support ZIP, Data Center thread dump and GC log collection, plugin conflict isolation, and P1 critical incident escalation via Atlassian Support Portal

**Why last**: Troubleshooting makes most sense once you understand how workflows, schemes, and permissions interact and what healthy Jira logs and performance metrics look like.
