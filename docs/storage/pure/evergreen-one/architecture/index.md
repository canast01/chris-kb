---
tags:
  - architecture
  - pure
---
# Evergreen//One — Architecture

<div class="kb-summary">
Evergreen//One is Pure's Storage-as-a-Service model. Pure owns and manages the hardware on-premises or in colocation. The customer pays for consumed capacity against a committed reserve, with a 99.9999% availability SLA and guaranteed performance tiers.

*Applies to: Evergreen//One*
</div>

```text
┌─────────────────────── Pure Evergreen//One — Storage as a Service Architecture ───────────────────────┐
│                                                                                                       │
│  Pure Storage STaaS: all-NVMe FlashArray delivered to customer DC; Pure manages HW;                   │
│  non-disruptive controller upgrades; consumption billing via Pure1 portal.                            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Service Model                 │  │             Underlying Platform             │   │
│   │         FlashArray in customer rack          │  │          FlashArray //X: block NVMe         │   │
│   │         Pure manages HW + Purity OS          │  │          FlashBlade //S: file + obj         │   │
│   │        Non-disruptive controller swap        │  │          All-NVMe: no spinning disk         │   │
│   │         Customer manages data + VMs          │  │          SafeMode: immutable snaps          │   │
│   │          Subscription: per TB/month          │  │           Pure1: management portal          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Pure guarantees controller upgrades are included; no forklift needed ever.                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              SLA and Guarantees              │  │                  Management                 │   │
│   │          Availability: 99.9999% SLA          │  │              Pure1: SaaS portal             │   │
│   │         Performance: guaranteed IOPS         │  │             REST API: automation            │   │
│   │        Non-disruptive upgrade: always        │  │           Pure Support: proactive           │   │
│   │           Capacity burst: elastic            │  │         Pure1 AI: predictive alerts         │   │
│   │          Energy efficiency included          │  │         MSP option: partner managed         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Pure FlashArray //X or //C in customer rack; FC or iSCSI or NVMe-oF host connections;                │
│  Pure1 cloud portal management; phone-home telemetry over TCP 443 to Pure cloud.                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Evergreen//One = Pure STaaS; hardware in your DC, Pure manages it, you consume it                    │
│  STaaS          = Storage as a Service; pay per TB used, not upfront CapEx                            │
│  Non-disruptive = controller upgrade without IO downtime; Pure guarantee                              │
│  SafeMode       = immutable Snapshot; cannot be deleted even by admin; ransomware                     │
│  Pure1          = Pure SaaS management and analytics portal; all arrays in one view                   │
│  FlashArray //X = Pure block storage array; NVMe; target for Evergreen//One block                     │
│  FlashBlade //S = Pure scale-out file+object; target for Evergreen//One unstructured                  │
│  Purity OS      = Pure storage OS; runs on FlashArray; managed by Pure under contract                 │
│  99.9999% SLA   = six nines; ~32 seconds total downtime per year                                      │
│  Capacity burst = use more than committed; billed at overage rate automatically                       │
│  Proactive support= Pure1 AI detects issues and opens support cases before you do                     │
│  Phone-home     = telemetry from array to Pure cloud; required for managed service                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```mermaid
graph TB
  FA["FlashArray / FlashBlade\n(on-premises)"] -->|"telemetry"| PURE1["Pure1 Cloud\n(subscription management)"]
  PURE1 -->|"capacity orders · firmware · support"| FA
  ADMIN(["Storage Admin"]) -->|"portal"| PURE1
  PURE1 -->|"alerts · forecasting · health score"| ADMIN
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class FA ctrl
  class PURE1 cloud
  class ADMIN host
```
![Evergreen//One Architecture](../../../../assets/evergreen-one-architecture-overview.svg)

Unlike Evergreen//Forever — where the customer owns the subscription and hardware is refreshed in place — Evergreen//One means Pure owns and manages the physical hardware for the duration of the service term.

| Aspect | Evergreen//Forever | Evergreen//One |
|---|---|---|
| Hardware ownership | Customer (subscription) | Pure Storage |
| Capacity model | Fixed entitlement, True Forward annual reconciliation | Monthly consumption against committed reserve |
| Hardware management | Customer-initiated (Pure executes) | Pure-managed, fully transparent |
| Availability SLA | Platform availability + controller refresh guarantee | 99.9999% with performance guarantees |

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>STaaS delivery model, components, HA topology, connectivity, and sizing.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Pure1, vSphere, host connectivity, and monitoring integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Sizing standards, committed reserve guidance, and connectivity requirements.</span></a>
</div>

---

## STaaS Delivery Model


