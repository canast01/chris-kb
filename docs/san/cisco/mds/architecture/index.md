# Cisco MDS — Architecture

<div class="kb-summary">
Cisco MDS 9000 series FC switches running NX-OS. Core isolation mechanism is the VSAN — multiple logical fabrics share physical hardware with separate name servers, zone databases, and domain IDs per VSAN. Directors support ISSU for zero-downtime maintenance.
</div>

![Cisco MDS Architecture](../../../../assets/cisco-mds-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with DCNM/NDFC, storage arrays, and host connectivity.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Dual-fabric design, VSAN allocation, zoning model, and ISL standards.</span></a>
</div>

## Platform Reference

| Model | Type | Max FC Ports | Notes |
|---|---|---|---|
| MDS 9132T | Fixed | 32× 32G FC | Entry/mid-range |
| MDS 9148T | Fixed | 48× 32G FC | Mid-range |
| MDS 9396T | Fixed | 96× 32G FC | High-density fixed |
| MDS 9706 | Director | Up to 384 FC | Modular director — ISSU |
| MDS 9710 | Director | Up to 576 FC | Large-scale director — ISSU |

## Dual-Fabric Topology

```mermaid
graph TB
  H1A(["esxi-01 HBA0"]) --> MDSA["MDS-9710 Director A"]
  H2A(["esxi-02 HBA0"]) --> MDSA
  H1B(["esxi-01 HBA1"]) --> MDSB["MDS-9710 Director B"]
  H2B(["esxi-02 HBA1"]) --> MDSB
  MDSA <-->|"4× 100G ISL"| MDSB
  MDSA --> FA_CT0[("FlashArray CT0")]
  MDSB --> FA_CT1[("FlashArray CT1")]
  classDef switch fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef storage fill:#7c3aed,stroke:#6d28d9,color:#fff
  class MDSA,MDSB switch
  class H1A,H2A,H1B,H2B host
  class FA_CT0,FA_CT1 storage
```
