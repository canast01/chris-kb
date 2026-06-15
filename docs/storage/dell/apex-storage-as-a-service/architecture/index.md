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

```text
┌─────────────────────── Dell APEX Storage-as-a-Service — Architecture Overview ────────────────────────┐
│                                                                                                       │
│  Consumption-based storage delivered to your data center or AWS; no upfront CapEx;                    │
│  Dell provisions and manages hardware; customer manages data and workloads.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Service Model                 │  │         Underlying Storage Platforms        │   │
│   │          Pay per GB/month consumed           │  │        PowerStore X: block workloads        │   │
│   │           Hardware delivered to DC           │  │          PowerMax: mission-critical         │   │
│   │           No upfront capital cost            │  │          PowerFlex: hyper-converged         │   │
│   │          Dell manages HW lifecycle           │  │           ECS: object storage (S3)          │   │
│   │         Elastic burst: +/- capacity          │  │          PowerScale: scale-out NAS          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Customer retains control of data placement, access, and security policies.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          APEX Console (Management)           │  │              Operational Model              │   │
│   │         Single portal: all services          │  │        Dell: HW monitoring + support        │   │
│   │           REST API for automation            │  │          Customer: VM/app workloads         │   │
│   │           Subscription management            │  │        CloudIQ: performance insights        │   │
│   │            Consumption dashboards            │  │         APEX Observer: on-prem agent        │   │
│   │          Multi-site view: one pane           │  │          SLA: 99.9999% availability         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell-supplied arrays in customer rack; dedicated rack power and cooling by customer;                 │
│  network connectivity to APEX Console via internet (TCP 443); APEX Observer VM on-prem.               │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  APEX           = Dell Storage-as-a-Service brand; on-prem hardware, cloud billing                    │
│  APEX Console   = SaaS management portal for all APEX services; REST API                              │
│  OpEx model     = operational expenditure; no large upfront hardware purchase                         │
│  Commitment period= minimum contract term (1, 3, or 5 years)                                          │
│  Burst capacity = temporary capacity above committed level; billed at higher rate                     │
│  APEX Observer  = on-prem VM that reports telemetry to APEX Console                                   │
│  CloudIQ        = Dell AIOps analytics; integrated with APEX for health scoring                       │
│  PowerStore     = Dell mid-range AFA; common APEX block storage platform                              │
│  PowerMax       = Dell high-end AFA; APEX option for mission-critical block                           │
│  PowerFlex      = Dell hyper-converged / software-defined storage option                              │
│  ECS            = Elastic Cloud Storage; Dell object storage; S3-compatible                           │
│  Elastic scaling= add or reduce committed capacity via APEX Console request                           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

## Underlying Platforms

| Platform | Storage Type | Use Case |
|---|---|---|
| PowerStore | Block (NVMe) and file | General-purpose primary storage |
| PowerScale | NAS (scale-out NFS/SMB) | Unstructured data and file workloads |
| PowerFlex | Block (software-defined) | High-performance and Kubernetes workloads |

## How APEX STaaS Works


