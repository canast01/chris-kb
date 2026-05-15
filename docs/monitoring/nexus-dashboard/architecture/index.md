# Nexus Dashboard — Architecture

<div class="kb-summary">
Nexus Dashboard is a 3- or 5-node Raft-consensus cluster hosting microservice bundles (NDFC, NDI, NDO) that provide unified management and observability across Cisco ACI and NX-OS fabrics.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Cluster architecture, deployment modes, services, ACI/NX-OS integration, and network ports.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>ACI APIC, NX-OS fabrics, multi-site orchestration, and third-party integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Cluster sizing, naming conventions, and configuration baselines.</span></a>
</div>

---

## Cluster Sizing

| Cluster Size | Use Case |
|---|---|
| 3 nodes | Standard production (NDFC or NDI, not both at scale) |
| 5 nodes | HA / multi-service deployment (NDFC + NDI at scale) |
| 1 node | Lab only — not supported for production |

---

## Cluster Architecture

```mermaid
graph TB
  ND["Cisco Nexus Dashboard\n(3-node cluster)"] --> NDFC["NDFC — Fabric Controller"]
  ND --> NDI["ND Insights\ntelemetry · flow analysis"]
  ND --> NDO["ND Orchestrator\nmulti-site ACI"]
  NDFC & NDI & NDO --> FABRICS["Managed Fabrics\nNexus · ACI · MDS"]
  ADMIN(["Network Admin"]) -->|"browser"| ND
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ND ctrl
  class NDFC,NDI,NDO mgmt
  class ADMIN,FABRICS host
```
