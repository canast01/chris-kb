# Pure Storage Evergreen

<div class="kb-summary">
Pure Storage Evergreen hardware subscription model — non-disruptive controller refreshes, Purity upgrades, and Ever Modern lifecycle for FlashArray and FlashBlade. Covers architecture, operations, security, and troubleshooting.
</div>

```
Evergreen Lifecycle Model
  Customer subscribes ──► capacity + performance tier
          │
          ▼
  FlashArray installed (customer-owned via subscription)
  ├── Purity NDU upgrades ──► non-disruptive, included
  └── Ever Modern (3 yr cycle):
          │
          ▼
  Controller refresh (Pure engineer on-site)
  ├── New controller chassis installed alongside old
  ├── NVMe shelves remain in place (data stays on drives)
  ├── I/O continues during swap (no host disruption)
  └── Old controller removed ──► cycle repeats in ~3 yrs

  Evergreen tiers:
  ├── Evergreen//Forever ─ CapEx purchase + subscription
  ├── Evergreen//Flex    ─ OpEx lease
  └── Evergreen//One    ─ STaaS (Pure owns HW)
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
