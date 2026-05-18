# Aria Operations — Operations

```
Aria Operations — Operations Overview
┌─────────────────────────────────────────────────────┐
│  Daily Operations Loop                              │
│                                                     │
│  ┌─────────────┐    ┌─────────────────────────────┐ │
│  │ Health Check│    │  Alert Triage               │ │
│  │             │    │                             │ │
│  │ vracli      │───►│  Alerts → All Alerts        │ │
│  │ cluster     │    │  filter by Critical/Immed.   ││
│  │ health      │    │  → investigate → acknowledge ││
│  └─────────────┘    └─────────────────────────────┘ │
│          │                                          │
│          ▼                                          │
│  ┌─────────────────────────────────────────────┐    │
│  │  Capacity Review (weekly)                   │    │
│  │  Optimize → Capacity Overview               │    │
│  │  → clusters/datastores < 60 days remaining  │    │
│  │  → rightsizing: idle + oversized VMs        │    │
│  └─────────────────────────────────────────────┘    │
│          │                                          │
│          ▼                                          │
│  ┌─────────────────────────────────────────────┐    │
│  │  Lifecycle (upgrades via LCM or in-product) │    │
│  │  Pre-check → snapshot VMs → upgrade nodes  │     │
│  │  data → replica → primary (LCM order)       │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Commands, syntax, and quick reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Routine checks, service validation, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Day-to-day operational tasks and how-to guides.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Installation, upgrade, patching, and decommission.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Backup configuration, restore procedures, and validation.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts and reusable code.</span>
</a>

</div>
