---
tags:
  - troubleshooting
  - cod
  - dell
  - known-issues
---
# Dell COD — Known Issues and Error Codes

<div class="kb-summary">
Dell COD (Capacity on Demand) is a PowerMax capacity licensing model, not a separate software product. Known issues relate to license activation via ESRS and capacity validation.

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


## Before you begin

- COD issues are almost always ESRS connectivity (TCP 443 to esrs.dell.com) or license entitlement mismatch.
- View COD status in Unisphere for PowerMax → System → Capacity On Demand.

## License Activation

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| COD capacity not activating: `ESRS unreachable` | PowerMax | TCP 443 blocked from PowerMax to esrs.dell.com | Open firewall; verify: `curl -sk https://esrs.dell.com` from management network | N/A |
| `COD license limit exceeded` alert | PowerMax | Provisioned capacity exceeds purchased COD tier | Contact Dell to expand COD entitlement; or decommission storage | N/A |
| COD validation fails after ESRS gateway replacement | PowerMax | ESRS gateway not re-registered with PowerMax | Re-register new ESRS gateway in Unisphere → System → ConnectEMC | N/A |

## See also

- [Dell COD — Common Issues](common-issues.md)
- [Dell PowerMax — Known Issues](../../powermax/troubleshooting/known-issues/)
- [Dell FOD — Known Issues](../../fod/troubleshooting/known-issues/)
