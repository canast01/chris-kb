# VxRail — Learning Path

<div class="kb-summary">
Recommended reading order for VxRail. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌─────────────────────────────────────── VxRail — Learning Path ────────────────────────────────────────┐
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
  classDef done fill:#15803d,stroke:#166534,color:#fff
  classDef stage fill:#1e3a5f,stroke:#2563eb,color:#fff
  class S1,S2,S3,S4,S5 stage
```
## Stage 1 — Architecture

**Goal**: Understand how VxRail Manager orchestrates a tightly integrated Dell hardware and VMware software stack that must always be upgraded as a single validated bundle.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — VxRail Manager VM role (embedded in the cluster), node anatomy (cache/capacity drive layout, NIC topology), cluster formation via the first-run wizard, and the relationship to vCenter and vSAN
- [Design Standards](../architecture/design-standards/) — node model selection, network profile (dynamic vs static), vSAN disk group layout per node type, and stretched cluster witness appliance placement
- [Integrations](../architecture/integrations/) — VxRail Manager integration with vCenter, iDRAC out-of-band management, OMIVV for OpenManage integration, and SDDC Manager when deployed as a VCF-managed system

**Why first**: VxRail is opinionated — firmware, ESXi, vSAN, and VxRail Manager versions must match the validated bundle. Understanding why manual patching of any individual component is unsupported before touching any upgrade or configuration task prevents the cluster entering an unsupported state that voids Dell support.

---

## Stage 2 — Deployment

**Goal**: Know the network pre-requisites, the first-run wizard sequence, and the iDRAC validation steps before powering on the first node.

**Read**:

- [Deploy](../deploy/) — physical cabling validation, iDRAC network configuration, first-run wizard inputs (network profile, DNS, NTP, vCenter credentials), and initial vSAN policy assignment
- [Install & Upgrade](../operations/install-upgrade/) — LCM bundle download via VxRail Manager, pre-upgrade health checks, upgrade sequence (VxRail Manager → vCenter → NSX → ESXi+firmware), and post-upgrade validation

**Why second**: The first-run wizard makes irreversible decisions about the cluster network profile, vCenter registration, and vSAN disk group layout. Running it without fully validated iDRAC access, DNS resolution, and NTP synchronisation results in a failed bring-up that requires factory reset of the nodes.

---

## Stage 3 — Operations

**Goal**: Monitor cluster health through VxRail Manager, manage the LCM bundle lifecycle, and handle node-level hardware events without breaking vSAN.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — start here every shift; run the routine covering VxRail Manager service health, iDRAC hardware alerts, vSAN component states, and LCM bundle currency
- [CLI Reference](../operations/cli-reference/) — VxRail Manager API endpoints for cluster health, `vxrail-callhome` CLI, `esxcli` on VxRail nodes for storage path inspection, and iDRAC RACADM commands
- [Procedures](../operations/procedures/) — node expansion workflow via VxRail Manager, disk replacement and rebuild monitoring, entering maintenance mode on a VxRail node, and VxRail Manager VM recovery
- [Backup & Restore](../operations/backup-restore/) — VxRail Manager configuration backup, cluster state backup dependencies (vCenter file-based backup), and recovery sequence after total cluster failure
- [Scripts](../operations/scripts/) — VxRail Manager API scripts for health polling, LCM bundle status monitoring, and iDRAC firmware inventory export

**Why third**: VxRail LCM bundles are the only supported upgrade path — no manual ESXi patch, driver update, or firmware flash outside of LCM. Understanding the LCM pre-check requirements and the upgrade sequence before any maintenance window prevents an upgrade failure that can leave nodes in an inconsistent state.

---

## Stage 4 — Security

**Goal**: Secure iDRAC access, manage VxRail Manager credentials, and apply hardening without breaking the LCM service account dependencies.

**Read**:

- [Access Control](../security/access-control/) — VxRail Manager local accounts, vCenter integration permissions, iDRAC user management, and the Dell service account required for OMIVV
- [Authentication](../security/authentication/) — VxRail Manager certificate replacement, iDRAC certificate management, and integrating iDRAC with AD for out-of-band access
- [Encryption](../security/encryption/) — vSAN data-at-rest encryption on VxRail nodes (requires external KMS), iDRAC TLS enforcement, and encrypted vMotion between nodes
- [Hardening](../security/hardening/) — iDRAC network isolation, disabling default credentials, VxRail Manager API access restriction, and audit log configuration for compliance reporting

**Why fourth**: VxRail hardening must account for the iDRAC and OMIVV service accounts that LCM uses during firmware upgrades. Rotating iDRAC credentials without updating VxRail Manager causes the next LCM operation to fail at the firmware stage.

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose LCM upgrade failures, node disconnections, iDRAC hardware alerts, and VxRail Manager service unavailability.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — LCM upgrade failure mid-node, VxRail Manager VM unresponsive, node disconnected from vCenter after hardware event, and iDRAC alert flooding after a drive failure
- [Diagnostics](../troubleshooting/diagnostics/) — VxRail Manager log collection (`/var/log/mystic/`), LCM job history via API, iDRAC SEL log export, and `esxcli storage core path list` for drive path validation
- [Escalation](../troubleshooting/escalation/) — Dell SupportAssist log bundle generation, required VxRail Manager API exports before opening a case, and when to engage Dell Hardware vs VMware GSS separately

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
