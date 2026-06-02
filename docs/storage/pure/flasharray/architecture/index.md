# FlashArray — Architecture

<div class="kb-summary">
Architecture reference for Pure Storage FlashArray. Covers the dual-controller HA model, product lines (//X/C/E), host connectivity protocols (FC, iSCSI, NVMe-oF), Purity data services, ActiveCluster synchronous replication, and design standards.
</div>

```
┌──────────────────────────────────── Pure FlashArray Architecture ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                     FlashArray Architecture — Purity//FA Operating System                     │   │
│   │      Dual-controller HA: CT0 + CT1 active/active, NVRAM write mirroring, < 1 ms write ACK     │   │
│   │   NVMe flash shelves: DirectFlash modules eliminate SSD translation layer for lower latency   │   │
│   │      Inline dedup + compression + thin provisioning applied before data hits flash media      │   │
│   │  Scale-up: add flash shelves to existing array; scale-out via FlashArray//X and FlashArray//C │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Purity//FA manages the full data path from host I/O down to DirectFlash modules                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │         Controller Layer (CT0 / CT1)         │  │             Data Services Layer             │   │
│   │        Active/active: both serve I/O         │  │       Inline dedup: global hash table       │   │
│   │      NVRAM: mirror write buffer CT0-CT1      │  │      Compression: LZ4 + pattern detect      │   │
│   │     Failover: < 30 s automatic takeover      │  │     Thin provisioning: no pre-allocation    │   │
│   │       FC / iSCSI / NVMe/FC host ports        │  │     Snapshots: read-only space-efficient    │   │
│   │          Mgmt: REST API + GUI + CLI          │  │       Clones: writable snapshot copies      │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Controllers handle protocol termination · Data services run inline on every I/O                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Controller HW   │  Flash Shelves   │     Protocols     │   Replication    │   HA Behavior    │   │
│   │  Dual-port HBAs  │ DirectFlash DFM  │     FC: 16/32G    │ ActiveDR: async  │ CT failover <30s │   │
│   │  NVRAM modules   │  NVMe-attached   │   iSCSI: 10/25G   │ActiveCluster sync│  NVRAM protects  │   │
│   │ 10/25G eth mgmt  │ No RAID overhead │   NVMe/FC ports   │   PG schedules   │   No data loss   │   │
│   │ Out-of-band IPMI │  Hot-pluggable   │     NVMe/RoCE     │Cloud snap target │   Transparent    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashArray chassis (//X, //C, //E) · DirectFlash Shelf · FC/iSCSI HBAs · SAN switches · dual PSU     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Purity//FA    = FlashArray OS; manages data services, protocols, and replication                     │
│  CT0 / CT1     = Controller 0 and 1; active/active HA pair serving I/O simultaneously                 │
│  NVRAM         = Non-volatile RAM write buffer; mirrored between controllers before host ACK          │
│  DirectFlash   = Pure custom NVMe SSD (DFM); removes FTL layer for deterministic low latency          │
│  Inline dedup  = Global deduplication run inline on every write; reduces effective flash usage        │
│  ActiveCluster = Synchronous replication stretch cluster; zero RPO, zero RTO failover                 │
│  ActiveDR      = Asynchronous replication; RPO measured in minutes; automated failover                │
│  Protection Group= PG; set of volumes/hosts replicated together on a defined schedule                 │
│  Snapshot      = Read-only, space-efficient point-in-time copy; metadata pointer only                 │
│  Clone         = Writable copy from snapshot; instant, no data movement required                      │
│  NVMe/RoCE     = NVMe over RDMA over Converged Ethernet; low-latency block over IP                    │
│  SafeMode      = Immutable snapshot protection; delete operations require Pure Storage PIN            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

## FlashArray Architecture Models

![FlashArray Architecture Models](../../../../assets/flasharray-architecture-overview.svg)
