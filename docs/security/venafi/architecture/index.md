---
tags:
  - architecture
  - security
---
# Venafi — Architecture

<div class="kb-summary">
Enterprise certificate lifecycle management — TPP enforces policy, integrates with ADCS and commercial CAs, automates renewal via CA connectors, and provides visibility across all managed certificates; SQL Server-backed HA pair behind a load balancer.

*Applies to: Venafi TLS Protect*
</div>

![Venafi — Architecture — Diagram](../../../assets/security-venafi-architecture-diagram.svg)

![Venafi Architecture](../../../assets/venafi-architecture-overview.svg)

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="how-it-works/">
  <strong>How It Works</strong>
  <span>Policy tree, CA connectors, certificate lifecycle, HA topology, and network requirements.</span>
</a>

<a class="kb-card" href="integrations/">
  <strong>Integrations</strong>
  <span>Integration with other platforms and external systems.</span>
</a>

<a class="kb-card" href="design-standards/">
  <strong>Design Standards</strong>
  <span>Sizing guidelines, design standards, and best practices.</span>
</a>

</div>

## Component Overview

| Component | Role | Deployment |
|---|---|---|
| Policy Server | Lifecycle management, CA integration, policy enforcement | On-prem VM (primary + secondary) |
| Edge Proxy | Certificate discovery across segmented networks | Lightweight on-prem agent |
| Log Server | Audit event aggregation and SIEM forwarding | On-prem VM or syslog target |
| VaaS / TLS Protect Cloud | SaaS alternative to TPP | Hosted by Venafi |
| CA Connectors | Integration adapters for ADCS, DigiCert, Entrust | Configured on Policy Server |
| Venafi SDK / REST API | Automation and integration interface | Consumed by CI/CD and scripts |

## Trust Protection Platform Topology

```mermaid
graph TB
  TPP["Venafi Trust Protection Platform"]
  TPP --> DISC["Discovery Engine\n(network scan / agent)"]
  TPP --> CA1["CA Connector — ADCS"]
  TPP --> CA2["CA Connector — DigiCert / Entrust"]
  TPP --> AUTO["Automation\n(renewal / provisioning)"]
  DISC -->|"found certs"| TPP
  ADMIN(["Security Admin"]) -->|"portal"| TPP
  TPP -->|"SIEM / SNMP"| SIEM(["SIEM / Monitoring"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class TPP,DISC ctrl
  class CA1,CA2,AUTO mgmt
  class ADMIN,SIEM host
```
