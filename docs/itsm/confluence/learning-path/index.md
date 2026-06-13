# Confluence — Learning Path

<div class="kb-summary">
Recommended reading order for Atlassian Confluence. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌───────────────────────────────────── Confluence — Learning Path ──────────────────────────────────────┐
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
| 1 — Architecture | Space-page hierarchy, permissions cascade, Data Center vs Cloud | 3–4 h |
| 2 — Deployment | Installation, database, reverse proxy, upgrades | 3–4 h |
| 3 — Operations | Performance, index health, content lifecycle | ongoing |
| 4 — Security | Space permissions, SSO, audit log | 2–3 h |
| 5 — Troubleshooting | Logs, index rebuild, macro failures, hang diagnosis | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand Confluence's space-page-permission hierarchy and how it differs between Data Center (self-managed) and Cloud deployments.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — space hierarchy, page tree model, version history, the macro rendering pipeline (server-side vs connect macros), and the key differences between Confluence Data Center and Confluence Cloud
- [Design Standards](../architecture/design-standards/) — space design patterns (team space, project space, personal space), page template strategy for consistent documentation, label taxonomy for cross-space findability, and naming conventions
- [Integrations](../architecture/integrations/) — Jira issue and sprint macros for live data embedding, Atlassian Access for SAML/OIDC SSO, REST API for content automation, and the third-party app marketplace (Scroll Viewport, Gliffy)

**Key concepts before moving on**:

- Space permissions are the outer boundary; page restrictions are an inner layer — both must allow access for a user to view a page
- Anonymous access is disabled per-space; if any space allows anonymous access, sensitive content in that space is publicly visible
- In Data Center, the Lucene search index is separate from the database — a corrupted index causes search failures even when the DB is healthy
- Confluence Cloud and Data Center have different app ecosystems; not all marketplace apps work on both deployment types

**Why first**: Confluence permissions cascade from space to page. Understanding the hierarchy before creating spaces prevents accidental public exposure and orphaned content that cannot be found or governed.

---

## Stage 2 — Deployment

**Goal**: Stand up or migrate a Confluence instance with correct database, shared home, and reverse proxy configuration.

**Read**:

- [Deploy](../deploy/) — Data Center installation (Tomcat, database driver, `confluence.cfg.xml`), shared home directory for cluster nodes, reverse proxy configuration (nginx with `proxy_pass` and correct headers), and Confluence Cloud onboarding and space migration
- [Install & Upgrade](../operations/install-upgrade/) — upgrade wizard pre-check (plugin compatibility, DB version), step-by-step upgrade procedure, rolling upgrade for Data Center cluster nodes, and post-upgrade validation checklist

**Deployment principles**:

- Set the correct `X-Forwarded-For` and `X-Forwarded-Proto` headers at the reverse proxy — Confluence uses these for self-referential URLs in notifications and links
- Run the upgrade on a restored DB copy first to validate plugin compatibility before touching production
- Configure a shared home on NFS or Azure Files for Data Center so all cluster nodes access the same attachments

---

## Stage 3 — Operations

**Goal**: Keep Confluence healthy — monitoring performance, managing space growth, and maintaining content quality on every shift.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; application log for WARN/ERROR, index health via Admin → Content Indexing, DB connection pool (Tomcat JDBC), cluster node status, and attachment storage disk usage
- [CLI Reference](../operations/cli-reference/) — REST API v1 and v2 calls for content export, space listing, user search, page creation, and bulk page moves using `curl` or Python `requests`
- [Procedures](../operations/procedures/) — space archiving, bulk page move between spaces, content export to PDF or Word, user deprovisioning, and space permission audit
- [Backup & Restore](../operations/backup-restore/) — XML site backup schedule and limitations (large instances use DB dump + shared home backup), attachment backup, and restore testing on a staging instance
- [Scripts](../operations/scripts/) — REST API automation for stale content identification (pages not updated in 12 months), space permission reporting, label compliance auditing, and user activity reporting

**Daily rhythm**: Application log check → index health → DB connection pool → attachment disk usage → recent space activity.

---

## Stage 4 — Security

**Goal**: Enforce appropriate access boundaries, prevent sensitive content from being publicly visible, and audit all changes.

**Read**:

- [Access Control](../security/access-control/) — space permissions (view, add page, add blog, add comment, add attachment, delete, admin), page restrictions (view and edit), group-based permission assignment, and the permissions audit tool
- [Authentication](../security/authentication/) — Atlassian Access SAML 2.0 / OIDC SSO configuration, session timeout settings, 2FA enforcement through Atlassian Access, and API token management for REST API automation
- [Encryption](../security/encryption/) — TLS termination at the reverse proxy (never expose Tomcat port 8090 directly), database encryption at rest, and attachment storage encryption for Data Center shared home
- [Hardening](../security/hardening/) — disabling public signup (`Confluence Administration → Security Configuration`), restricting macro execution to trusted user groups, audit log retention configuration, and outbound link domain allowlisting

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose Confluence performance issues, broken macros, and search index problems without data loss.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — slow page loads (macro rendering timeout, DB query), broken Jira macros (application link token expired), space permissions not cascading to child pages, search returning stale results (index out of sync), and attachment upload failure (disk quota or shared home permissions)
- [Diagnostics](../troubleshooting/diagnostics/) — `atlassian-confluence.log` analysis, full Lucene index rebuild via Admin (`Re-index`), thread dump generation via `kill -3` or JMX for hang diagnosis, DB slow query log correlation, and `atlas-troubleshoot` support tool
- [Escalation](../troubleshooting/escalation/) — Atlassian Support ticket creation with support ZIP (`atlas-troubleshoot` output), Data Center cluster diagnostic collection, plugin conflict isolation by disabling plugins, and P1 critical incident escalation via Atlassian Support Portal

**Why last**: Troubleshooting makes most sense once you understand the space-page model, macro rendering pipeline, and what healthy Confluence logs and performance metrics look like.
