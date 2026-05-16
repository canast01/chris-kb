# Aria Operations — Architecture

<div class="kb-summary">
Analytics cluster for vSphere performance, capacity, and compliance monitoring. Adapters collect metrics from vCenter, NSX, and storage; remote collectors extend reach into remote sites and DMZs without direct cluster connectivity.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with vCenter, NSX, storage, and external monitoring tools.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, adapter configuration, and cluster design best practices.</span></a>
</div>

## Aria Operations Cluster Architecture

![Aria Operations Cluster Architecture](../../../../assets/aria-operations-architecture-overview.svg)

## Node Roles

| Node Role | Description |
|---|---|
| Primary | Hosts the UI, analytics controller, and cluster coordination |
| Primary Replica | Hot standby — automatically promoted if Primary fails |
| Data | Scale-out metric ingestion and storage nodes |
| Remote Collector | Lightweight proxy for remote sites/DMZs; forwards to cluster without joining it |
| Cloud Proxy | SaaS-hosted proxy for VMware Cloud on AWS integrations |

## Component Topology

```mermaid
graph TB
  ADP1["vCenter Adapter"] & ADP2["NSX Adapter"] & ADP3["Storage Adapter"] --> COL["Remote Collector\n(cloud proxy)"]
  COL --> ANAL["Aria Operations\nAnalytics Cluster"]
  ANAL --> DATA[("Metrics Store\nCassandra + GemFire")]
  ANAL --> ALERTS["Alerts · Capacity · Rightsizing"]
  ADMIN(["vSphere Admin"]) -->|"browser"| ANAL
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  class ANAL,COL ctrl
  class DATA store
  class ADP1,ADP2,ADP3,ALERTS mgmt
  class ADMIN host
```
