---
tags:
  - troubleshooting
  - evergreen
  - pure-storage
  - known-issues
---
# Pure Storage Evergreen — Known Issues and Error Codes

<div class="kb-summary">
Evergreen is a commercial subscription program — it has no dedicated software or appliance. All operational known issues are tracked in the underlying array (FlashArray or FlashBlade) known-issues pages. This page covers Evergreen-specific subscription and upgrade process issues.

*Applies to: Evergreen//Forever, Evergreen//Flex*
</div>

```text
┌─────────────────────────────────────────── Pure Evergreen ────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │          Non-disruptive upgrade program — hardware/software refresh with no downtime          │   │
│   │            Protocols: Purity REST API · Pure1 cloud portal · support case workflow            │   │
│   │              Management: Purity UI · Pure1 · Pure support; hardware swap process              │   │
│   │           Upgrade plan -> parts staged -> controller swap -> data migrated -> verify          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           Contract          │  │      Evergreen license      │  │     Per-TiB subscription    │   │
│   │           Hardware          │  │       Controller swap       │  │      Non-disruptive HA      │   │
│   │           Software          │  │       Purity upgrades       │  │     Included in program     │   │
│   │           Capacity          │  │       Entitlement pool      │  │      Flex TiB transfers     │   │
│   │          Monitoring         │  │         Pure1 health        │  │      Capacity + perf AI     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Component     │     Purpose      │      Protocol     │       Auth       │      Notes       │   │
│   │    FlashArray    │  Block storage   │     FC / iSCSI    │   Host zoning    │Evergreen-eligible│   │
│   │    FlashBlade    │File/object array │      NFS / S3     │  Kerberos / S3   │Evergreen-eligible│   │
│   │      Pure1       │   Cloud portal   │     HTTPS 443     │     Pure SSO     │AI/health/license │   │
│   │   Support case   │ Upgrade request  │   Portal / phone  │  Support login   │Parts + SE onsite │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical: existing FlashArray/Blade -> Pure SE arrives -> controller swap -> verify                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Evergreen    = Pure non-disruptive hardware+software upgrade program                                 │
│  Evergreen//One = as-a-service tier; Pure owns hardware, customer pays per TiB                        │
│  Controller swap = replacing array controllers while data stays online (HA pair)                      │
│  Purity       = Pure Storage array OS; upgrades included in Evergreen                                 │
│  Entitlement  = licensed TiB capacity; can move between arrays under a contract                       │
│  Flex model   = pay only for used capacity; scale up/down monthly                                     │
│  Pure1        = cloud management portal; includes upgrade scheduling + AI analytics                   │
│  DirectFlash  = Pure proprietary flash module replacing commodity SSDs                                │
│  DFM          = DirectFlash Module; managed by Purity, not host OS                                    │
│  //S          = Pure Evergreen//S; subscription tier for newer hardware refresh                       │
│  SE           = Solution Engineer; Pure staff member executing upgrade on-site                        │
│  NDU          = Non-Disruptive Upgrade; hardware/software upgrade with 0 host I/O impact              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Before you begin

- Evergreen is a subscription program — all operational port/software issues are tracked against the underlying FlashArray or FlashBlade hardware.
- For controller swap scheduling or upgrade process questions, contact **Pure Storage Customer Success**.

## Upgrade Process Issues

| Error / Symptom | Affected Versions | Cause | Workaround / Fix | Fixed In |
|---|---|---|---|---|
| Controller swap window missed — array shows old controller | Any | Pure scheduling gap; controller not swapped during agreed maintenance window | Contact Pure Customer Success to reschedule controller swap | N/A |
| `Cannot upgrade — Pure1 connectivity required` message | Purity 6.x | Non-disruptive controller upgrade requires active phone-home | Restore Pure1 connectivity (TCP 443 to pure1.purestorage.com); retry upgrade scheduling | N/A |

## See also

- [Pure Storage FlashArray — Known Issues](../../flasharray/troubleshooting/known-issues/)
- [Pure Storage FlashBlade — Known Issues](../../flashblade/troubleshooting/known-issues/)
- [Pure1 — Known Issues](../../pure1/troubleshooting/known-issues/)
