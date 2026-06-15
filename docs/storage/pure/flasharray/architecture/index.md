---
tags:
  - architecture
  - pure
---
# FlashArray — Architecture

<div class="kb-summary">
Architecture reference for Pure Storage FlashArray. Covers the dual-controller HA model, product lines (//X/C/E), host connectivity protocols (FC, iSCSI, NVMe-oF), Purity data services, ActiveCluster synchronous replication, and design standards.

*Applies to: FlashArray Purity 6.x*
</div>

```text
┌──────────────────────── Pure FlashArray — All-NVMe Block Storage Architecture ────────────────────────┐
│                                                                                                       │
│  All-NVMe all-flash array for block workloads; Purity//FA OS; ActiveCluster for                       │
│  active-active stretch; SafeMode immutable snapshots; Pure1 SaaS management.                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                   Platform                   │  │                Data Services                │   │
│   │          //X: NVMe enterprise block          │  │        Snapshots: instant, space-eff        │   │
│   │           //C: QLC capacity block            │  │          Clones: writable snap copy         │   │
│   │           //XL: extreme enterprise           │  │         Async replication: remote DR        │   │
│   │        Dual controller: active-active        │  │            ActiveCluster: sync AA           │   │
│   │           FC, iSCSI, NVMe-oF: host           │  │          SafeMode: immutable snaps          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Inline dedup and compression are always on; no performance impact on NVMe.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          ActiveCluster (Sync Repl)           │  │                  Management                 │   │
│   │          Synchronous: 0 RPO, 0 RTO           │  │              Pure1: SaaS portal             │   │
│   │          Both arrays serve host IO           │  │           Purity UI: per-array web          │   │
│   │        Mediator: Pure cloud tiebreak         │  │           REST API: v2; automation          │   │
│   │         Max RTT: 10ms between sites          │  │          PowerShell/Ansible modules         │   │
│   │            VMware vMSC: certified            │  │         Pure1 AI: predictive alerts         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashArray chassis (3U); dual controllers active-active internally; NVMe drive modules;              │
│  FC or 25GbE iSCSI or NVMe-oF to host; management on dedicated port.                                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FlashArray     = Pure all-NVMe block storage array; //X //C //XL variants                            │
│  Purity//FA     = FlashArray OS; manages dedup, compression, replication                              │
│  ActiveCluster  = Pure synchronous replication; active-active; 0 RPO and 0 RTO                        │
│  SafeMode       = immutable Snapshot; protected from deletion even by admin                           │
│  Pure1          = SaaS management portal; all FlashArrays in one view                                 │
│  Snapshot       = instant point-in-time copy; no performance impact                                   │
│  Clone          = writable copy from Snapshot; dev/test use case                                      │
│  Mediator       = Pure cloud service; tiebreaker for ActiveCluster failover                           │
│  NVMe-oF        = NVMe over Fabrics; FC-NVMe or iSER; lowest latency path                             │
│  //X series     = mainstream enterprise; NVMe with DirectFlash modules                                │
│  //C series     = capacity-optimized; QLC NAND; lower cost per GB                                     │
│  vMSC           = vSphere Metro Storage Cluster; ActiveCluster is certified                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![FlashArray Architecture Models](../../../../assets/flasharray-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Dual-controller HA, NVRAM write path, DirectFlash, and data services.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>ActiveCluster, ActiveDR, vSphere plugin, and Pure1 cloud portal.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, protocol selection, and replication design standards.</span>
</a>

</div>

