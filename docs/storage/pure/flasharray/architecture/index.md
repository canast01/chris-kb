# FlashArray — Architecture

<div class="kb-summary">
Architecture reference for Pure Storage FlashArray. Covers the dual-controller HA model, product lines (//X/C/E), host connectivity protocols (FC, iSCSI, NVMe-oF), Purity data services, ActiveCluster synchronous replication, and design standards.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>HA topology, Purity data services, ActiveCluster, and protection groups.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>VMware, backup tools, Pure1, authentication, and REST API.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, sizing, build baseline, and configuration checklist.</span></a>
</div>

| Model | Flash Type | Target Workload |
|---|---|---|
| FlashArray //X | TLC NVMe | Tier-1 databases, VDI, NVMe/FC or NVMe/RoCE latency-sensitive block |
| FlashArray //C | QLC NVMe | Secondary storage, backup staging, dev/test at lower cost per TB |
| FlashArray //E | High-density QLC | Large-scale consolidation at the lowest $/TB |

All models run Purity//FA OS and share the same dual-controller active-active HA model, CLI, and REST API surface.

```mermaid
graph LR
  H1(["ESXi-01"]) & H2(["ESXi-02"]) --> FabA["FC Fabric A"] & FabB["FC Fabric B"]
  H3(["ESXi-03"]) & H4(["ESXi-04"]) --> FabA & FabB
  FabA & FabB --> FA_A["FlashArray Site A\nCT0 · CT1"]
  FabA & FabB --> FA_B["FlashArray Site B\nCT0 · CT1"]
  FA_A <-->|"ActiveCluster\nsync replication"| FA_B
  FA_A & FA_B -.->|"heartbeat"| MED(["Purity Mediator"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef med fill:#b45309,stroke:#92400e,color:#fff
  class FA_A,FA_B ctrl
  class FabA,FabB net
  class H1,H2,H3,H4 host
  class MED med
```
