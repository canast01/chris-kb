# Cisco DCNM — Learning Path

<div class="kb-summary">
Recommended reading order for Cisco DCNM (Nexus Dashboard Fabric Controller). Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌───────────────────────────────────── Cisco DCNM — Learning Path ──────────────────────────────────────┐
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

**Goal**: Understand DCNM's role as the SAN and LAN fabric management platform, its discovery model, and its evolution toward Nexus Dashboard Fabric Controller (NDFC).

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — DCNM architecture: fabric discovery via SNMP/SSH, POAP (Power On Auto Provisioning) for zero-touch switch bring-up, topology view construction, zone management database, performance collection from MDS and Nexus switches
- [Design Standards](../architecture/design-standards/) — Deployment mode selection (OVA vs ISO, standalone vs HA), SAN vs LAN fabric scope, seed switch strategy for discovery, migration path from standalone DCNM to NDFC on Nexus Dashboard
- [Integrations](../architecture/integrations/) — MDS 9000 SAN fabric management, Nexus LAN fabric integration, TACACS+/LDAP for management RBAC, Cisco Intersight for cloud management, syslog export to SIEM

**Why first**: DCNM sits above the switch fabric — understanding the boundary between switch-level config (NX-OS) and DCNM-managed config is essential before making changes from either interface.

---

## Stage 2 — Deployment

**Goal**: Install DCNM, discover fabrics, and configure POAP for future switch provisioning.

**Read**:

- [Deploy](../deploy/) — OVA/ISO deployment, initial configuration wizard, seed switch entry for fabric discovery, POAP configuration for zero-touch provisioning, license activation
- [Install & Upgrade](../operations/install-upgrade/) — DCNM version upgrade procedure, database backup before upgrade, migration to NDFC on Nexus Dashboard, post-upgrade fabric re-discovery

---

## Stage 3 — Operations

**Goal**: Use DCNM to manage SAN zones, monitor topology, deploy firmware updates, and respond to fabric events.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check fabric discovery status, switch reachability, POAP device queue, pending firmware compliance alerts
- [CLI Reference](../operations/cli-reference/) — DCNM REST API for fabric topology queries, zone management, switch provisioning; `dcnm-cli` for appliance management
- [Procedures](../operations/procedures/) — SAN zone create/modify/delete via DCNM GUI, firmware upgrade deployment to switch group, POAP device onboarding, topology-based path tracing
- [Backup & Restore](../operations/backup-restore/) — DCNM database backup, configuration export, restore to new DCNM instance, switch config archive management
- [Scripts](../operations/scripts/) — Automated switch inventory export via REST API, zone change audit reports, firmware compliance matrix generation

---

## Stage 4 — Security

**Goal**: Enforce RBAC in DCNM and secure both the management appliance and its connections to switches.

**Read**:

- [Access Control](../security/access-control/) — DCNM RBAC roles (Network-Admin, Network-Operator, Zone-Admin), fabric-scoped permissions, LDAP group-to-role mapping
- [Authentication](../security/authentication/) — LDAP/AD integration for DCNM login, local admin hardening, HTTPS certificate configuration, switch SSH credential management in DCNM
- [Encryption](../security/encryption/) — HTTPS enforcement for DCNM portal, TLS for switch SSH connections, encrypted DCNM database credentials, SCP for config archive transfers
- [Hardening](../security/hardening/) — Restrict DCNM management network exposure, disable HTTP, audit log export to SIEM, enforce zone change approval workflows

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose discovery failures, POAP issues, zone push errors, and stale topology data.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Switch not discovered after seed entry, POAP device stuck in pending, zone activation from DCNM failing, topology links missing for known ISL
- [Diagnostics](../troubleshooting/diagnostics/) — DCNM application logs, fabric re-discovery trigger, switch SNMP credential revalidation, SSH connectivity test from DCNM to switch, REST API health check
- [Escalation](../troubleshooting/escalation/) — Cisco TAC case for DCNM bugs, log bundle collection from DCNM appliance, NX-OS `show tech-support` for switch-side issues

**Why last**: Troubleshooting DCNM requires understanding both the NX-OS fabric model (what DCNM discovers) and the DCNM collection pipeline — context built in the Architecture and Operations stages.
