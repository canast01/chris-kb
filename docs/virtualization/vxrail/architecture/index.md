---
tags:
  - architecture
  - vxrail
---
# VxRail — Architecture

<div class="kb-summary">
VxRail architecture overview — node hardware, HCI cluster topology, vSAN disk groups, and management stack integration.
</div>

![VxRail Architecture](../../../assets/vxrail-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="../integration/"><strong>Integration</strong><span>Integration with vCenter, NSX, Aria Operations, and Dell SupportAssist.</span></a>
<a class="kb-card" href="../design-standards/"><strong>Design Standards</strong><span>Sizing, VMkernel network design, vSAN policy, and cluster configuration best practices.</span></a>
</div>

## Cluster Topology

| Parameter | Value |
|---|---|
| Minimum cluster size | 3 nodes (FTT=1 vSAN RAID-1 or RAID-5 with 4+ nodes) |
| Maximum cluster size | 64 nodes |
| Node types | All-flash, NVMe, hybrid (spinning + cache tier) |
| Dedicated management nodes | Optional — separate nodes for vCenter and management VMs |
| Stretched cluster | 2 data sites + 1 witness; requires stretched vSAN |

## HCI Node Cluster

```mermaid
graph TB
  VXM["VxRail Manager\n(lifecycle management)"] --> VCSA["vCenter Server"]
  VXM --> NODES["VxRail Cluster\n3 – 64 nodes"]
  NODES --> N1["VxRail Node 1\nvSAN cache + capacity"]
  NODES --> N2["Node 2"]
  NODES --> N3["Node N…"]
  N1 & N2 & N3 --> DS[("vSAN Datastore")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class VXM,VCSA mgmt
  class NODES ctrl
  class N1,N2,N3 host
  class DS store
```
