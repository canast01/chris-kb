---
tags:
  - fod
  - dell
  - feature-on-demand
  - networking
  - firewall
  - ports
---
# Dell FOD — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell FOD (Feature on Demand). FOD enables software features on Dell arrays via license keys downloaded from Dell or activated via ESRS. Port requirements are the same as call-home / ESRS.

*Applies to: Dell FOD for PowerStore, PowerMax, Unity*
</div>

```text
┌────────────────────────────────────────────── Dell FoD ───────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │              FoD: Feature on Demand — software features unlocked via license keys             │   │
│   │               Protocols: REST API · HTTPS (license portal) · array management UI              │   │
│   │                          Management: Dell License Manager / array CLI                         │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │         License type        │  │        Permanent/Term       │  │       Feature-specific      │   │
│   │          Activation         │  │         Key → array         │  │        Instant unlock       │   │
│   │            Scope            │  │         Per-array SN        │  │       Non-transferable      │   │
│   │           Features          │  │       Replication/Tier      │  │       Product-defined       │   │
│   │            Audit            │  │        License report       │  │          Compliance         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │       Access      │       Auth       │      Notes       │   │
│   │   FoD license    │  Feature unlock  │  Portal download  │   Entitlement    │   Array-bound    │   │
│   │  License portal  │  Purchase/track  │       HTTPS       │    SSO login     │ licensing.dell.  │   │
│   │  Array firmware  │ FoD enforcement  │     Array mgmt    │    Admin role    │  Validates key   │   │
│   │   Audit report   │ Compliance check │     DDMC/array    │    Read-only     │  Monthly review  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell array with FoD-capable firmware · Dell licensing portal · array management          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    FoD                = Feature on Demand; software capabilities locked in firmware, unlocked by lic  │
│    License key        = alphanumeric string generated at purchase; applied via GUI, CLI, or REST API  │
│    Permanent license  = perpetual feature unlock; tied to specific array serial number                │
│    Term license       = time-limited feature unlock; expires unless renewed through Dell portal       │
│    Entitlement        = purchased right to use a feature; tracked in Dell software licensing portal   │
│    License transfer   = FoD licenses are non-transferable between different array serial numbers      │
│    Replication FoD    = unlocks synchronous or asynchronous array replication features                │
│    Tier FoD           = unlocks FAST VP or cloud tiering between performance and capacity tiers       │
│    License audit      = periodic reconciliation of active features versus licensed entitlements       │
│    LicenseManager     = Dell tool for bulk license management across multiple array systems           │
│    Array serial       = unique array identifier; FoD licenses are cryptographically bound to it       │
│    FoD portal         = licensing.dell.com; purchase, download, and track all FoD license keys        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Feature Activation (ESRS / Dell Support Portal)

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | Array management IP | esrs.dell.com, licensing.dell.com | FOD license key validation and download |
| 443 | TCP | Admin workstation | my.dell.com | Admin downloads license key from Dell portal |

## Array Management UI (License Activation)

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 443 | TCP | Admin workstations | Unisphere / PowerStore Manager — apply FOD license |
| 8443 | TCP | Admin workstations | Unisphere for PowerMax — apply FOD license |

## Firewall Summary

| From | To | Ports | Notes |
|---|---|---|---|
| Array mgmt IP | esrs.dell.com | 443 | License key pull from Dell |
| Admin workstation | my.dell.com | 443 | Portal download (optional — can transfer offline) |

## See also

- [Dell FOD — Architecture](how-it-works/)
- [Dell COD — Ports](../../cod/architecture/ports.md)
- [Dell PowerStore — Ports](../../powerstore/architecture/ports.md)
