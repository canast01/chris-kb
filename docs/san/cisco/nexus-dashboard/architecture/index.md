---
tags:
  - architecture
  - san
---
# Nexus Dashboard — Architecture

<div class="kb-summary">
Cisco Nexus Dashboard is an app-hosting platform for Cisco data centre management. A 3-node or 5-node cluster provides shared identity, multi-site connectivity, and API gateway. NDFC (SAN/LAN), NDI (Insights), and NDO (Orchestrator) run as hosted applications on the cluster.

*Applies to: Cisco MDS · Nexus*
</div>

![Nexus Dashboard — Architecture — Diagram](../../../../assets/san-cisco-nexus-dashboard-architecture-diagram.svg)
![Cisco Nexus Dashboard Architecture](../../../../assets/cisco-nexus-dashboard-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with MDS SAN, ACI, VXLAN, and Nexus fabrics.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Cluster sizing, form factor selection, and multi-site design standards.</span></a>
</div>

```d2
direction: right

center: "Nexus Dashboard" {shape: hexagon}
hosted_applications: "Hosted Applications" {shape: rectangle}
cluster_topology: "Cluster Topology" {shape: rectangle}

center -> hosted_applications
center -> cluster_topology
```

## Hosted Applications

| Application | Abbreviation | Role |
|---|---|---|
| Nexus Dashboard Fabric Controller | NDFC | SAN and LAN fabric management (successor to DCNM) |
| Nexus Dashboard Insights | NDI | Network assurance, anomaly detection, flow telemetry |
| Nexus Dashboard Orchestrator | NDO | Multi-site ACI and VXLAN fabric policy orchestration |

## Cluster Topology

