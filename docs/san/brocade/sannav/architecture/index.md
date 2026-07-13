---
tags:
  - architecture
  - san
description: "Brocade SANnav is a SAN management platform in two variants: Management Portal (per-fabric operations) and Global View (multi-portal aggregation)..."
---
# SANnav — Architecture

<div class="kb-summary">
Brocade SANnav is a SAN management platform in two variants: Management Portal (per-fabric operations) and Global View (multi-portal aggregation). Deployed as Linux virtual appliances; communicates with switches via HTTPS and SNMP v3.

*Applies to: Brocade FOS 9.x*
</div>

![SANnav — Architecture — Diagram](../../../../assets/san-brocade-sannav-architecture-diagram.svg)
![SANnav Architecture](../../../../assets/sannav-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with Brocade FC switches, vCenter, LDAP, and SIEM.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, HA design, and deployment best practices.</span></a>
</div>

## VM Sizing

| Variant | Environment | vCPU | RAM | Storage | Max Switches |
|---|---|---|---|---|---|
| Management Portal | Small | 8 | 32 GB | 300 GB | 50 |
| Management Portal | Medium | 16 | 64 GB | 500 GB | 150 |
| Management Portal | Large | 24 | 96 GB | 1 TB | 300 |
| Global View | Standard | 8 | 32 GB | 500 GB | 10 portals |

## Management Topology

