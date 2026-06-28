---
tags:
  - architecture
  - dell
---
# Flex on Demand — Architecture

<div class="kb-summary">
Consumption-based capacity model on PowerMax, PowerStore, and PowerScale. Additional capacity is pre-installed in the array and metered monthly — billing is based on peak-hour consumption above the committed baseline, not physical installation.

*Applies to: Dell FOD*
</div>

![Flex on Demand — Architecture — Diagram](../../../../assets/storage-dell-fod-architecture-diagram.svg)

```mermaid
graph TB
  ARRAY["Dell Array\nPowerMax / PowerStore / PowerScale"] -->|"telemetry"| SCG["Secure Connect Gateway"]
  SCG -->|"HTTPS 443"| CLOUDIQ["Dell CloudIQ\n(metering & reporting)"]
  CLOUDIQ --> BILL["APEX Console\nMonthly billing"]
  ADMIN(["Storage Admin"]) -->|"portal"| CLOUDIQ
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAY ctrl
  class SCG ctrl
  class CLOUDIQ,BILL cloud
  class ADMIN host
```
![Flex on Demand Architecture](../../../../assets/fod-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with CloudIQ, Secure Connect Gateway, and APEX billing.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Baseline configuration, burst monitoring, and SCG redundancy practices.</span></a>
</div>

## Metering Model

| Tier | Description |
|---|---|
| Committed baseline | Licensed outright — always billed; immediately usable |
| Burst range | Pre-installed; metered monthly at per-TiB rate above baseline |
| Burst ceiling | Maximum metered capacity; over-ceiling usage may incur over-usage charges |

Billing is based on the **maximum capacity used in any single hour** during the billing month (peak-hour metering).

## FOD Data Flow

