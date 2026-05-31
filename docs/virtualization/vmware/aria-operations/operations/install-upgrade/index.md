# Aria Operations — Install & Upgrade

```text
Aria Operations — Upgrade Paths
┌─────────────────────────────────────────────────────┐
│  Option A: Aria Suite Lifecycle (Recommended)       │
│                                                     │
│  Aria LCM → Lifecycle Operations                    │
│  → select environment → Upgrade                     │
│  → select target version from marketplace           │
│  → run pre-upgrade health checks                    │
│  → LCM upgrades nodes in sequence:                  │
│                                                     │
│    Data nodes → Replica → Primary                   │
│    (primary always last)                            │
└──────────────────────────┬──────────────────────────┘
                           │ or
                           ▼
┌─────────────────────────────────────────────────────┐
│  Option B: In-Product Upgrade (Standalone)          │
│                                                     │
│  Admin → Software Update → Upload PAK               │
│  → Run pre-check → Proceed                          │
│                                                     │
│  Air-gap:                                           │
│  vracli software-update install --file <pak>        │
└──────────────────────────┬──────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────┐
│  Pre-Upgrade Gate (must pass before proceeding)     │
│  ✔ All nodes Online (Admin → Cluster Management)    │
│  ✔ All adapters Collecting                          │
│  ✔ Disk < 70% on /storage/db                        │
│  ✔ NTP delta < 1s on all nodes                      │
│  ✔ VM snapshots taken (revert window)               │
│  ✔ Backup completed within last 24h                 │
└─────────────────────────────────────────────────────┘
```
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

---

## Interoperability Matrix

| Aria Operations | vSphere / ESXi | NSX-T | vSAN |
|-----------------|---------------|-------|------|
| 8.18 | 7.0 U3+, 8.0+ | 4.x | 8.0+ |
| 8.16 | 7.0 U2+, 8.0 | 4.x | 7.0+ |
| 8.14 | 7.0 U1+, 8.0 | 3.x, 4.x | 7.0+ |

> Always verify against the official interop matrix before upgrading.

---

## EOL Tracking

| Version | GA Date | EOL Date |
|---------|---------|----------|
| vROps 8.6.x | 2021-10 | Per Broadcom lifecycle policy |
| vROps 8.10.x | 2022-10 | Per Broadcom lifecycle policy |
| Aria Operations 8.14+ | 2023+ | Check Broadcom lifecycle page |

Reference: [Broadcom Lifecycle Policy](https://support.broadcom.com/lifecycle-management)

---

## Pre-Upgrade Checklist

- [ ] Current version and target version interoperability verified
- [ ] Snapshot of all cluster VMs taken (revert window)
- [ ] Cluster health shows all nodes **Online**
- [ ] All adapter instances show **Collecting**
- [ ] PAK file or LCM repository access confirmed
- [ ] Maintenance window scheduled; alert notification sent
- [ ] Backup of custom dashboards, alert definitions, and super metrics exported

---

## Post-Upgrade Validation

- [ ] Cluster management page shows all nodes **Online**
- [ ] All adapters resume collecting (allow 15–30 min after upgrade)
- [ ] UI version string matches target in Administration > About
- [ ] Dashboards and alerts still present
- [ ] Custom content (super metrics, views) intact

---

## Related Sections

- [Architecture](../../architecture/index.md) — node roles
- [Operations](../index.md) — health checks
- [Escalation](../../troubleshooting/escalation/index.md) — opening upgrade-related cases
