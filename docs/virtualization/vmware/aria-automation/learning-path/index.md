---
tags:
  - aria-automation
  - learning-path
  - vmware
---
# Aria Automation — Learning Path

<div class="kb-summary">
Recommended reading order for Aria Automation (vRA). Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Aria Automation 8.x*
</div>

```text
┌─────────────────────────────────── Aria Automation — Learning Path ───────────────────────────────────┐
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
## Stage 1 — Architecture
**Goal**: Understand how Aria Automation maps cloud accounts, projects, and blueprints into a self-service catalog.
**Read in this order**:
- [How It Works](../architecture/how-it-works/) — service architecture (Automation Assembler, Service Broker, ABX), cloud account abstraction, and the project-scoped resource model
- [Design Standards](../architecture/design-standards/) — cloud account naming, project structure, zone and flavor mapping, and blueprint versioning strategy
- [Integrations](../architecture/integrations/) — vCenter, NSX, vSAN, Aria Suite Lifecycle, external Git for blueprint source control, and ITSM integration via ABX

**Why first**: Aria Automation's catalog experience is built on top of cloud accounts and projects; understanding the layering prevents schema confusion when writing blueprints that span multiple endpoints.

---

## Stage 2 — Deployment
**Goal**: Deploy a production Aria Automation environment integrated with vCenter and NSX, with projects and catalog items published.
**Read**:
- [Deploy](../deploy/) — LCM-based deployment, prerequisite checks, cloud account registration sequence, and initial project setup
- [Install & Upgrade](../operations/install-upgrade/) — LCM-driven upgrade workflow, pre-upgrade snapshot policy, and post-upgrade catalog validation

**Why second**: Cloud account credentials and network profiles set during deployment define what blueprint authors can request; getting the scope right avoids rework in every downstream blueprint.

---

## Stage 3 — Operations
**Goal**: Maintain catalog health, manage blueprint lifecycle, and operate day-2 actions reliably.
**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift
- [CLI Reference](../operations/cli-reference/) — vracli commands for service status, cloud account token refresh, and ABX action log retrieval
- [Procedures](../operations/procedures/) — blueprint authoring workflow, catalog item publishing, approval policy configuration, day-2 action development, and ABX action debugging
- [Backup & Restore](../operations/backup-restore/) — LCM-managed backup schedule, content snapshot export, and restore sequence for database corruption
- [Scripts](../operations/scripts/) — REST API scripts for catalog item export, deployment bulk-delete, and resource tagging automation

**Why third**: Blueprint authoring and day-2 operations require cloud accounts, projects, and flavor mappings to already be stable and tested.

---

## Stage 4 — Security
**Goal**: Enforce project-scoped access, protect cloud account credentials, and apply least-privilege to catalog consumers.
**Read**:
- [Access Control](../security/access-control/) — project membership roles (Administrator, Member, Viewer), catalog entitlements, and approval policy chains
- [Authentication](../security/authentication/) — vIDM/Workspace ONE integration, LDAP group-to-project mapping, and API token lifecycle management
- [Encryption](../security/encryption/) — cloud account credential storage, ABX secret management, and TLS certificate requirements across services
- [Hardening](../security/hardening/) — restricting catalog visibility by entitlement, disabling unused cloud account types, and auditing blueprint deployment history

**Why fourth**: Approval policies and entitlements sit on top of projects and catalog items; they can only be meaningfully configured once the catalog structure is known.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose failed deployments, broken ABX actions, and cloud account sync errors quickly without impacting running workloads.
**Read**:
- [Common Issues](../troubleshooting/common-issues/) — deployment failures mid-blueprint, cloud account token expiry, ABX action timeout, and approval policy loop issues
- [Diagnostics](../troubleshooting/diagnostics/) — deployment request event log, ABX action run logs, and cloud account data collection status
- [Escalation](../troubleshooting/escalation/) — GSS data requirements, log bundle collection from LCM, and SR classification for blueprint engine failures

**Why last**: Troubleshooting makes most sense once you know the normal operating state.

---

## See also

- [Aria Automation — Deploy](../deploy/)
- [Aria Automation — Procedures](../operations/procedures/)
- [Aria Automation — Common Issues](../troubleshooting/common-issues/)
