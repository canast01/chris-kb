# Pure Storage Evergreen

<div class="kb-summary">
Pure Storage Evergreen hardware subscription model — non-disruptive controller refreshes, Purity upgrades, and Ever Modern lifecycle for FlashArray and FlashBlade. Covers architecture, operations, security, and troubleshooting.
</div>

```text
┌─────────────────────────────────────── Pure Evergreen Program ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │               Pure Evergreen — Hardware Subscription + Non-Disruptive Lifecycle               │   │
│   │    Ever Modern: periodic controller refresh with zero downtime — no forklift upgrades, ever   │   │
│   │  Purity upgrades: OS updates delivered non-disruptively on same hardware via Pure1 scheduling │   │
│   │ Subscription tiers: Evergreen//Forever (purchased) · Evergreen//One (STaaS) · Evergreen//Flex │   │
│   │   Controller refresh: new CT shipped, slide-in swap; no data migration, no reformat required  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Evergreen covers the full lifecycle: architecture, operations, refresh, security, and              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Architecture        │  │          Operations         │  │          Lifecycle          │   │
│   │   Subscription model: NDU   │  │   Purity upgrade: schedule  │  │    Version matrix: FA/FB    │   │
│   │  Controller: slide-in swap  │  │   Controller refresh prep   │  │  EOL tracking: model dates  │   │
│   │  Flash: add shelf/blade NDU │  │  Pre-check: health + alerts │  │  Refresh planning: timeline │   │
│   │   Evergreen//Forever model  │  │   Post-val: array + hosts   │  │   Upgrade path: hop rules   │   │
│   │ Pure1: lifecycle visibility │  │   Security: baseline check  │  │  Compatibility matrix check │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Architecture defines the subscription model · Operations execute upgrades                          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  Common Issues   │   Diagnostics    │   Health Checks   │    Escalation    │  CLI Quick Ref   │   │
│   │  Upgrade fails   │  purearray get   │   SW version OK?  │  Case: upgrade   │  purearray get   │   │
│   │  CT swap issues  │ purelog download │  Drive health OK  │  TAM escalation  │  purearray list  │   │
│   │Host I/O during ND│puresupport bundle│  Pre-check: pass? │  Remote assist   │ purevolume list  │   │
│   │Repl: pause+resume│ netconfig verify │   Post-val: vols  │  P1/P2 severity  │  pureport list   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  FlashArray controllers (CT0/CT1) · NVMe flash shelves · FC/iSCSI/NVMe HBAs · SAN switches · Power    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Evergreen      = Pure hardware + software subscription model; replaces forklift upgrade cycle        │
│  NDU            = Non-Disruptive Upgrade; Purity OS updates applied with zero downtime to hosts       │
│  Ever Modern    = Controller refresh entitlement; new CT0/CT1 shipped and swapped non-disruptively    │
│  Purity upgrade = Operating system upgrade applied to FlashArray or FlashBlade via Pure1 schedule     │
│  Evergreen//Forever = Purchased subscription; hardware refresh rights included; perpetual entitlement │
│  Evergreen//One = STaaS tier; Pure-owned hardware, consumption billing, 99.9999% SLA guaranteed       │
│  Evergreen//Flex= Flex subscription; capacity can scale up or down; usage-based billing model         │
│  Controller swap= Physical CT replacement; slides in while array stays online serving I/O             │
│  EOL            = End of Life; model or Purity version reaching end of support/maintenance            │
│  Hop limit      = Maximum Purity version jump in one upgrade step; check compatibility matrix         │
│  Pre-check      = Automated or manual health validation before starting controller or Purity upgrade  │
│  Pure1          = Cloud portal that schedules and monitors Evergreen upgrades and refresh events      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, integrations, and design standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>Health checks, procedures, install, upgrade, and runbooks.</span>
</a>

<a class="kb-card" href="lifecycle/">
  <strong>Lifecycle</strong>
  <span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostic commands, log locations, and error codes.</span>
</a>

<a class="kb-card" href="controller-upgrades/">
  <strong>Controller Upgrades</strong>
  <span>Ever Modern refresh procedures, pre-checks, and validation steps.</span>
</a>

</div>
