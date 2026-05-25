# CloudIQ — Architecture (Monitoring)

<div class="kb-summary">
CloudIQ is a SaaS AIOps platform. The only on-premises component is the Secure Connect Gateway (SCG) virtual appliance, which collects telemetry from Dell arrays and forwards it outbound over HTTPS — no inbound firewall rules required.
</div>

![CloudIQ Architecture](../../../assets/cloudiq-monitoring-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>SaaS architecture, SCG sizing, telemetry collection, data residency, and network requirements.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Supported Dell platforms, ServiceNow, SIEM, and notification integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>SCG deployment standards, naming conventions, and configuration baselines.</span></a>
</div>

---

## Component Roles

| Component | Role |
|---|---|
| CloudIQ Cloud | SaaS platform hosted by Dell — health scores, capacity forecasts, AI recommendations |
| Secure Connect Gateway (SCG) | On-premises OVA; collects telemetry and relays to CloudIQ over HTTPS |
| CloudIQ REST API | Programmatic access to fleet data, alerts, and capacity metrics |

---

## Architecture

```mermaid
graph TB
  ARRAYS["Dell Arrays\nPowerMax · Unity · PowerScale"] -->|"HTTPS outbound via SCG"| CLOUDIQ["Dell CloudIQ\n(SaaS)"]
  CLOUDIQ --> HEALTH["Health Score & Alerts"]
  CLOUDIQ --> CAP["Capacity Forecasting"]
  CLOUDIQ --> REC["AI Recommendations"]
  ADMIN(["IT Admin"]) -->|"web portal"| CLOUDIQ
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAYS ctrl
  class CLOUDIQ,HEALTH,CAP,REC cloud
  class ADMIN host
```
