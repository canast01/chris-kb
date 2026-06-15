---
tags:
  - architecture
  - netapp
---
# ONTAP — Architecture

<div class="kb-summary">
ONTAP architecture reference — HA topology, WAFL filesystem engine, SVM design, cluster networking, protocol stack, and data protection built-ins.

*Applies to: ONTAP 9.x*
</div>

```text
┌─────────────────────────── NetApp ONTAP — Unified Storage OS Architecture ────────────────────────────┐
│                                                                                                       │
│  ONTAP is the OS for AFF and FAS arrays; unified SAN + NAS from the same system;                      │
│  SVM for multi-tenancy; Snapshot for instant copies; SnapMirror for replication.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                 Architecture                 │  │                  Protocols                  │   │
│   │       HA pair: two nodes active-active       │  │              NFS v3/v4.1: file              │   │
│   │             Cluster: 2-24 nodes              │  │            SMB/CIFS: Windows file           │   │
│   │         SVM: storage virtual machine         │  │             FC: block SAN (FCP)             │   │
│   │        Aggregate: RAID group of disks        │  │             iSCSI: block over IP            │   │
│   │        Volume: logical data container        │  │             NVMe-oF: FC or RDMA             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SVM is the tenant unit; each has own protocols, LIFs, volumes, and network config.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Data Services                 │  │                  Management                 │   │
│   │       Snapshot: instant, no-cost copy        │  │            System Manager: web UI           │   │
│   │        SnapMirror: async replication         │  │            ONTAP CLI: SSH session           │   │
│   │          SnapVault: backup-to-disk           │  │                REST API: 9.6+               │   │
│   │           SMBC: sync active-active           │  │           ZAPI: legacy automation           │   │
│   │          FabricPool: cloud tiering           │  │            ActiveIQ: cloud health           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  AFF (all-flash) or FAS (hybrid) HA pair in rack; cluster interconnect (100GbE);                      │
│  FC or Ethernet host connectivity; dedicated e0M management port per node.                            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ONTAP          = NetApp unified storage OS; runs on AFF and FAS hardware                             │
│  SVM            = Storage Virtual Machine; multi-tenant partition; own protocols                      │
│  HA pair        = two ONTAP nodes in active-active cluster; failover in seconds                       │
│  Aggregate      = physical RAID group; contains one or more volumes                                   │
│  Volume         = logical data container; flexible size; thin or thick                                │
│  LIF            = Logical Interface; floating IP that moves on failover                               │
│  Snapshot       = space-efficient point-in-time copy; no IO impact                                    │
│  SnapMirror     = async replication between ONTAP systems; DR foundation                              │
│  SnapVault      = vault-mode SnapMirror; retains long-term backup snapshots                           │
│  SMBC           = SnapMirror Business Continuity; synchronous active-active                           │
│  FabricPool     = auto-tier cold data to S3 object store (AWS, GCP, Azure, ECS)                       │
│  RAID-DP        = ONTAP RAID level; double parity; default for FAS                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TB
  N1["Node 1 (Controller)\nSVM-1 · SVM-2"] <-->|"HA interconnect\n100GbE cluster net"| N2["Node 2 (Controller)\n(takeover on failover)"]
  N1 & N2 --> SHELVES[("Disk Shelves\nNVMe SSD / SAS HDD")]
  N1 --> NAS["NFS · SMB/CIFS"]
  N1 --> SAN["iSCSI · FC · NVMe-oF"]
  N2 --> NAS & SAN
  NAS --> NC(["NAS Clients"])
  SAN --> SC(["SAN Hosts"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2 ctrl
  class SHELVES store
  class NC,SC host
```
![ONTAP Architecture](../../../../assets/ontap-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>HA topology, WAFL engine, cluster networking, SVM architecture, protocols, and data protection.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware, SnapCenter, Active Directory, Veeam, REST API, and cloud integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, sizing guidelines, and configuration checklist.</span></a>
</div>

| Platform | Storage Type | Target Workload |
|---|---|---|
| AFF (All Flash FAS) | All-NVMe or all-SSD | Latency-sensitive databases, VDI, high-IOPS workloads |
| FAS (Fabric-Attached Storage) | Hybrid flash/disk | Capacity-optimised, mixed, file, and backup workloads |
| ONTAP Select | Software-defined on x86 | Edge, ROBO, dev/test; VMware or KVM hypervisor |


