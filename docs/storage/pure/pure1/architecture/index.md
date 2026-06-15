---
tags:
  - architecture
  - pure
---
# Pure1 — Architecture

<div class="kb-summary">
Pure1 is a SaaS monitoring and analytics platform. FlashArray and FlashBlade systems connect directly to Pure1 via outbound HTTPS — no on-premises collector required. Pure1 Meta provides AI-driven capacity forecasting and anomaly detection.

*Applies to: Pure1*
</div>

```text
┌───────────────────────────── Pure1 — SaaS Management and AIOps Platform ──────────────────────────────┐
│                                                                                                       │
│  Pure1 is Pure Storage cloud-hosted SaaS for managing all FlashArrays and FlashBlades;                │
│  AIOps: predictive analytics, capacity forecasting, anomaly detection via Pure1 AI.                   │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │            Platform Architecture             │  │            Analytics Capabilities           │   │
│   │           SaaS: Pure-hosted cloud            │  │             Pure1 AI: ML models             │   │
│   │           All arrays: single pane            │  │          Capacity forecast: 90 days         │   │
│   │          Phone-home: telemetry feed          │  │            Anomaly: vs peer fleet           │   │
│   │           REST API v2: management            │  │          Workload planning advisor          │   │
│   │          Multi-site: cross-DC view           │  │         Proactive: auto support case        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Pure1 is the only management plane; there is no on-prem equivalent management server.                │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Telemetry Collection             │  │             Support Integration             │   │
│   │          Array: phone-home over 443          │  │          SR: auto-open by Pure1 AI          │   │
│   │         No on-prem collector needed          │  │           Case: status in Pure1 UI          │   │
│   │           Logs + metrics + events            │  │           Remote assist: TAM view           │   │
│   │        Historical: 1 year+ retention         │  │           My Pure1: customer login          │   │
│   │          Real-time: 30s granularity          │  │          Role-based: view or manage         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Pure1 is fully SaaS; arrays need TCP 443 outbound to pure1.purestorage.com;                          │
│  no on-prem servers or agents required.                                                               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Pure1          = Pure Storage SaaS management and analytics portal                                   │
│  SaaS           = Software as a Service; Pure hosts it; no on-prem infra needed                       │
│  Phone-home     = array telemetry sent to Pure cloud; enables Pure1 AI analytics                      │
│  Pure1 AI       = ML-based analytics; trained on Pure fleet; detects anomalies                        │
│  Capacity forecast= predicts when arrays will hit threshold; 90-day horizon                           │
│  Anomaly        = Pure1 AI flags unusual performance vs fleet peer comparison                         │
│  Proactive SR   = Pure1 AI opens support case before you notice a problem                             │
│  REST API v2    = Pure1 northbound API; pull metrics, manage arrays programmatically                  │
│  Multi-site     = all arrays across all sites visible in one Pure1 login                              │
│  TAM            = Technical Account Manager; has read-only view of your Pure1                         │
│  My Pure1       = customer-facing login at pure1.purestorage.com                                      │
│  Historical retention= Pure1 keeps 1 year+ of telemetry for trend analysis                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Pure1 Architecture](../../../../assets/pure1-architecture-overview.svg)

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

