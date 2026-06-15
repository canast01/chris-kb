---
tags:
  - architecture
  - dell
---
# Capacity on Demand — Architecture

<div class="kb-summary">
Software-defined capacity licensing for Dell PowerMax and VMAX arrays. Physical drives are pre-installed at the factory but logically locked until a COD license is applied — activation is instantaneous via SYMCLI or Unisphere with no truck roll required.

*Applies to: Cloud for Desktop (COD)*
</div>

```text
┌───────────────────────────── Dell COD — Capacity on Demand Architecture ──────────────────────────────┐
│                                                                                                       │
│  Software-defined capacity expansion for PowerMax; no hardware shipment needed;                       │
│  activated via ESRS connectivity to Dell cloud; license key unlocks pre-installed capacity.           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Licensing Model                │  │              Activation Process             │   │
│   │      Base capacity: shipped with array       │  │          Order COD units from Dell          │   │
│   │          COD: pre-installed, locked          │  │          License key sent by email          │   │
│   │        Tiers: increments of capacity         │  │           Import in Unisphere: COD          │   │
│   │         Pay: only activated capacity         │  │          ESRS validates entitlement         │   │
│   │        Grace period: 30 days offline         │  │        Capacity available in minutes        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  COD is capacity only; FOD is for software features; both require ESRS connectivity.                  │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               ESRS Integration               │  │                  COD vs FOD                 │   │
│   │       ESRS: call-home to esrs.dell.com       │  │           COD: raw capacity unlock          │   │
│   │          TCP 443 outbound required           │  │           FOD: feature activation           │   │
│   │         ESRS gateway: optional proxy         │  │           Both: same ESRS channel           │   │
│   │         Offline: 30-day grace period         │  │         Both: supported on PowerMax         │   │
│   │         ConnectEMC: legacy ESRS name         │  │           Both: instant activation          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  PowerMax array (all capacity physically installed); ESRS gateway VM optional;                        │
│  management network with internet access to esrs.dell.com on TCP 443.                                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  COD            = Capacity on Demand; pre-installed capacity unlocked by license                      │
│  FOD            = Features on Demand; software feature activation (SRDF, TimeFinder)                  │
│  ESRS           = EMC Secure Remote Services; call-home + license validation channel                  │
│  Unisphere      = PowerMax web management UI; where COD is activated                                  │
│  License key    = alphanumeric string delivered by Dell email after order                             │
│  Capacity tier  = fixed increment of COD capacity available for activation                            │
│  Grace period   = 30 days ESRS offline before COD locks; contact Dell to extend                       │
│  ConnectEMC     = legacy name for ESRS call-home service                                              │
│  ESRS gateway   = optional on-prem VM that proxies array call-home traffic                            │
│  PowerMax       = Dell high-end AFA; COD applies to this platform                                     │
│  Entitlement    = Dell contract record matching license key to serial number                          │
│  esrs.dell.com  = Dell ESRS validation endpoint; TCP 443 must be reachable                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Capacity on Demand Architecture](../../../../assets/cod-architecture-overview.svg)

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

