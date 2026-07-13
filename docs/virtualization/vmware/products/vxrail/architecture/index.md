---
tags:
  - architecture
  - vxrail
description: "VxRail architecture overview — node hardware, HCI cluster topology, vSAN disk groups, and management stack integration."
---
# VxRail — Architecture

<div class="kb-summary">
VxRail architecture overview — node hardware, HCI cluster topology, vSAN disk groups, and management stack integration.

*Applies to: VxRail 7.x · 8.x*
</div>

![VxRail Architecture](../../../../../assets/vxrail-architecture-overview.svg)

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

```d2
direction: right

VXM: "VxRail Manager\n(lifecycle management" {shape: rectangle}
VCSA: "vCenter Server" {shape: rectangle}
NODES: "VxRail Cluster\n3 – 64 nodes" {shape: rectangle}
N1: "VxRail Node 1\nvSAN cache + capacity" {shape: rectangle}
N2: "Node 2" {shape: rectangle}
N3: "Node N…" {shape: rectangle}
DS: "vSAN Datastore" {shape: rectangle}

VXM -> VCSA
VXM -> NODES
NODES -> N1
NODES -> N2
NODES -> N3
N1 -> N2
N2 -> N3
N3 -> DS
```
