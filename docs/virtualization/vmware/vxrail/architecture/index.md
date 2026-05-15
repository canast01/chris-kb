# VxRail — Architecture

<div class="kb-summary">
Dell VxRail is an HCI appliance built on vSphere and vSAN. VxRail Manager orchestrates lifecycle upgrades as a single tested bundle (ESXi + vCenter + vSAN + firmware). All storage is vSAN-based — no external shared storage in a standard deployment.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Cluster topology, node families, vSAN integration, network design, deployment models, and VxRail Manager API.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>vCenter plugin, Dell support APIs, Aria Operations, and external system integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, network design rules, and configuration baselines.</span></a>
</div>

---

## Key Components

| Component | Purpose |
|---|---|
| VxRail Manager | Cluster lifecycle, expansion, LCM orchestration; deployed as a VM |
| vCenter Server | vSphere cluster management — embedded or customer-provided external |
| vSAN | Distributed storage layer; all node storage pooled into one vSAN datastore |
| iDRAC | Dell OOB management on each node; used by VxRail for hardware health |
| VxRail LCM | Orchestrates bundles of ESXi + vCenter + firmware updates |

---

## Architecture Overview

```mermaid
graph TB
  VXM["VxRail Manager\n(VM on first node)"]
  VXM --> VC["vCenter Server"]
  VC --> CL["vSphere Cluster"]
  CL --> N1["Node 1\nESXi + vSAN Disk Groups"]
  CL --> N2["Node 2\nESXi + vSAN Disk Groups"]
  CL --> N3["Node 3\nESXi + vSAN Disk Groups"]
  N1 --> DS["vSAN Datastore\n(distributed across all nodes)"]
  N2 --> DS
  N3 --> DS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef node fill:#15803d,stroke:#166534,color:#fff
  classDef storage fill:#7c3aed,stroke:#6d28d9,color:#fff
  class VXM,VC ctrl
  class N1,N2,N3 node
  class DS storage
```
