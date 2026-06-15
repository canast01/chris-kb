---
tags:
  - architecture
  - netapp
---
# Keystone — Architecture

<div class="kb-summary">
Keystone STaaS architecture reference — delivery model, service tiers, components, capacity model, and consumption reporting.

*Applies to: Keystone STaaS*
</div>

```text
┌───────────────────────── NetApp Keystone — Storage as a Service Architecture ─────────────────────────┐
│                                                                                                       │
│  Pay-per-use STaaS for NetApp AFF, FAS, and Cloud Volumes; Keystone Collector                         │
│  deployed on-prem to track consumption; subscription managed via Keystone Manager.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Service Model                 │  │                Service Levels               │   │
│   │        OpEx: monthly consumption bill        │  │           Extreme: 1ms latency SLA          │   │
│   │          Hardware on-prem or cloud           │  │            Premium: <2ms latency            │   │
│   │         NetApp manages HW lifecycle          │  │            Standard: 4ms latency            │   │
│   │        Burst: auto approved up to X%         │  │           CVO: Cloud Volumes ONTAP          │   │
│   │          Committed + burst billing           │  │         Data protection: add-on tier        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Keystone Collector is a lightweight VM deployed on customer premises to report usage.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Keystone Collector              │  │           Keystone Manager Portal           │   │
│   │          On-prem VM (or container)           │  │            Subscription overview            │   │
│   │          Polls ONTAP for usage data          │  │            Consumption dashboard            │   │
│   │          Reports to Keystone cloud           │  │             Burst usage tracking            │   │
│   │          REST API: cluster metrics           │  │            Invoice reconciliation           │   │
│   │           HTTPS 443: outbound only           │  │            Service request portal           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  NetApp AFF/FAS arrays or Cloud Volumes ONTAP; Keystone Collector VM on vSphere;                      │
│  internet access for Collector to reach Keystone cloud on TCP 443.                                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Keystone       = NetApp STaaS subscription offering; hardware + management included                  │
│  STaaS          = Storage as a Service; pay-per-use like cloud, but on-prem hardware                  │
│  Service level  = latency SLA tier (Extreme/Premium/Standard); billed separately                      │
│  Committed capacity= minimum subscribed amount; always billed regardless of use                       │
│  Burst capacity = usage above committed; auto-approved up to 20% over                                 │
│  Keystone Collector= on-prem VM that tracks and reports consumption to NetApp                         │
│  Keystone Manager= NetApp portal for subscription, usage, and invoice management                      │
│  AFF            = All Flash FAS; NetApp NVMe-ready all-flash array                                    │
│  CVO            = Cloud Volumes ONTAP; ONTAP on AWS/Azure/GCP as Keystone option                      │
│  OpEx model     = operational expense; monthly billing replaces CapEx purchase                        │
│  Data protection tier= add-on: SnapVault/SnapMirror included in the STaaS bill                        │
│  ONTAP API      = Collector queries cluster-mgmt LIF for capacity metrics                             │
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

