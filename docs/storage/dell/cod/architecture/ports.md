---
tags:
  - cod
  - dell
  - capacity-on-demand
  - networking
  - firewall
  - ports
---
# Dell COD — Ports and Network Requirements

<div class="kb-summary">
Firewall port reference for Dell COD (Capacity on Demand). COD is a capacity licensing model for PowerMax, not a separate software product. The relevant port is the ESRS/ConnectEMC call-home channel that validates COD entitlements.

*Applies to: Dell PowerMax COD licensing*
</div>

```text
┌────────────────────────────────────────────── Dell CoD ───────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             CoD: Capacity on Demand — pre-installed unlocked via license purchase             │   │
│   │                         Protocols: iSCSI · FC · REST API (activation)                         │   │
│   │                           Management: Unisphere / PowerStore Manager                          │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Storage           │  │          CoD drives         │  │        Pre-installed        │   │
│   │           License           │  │        Activation key       │  │         Unlocks cap.        │   │
│   │           Billing           │  │         Per-TB/month        │  │         Burst model         │   │
│   │           Pooling           │  │        Added to pool        │  │         Near-instant        │   │
│   │            Scope            │  │        Block or File        │  │        Array-specific       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │       Access      │       Auth       │      Notes       │   │
│   │    CoD drives    │ Locked capacity  │      Physical     │       N/A        │  Pre-installed   │   │
│   │   License key    │ Activation code  │  Portal download  │   Entitlement    │   Per array SN   │   │
│   │   Apex billing   │   Subscription   │    Apex Console   │     SAML SSO     │     Monthly      │   │
│   │    Array pool    │   Storage pool   │   Unisphere/PSM   │    RBAC admin    │   Instant add    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Dell array with CoD drives · Apex licensing portal · array management UI                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CoD                = Capacity on Demand; drives installed in factory, unlocked via license key pu  │
│    CoD drive          = physically present but inaccessible NVMe/SAS drive; licensed to activate      │
│    Activation key     = license file from Dell portal; applied in array GUI, CLI, or REST API         │
│    Committed cap.     = baseline permanently licensed capacity; billed monthly without burst          │
│    Burst cap.         = CoD capacity above committed level; billed monthly when accessed              │
│    Apex billing       = subscription model for CoD; consumption-based monthly invoicing via portal    │
│    Pooling            = activated CoD capacity is added to existing storage pool immediately          │
│    Graceful limit     = array serves existing I/O but blocks new allocations at capacity limit        │
│    Reclamation        = returning CoD capacity requires contacting Dell to downgrade the license      │
│    FAST VP            = Fully Automated Storage Tiering; moves data between tiers when CoD is active  │
│    Unisphere          = Dell Unity XT GUI; used to view CoD drive status and apply activation keys    │
│    REST API           = CoD activation via PowerStore REST or Unisphere REST API endpoints            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Call-Home (ESRS) — Required for COD License Validation

| Port | Protocol | Source | Destination | Purpose |
|---|---|---|---|---|
| 443 | TCP | PowerMax array management IP | esrs.dell.com | ESRS — COD license entitlement check and call-home |

## Unisphere Management

| Port | Protocol | Source | Purpose |
|---|---|---|---|
| 8443 | TCP | Admin workstations | Unisphere for PowerMax — view COD capacity status |

## Firewall Summary

| From | To | Ports | Notes |
|---|---|---|---|
| PowerMax mgmt IP | esrs.dell.com | 443 | Required for COD activation and validation |

## See also

- [Dell COD — Architecture](how-it-works/)
- [Dell PowerMax — Ports](../../powermax/architecture/ports/)
- [Dell FOD — Ports](../../fod/architecture/ports/)
