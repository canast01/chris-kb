# Aria Operations for Networks — Learning Path

<div class="kb-summary">
Recommended reading order for Aria Operations for Networks (vRNI). Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌──────────────────────────── Aria Operations for Networks — Learning Path ─────────────────────────────┐
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
**Goal**: Understand how vRNI collects flow data and topology from heterogeneous sources to build a queryable network model.
**Read in this order**:
- [How It Works](../architecture/how-it-works/) — Platform VM and Proxy VM roles, data source collection (NSX, vCenter, physical switches via SNMP/NetFlow), and flow processing pipeline
- [Design Standards](../architecture/design-standards/) — Platform and Proxy VM sizing, data source limits per proxy, and multi-site deployment patterns
- [Integrations](../architecture/integrations/) — NSX-T/NSX-V data sources, vCenter inventory sync, physical switch SNMP/IPFIX, and Aria Operations bi-directional linking

**Why first**: vRNI's analytical power depends on data source completeness; understanding which sources feed which network model elements prevents blind spots in path analysis and micro-segmentation planning.

---

## Stage 2 — Deployment
**Goal**: Deploy Platform and Proxy VMs, register all data sources, and validate flow visibility.
**Read**:
- [Deploy](../deploy/) — OVA deployment order (Platform first, then Proxy), licensing, and initial data source registration sequence
- [Install & Upgrade](../operations/install-upgrade/) — in-place upgrade path, proxy upgrade sequencing, and post-upgrade data source re-validation

**Why second**: Proxy VMs must be deployed and network-reachable to data sources before any flows appear; getting this right up front avoids re-registration churn.

---

## Stage 3 — Operations
**Goal**: Use flow search, path analysis, and micro-segmentation planning tools as routine operational instruments.
**Read in this order**:
- [Health Checks](../operations/health-checks/) — run the routine first on every shift
- [CLI Reference](../operations/cli-reference/) — API and CLI commands for data source status, flow query exports, and application definition management
- [Procedures](../operations/procedures/) — application grouping, micro-segmentation recommendation workflows, saved searches, and network assurance checks
- [Backup & Restore](../operations/backup-restore/) — configuration backup scope (data sources, apps, saved searches) and restore procedure for Platform VM failure
- [Scripts](../operations/scripts/) — API-driven application definition import/export and flow data extraction for SIEM or compliance reporting

**Why third**: Path analysis and micro-segmentation planning require stable, complete flow data that only appears after data sources are correctly registered and collecting.

---

## Stage 4 — Security
**Goal**: Control access to sensitive flow data and network topology by role, and protect data source credentials.
**Read**:
- [Access Control](../security/access-control/) — user roles (Network Admin, Security Admin, Member), application-scoped permissions, and read-only dashboard sharing
- [Authentication](../security/authentication/) — LDAP/Active Directory integration, local admin hardening, and SSO configuration
- [Encryption](../security/encryption/) — HTTPS enforcement, data source credential storage, and TLS certificate management for the Platform VM
- [Hardening](../security/hardening/) — restricting Proxy VM management access, SNMP community string rotation, and audit trail configuration

**Why fourth**: Flow data reveals internal network topology and VM communication patterns; access control must be validated before sharing dashboards with application teams.

---

## Stage 5 — Troubleshooting
**Goal**: Diagnose missing flows, incorrect path analysis results, and data source collection failures.
**Read**:
- [Common Issues](../troubleshooting/common-issues/) — data source collection errors, missing IPFIX flows, stale topology objects, and NSX rule recommendation gaps
- [Diagnostics](../troubleshooting/diagnostics/) — support bundle collection, proxy collection log analysis, and flow pipeline health checks via API
- [Escalation](../troubleshooting/escalation/) — GSS data requirements, data source diagnostic exports, and SR classification for flow data completeness issues

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
