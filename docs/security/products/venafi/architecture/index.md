---
tags:
  - architecture
  - security
description: "Enterprise certificate lifecycle management — TPP enforces policy, integrates with ADCS and commercial CAs, automates renewal via CA connectors, and..."
---
# Venafi — Architecture

<div class="kb-summary">
Enterprise certificate lifecycle management — TPP enforces policy, integrates with ADCS and commercial CAs, automates renewal via CA connectors, and provides visibility across all managed certificates; SQL Server-backed HA pair behind a load balancer.

*Applies to: Venafi TLS Protect*
</div>

![Venafi — Architecture — Diagram](../../../../assets/security-venafi-architecture-diagram.svg)

![Venafi Architecture](../../../../assets/venafi-architecture-overview.svg)

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

```d2
direction: right

TPP: "Venafi Trust Protection Platform" {shape: rectangle}
DISC: "Discovery Engine\n(network scan / agent" {shape: rectangle}
CA1: "CA Connector — ADCS" {shape: rectangle}
CA2: "CA Connector — DigiCert / Entrust" {shape: rectangle}
AUTO: "Automation\n(renewal / provisioning" {shape: rectangle}
ADMIN: "Security Admin" {shape: rectangle}
SIEM: "SIEM / Monitoring" {shape: rectangle}

TPP -> DISC
TPP -> CA1
TPP -> CA2
TPP -> AUTO
DISC -> TPP
ADMIN -> TPP
TPP -> SIEM
```
