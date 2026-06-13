---
tags:
  - pure
---
# Pure1 Vendor Support


<div class="kb-summary">
Pure1 Vendor Support reference.
</div>

```text
┌─────────────────────────────────────── Pure1 — Vendor Support ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                      Support Model — Pure Storage Evergreen All-Inclusive                     │   │
│   │           Pure1 included with every FlashArray and FlashBlade Evergreen subscription          │   │
│   │             Auto-cases opened by Pure1 before customer impact; no action required             │   │
│   │            Manual case: support.purestorage.com — 24x7 for Sev-1 production issues            │   │
│   │               Pure1 API support: developer.purestorage.com for API documentation              │   │
│   │            Community: community.purestorage.com — forums, code, and best practices            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Pure cloud hosted · support portal at support.purestorage.com · 24x7 for Sev-1                       │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Evergreen = All-inclusive subscription: support, upgrades, and hardware refresh                      │
│  All-inclusive = No per-incident charges; unlimited cases with Evergreen                              │
│  Auto-case = Pure1 ML opening case proactively; target is zero-touch resolution                       │
│  Severity 1 = Production array down or data unavailable; 24x7 phone response                          │
│  Severity 2 = Performance degraded or component failed; 4-hour response                               │
│  Severity 3 = Non-critical advisory; best-effort response                                             │
│  developer.purestorage.com = API documentation and py-pure-client reference                           │
│  Community = Pure Storage user community; code exchange and troubleshooting tips                      │
│  Pure1 feedback = Feedback link in Pure1 UI for feature requests                                      │
│  TAM = Technical Account Manager; proactive guidance for large Pure fleets                            │
│  Remote assist = Pure engineer accessing array via Pure1 secure tunnel for support                    │
│  Evergreen expiry = Subscription renewal required; Pure1 access may lapse if expired                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
Pure Storage support is accessed via the support portal at support.purestorage.com. Support cases (SRs) can be created directly from Pure1 for array issues, and Pure support engineers can pull remote support bundles (log collections) directly from the array via the Pure1 connection without requiring on-site access.

**Information to collect before opening a case:**

- Array serial number (from Pure1 > Arrays)
- Purity version
- Pure1 alert ID (if alert-related)
- Last-seen timestamp (if telemetry issue)
- Description of symptoms and timeline

| Resource | Detail |
|---|---|
| Support portal | support.purestorage.com |
| SR creation | Via Pure1 dashboard or support portal |
| Remote log pull | Pure support can pull bundles via Pure1 (no on-site needed) |
| SLA tiers | Evergreen//One, Evergreen//Forever (check contract) |
