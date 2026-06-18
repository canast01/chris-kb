---
tags:
  - troubleshooting
  - fod
  - dell
  - known-issues
---
# Dell FOD — Known Issues and Error Codes

<div class="kb-summary">
Dell FOD (Feature on Demand) is a software feature licensing mechanism for Dell arrays. Known issues relate to license key download, ESRS activation, and feature enablement on array.

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


## Before you begin

- FOD license keys are downloaded from `my.dell.com` or via ESRS.
- Features are enabled in the array management UI (Unisphere / PowerStore Manager) after applying the license key.
- If online activation fails, offline activation is always available via `my.dell.com` → Licensing portal.

## License Activation

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| `Invalid license key` when applying FOD | Any | License key for wrong array serial number | Verify license serial number matches array; regenerate key at `my.dell.com` | N/A |
| ESRS activation fails: `Cannot contact licensing server` | Any | TCP 443 blocked from array to licensing.dell.com | Open firewall; use offline activation from `my.dell.com` as alternative | N/A |
| Feature enabled in UI but not activating | Any | Array requires reboot or service restart after FOD | Follow array-specific FOD activation steps (some features require service restart) | N/A |

## See also

- [Dell FOD — Common Issues](common-issues/)
- [Dell COD — Known Issues](../../cod/troubleshooting/known-issues.md)
- [Dell PowerStore — Known Issues](../../powerstore/troubleshooting/known-issues.md)
