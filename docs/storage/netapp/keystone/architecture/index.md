# Keystone — Architecture

<div class="kb-summary">
Keystone STaaS architecture reference — delivery model, service tiers, components, capacity model, and consumption reporting.
</div>

```
┌─────────────────────────────────── NetApp Keystone — Architecture ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Architecture: ONTAP cluster + Keystone Collector VM + Active IQ management plane       │   │
│   │        Keystone Collector: Linux VM; gathers usage metrics; uploads to Active IQ portal       │   │
│   │           ONTAP cluster: AFF/FAS nodes in HA pair; manages SVMs, aggregates, volumes          │   │
│   │          Network: in-band data NFS/SMB/iSCSI/FC + out-of-band mgmt HTTPS/AutoSupport          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ONTAP cluster -> Keystone Collector -> Active IQ portal -> billing engine -> invoice               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Storage Layer        │  │       Collection Layer      │  │       Management Layer      │   │
│   │        AFF/FAS nodes        │  │        Keystone Coll.       │  │         Active IQ DA        │   │
│   │       HA pair (2 ctrl)      │  │           Linux VM          │  │       Keystone Portal       │   │
│   │           ONTAP OS          │  │         HTTPS upload        │  │        Billing engine       │   │
│   │         SVMs/volumes        │  │       Capacity metrics      │  │         AutoSupport         │   │
│   │        NFS/SMB/iSCSI        │  │        Perf counters        │  │           REST API          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Data path: host <-> ONTAP data LIFs; mgmt: ONTAP mgmt LIF -> Keystone Collector VM                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │       Role       │      Protocol     │    Placement     │      Notes       │   │
│   │     AFF node     │     Storage      │    NFS/FC/iSCSI   │   On-prem rack   │     HA pair      │   │
│   │   KS Collector   │     Metrics      │     HTTPS/REST    │   Customer VM    │  Sends to cloud  │   │
│   │    Active IQ     │   Portal/bill    │       HTTPS       │   NetApp cloud   │       SaaS       │   │
│   │   AutoSupport    │   Diagnostics    │     HTTPS/SMTP    │  ONTAP built-in  │    To NetApp     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: AFF/FAS 2U/4U shelves in rack · 10/25/100 GbE data NICs · FC 16/32Gb HBAs                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Keystone Collector = Linux VM on-prem; polls ONTAP REST API; uploads usage to cloud                │
│    Active IQ DA       = Digital Advisor; cloud portal for capacity, billing, health                   │
│    HA pair            = Two ONTAP nodes sharing disk shelves; automatic failover                      │
│    SVM                = Storage VM; isolated namespace with LIFs, volumes, protocols                  │
│    Data LIF           = Logical Interface for data traffic; bound to port/VLAN                        │
│    Mgmt LIF           = Management Logical Interface; SSH/REST/ONTAP API access                       │
│    Aggregate          = RAID group container; FlexVols and FlexGroups provisioned here                │
│    AutoSupport        = Built-in ONTAP telemetry; sends support bundles to NetApp                     │
│    REST API           = ONTAP 9.6+ native REST API; used by Keystone Collector                        │
│    ZAPI               = Legacy ONTAP API (pre-REST); still used by older tools                        │
│    ONTAP Mediator     = VM providing quorum for MetroCluster/SnapMirror SM-BC                         │
│    NVMe/FC            = Non-Volatile Memory Express over Fibre Channel; <100 us latency               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌─────────────────────────────────── NetApp Keystone — Architecture ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Architecture: ONTAP cluster + Keystone Collector VM + Active IQ management plane       │   │
│   │        Keystone Collector: Linux VM; gathers usage metrics; uploads to Active IQ portal       │   │
│   │           ONTAP cluster: AFF/FAS nodes in HA pair; manages SVMs, aggregates, volumes          │   │
│   │          Network: in-band data NFS/SMB/iSCSI/FC + out-of-band mgmt HTTPS/AutoSupport          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    ONTAP cluster -> Keystone Collector -> Active IQ portal -> billing engine -> invoice               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Storage Layer        │  │       Collection Layer      │  │       Management Layer      │   │
│   │        AFF/FAS nodes        │  │        Keystone Coll.       │  │         Active IQ DA        │   │
│   │       HA pair (2 ctrl)      │  │           Linux VM          │  │       Keystone Portal       │   │
│   │           ONTAP OS          │  │         HTTPS upload        │  │        Billing engine       │   │
│   │         SVMs/volumes        │  │       Capacity metrics      │  │         AutoSupport         │   │
│   │        NFS/SMB/iSCSI        │  │        Perf counters        │  │           REST API          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Data path: host <-> ONTAP data LIFs; mgmt: ONTAP mgmt LIF -> Keystone Collector VM                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │       Role       │      Protocol     │    Placement     │      Notes       │   │
│   │     AFF node     │     Storage      │    NFS/FC/iSCSI   │   On-prem rack   │     HA pair      │   │
│   │   KS Collector   │     Metrics      │     HTTPS/REST    │   Customer VM    │  Sends to cloud  │   │
│   │    Active IQ     │   Portal/bill    │       HTTPS       │   NetApp cloud   │       SaaS       │   │
│   │   AutoSupport    │   Diagnostics    │     HTTPS/SMTP    │  ONTAP built-in  │    To NetApp     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: AFF/FAS 2U/4U shelves in rack · 10/25/100 GbE data NICs · FC 16/32Gb HBAs                │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Keystone Collector = Linux VM on-prem; polls ONTAP REST API; uploads usage to cloud                │
│    Active IQ DA       = Digital Advisor; cloud portal for capacity, billing, health                   │
│    HA pair            = Two ONTAP nodes sharing disk shelves; automatic failover                      │
│    SVM                = Storage VM; isolated namespace with LIFs, volumes, protocols                  │
│    Data LIF           = Logical Interface for data traffic; bound to port/VLAN                        │
│    Mgmt LIF           = Management Logical Interface; SSH/REST/ONTAP API access                       │
│    Aggregate          = RAID group container; FlexVols and FlexGroups provisioned here                │
│    AutoSupport        = Built-in ONTAP telemetry; sends support bundles to NetApp                     │
│    REST API           = ONTAP 9.6+ native REST API; used by Keystone Collector                        │
│    ZAPI               = Legacy ONTAP API (pre-REST); still used by older tools                        │
│    ONTAP Mediator     = VM providing quorum for MetroCluster/SnapMirror SM-BC                         │
│    NVMe/FC            = Non-Volatile Memory Express over Fibre Channel; <100 us latency               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Keystone Architecture](../../../../assets/netapp-keystone-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>STaaS delivery model, service tiers, components, capacity model, and QoS mapping.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>BlueXP, ActiveIQ, ONTAP, and third-party integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Service level selection, naming conventions, and capacity management thresholds.</span></a>
</div>

| Tier | Platform | IOPS/TB | Latency | Use Case |
|---|---|---|---|---|
| Extreme | NVMe-AF (all-flash NVMe) | Up to 12,000 | < 1 ms | Latency-sensitive databases, high-IOPS workloads |
| Premium | AFF (all-flash SAS/NVMe) | Up to 4,000 | < 1 ms | Mixed workloads, virtualization |
| Standard | FAS (hybrid or capacity flash) | Up to 2,000 | < 2 ms | File storage, backup targets |
| Object | StorageGRID | Up to 64 | < 17 ms | Unstructured data, archives, S3 |


