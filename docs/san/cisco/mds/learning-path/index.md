# Cisco MDS 9000 — Learning Path

<div class="kb-summary">
Recommended reading order for Cisco MDS 9000. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌────────────────────────────────────── Cisco MDS — Learning Path ──────────────────────────────────────┐
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

**Goal**: Understand the MDS VSAN model, FC routing, NPIV, and how NX-OS fabric services map to physical connectivity.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — MDS fabric architecture: VSANs as logical fabric partitions, device alias zoning, NPIV for virtualised HBA ports, FCNS (name service), FSPF routing, port channels for ISL aggregation
- [Design Standards](../architecture/design-standards/) — VSAN design for multi-tenancy, device alias naming conventions, single-initiator single-target zone enforcement, port channel member selection, FCoE design on MDS 9700
- [Integrations](../architecture/integrations/) — DCNM/NDFC integration for fabric management, Cisco UCS with NPIV, storage array zoning coordination, TACACS+ for management authentication

**Why first**: VSANs and device aliases are the foundational isolation and naming layer on MDS — understanding these before deployment prevents zone sprawl and cross-VSAN connectivity errors.

---

## Stage 2 — Deployment

**Goal**: Configure initial MDS switch parameters, build VSANs, and establish fabric peering.

**Read**:

- [Deploy](../deploy/) — Initial NX-OS setup (hostname, mgmt, VSAN creation, domain ID), ISL/port channel configuration, device alias database population, zone policy and zone set activation
- [Install & Upgrade](../operations/install-upgrade/) — NX-OS upgrade (ISSU for non-disruptive), module firmware upgrade, EPLD upgrade, compatibility matrix validation before upgrade

---

## Stage 3 — Operations

**Goal**: Manage VSANs, zones, and device aliases; monitor fabric health; and execute day-to-day administrative procedures.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — Run the routine first on every shift; check `show interface`, `show zoneset active`, `show fcns database`, `show fspf internal`, port error counters
- [CLI Reference](../operations/cli-reference/) — Essential MDS NX-OS commands: `show vsan`, `zone`, `zoneset`, `device-alias`, `show flogi database`, `show port-channel summary`, `show interface fc` counters
- [Procedures](../operations/procedures/) — Zone add/remove, VSAN membership changes, device alias create/rename, port channel member add, FCSP authentication setup, NPIV enable on edge ports
- [Backup & Restore](../operations/backup-restore/) — `copy running-config startup-config`, config file export to TFTP/SCP, zone database backup, recovering from zone set activation failure
- [Scripts](../operations/scripts/) — Automated interface error polling, zone change audit logging via syslog, flogi database inventory export

---

## Stage 4 — Security

**Goal**: Enforce FC-SP fabric authentication, lock down NX-OS management access, and control zone change permissions.

**Read**:

- [Access Control](../security/access-control/) — NX-OS RBAC roles (network-admin, vsan-admin, zone-admin, read-only), VSAN-scoped role assignment, TACACS+ role mapping
- [Authentication](../security/authentication/) — TACACS+/RADIUS for management plane auth, FC-SP-2 DH-CHAP for inter-switch link authentication, SSH key-based access
- [Encryption](../security/encryption/) — FC-SP-2 switch-to-switch link encryption, MACsec on management interfaces, SCP/SFTP for config transfers, TLS for DCNM API connections
- [Hardening](../security/hardening/) — Disable Telnet and HTTP, restrict management VLANs, enable CFS (Cisco Fabric Services) distribution only over required VSANs, audit log to SIEM

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose VSAN segmentation, login failures, ISL issues, and performance degradation.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — VSAN segmented due to domain ID conflict, host FLOGI rejected (zone not found), ISL not forming, device alias database out of sync, FCoE VFC not coming up
- [Diagnostics](../troubleshooting/diagnostics/) — `show interface fc` error counters, `show flogi database`, `debug fc`, `show fcns database detail`, `show zoneset active vsan`, EthAnalyzer for FCoE
- [Escalation](../troubleshooting/escalation/) — Cisco TAC case creation, `show tech-support` collection, `show logging`, Cisco support for NX-OS bug escalation

**Why last**: MDS troubleshooting maps failure modes back to the VSAN isolation model and fabric login sequence — context established in the Architecture and Operations stages.
