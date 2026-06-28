---
tags:
  - architecture
  - vxrail
---
# VxRail — Cluster Software Stack and Data Plane
![VxRail — Cluster Software Stack and Data Plane](../../../../../assets/virtualization-vmware-vxrail-architecture-how-it-works-index.svg)




```d2
direction: right

center: "VxRail" {shape: hexagon}
hci_node_cluster: "HCI Node Cluster" {shape: rectangle}

center -> hci_node_cluster
```

## Overview

VxRail is a hyper-converged infrastructure (HCI) appliance built on Dell PowerEdge nodes running VMware vSphere and vSAN. Each node contributes local compute (CPU, RAM), NVMe flash cache, and capacity storage to a unified cluster. VxRail Manager orchestrates all lifecycle and configuration operations by communicating with vCenter.

VxRail is sold exclusively as a pre-configured appliance and managed as a system — firmware updates, vSphere upgrades, and vSAN configuration changes all go through the VxRail Manager lifecycle workflow, never independently.

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

## See also

- [VxRail — Design Standards](../design-standards/)
- [VxRail — Deploy](../../deploy/)
- [VxRail — Integrations](../integrations/)
