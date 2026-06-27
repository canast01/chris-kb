---
tags:
  - architecture
  - san
---
# Brocade Fabric OS — Architecture

<div class="kb-summary">
Fabric OS runs on Brocade/Broadcom FC switches in dual-fabric core-edge topology. Principal switch election, distributed name server, WWN-based zoning, ISL trunks, Virtual Fabrics (FID partitioning), and MAPS health monitoring are the core platform mechanisms.

*Applies to: Brocade FOS 9.x*
</div>

![Brocade Fabric OS — Architecture — Diagram](../../../../assets/san-brocade-fabric-os-architecture-diagram.svg)
![Fabric OS Architecture](../../../../assets/fabric-os-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with SANnav, vCenter, and storage arrays.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Dual-fabric design, zoning model, domain ID, and ISL trunking standards.</span></a>
</div>

## Platform Reference

| Platform | Type | Max Ports | Notes |
|---|---|---|---|
| G620 | Fixed | 64× 32G FC | Mid-range |
| G720 | Fixed | 64× 64G FC | High-performance fixed |
| X7-4 | Director | Up to 192 FC | 4-slot director — dual CP, non-disruptive upgrades |
| X7-8 | Director | Up to 384 FC | 8-slot director — dual CP, non-disruptive upgrades |
| 6510 | Fixed | 48× 16G FC | End-of-sale — plan migration |

## Dual-Fabric Topology

