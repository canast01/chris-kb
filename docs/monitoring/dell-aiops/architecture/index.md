# Dell AIOps — Architecture

<div class="kb-summary">
Dell AIOps is a fully SaaS-delivered AI operations platform. Telemetry flows from arrays through the on-premises Secure Connect Gateway to Dell's cloud AI pipeline, which produces anomaly detection, root cause analysis, and prioritised recommendations.
</div>

![Dell AIOps Architecture](../../../assets/dell-aiops-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>SaaS architecture, AI capabilities, telemetry sources, data flow, and component roles.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>CloudIQ integration, notification channels, and supported Dell platforms.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Deployment standards, naming conventions, and configuration baselines.</span></a>
</div>

---

## Component Roles

| Component | Role |
|---|---|
| CloudIQ / APEX Console | SaaS portal — recommendations, anomaly dashboard, health scores |
| Secure Connect Gateway (SCG) | On-premises telemetry collection and forwarding (customer-managed) |
| Dell AI Pipeline | Anomaly detection, RCA, and capacity forecasting (Dell-managed cloud) |

---

## Architecture

```mermaid
graph TB
  ARRAYS["Dell Storage Arrays\n(telemetry streams)"] --> AIOPS["Dell AIOps\n(AI analytics engine)"]
  AIOPS --> ANOM["Anomaly Detection"]
  AIOPS --> PRED["Predictive Insights"]
  AIOPS --> RECS["Actionable Recommendations"]
  ADMIN(["Storage Team"]) -->|"dashboard"| AIOPS
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAYS ctrl
  class AIOPS,ANOM,PRED,RECS cloud
  class ADMIN host
```
