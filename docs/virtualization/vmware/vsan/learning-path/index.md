# vSAN — Learning Path

<div class="kb-summary">
Recommended reading order for vSAN. Follow these stages in order to build a complete mental model before working with it in production.
</div>

```text
┌──────────────────────────────────────── vSAN — Learning Path ─────────────────────────────────────────┐
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

**Goal**: Understand how vSAN distributes storage across hosts using disk groups, SPBM policies, and the CLOM/CLOMD resync engine.

**Read in this order**:

- [How It Works](../architecture/how-it-works/) — OSA vs ESA architecture, disk groups, CRUSH-based placement, the CLOM daemon, and how SPBM policies translate to component layouts
- [Design Standards](../architecture/design-standards/) — FTT/RAID-5/RAID-6 policy selection, witness node sizing for stretched clusters, and minimum host counts per failure domain
- [Integrations](../architecture/integrations/) — vSAN as the default datastore in vSphere, integration with vCenter HA, NSX storage policies, and HCI Mesh cross-cluster mounts

**Why first**: vSAN's behaviour during a host failure or disk failure is entirely determined by the SPBM policy applied at VM creation. Understanding FTT, component states, and the resync queue before modifying any policy or adding capacity prevents data unavailability events caused by policy mismatches.

---

## Stage 2 — Deployment

**Goal**: Know the network, disk, and host pre-requisites that must be validated before enabling vSAN, and the correct cluster bring-up sequence.

**Read**:

- [Deploy](../deploy/) — vSAN network design (dedicated vmk, MTU 9000), disk group creation, witnessed vs non-witnessed topologies, and two-node ROBO configuration
- [Install & Upgrade](../operations/install-upgrade/) — vSAN on-disk format upgrades, ESA migration from OSA, rolling upgrade sequence with CLOM monitoring, and compatibility matrix validation

**Why second**: vSAN network requirements (dedicated VMkernel, jumbo frames, low-latency links) must be validated before the cluster is enabled. Correcting the network after vSAN is active risks component object degradation and triggers resync storms.

---

## Stage 3 — Operations

**Goal**: Monitor cluster health, understand resync behaviour, and manage capacity without creating unintended policy compliance failures.

**Read in this order**:

- [Health Checks](../operations/health-checks/) — start here every shift; run the routine covering cluster health service checks, component states, resync queue depth, and capacity utilisation
- [CLI Reference](../operations/cli-reference/) — `esxcli vsan`, `cmmds-tool`, `vdq`, and RVC commands for component-level inspection and live object tracing
- [Procedures](../operations/procedures/) — disk replacement workflow, removing a host from a vSAN cluster safely, evacuating capacity before maintenance, and rebalancing after expansion
- [Backup & Restore](../operations/backup-restore/) — vSAN is not a backup target; covers snapshot limitations, Veeam/Avamar integration patterns, and object-level restore limitations
- [Scripts](../operations/scripts/) — PowerCLI scripts for policy compliance reporting, resync monitoring, and cluster capacity forecasting

**Why third**: vSAN operations require you to understand component state transitions (active/absent/degraded) and the resync priority model before making any capacity change. Acting without this knowledge can cause an FTT=1 cluster to drop below the rebuild threshold.

---

## Stage 4 — Security

**Goal**: Enable vSAN encryption at rest or in transit and understand the key provider dependency chain.

**Read**:

- [Access Control](../security/access-control/) — vSAN cluster and datastore permissions, SPBM policy administration roles, and service account requirements for Aria Operations integration
- [Authentication](../security/authentication/) — vCenter SSO dependency for vSAN management operations and the impact of SSO downtime on vSAN cluster configuration changes
- [Encryption](../security/encryption/) — Data-at-rest encryption (D@RE) with KMIP key provider, in-transit encryption between hosts, key rotation procedure, and impact on deduplication/compression
- [Hardening](../security/hardening/) — vSAN iSCSI target hardening, CHAP authentication, audit log review for policy changes, and disabling management access from guest VMs

**Why fourth**: vSAN encryption introduces a hard dependency on the external KMS or vCenter native key provider. Enabling encryption before understanding the key rotation and KMS HA requirements risks an unrecoverable encrypted cluster if the key provider fails.

---

## Stage 5 — Troubleshooting

**Goal**: Diagnose component degradation, resync stalls, stretched cluster split-brain, and capacity alarm root causes.

**Read**:

- [Common Issues](../troubleshooting/common-issues/) — component objects stuck in absent/degraded, resync not progressing, capacity alarm with sufficient free space, and witness appliance unreachable
- [Diagnostics](../troubleshooting/diagnostics/) — `cmmds-tool find`, vSAN health service logs, `vsan.check_state` RVC command, and interpreting proactive tests output
- [Escalation](../troubleshooting/escalation/) — support bundle collection for vSAN (vc-support and per-host vm-support), CLOMD log extraction, and when to engage VMware GSS vs Dell/HPE storage teams

**Why last**: Troubleshooting makes most sense once you know the normal operating state.
