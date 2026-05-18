# VCF — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware Cloud Foundation. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```
VCF Operations — Day-to-Day Workflow
┌─────────────────────────────────────────────────────┐
│  SDDC Manager UI / API                              │
│  https://sddc-manager.corp.local                    │
└──────┬──────────┬────────────┬──────────────────────┘
       │          │            │
       ▼          ▼            ▼
┌──────────┐ ┌─────────┐ ┌──────────────────────────┐
│ Health   │ │ LCM     │ │ Security                   │
│ Checks   │ │ Upgrades│ │ Passwords · Certs          │
│          │ │         │ │                            │
│ SoS tool │ │ Bundles │ │ SDDC Mgr → Security        │
│ --health │ │ Pre-chk │ │ → Password Management      │
│ -summary │ │ Schedule│ │ → Cert Management          │
└──────────┘ └─────────┘ └──────────────────────────┘
       │          │            │
       ▼          ▼            ▼
┌─────────────────────────────────────────────────────┐
│  Backup & Restore                                   │
│  SDDC Manager (SFTP) → NSX Manager (SFTP)           │
│  → vCenter (FBB/SFTP)                               │
│  Restore order: SDDC Mgr → NSX → vCenter            │
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
