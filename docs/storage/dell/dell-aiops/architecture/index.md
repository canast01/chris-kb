---
tags:
  - architecture
  - dell
---
# Dell AIOps — Architecture

<div class="kb-summary">
Dell AIOps is a fully SaaS-delivered AI operations platform. Telemetry flows from arrays through the on-premises Secure Connect Gateway to Dell's cloud AI pipeline, which produces anomaly detection, root cause analysis, and prioritised recommendations.

*Applies to: Dell AIOps*
</div>

![Dell AIOps Architecture](../../../../assets/dell-aiops-architecture-overview.svg)

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

