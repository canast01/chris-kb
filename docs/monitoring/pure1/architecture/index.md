# Pure1 — Architecture

<div class="kb-summary">
Pure1 is a SaaS monitoring and analytics platform. FlashArray and FlashBlade systems connect directly to Pure1 via outbound HTTPS — no on-premises collector required. Pure1 Meta provides AI-driven capacity forecasting and anomaly detection.
</div>

![Pure1 Architecture](../../../assets/pure1-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>SaaS architecture, telemetry collection, Pure1 Meta AI, data retention, and network requirements.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>REST API, support integration, and third-party platform connections.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Array onboarding standards, naming conventions, and configuration baselines.</span></a>
</div>

---

## Component Roles

| Component | Role |
|---|---|
| Pure1 Cloud | SaaS platform — health, capacity, performance, alerts, REST API |
| Array Purity OS | Generates and uploads telemetry to Pure1 via outbound HTTPS |
| Pure1 Meta | AI/ML engine — workload analytics, anomaly detection, capacity forecasting |

---

## Architecture

```mermaid
graph TB
  FA["FlashArray / FlashBlade\n(on-premises)"] -->|"telemetry HTTPS"| PURE1["Pure1 Cloud\n(SaaS)"]
  PURE1 --> HEALTH["Health Score & Alerts"]
  PURE1 --> CAP["Capacity Forecasting"]
  PURE1 --> PERF["Performance Analytics"]
  PURE1 --> SUP["Support Integration"]
  ADMIN(["Storage Admin"]) -->|"browser / mobile"| PURE1
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class FA ctrl
  class PURE1,HEALTH,CAP,PERF,SUP cloud
  class ADMIN host
```
