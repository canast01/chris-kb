# Aria Operations Install & Upgrade

```text
┌────────────────────────────────── Aria Operations Install & Upgrade ──────────────────────────────────┐
│                                                                                                       │
│  OVA/PAK deployment, node cluster setup, and upgrade for Aria Operations (vROps).                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Pre-Requisites                │  │               OVA Deploy Steps              │   │
│   │           vSphere 6.7+ environment           │  │          1. Download OVA from depot         │   │
│   │        DNS forward + reverse records         │  │         2. Deploy via vSphere client        │   │
│   │            NTP server configured             │  │        3. Complete VAMI setup wizard        │   │
│   │           SMTP for alert delivery            │  │         4. Add data nodes if needed         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Pre-requisites validated before OVA; cluster nodes added after master is ready.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              PAK Upgrade Steps               │  │             LCM-Managed Upgrade             │   │
│   │          1. Backup CaSA + snapshot           │  │          LCM: Environment > Upgrade         │   │
│   │            2. Upload PAK in VAMI             │  │          LCM handles PAK + sequence         │   │
│   │           3. Upgrade master first            │  │            Pre-check before apply           │   │
│   │          4. Then data/replica nodes          │  │          Validate after completion          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  vSphere cluster; SSD-backed NFS or vSAN; SMTP server; NTP; DNS with PTR records                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  OVA                 = Open Virtualization Appliance; vROps node deployment package                   │
│  PAK File            = Product upgrade bundle; applied via VAMI or LCM                                │
│  VAMI Setup Wizard   = First-boot configuration: IP, DNS, NTP, admin password                         │
│  Data Node           = Analytics scale-out node added to master cluster post-deploy                   │
│  Replica Node        = HA standby for master; added and promoted via VAMI cluster UI                  │
│  LCM Upgrade         = Aria Suite LCM orchestrates full cluster upgrade                               │
│  CaSA Backup         = Required before any upgrade; stored on NFS or SFTP                             │
│  Pre-check           = LCM validation before upgrade: disk, memory, connectivity                      │
│  Upgrade Sequence    = Master first, then replica, then data nodes, then collectors                   │
│  DNS PTR             = Reverse DNS required for node-to-node cluster communication                    │
│  NTP Sync            = All nodes must be time-synced before and after upgrade                         │
│  Depot               = VMware/Broadcom source for PAK file download via LCM                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────────────────────────┐
│  Pre-Upgrade Gate (must pass before proceeding)                                                       │
│  ✔ All nodes Online (Admin → Cluster Management)                                                      │
│  ✔ All adapters Collecting                                                                            │
│  ✔ Disk < 70% on /storage/db                                                                          │
│  ✔ NTP delta < 1s on all nodes                                                                        │
│  ✔ VM snapshots taken (revert window)                                                                 │
│  ✔ Backup completed within last 24h                                                                   │
└─────────────────────────────────────────────────────┘
```

## Backup

Aria Operations does not have a native backup tool. Use the following:

| Method | What is Backed Up |
|---|---|
| VM snapshot (via vCenter) | Full appliance state — use before upgrades, not for operational backup |
| File-level backup agent | PostgreSQL data files + config (requires LCM configuration) |
| LCM backup | LCM configuration and product manifests |

## EOL Tracking

- Broadcom Product Lifecycle Matrix: [support.broadcom.com/group/ecx/productlifecycle](https://support.broadcom.com/group/ecx/productlifecycle)
- Aria Suite Lifecycle Manager — check installed product versions against the matrix quarterly
- Aim to be no more than one major version behind the current release
