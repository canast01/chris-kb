---
tags:
  - architecture
  - netapp
---
# InsightIQ — Architecture

<div class="kb-summary">
InsightIQ is an on-premises virtual appliance that collects performance telemetry from PowerScale clusters via the OneFS REST API and stores it in a local PostgreSQL database for historical trend analysis and reporting.

*Applies to: InsightIQ*
</div>

![InsightIQ — Architecture — Diagram](../../../../assets/storage-netapp-insightiq-architecture-diagram.svg)
![InsightIQ Architecture](../../../../assets/insightiq-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Deployment architecture, data collection, retention sizing, network requirements, and HA.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>PowerScale OneFS integration, SIEM forwarding, and email alerting.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing guidelines, naming conventions, and configuration baselines.</span></a>
</div>

---

## Component Roles

| Component | Details |
|---|---|
| InsightIQ VM | OVA (VMware) or Linux installer; hosts collection engine and web dashboard |
| PostgreSQL | Local metrics database on the appliance |
| OneFS data connector | REST API pull from cluster management IP (port 8080) |

---

## Deployment Architecture

