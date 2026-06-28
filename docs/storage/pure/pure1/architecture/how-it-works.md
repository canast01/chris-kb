---
tags:
  - architecture
  - pure
---
# Pure1 — How It Works

<div class="kb-summary">
How It Works reference covering Architecture, High Availability.

*Applies to: Pure1*
</div>
![Pure1 — How It Works](../../../../assets/storage-pure-pure1-architecture-how-it-works.svg)

Pure1 is Pure Storage's cloud-based management and analytics platform for FlashArray and FlashBlade systems. It requires no on-premises management infrastructure — each array connects to Pure1 directly via outbound HTTPS. Pure1 provides AI-driven analytics (Pure1 Meta), capacity forecasting, health scoring, and a REST API for programmatic fleet management.

---

```plantuml
@startuml
skinparam sequenceArrowThickness 1.5
skinparam roundcorner 5

participant "FlashArray /\nFlashBlade" as ARR
participant "Pure1 Cloud\nGateway (array-side)" as GW
participant "Pure1 SaaS\n(cloud.purestorage.com)" as P1
participant "AI Engine\n(Pure1 Meta)" as AI
actor "Admin" as ADM

ARR -> GW: Telemetry (metrics / logs / config)
GW -> P1: Encrypted upload (REST HTTPS)
P1 -> AI: Capacity + workload analysis
AI --> P1: Forecast + anomaly
P1 --> ADM: Dashboard + proactive alert
ADM -> P1: Open support case
P1 -> ARR: Remote assist session (Pure1 Connect)
@enduml
```

## Architecture

```mermaid
graph LR
    Arrays["FlashArray / FlashBlade<br/>Purity OS phonehome<br/>every 30 seconds<br/>HTTPS outbound"]
    Pure1Cloud["Pure1 Cloud Platform<br/>SaaS · Pure-managed<br/>time-series DB<br/>full resolution storage"]
    Meta["Pure1 Meta (AI)<br/>ML health scoring<br/>workload classification<br/>capacity forecasting"]
    Dashboard["Pure1 Dashboard<br/>fleet management<br/>health scores · alerts<br/>capacity trends"]
    TAC["Pure Storage TAC<br/>auto case creation<br/>proactive swap<br/>zero-touch resolution"]

    Arrays -->|"phonehome telemetry HTTPS"| Pure1Cloud
    Pure1Cloud -->|"metrics ingest"| Meta
    Meta -->|"health scores · alerts"| Dashboard
    Meta -->|"pre-failure detection"| TAC
    TAC -->|"auto case + diagnostics"| Dashboard

    style Arrays fill:#2563eb,stroke:#1d4ed8,color:#fff
    style Pure1Cloud fill:#7c3aed,stroke:#6d28d9,color:#fff
    style Meta fill:#b45309,stroke:#92400e,color:#fff
    style Dashboard fill:#15803d,stroke:#166534,color:#fff
    style TAC fill:#15803d,stroke:#166534,color:#fff
```

---

## High Availability

Pure1 is managed entirely by Pure Storage as a SaaS platform. Availability SLA and disaster recovery are Pure Storage's responsibility. Customer action is not required for Pure1 infrastructure HA.

---

## See also

- [Pure1 — Design Standards](../design-standards/)
- [Pure1 — Integrations](../integrations/)
- [Pure1 — Deploy](../../deploy/)
