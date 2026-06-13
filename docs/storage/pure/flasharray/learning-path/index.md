# Pure Storage FlashArray — Learning Path

<div class="kb-summary">
Recommended reading order for Pure Storage FlashArray. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌───────────────────────────────────── FlashArray — Learning Path ──────────────────────────────────────┐
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

**Goal**: Understand how Purity//FA manages DirectFlash modules, how volumes and pods are structured, and how ActiveCluster delivers zero-RPO replication.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — DirectFlash module architecture, Purity//FA OS data services layer, inline deduplication and compression pipeline, volume and host connectivity model (FC/iSCSI/NVMe-oF), and pod (ActiveCluster) stretch topology
- [Design Standards](../architecture/design-standards/) — volume naming conventions, host group design, protection group membership rules, replication target pairing, and ActiveCluster mediator placement
- [Integrations](../architecture/integrations/) — vSphere VASA/VAAI, Kubernetes CSI (pure-csi), VMware SRM integration, and REST API / Pure1 cloud connectivity

**Why first**: Purity's abstraction of DirectFlash modules is fundamentally different from traditional SAN. Understanding pods and protection groups before touching replication prevents split-brain scenarios on ActiveCluster.

---

## Stage 2 — Deployment

**Goal**: Understand initial array setup, host connectivity, and how to validate a new array before attaching production workloads.

**Read**:

- [Deploy](../deploy/) — initial Purity setup wizard, management network configuration, array-to-array replication pairing, ActiveCluster mediator configuration, and post-deployment validation checklist
- [Install & Upgrade](../operations/install-upgrade/) — Purity//FA upgrade procedure (non-disruptive), pre-upgrade health check, upgrade scheduling via Pure1, and post-upgrade validation steps

**Why second**: ActiveCluster mediator misconfiguration is the leading cause of unplanned failover during maintenance. Understanding pairing and mediator roles prevents it.

---

## Stage 3 — Operations

**Goal**: Manage volumes, protection groups, and snapshots confidently; maintain replication; and respond to capacity and performance events.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — run the routine first on every shift; covers array health dashboard, drive status, replication lag, protection group snapshot age, and SafeMode status
- [CLI Reference](../operations/cli-reference/) — `purevol`, `purepgroup`, `purehost`, `purerepl`, and `puresupport` command reference for day-to-day volume and replication management
- [Procedures](../operations/procedures/) — volume provisioning and host mapping, protection group snapshot and replication configuration, ActiveCluster failover and failback, and SafeMode enable/disable workflow
- [Backup & Restore](../operations/backup-restore/) — protection group snapshot schedules, offload to NFS/S3 targets, volume restore from snapshot, and cross-array clone workflows
- [Scripts](../operations/scripts/) — automation for snapshot age auditing, replication lag alerting, and capacity trend reporting via REST API

**Why third**: Snapshot and replication management on FlashArray is policy-driven. Understanding protection groups before scripting snapshot workflows prevents orphaned snapshots consuming capacity.

---

## Stage 4 — Security

**Goal**: Enforce access control using roles and API tokens, ensure data-at-rest encryption is validated, and lock down SafeMode to protect snapshots from ransomware.

**Read**:

- [Access Control](../security/access-control/) — Purity role model (array admin/storage admin/read-only), local vs directory-service users, and API token scoping per integration
- [Authentication](../security/authentication/) — LDAP/AD integration for Purity GUI/CLI, SAML SSO via Pure1, multi-factor authentication requirements, and API token rotation
- [Encryption](../security/encryption/) — FIPS 140-2 validated encryption on DirectFlash modules, encryption key management (internal vs KMIP external), and encryption status validation
- [Hardening](../security/hardening/) — SafeMode snapshot protection (eradicator lockout), management network isolation, audit log forwarding (syslog), and TLS cipher configuration

**Why fourth**: SafeMode is a critical ransomware protection feature that requires Pure support to disable — enabling it is a one-way door. Understand the access model before activating it in production.

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose connectivity, performance, and replication failures using Purity logs and Pure1 analytics before escalating to Pure Support.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — host connectivity loss (FC zoning, iSCSI session drops), replication paused states, protection group snapshot failures, and capacity alert thresholds
- [Diagnostics](../troubleshooting/diagnostics/) — Purity diagnostic bundle collection, Pure1 anomaly detection alerts, latency histogram analysis, and ActiveCluster mediator connectivity checks
- [Escalation](../troubleshooting/escalation/) — Pure Support case creation (via Pure1 or phone), diagnostic bundle upload, Evergreen SLA response time tiers, and on-site hardware replacement workflow

**Why last**: Troubleshooting makes most sense once you know the normal operating state — healthy replication lag ranges, expected latency baselines, and what protection group states indicate active data protection.
