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

