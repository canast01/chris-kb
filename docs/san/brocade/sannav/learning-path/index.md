---
tags:
  - learning-path
  - san
---
# Brocade SANnav — Learning Path

<div class="kb-summary">
Recommended reading order for Brocade SANnav. Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Brocade FOS 9.x*
</div>

```text
┌─────────────────────────────────────── SANnav — Learning Path ────────────────────────────────────────┐
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

**Goal**: Understand SANnav's role as the SAN management platform, its fabric discovery model, and how it replaces legacy BNA/DCNM tools.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — SANnav Management Portal architecture: fabric discovery via SNMP/REST, switch agent communication, embedded analytics engine, performance data collection pipeline
- [Design Standards](../architecture/design-standards/) — Multi-fabric deployment sizing, seed switch selection for discovery, zone management workflow design, alert policy design, migration from BNA/DCNM
- [Integrations](../architecture/integrations/) — Brocade FOS switch compatibility matrix, LDAP/AD integration for RBAC, syslog forwarding to SIEM, SNMP trap receiver configuration, email alert delivery

**Why first**: SANnav must be understood as a management overlay, not a data plane component — its discovery and monitoring capabilities depend on FOS fabric health covered in the Fabric OS learning path.

---

## Stage 2 — Deployment

**Goal**: Install SANnav as a virtual appliance, discover fabrics, and migrate zone management from legacy tools.

**Read**:

- [Deploy](../deploy/) — OVA/ISO deployment, initial configuration, fabric seed switch entry, full fabric discovery, BNA/DCNM zone database migration, license activation
- [Install & Upgrade](../operations/install-upgrade/) — SANnav version upgrade procedure, database backup before upgrade, post-upgrade fabric re-discovery validation

---

## Stage 3 — Operations

**Goal**: Use SANnav to manage zones across fabrics, monitor performance, push firmware updates, and respond to alerts.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check fabric discovery health, switch reachability, pending alerts, performance threshold violations
- [CLI Reference](../operations/cli-reference/) — SANnav REST API for fabric queries, zone operations, device inventory export; `sannav` CLI for appliance management
- [Procedures](../operations/procedures/) — Zone create/modify/delete via SANnav GUI, firmware update deployment to switch group, alert policy configuration, device inventory report generation
- [Backup & Restore](../operations/backup-restore/) — SANnav database backup, configuration export, disaster recovery restore to a new appliance instance
- [Scripts](../operations/scripts/) — Automated zone change audit reports via REST API, performance trend extraction, firmware compliance reporting

---

## Stage 4 — Security

**Goal**: Enforce role-based access in SANnav and secure the management plane.

**Read**:

- [Access Control](../security/access-control/) — SANnav RBAC roles (Super Admin, Fabric Admin, Zone Admin, Operator, View Only), fabric-scoped role assignment, AD group mapping
- [Authentication](../security/authentication/) — LDAP/AD integration for SANnav login, local admin account hardening, certificate-based HTTPS, session timeout policy
- [Encryption](../security/encryption/) — HTTPS enforcement for SANnav portal, TLS for switch API connections, encrypted SANnav database at rest
- [Hardening](../security/hardening/) — Restrict SANnav management network access, audit log export, disable default admin credentials post-deployment, enforce zone change approval workflow

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose fabric discovery failures, missing switches, stale performance data, and zone push failures.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Switch showing unreachable in SANnav, zone activation failure from GUI, performance charts missing data, alert not firing for known MAPS event
- [Diagnostics](../troubleshooting/diagnostics/) — SANnav application logs (`/var/log/sannav`), fabric re-discovery trigger, switch SNMP credential validation, REST API connectivity test from SANnav to FOS
- [Escalation](../troubleshooting/escalation/) — Broadcom support case for SANnav bugs, log bundle collection from SANnav appliance, FOS `supportsave` for switch-side issues

**Why last**: SANnav troubleshooting requires understanding both the FOS fabric model (what SANnav is monitoring) and the SANnav data collection pipeline — both established in earlier stages.
