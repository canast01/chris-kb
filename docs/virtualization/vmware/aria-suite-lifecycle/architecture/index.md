---
tags:
  - architecture
  - aria-lcm
  - vmware
---
# Aria Suite Lifecycle — Architecture

<div class="kb-summary">
Central management appliance for deploying and upgrading the full VMware Aria Suite. Orchestrates pre-check → snapshot → stage → upgrade → post-check as a single audited workflow; stores all credentials and certificates in the integrated Locker vault.

*Applies to: Aria Suite Lifecycle 8.x*
</div>

```text
┌────────────────────── Aria Suite Lifecycle — Orchestrated Lifecycle Management ───────────────────────┐
│                                                                                                       │
│  Central appliance for deploying and upgrading Aria Suite; orchestrates pre-check                     │
│  -> snapshot -> stage -> upgrade -> post-check; Locker vault for creds/certs.                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               LCM Architecture               │  │               Upgrade Workflow              │   │
│   │         Single management appliance          │  │          Pre-check: compat + health         │   │
│   │          Locker: creds + cert vault          │  │           Snapshot: rollback point          │   │
│   │          Binary repo: local or CDN           │  │           Stage: download + verify          │   │
│   │           PostgreSQL: LCM database           │  │         Upgrade: rolling per product        │   │
│   │          Request tracker: audit log          │  │         Post-check: health validate         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Order: IDM -> vRSLCM -> Aria Ops -> Aria Logs -> Aria Automation (dependency order).                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Managed Products               │  │                 Locker Vault                │   │
│   │               Aria Operations                │  │         Passwords: product accounts         │   │
│   │           Aria Operations for Logs           │  │        Certificates: PEM format store       │   │
│   │               Aria Automation                │  │          Licenses: per-product keys         │   │
│   │         Aria Operations for Networks         │  │         Passwords: rotate via LCM UI        │   │
│   │            Identity Manager (IDM)            │  │          Cert renewal: LCM-managed          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Photon OS appliance (Aria LCM VM); vCenter access for snapshot operations;                           │
│  HTTPS to VMware CDN or local binary repo for downloading product binaries.                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  LCM           = Aria Suite Lifecycle Manager; formerly vRSLCM                                        │
│  Locker        = integrated credential/cert/license vault in LCM                                      │
│  Environment   = logical grouping of Aria products managed as a unit                                  │
│  Binary repo   = product installer repository; local NFS or CDN                                       │
│  Pre-check     = compatibility matrix validation before upgrade starts                                │
│  Stage         = download binary + verify checksum before maintenance                                 │
│  Snapshot      = VM snapshot before upgrade; rollback if upgrade fails                                │
│  Post-check    = health validation; services up and APIs responding                                   │
│  IDM           = Identity Manager; must be upgraded before other products                             │
│  Request       = LCM async task; each upgrade is a tracked request                                    │
│  Audit log     = LCM request history; shows who ran what upgrade when                                 │
│  Rolling       = upgrades one product node at a time within a product                                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Aria Suite Lifecycle Architecture](../../../../assets/aria-suite-lifecycle-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with vCenter, VIDM, NFS, and managed Aria products.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Pre-requisite checklist, upgrade sequencing, and DNS/NTP requirements.</span></a>
</div>

```d2
direction: right

center: "Aria Suite Lifecycle" {shape: hexagon}
core_components: "Core Components" {shape: rectangle}

center -> core_components
```

## Core Components

| Component | Role |
|---|---|
| LCM Appliance | Central orchestration, UI, REST API, Locker vault |
| Workspace ONE Access (VIDM) | Identity provider and SSO for all Aria products |
| vRealize Easy Installer | Bootstrap ISO for initial multi-product deployment |
| NFS Share | Binary repository (`.pak` files) and snapshot storage |
| NTP Server | Time synchronisation — mandatory; certificate operations fail on >5 s skew |
| DNS | Forward + reverse resolution required for every node FQDN |

