# CloudIQ — Architecture

<div class="kb-summary">
Cloud-native AIOps SaaS platform hosted by Dell. Receives telemetry from on-premises Dell arrays via the Secure Connect Gateway and produces health scores (0–100), capacity forecasts, and AI-driven recommendations. No on-premises compute required beyond the SCG.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with Dell arrays, Secure Connect Gateway, and REST API.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>SCG redundancy, notification configuration, and API integration practices.</span></a>
</div>

## Supported Platforms

| Platform | Telemetry Source |
|---|---|
| PowerMax / VMAX | Embedded telemetry agent |
| Unity XT | CloudIQ data collection service |
| PowerScale (Isilon) | OneFS embedded agent |
| PowerStore | REST API |
| PowerFlex (VxFlex OS) | SDC telemetry |

## Data Pipeline

```mermaid
graph TB
  ARRAYS["Dell Arrays\nPowerMax · Unity · PowerScale · PowerStore"] -->|"secure telemetry HTTPS"| CLOUDIQ["Dell CloudIQ\n(SaaS analytics)"]
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
