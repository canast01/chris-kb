---
tags:
  - architecture
  - dell
---
# APEX Storage as a Service — Architecture

<div class="kb-summary">
Consumption-based STaaS model — Dell owns and manages on-premises PowerStore, PowerScale, or PowerFlex hardware; capacity is metered monthly via the APEX Console with committed and burst tiers.

*Applies to: APEX Storage-as-a-Service*
</div>

![APEX Storage as a Service — Architecture — Diagram](../../../../assets/storage-dell-apex-storage-as-a-service-architecture-diagram.svg)

```mermaid
graph TB
  DELL["Dell Infrastructure\n(owned and managed by Dell)"] --> SCG["Secure Connect Gateway\n(on-premises telemetry relay)"]
  SCG -->|"outbound HTTPS 443"| APEX["APEX Console\n(SaaS — Dell cloud)"]
  APEX --> METER["Usage Metering\n& Billing"]
  APEX --> ALERT["Capacity Alerts\n& Health Reporting"]
  ADMIN(["Customer Admin"]) -->|"web portal / API"| APEX
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class DELL ctrl
  class SCG ctrl
  class APEX,METER,ALERT cloud
  class ADMIN host
```
![APEX STaaS Architecture](../../../../assets/apex-storage-as-a-service-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with APEX Console, Secure Connect Gateway, and REST API.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>SCG redundancy, capacity planning, and subscription management practices.</span></a>
</div>

```d2
direction: right

center: "APEX Storage" {shape: hexagon}
underlying_platforms: "Underlying Platforms" {shape: rectangle}
how_apex_staas_works: "How APEX STaaS Works" {shape: rectangle}

center -> underlying_platforms
center -> how_apex_staas_works
```

## Underlying Platforms

| Platform | Storage Type | Use Case |
|---|---|---|
| PowerStore | Block (NVMe) and file | General-purpose primary storage |
| PowerScale | NAS (scale-out NFS/SMB) | Unstructured data and file workloads |
| PowerFlex | Block (software-defined) | High-performance and Kubernetes workloads |

## How APEX STaaS Works


