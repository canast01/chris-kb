# InsightIQ — Architecture

<div class="kb-summary">
InsightIQ is an on-premises virtual appliance that collects performance telemetry from PowerScale clusters via the OneFS REST API and stores it in a local PostgreSQL database for historical trend analysis and reporting.
</div>

![InsightIQ Architecture](../../../assets/insightiq-architecture-overview.svg)

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

```mermaid
graph TB
  PS["PowerScale Cluster\n(OneFS API)"] -->|"performance telemetry"| IIQ["InsightIQ Server\n(analytics VM)"]
  IIQ --> PERF["Performance Dashboards"]
  IIQ --> CAP["Capacity Trending"]
  IIQ --> REP["Scheduled Reports"]
  ADMIN(["Storage Admin"]) -->|"browser"| IIQ
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class PS ctrl
  class IIQ,PERF,CAP,REP cloud
  class ADMIN host
```
