# Aria Suite Lifecycle — Learning Path

<div class="kb-summary">
Recommended reading order for Aria Suite Lifecycle (LCM/vRSLCM). Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌──────────────────────────────── Aria Suite Lifecycle — Learning Path ─────────────────────────────────┐
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
**Goal**: Understand how LCM centralises deployment, upgrade, and configuration lifecycle for all Aria suite products.
**Read in this order**:
- [How It Works](../architecture/how-it-works/) — environment and product model, Locker (certificates, passwords, binaries), content lifecycle model, and request pipeline
- [Design Standards](../architecture/design-standards/) — LCM appliance sizing, environment naming conventions, datacenter/vCenter mapping, and Locker credential organisation
- [Integrations](../architecture/integrations/) — vCenter compute integration, NFS/SFTP binary repository, DNS/NTP prerequisites, and product-specific integration hooks (vIDM, vRSLCM API)

**Why first**: LCM is the control plane for all other Aria products; understanding environments and Locker before touching any product deployment prevents credential and certificate mismatches that are painful to unwind.

---

## Stage 2 — Deployment
**Goal**: Deploy LCM and use it to deploy a complete Aria suite environment with certificates and passwords in Locker.
**Read**:
- [Deploy](../deploy/) — LCM OVA deployment, initial wizard, Locker population (CA certificates, service passwords, binaries), and first environment creation
- [Install & Upgrade](../operations/install-upgrade/) — LCM self-upgrade procedure, product upgrade request workflow, pre-upgrade compliance checks, and rollback snapshot strategy

**Why second**: Locker must be populated with certificates and passwords before any product can be deployed; skipping this step forces manual credential re-entry across multiple products.

---

## Stage 3 — Operations
**Goal**: Manage product upgrades, certificates, and compliance checks as routine lifecycle events.
**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift
- [CLI Reference](../operations/cli-reference/) — LCM API and CLI commands for environment status, product health, and Locker certificate expiry queries
- [Procedures](../operations/procedures/) — certificate rotation across products, password rotation via Locker, product patch deployment, and compliance drift remediation
- [Backup & Restore](../operations/backup-restore/) — LCM configuration backup, product backup orchestration, and restore sequence for LCM appliance failure
- [Scripts](../operations/scripts/) — API-driven certificate expiry reporting, bulk password rotation scripts, and environment health summary automation

**Why third**: Routine operations like certificate rotation and upgrades require familiarity with how Locker propagates changes to managed products.

---

## Stage 4 — Security
**Goal**: Protect Locker credentials, enforce access controls on LCM, and maintain certificate hygiene across the suite.
**Read**:
- [Access Control](../security/access-control/) — LCM user roles, environment-scoped permissions, and Locker object sharing controls
- [Authentication](../security/authentication/) — local admin hardening, vIDM integration for SSO, and API token lifecycle management
- [Encryption](../security/encryption/) — Locker encryption at rest, certificate chain management, and TLS enforcement for LCM API and UI
- [Hardening](../security/hardening/) — restricting LCM UI access by IP, disabling SSH after deployment, audit log configuration, and binary repository integrity checks

**Why fourth**: Locker holds credentials for every managed Aria product; its access controls must be validated before delegating environment management to other teams.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose failed product deployments, upgrade request stalls, and certificate propagation failures.
**Read**:
- [Common Issues](../troubleshooting/common-issues/) — product deployment failures, Locker certificate sync errors, upgrade pre-check failures, and environment health drift
- [Diagnostics](../troubleshooting/diagnostics/) — LCM request log analysis, product health API queries, and Locker connectivity tests to managed products
- [Escalation](../troubleshooting/escalation/) — GSS data requirements for LCM SRs, log bundle export, and SR classification for upgrade pipeline failures

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
