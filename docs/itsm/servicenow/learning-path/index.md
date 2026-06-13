---
tags:
  - learning-path
  - servicenow
---
# ServiceNow — Learning Path

<div class="kb-summary">
Recommended reading order for ServiceNow ITSM. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌───────────────────────────────────── ServiceNow — Learning Path ──────────────────────────────────────┐
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
| 1 — Architecture | Table model, CMDB, update set discipline | 4–5 h |
| 2 — Deployment | Update set promotion, Discovery, catalog | 2–3 h |
| 3 — Operations | ITSM process health, MID Server, SLAs | ongoing |
| 4 — Security | ACLs, SSO, OAuth, audit log | 2–3 h |
| 5 — Troubleshooting | Flow history, sys_log, MID Server logs | as needed |

---

## Stage 1 — Architecture

**Goal**: Understand ServiceNow's table-based data model, the CMDB as a single source of truth, and how ITSM modules relate to each other through the Now Platform.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — multi-tenant SaaS instance architecture, table inheritance model (`Task` → `Incident`, `Change_Request`, `Problem`), CMDB CI class hierarchy and relationship types, and the Now Platform application framework (Business Rules, Client Scripts, UI Policies, Script Includes)
- [Design Standards](../architecture/design-standards/) — CMDB class hierarchy design for your environment, update set discipline (always develop in a named update set, never in Default), and naming conventions for catalog items, flows, and script includes
- [Integrations](../architecture/integrations/) — IntegrationHub spokes (AWS, Azure, Jira, Slack), MID Server for on-premises Discovery and integrations, outbound REST/SOAP messages from ServiceNow, and inbound REST (Table API, Scripted REST) for external systems

**Key concepts before moving on**:

- Everything in ServiceNow is a table record — incidents, changes, users, CI items, and even application metadata are rows in tables
- Update sets capture configuration changes (not data) and are the transport mechanism for promoting changes between dev → test → prod instances
- The CMDB is only as reliable as Discovery and its data quality — a CMDB with stale or wrong CIs will actively mislead incident and change processes
- Business Rules fire on server-side events; Client Scripts fire in the browser — mixing them up causes bugs that are hard to reproduce

**Why first**: ServiceNow is a platform, not just a ticket tool. Understanding the table model and CMDB relationships before customising prevents data model debt that is expensive to unwind later.

---

## Stage 2 — Deployment

**Goal**: Promote changes through dev → test → prod using update sets safely, and configure Discovery for automatic CMDB population.

**Read**:

- [Deploy](../deploy/) — update set creation (scope, description), remote update set retrieval, preview (conflict resolution), and commit on the target instance; MID Server installation on Windows/Linux and probe/sensor configuration; and Service Catalog item publication flow
- [Install & Upgrade](../operations/install-upgrade/) — ServiceNow release upgrade procedure (Family upgrade), pre-upgrade skipped record review, plugin activation, post-upgrade validation checklist, and instance clone for upgrade testing

**Deployment principles**:

- Never make configuration changes directly on the production instance — always develop in dev, promote via update set through test, then to prod
- Preview update sets in the target instance before committing — conflicts must be resolved manually if the same record was modified in both instances
- Run Discovery against a lab environment first to tune CI class mapping and identifier rules before enabling it in production

---

## Stage 3 — Operations

**Goal**: Keep ITSM processes running smoothly — managing incidents, changes, and the CMDB on a daily basis with visibility into platform health.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; instance performance metrics (Admin → Stats), MID Server online status, Discovery schedule last run and CI count, SLA breach risk (near-breach incidents), integration health (IntegrationHub activity), and open change windows
- [CLI Reference](../operations/cli-reference/) — Table API REST calls (`GET /api/now/table/incident`), `sys_id` lookup patterns, bulk import via Transform Maps and Data Sources, and scripted background jobs via `Scripts - Background`
- [Procedures](../operations/procedures/) — incident creation and priority escalation, change request approval routing, CMDB CI update via Discovery or manual correction, Flow Designer flow activation and testing, and scheduled report configuration
- [Backup & Restore](../operations/backup-restore/) — ServiceNow managed clone procedure (prod → dev/test), update set XML export for configuration backup, and data export via scheduled reports to SFTP or S3
- [Scripts](../operations/scripts/) — Business Rule templates, Script Include reusable utility classes, Scheduled Script Execution for maintenance tasks, and REST API automation wrappers for external integrations

**Daily rhythm**: Instance health → MID Server status → SLA near-breach list → open change approvals → Discovery schedule outcomes.

---

## Stage 4 — Security

**Goal**: Enforce role-based access to ITSM data, protect integration credentials, and audit all platform configuration changes.

**Read**:

- [Access Control](../security/access-control/) — ACL (Access Control List) rules for table/field/record-level access, role assignment (`sys_user_has_role`), user criteria for Service Portal widget visibility, and data classification label enforcement
- [Authentication](../security/authentication/) — SAML 2.0 / OIDC SSO configuration (Multi-Provider SSO plugin), MFA enforcement, OAuth 2.0 provider configuration for inbound integrations, and service account management with API key rotation
- [Encryption](../security/encryption/) — HTTPS-only instance access (TLS 1.2+), credential storage in Connection & Credential Aliases (not hardcoded in scripts), and field-level encryption for PII attributes using the Encrypted Fields plugin
- [Hardening](../security/hardening/) — High Security Plugin settings (session timeout, failed login lockout, password policy), audit log (`sys_audit`) retention and SIEM export, IP allowlisting for admin UI access, and Security Jump Start assessment findings remediation

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose broken flows, failed integrations, Discovery issues, and performance degradation without impacting live ITSM processes.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Flow not triggering (trigger condition or active flag), MID Server offline (service stopped or certificate expired), Discovery creating duplicate CIs (identifier rules), SLA not pausing on Hold state (SLA condition error), and email inbound not creating incidents (inbound action rules)
- [Diagnostics](../troubleshooting/diagnostics/) — Flow Designer execution history (execution detail per step), MID Server log (`agent/logs/agent0.log`), `sys_log` table for Business Rule errors, REST API tester (`/api/now/table/` in browser), instance performance analytics for slow queries, and `Script Debugger` for server-side code
- [Escalation](../troubleshooting/escalation/) — ServiceNow Support case on the Hi Portal (severity 1–4), Instance Clone for issue reproduction without impacting production, HAR file capture for browser-side issues, and CSM (Customer Success Manager) escalation for business-critical platform failures

**Why last**: Troubleshooting makes most sense once you understand the platform table model, CMDB relationships, and how Flows and Business Rules fire under normal conditions.
