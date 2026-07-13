---
tags:
  - architecture
  - pure
description: "Pure1 is a SaaS monitoring and analytics platform. FlashArray and FlashBlade systems connect directly to Pure1 via outbound HTTPS — no on-premises..."
---
# Pure1 — Architecture

<div class="kb-summary">
Pure1 is a SaaS monitoring and analytics platform. FlashArray and FlashBlade systems connect directly to Pure1 via outbound HTTPS — no on-premises collector required. Pure1 Meta provides AI-driven capacity forecasting and anomaly detection.

*Applies to: Pure1*
</div>

![Pure1 — Architecture — Diagram](../../../../../assets/storage-pure-pure1-architecture-diagram.svg)
![Pure1 Architecture](../../../../../assets/pure1-architecture-overview.svg)

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

