# vCenter — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware vCenter Server. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```
vCenter Operations Overview
════════════════════════════════════════════════════════

  Day-to-Day Operations Loop
  ┌──────────────────────────────────────────────────┐
  │                                                  │
  │  Monitor          Maintain         Automate      │
  │  ┌──────────┐    ┌──────────┐    ┌──────────┐   │
  │  │ Health   │    │ Backup   │    │ PowerCLI │   │
  │  │ Checks   │───▶│ Restore  │───▶│ Scripts  │   │
  │  │ (daily)  │    │ (daily)  │    │          │   │
  │  └──────────┘    └──────────┘    └──────────┘   │
  │       │                │               │        │
  │       ▼                ▼               ▼        │
  │  ┌──────────┐    ┌──────────┐    ┌──────────┐   │
  │  │ CLI /    │    │ Install  │    │ Incident │   │
  │  │ DCLI     │    │ Upgrade  │    │ Procedures│  │
  │  └──────────┘    └──────────┘    └──────────┘   │
  │                                                  │
  └──────────────────────────────────────────────────┘

  Access Points
  ┌────────────────────────────────────────────────────┐
  │  vSphere Client  https://<vcenter>/ui       :443   │
  │  VAMI            https://<vcenter>:5480     :5480  │
  │  REST API        https://<vcenter>/api      :443   │
  │  PowerCLI        Connect-VIServer ...       :443   │
  │  SSH (VCSA)      ssh root@<vcenter>         :22    │
  └────────────────────────────────────────────────────┘
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
