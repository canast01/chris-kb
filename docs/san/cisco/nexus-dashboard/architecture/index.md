# Nexus Dashboard — Architecture

<div class="kb-summary">
Cisco Nexus Dashboard is an app-hosting platform for Cisco data centre management. A 3-node or 5-node cluster provides shared identity, multi-site connectivity, and API gateway. NDFC (SAN/LAN), NDI (Insights), and NDO (Orchestrator) run as hosted applications on the cluster.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with MDS SAN, ACI, VXLAN, and Nexus fabrics.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Cluster sizing, form factor selection, and multi-site design standards.</span></a>
</div>

## Hosted Applications

| Application | Abbreviation | Role |
|---|---|---|
| Nexus Dashboard Fabric Controller | NDFC | SAN and LAN fabric management (successor to DCNM) |
| Nexus Dashboard Insights | NDI | Network assurance, anomaly detection, flow telemetry |
| Nexus Dashboard Orchestrator | NDO | Multi-site ACI and VXLAN fabric policy orchestration |

## Cluster Topology

```mermaid
graph TB
  ND["Nexus Dashboard Cluster\n(3 or 5 nodes)"]
  ND --> NDFC["NDFC\n(SAN / LAN management)"]
  ND --> NDI["NDI\n(Insights & anomaly detection)"]
  ND --> NDO["NDO\n(Multi-site orchestration)"]
  NDFC -->|"SSH + SNMP"| MDS["MDS SAN Fabric"]
  NDO --> ACI["ACI / Nexus Fabric"]
  ADMIN(["Cisco Admin"]) -->|"HTTPS"| ND
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ND,NDFC,NDI,NDO ctrl
  class MDS,ACI ctrl
  class ADMIN host
```
