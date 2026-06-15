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

```text
┌───────────────────────────── Dell FOD — Features on Demand Architecture ──────────────────────────────┐
│                                                                                                       │
│  Software feature licensing for PowerMax; activates SRDF, TimeFinder, and other features              │
│  without hardware changes; license key via ESRS or offline import in Unisphere.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Licensing Model                │  │              Available Features             │   │
│   │         Software-defined activation          │  │        SRDF: synchronous replication        │   │
│   │        License key: term or permanent        │  │         TimeFinder: snapshots+clones        │   │
│   │           ESRS: online validation            │  │          SRDF/Metro: active-active          │   │
│   │         Offline: import license file         │  │           Analytics: AI-based recs          │   │
│   │          No hardware change needed           │  │             Cloud tiering: to S3            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  SRDF and TimeFinder are most commonly licensed via FOD; both need ESRS for validation.               │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Activation Steps               │  │                  FOD vs COD                 │   │
│   │           Order feature from Dell            │  │         FOD: software feature unlock        │   │
│   │          License key sent by email           │  │           COD: raw capacity unlock          │   │
│   │           Unisphere: System → FOD            │  │          Same ESRS channel for both         │   │
│   │         Import key → ESRS validates          │  │          Can combine on same array          │   │
│   │          Feature active in minutes           │  │             Both: PowerMax only             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  PowerMax array (all features physically capable but software-locked);                                │
│  ESRS connectivity to esrs.dell.com on TCP 443 required for online activation.                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  FOD            = Features on Demand; PowerMax software feature licensing                             │
│  SRDF           = Symmetrix Remote Data Facility; PowerMax replication technology                     │
│  TimeFinder     = PowerMax snapshot and clone technology                                              │
│  SRDF/Metro     = synchronous active-active replication; zero RPO Metro stretch                       │
│  ESRS           = EMC Secure Remote Services; Dell license validation channel                         │
│  Unisphere      = PowerMax web management UI; FOD license import location                             │
│  Term license   = time-limited feature license; must be renewed                                       │
│  Permanent license= one-time purchase; no renewal; tied to array serial number                        │
│  COD            = Capacity on Demand; capacity extension (different from FOD)                         │
│  Feature lock   = feature code in array firmware; FOD key unlocks it                                  │
│  Offline import = load license file via USB/SFTP without ESRS connectivity                            │
│  PowerMax       = Dell high-end AFA; only platform supporting FOD                                     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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


