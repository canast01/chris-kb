---
tags:
  - architecture
  - vxrail
---
# VxRail — Cluster Software Stack and Data Plane

## Overview

VxRail is a hyper-converged infrastructure (HCI) appliance built on Dell PowerEdge nodes running VMware vSphere and vSAN. Each node contributes local compute (CPU, RAM), NVMe flash cache, and capacity storage to a unified cluster. VxRail Manager orchestrates all lifecycle and configuration operations by communicating with vCenter.

VxRail is sold exclusively as a pre-configured appliance and managed as a system — firmware updates, vSphere upgrades, and vSAN configuration changes all go through the VxRail Manager lifecycle workflow, never independently.

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

## See also

- [VxRail — Design Standards](../design-standards/)
- [VxRail — Deploy](../../deploy/)
- [VxRail — Integrations](../integrations/)
