# Aria Operations Lifecycle


<div class="kb-summary">
Aria Operations Lifecycle reference covering Upgrade Overview, Pre-Upgrade Checklist, Upgrade Procedure via LCM, Backup, EOL Tracking.
</div>

```
┌─────────────────────────────── Aria Operations — Lifecycle Management ────────────────────────────────┐
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Install / Deploy               │  │                 Upgrade Path                │   │
│   │            OVA deploy to vCenter             │  │             Check interop matrix            │   │
│   │             Size per node count              │  │              PAK upgrade first              │   │
│   │             License via Aria LCM             │  │           Snapshot before upgrade           │   │
│   │            vCenter adapter setup             │  │             Upgrade via Admin UI            │   │
│   │            Initial policy config             │  │               Data nodes first              │   │
│   │                Add data nodes                │  │               Master node last              │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Snapshots before upgrade + rollback plan required; Aria LCM preferred for orchestrated upgrades    │
│                                                                                                       │
│                                                  ▼                                                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Backup & Restore               │  │                 Decommission                │   │
│   │              File-based backup               │  │              Export dashboards              │   │
│   │              NFS or SCP target               │  │              Export alert defs              │   │
│   │              Scheduled nightly               │  │               Remove adapters               │   │
│   │             Retention: 7 copies              │  │                Power off VMs                │   │
│   │             Restore via Admin UI             │  │             Delete from vCenter             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  OVA size S: 4 vCPU/16 GB · M: 8/32 · L: 16/48 · NFS backup target requires TCP 2049                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Aria LCM = Aria Lifecycle Manager; orchestrates upgrade sequencing across Aria product stack         │
│  OVA = Open Virtual Appliance; VM image format used to deploy Aria Ops nodes                          │
│  Interop matrix = VMware compatibility matrix; confirms supported vCenter/ESXi versions               │
│  PAK upgrade = Updating adapter packages before upgrading the core platform                           │
│  File-based backup = Aria Ops native backup creating encrypted archive of config and data             │
│  Data node = Worker node that stores metric data and runs analytics jobs                              │
│  Master node = Primary node hosting the UI, REST API, and cluster coordinator                         │
│  Rollback = Restoring from snapshot if upgrade fails; requires VM snapshot taken before start         │
│  License key = Aria Ops license applied via Administration > Licensing; tied to object count          │
│  SCP target = SSH-based file copy destination for backup archives                                     │
│  Admin UI = Web-based cluster management at https://<master>:5480                                     │
│  Upgrade token = Short-lived credential required for cluster join during multi-node upgrade           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Backup

Aria Operations does not have a native backup tool. Use the following:

| Method | What is Backed Up |
|---|---|
| VM snapshot (via vCenter) | Full appliance state — use before upgrades, not for operational backup |
| File-level backup agent | PostgreSQL data files + config (requires LCM configuration) |
| LCM backup | LCM configuration and product manifests |

## EOL Tracking

- Broadcom Product Lifecycle Matrix: [lifecycle.broadcom.com](https://lifecycle.broadcom.com)
- Aria Suite Lifecycle Manager — check installed product versions against the matrix quarterly
- Aim to be no more than one major version behind the current release
