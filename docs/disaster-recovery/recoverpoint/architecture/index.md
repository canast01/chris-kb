# RecoverPoint — Architecture

<div class="kb-summary">
Dell EMC RecoverPoint journal-based replication — RPA clusters intercept writes via splitters and maintain a rolling journal enabling point-in-time recovery across CDP, CRR, and CLR modes.
</div>

![RecoverPoint Architecture](../../../assets/recoverpoint-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>RPA topology, splitter types, consistency groups, journal sizing, and HA model.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>PowerMax, Unity, VPLEX, and RecoverPoint for VMs (RP4VM).</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>CG naming, journal sizing formula, RPO targets, and RPA cluster placement.</span></a>
</div>

| Mode | Description | RPO |
|---|---|---|
| CDP (Continuous Data Protection) | Local journal; recover to any point in time | ~0 seconds |
| CRR (Continuous Remote Replication) | Async replication to DR site | Seconds to minutes |
| CLR (Concurrent Local and Remote) | Simultaneous local CDP + remote CRR | Per-copy |

```mermaid
graph LR
  H_A(["Production Hosts"]) --> STG_A[("Storage A\nProduction LUNs")]
  STG_A -->|"splitter intercepts writes"| RPA1["RPA Cluster\nSite A"]
  RPA1 <-->|"WAN — compressed replication"| RPA2["RPA Cluster\nSite B"]
  RPA2 --> STG_B[("Storage B\nReplica + Journal")]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef dr fill:#be123c,stroke:#9f1239,color:#fff
  classDef store fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class RPA1 ctrl
  class RPA2 dr
  class STG_A,STG_B store
  class H_A host
```
