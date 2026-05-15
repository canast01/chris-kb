# Capacity on Demand — Architecture

<div class="kb-summary">
Software-defined capacity licensing for Dell PowerMax and VMAX arrays. Physical drives are pre-installed at the factory but logically locked until a COD license is applied — activation is instantaneous via SYMCLI or Unisphere with no truck roll required.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with PowerMax, Unisphere, SYMCLI, and Dell License Portal.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>COD activation workflow, DR site pre-install patterns, and license management.</span></a>
</div>

## Capacity States

| State | Description |
|---|---|
| Active capacity | Licensed and immediately allocatable to thin pools and storage groups |
| COD reserved capacity | Physically installed; logically locked — visible in hardware inventory but not allocatable |
| Activated COD | Former reserved capacity after license applied — instantly joins the active pool |

## COD Model

```mermaid
graph LR
  ARRAY["Dell Array\nPowerMax\n(on-premises)"] <-->|"license activation"| APEX["Dell APEX\nCloud Console"]
  ADMIN(["Storage Admin"]) -->|"portal / SYMCLI"| APEX
  APEX --> BILL["Usage-based Billing\n& Reporting"]
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class ARRAY ctrl
  class APEX,BILL cloud
  class ADMIN host
```
