# Keystone — Architecture

<div class="kb-summary">
Keystone STaaS architecture reference — delivery model, service tiers, components, capacity model, and consumption reporting.
</div>

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

```mermaid
graph TB
  ONTAP["NetApp ONTAP\n(on-premises / colocation)"] -->|"telemetry"| KS["NetApp Keystone\n(STaaS portal)"]
  KS --> COMMIT["Committed Capacity Tier"]
  KS --> BURST["Burst Capacity\n(on-demand)"]
  KS --> BILL["Monthly Billing"]
  ADMIN(["Customer Admin"]) -->|"portal"| KS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ONTAP ctrl
  class KS,COMMIT,BURST,BILL cloud
  class ADMIN host
```
