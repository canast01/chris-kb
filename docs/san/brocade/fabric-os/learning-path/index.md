---
tags:
  - learning-path
  - san
---
# Brocade Fabric OS — Learning Path

<div class="kb-summary">
Recommended reading order for Brocade Fabric OS (FOS). Follow these stages in order to build a complete mental model before working with it in production.

*Applies to: Brocade FOS 9.x*
</div>

```text
┌────────────────────────────────────── Fabric OS — Learning Path ──────────────────────────────────────┐
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

**Goal**: Understand the FC fabric model, the login sequence (FLOGI/PLOGI/PRLI), zoning types, and how ISLs and trunking connect switches in a fabric.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — FC fabric architecture: domain IDs, principal switch election, FLOGI/PLOGI/PRLI login sequence, name server (FCNS), fabric shortest path first (FSPF) routing
- [Design Standards](../architecture/design-standards/) — Zoning best practices (WWN soft vs port hard zoning), single-initiator single-target zone rule, ISL oversubscription ratios, trunking group design, MAPS health threshold baselines
- [Integrations](../architecture/integrations/) — SANnav integration for fabric management, DCNM/BNA migration, syslog to SIEM, SNMP traps to monitoring, Active Directory for RBAC

**Why first**: Misunderstanding FC login sequence or zoning scope causes host connectivity outages — establish the fabric model before configuring anything.

---

## Stage 2 — Deployment

**Goal**: Understand initial FOS configuration, fabric build, and firmware baseline establishment.

**Read**:

- [Deploy](../deploy/) — Switch initial config (IP, domain ID, fabric parameters), fabric join, ISL/trunk configuration, zone database creation and activation, MAPS policy activation
- [Install & Upgrade](../operations/install-upgrade/) — FOS firmware upgrade procedure: single-switch non-disruptive upgrade (ISSU), dual-switch fabric firmware rolling upgrade, firmware download and activation steps

---

## Stage 3 — Operations

**Goal**: Manage zoning, monitor fabric health via MAPS, handle firmware upgrades, and execute day-to-day administrative procedures.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check `switchshow`, `fabricshow`, `islshow`, MAPS health summary, SFP status, error counters
- [CLI Reference](../operations/cli-reference/) — Essential FOS commands: `zoneshow`, `cfgshow`, `cfgsave`, `cfgenable`, `portshow`, `porterrshow`, `switchstatusshow`, `supportshow`
- [Procedures](../operations/procedures/) — Zone add/remove/rename, ISL bounce, port disable/enable, alias management, MAPS policy adjustment, RBAC user management
- [Backup & Restore](../operations/backup-restore/) — `configupload`/`configdownload` for switch config backup, zone database export/import, recovering from zone database corruption
- [Scripts](../operations/scripts/) — Automated `porterrshow` polling, zone change audit logging, MAPS alert integration scripts

---

## Stage 4 — Security

**Goal**: Enforce FC-SP-2 fabric authentication, lock down switch management access, and harden FOS against unauthorised zone changes.

**Read**:

- [Access Control](../security/access-control/) — FOS RBAC roles (admin, zoneadmin, operator, user), chassis-level vs switch-level role scope, AD integration via LDAP
- [Authentication](../security/authentication/) — FC-SP-2 switch authentication (DH-CHAP), management plane SSH key authentication, RADIUS/TACACS+ integration for admin accounts
- [Encryption](../security/encryption/) — Fabric-level FC-SP-2 encryption between switches, management session TLS, SCP for config file transfers
- [Hardening](../security/hardening/) — Disable Telnet and HTTP, restrict management VLANs, enable audit logging (`auditlog`), enforce zone change approval workflows in SANnav

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose fabric segmentation, port login failures, and performance degradation from ISL congestion or credit loss.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — Fabric segmented (domain ID conflict), host FLOGI rejected (zone not found), ISL going offline, port showing FC_LOCK error, MAPS alert for CRC errors
- [Diagnostics](../troubleshooting/diagnostics/) — `portlogshow`, `errdump`, `supportshow`, `fcping`, `fctraceroute`, RASlog analysis, SFP DOM threshold review
- [Escalation](../troubleshooting/escalation/) — Broadcom/Brocade support case creation, `supportsave` bundle collection, Escalation to SAN storage team for end-to-end path tracing

**Why last**: FC fabric troubleshooting requires knowing the normal login sequence and zoning model — established in the Architecture stage — to distinguish misconfiguration from hardware failure.

---

## See also

- [Fabric Os — Deploy](../deploy/)
- [Fabric Os — Procedures](../operations/procedures/)
- [Fabric Os — Common Issues](../troubleshooting/common-issues/)
