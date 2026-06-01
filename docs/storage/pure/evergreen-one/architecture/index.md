# Evergreen//One — Architecture

<div class="kb-summary">
Evergreen//One is Pure's Storage-as-a-Service model. Pure owns and manages the hardware on-premises or in colocation. The customer pays for consumed capacity against a committed reserve, with a 99.9999% availability SLA and guaranteed performance tiers.
</div>
```text
┌───────────────────────────────── Pure Evergreen//ONE — Architecture ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ Evergreen//ONE architecture overview: Storage as a Service subscription delivered on Pure Fla │   │
│   │                        Protocols: FC · iSCSI · NVMe-oF · NFS · SMB · S3                       │   │
│   │              Key components: Pure1 SaaS, FlashArray, FlashBlade, Hardware refresh             │   │
│   │          Design principles: HA, scalability, non-disruptive operations, and security          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Design → deploy → configure → validate → monitor → optimise                                        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Hardware          │  │         On-prem Pure        │  │          Pure-owned         │   │
│   │           Billing           │  │        Committed TiB        │  │         Monthly sub.        │   │
│   │           Refresh           │  │        Non-disruptive       │  │        Pure delivers        │   │
│   │          Management         │  │          Pure1 SaaS         │  │         AI analytics        │   │
│   │           Support           │  │        24x7 proactive       │  │          AI-driven          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │      Pure1       │   SaaS portal    │       HTTPS       │     SSO/SAML     │   AI analytics   │   │
│   │    FlashArray    │    Block/file    │    FC/iSCSI/NFS   │  CHAP/Kerberos   │     All-NVMe     │   │
│   │    FlashBlade    │   File/object    │     NFS/SMB/S3    │   Kerberos/IAM   │   Parallel I/O   │   │
│   │  ActiveCluster   │ Sync replication │    Internal RPC   │   Certificate    │     Zero RPO     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Pure FlashArray or FlashBlade on-prem (Pure-owned) · Pure1 cloud · WAN to Pure           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Evergreen//ONE     = Pure STaaS; Pure-owned hardware on customer premises with subscription billing│
│    Pure1              = Pure Storage cloud management portal; AI-based analytics and capacity planning│
│    Non-disruptive upgrade = hardware upgrade without host I/O interruption; Pure handles logistics    │
│    Committed TiB      = minimum subscribed capacity; billed monthly regardless of actual usage        │
│    Burst capacity     = additional capacity above commitment; no pre-ordering; billed as consumed     │
│    Hardware refresh   = Pure delivers and installs new controllers and shelves on 3-year cadence      │
│    Purity//FA         = FlashArray OS; unified block and file with NVMe-native architecture           │
│    Purity//FB         = FlashBlade OS; object and file storage with massive parallel throughput       │
│    AI copilot         = Pure1 AI feature; recommends workload placement and anomaly remediation       │
│    TaaS               = Technology as a Service; hardware ownership stays with Pure throughout subs...│
│    ActiveCluster      = sync stretch replication included; ActiveDR async replication optional        │
│    SAML SSO           = Pure1 supports SAML 2.0; identity provider integrates with corporate IdP      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
