# Aria Operations — Architecture (Monitoring)

<div class="kb-summary">
Aria Operations deploys as an analytics cluster (Primary + Replica + optional Data Nodes) with Remote Collectors distributing telemetry collection across sites. Management Packs extend coverage to third-party platforms.
</div>

![Aria Operations Architecture](../../../assets/aria-operations-monitoring-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Analytics cluster topology, component roles, sizing, Remote Collectors, and network ports.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Management packs, vCenter, NSX, storage adapters, and third-party integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Cluster sizing guidelines, naming conventions, and configuration baselines.</span></a>
</div>

---

## Deployment Sizing

| Deployment Size | Nodes | Use Case |
|---|---|---|
| Small (xSmall) | 1 node | Lab / proof-of-concept |
| Medium | Primary + Replica | Up to ~3,000 VMs |
| Large | Primary + Replica + 2–4 Data Nodes | Up to ~10,000 VMs |
| Extra Large | Primary + Replica + 4+ Data Nodes | Enterprise fleet |

---

## Analytics Cluster Topology

```mermaid
graph TB
  ADP1["vCenter Adapter"] & ADP2["NSX Adapter"] & ADP3["Third-party Adapters"] --> COL["Remote Collector"]
  COL --> ANAL["Analytics Cluster\n(Primary + Replica + Data Nodes)"]
  ANAL --> DATA[("Metrics Store")]
  ANAL --> ALERTS["Alert Engine\nCapacity · Compliance"]
  ADMIN(["Admin"]) -->|"browser"| ANAL
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class ANAL,COL ctrl
  class DATA store
  class ADP1,ADP2,ADP3,ALERTS mgmt
```
