# Nutanix — Architecture

<div class="kb-summary">
AOS distributed architecture, AHV hypervisor, Prism management plane, and cluster design standards. Foundation for understanding how Nutanix HCI works and how to design clusters for production workloads.

*Applies to: AOS 6.x · AHV*
</div>

![Nutanix Architecture Overview](../../../assets/nutanix-architecture-overview.svg)

```text
┌─────────────────────────────── Nutanix Architecture — AOS HCI Cluster ────────────────────────────────┐
│                                                                                                       │
│  Each Nutanix node runs AHV hypervisor + CVM (Controller VM) for local storage;                       │
│  DSF pools all node disks into one distributed datastore; Prism manages cluster.                      │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Node Architecture               │  │          Distributed Storage Fabric         │   │
│   │         AHV: Type-1 hypervisor (KVM)         │  │          DSF: pools all node disks          │   │
│   │         CVM: runs AOS + storage svc          │  │           RF2/RF3: replica factor           │   │
│   │         CVM: reserved 4 vCPU / 12 GB         │  │          Erasure coding: 4+2 / 8+2          │   │
│   │          Local SSD: CVM cache tier           │  │         OpLog: write buffer per node        │   │
│   │        HDD: persistent capacity tier         │  │          Medusa: metadata key-value         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  CVM intercepts all storage I/O from VMs via iSCSI/NFS; handles dedup/compression.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │           Management Plane (Prism)           │  │               Cluster Services              │   │
│   │        Prism Element: per-cluster UI         │  │          Zookeeper: cluster config          │   │
│   │         Prism Central: multi-cluster         │  │          Cassandra: metric storage          │   │
│   │          REST API v2/v3: automation          │  │           Genesis: service manager          │   │
│   │           RBAC: role-based access            │  │         Cerebro: replication engine         │   │
│   │            LCM: lifecycle manager            │  │          Stargate: I/O path handler         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Nutanix NX or OEM (Dell XC, HPE DX, Lenovo HX) nodes; 10/25 GbE switches;                            │
│  IPMI/iDRAC/iLO for OOB management; Foundation for bare-metal imaging.                                │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  AOS           = Acropolis OS; Nutanix hyperconverged OS on each node                                 │
│  AHV           = Acropolis Hypervisor; KVM-based Type-1; replaces ESXi/Hyper-V                        │
│  CVM           = Controller VM; runs storage services per node; always on                             │
│  DSF           = Distributed Storage Fabric; cluster-wide virtual datastore                           │
│  RF2/RF3       = Replication Factor; 2 or 3 copies per block across nodes                             │
│  Prism Element = single-cluster management UI/API                                                     │
│  Prism Central = multi-cluster; required for Flow, Calm, Karbon, Leap                                 │
│  OpLog         = per-node SSD write buffer; flush to extent store async                               │
│  Medusa        = distributed key-value metadata store                                                 │
│  Stargate      = storage I/O handler in CVM; serves iSCSI/NFS to VMs                                  │
│  LCM           = Lifecycle Manager; AOS/AHV/firmware updates                                          │
│  Foundation    = Nutanix imaging tool; bare-metal cluster setup                                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="how-it-works/">
    <strong>How It Works</strong>
    <span>AOS data path, CVM role, Stargate I/O, replication factor, and storage tiers. Start here.</span>
  </a>
  <a class="kb-card" href="design-standards/">
    <strong>Design Standards</strong>
    <span>Node selection, cluster sizing, RF2 vs RF3, container design, network layout, and block awareness.</span>
  </a>
  <a class="kb-card" href="integrations/">
    <strong>Integrations</strong>
    <span>Prism Central registration, AD/LDAP, Veeam, HYCU, Zerto, Prometheus, Nutanix Files, and Calm.</span>
  </a>
</div>
