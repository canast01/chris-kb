# vSAN — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware vSAN. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```
vSAN OPERATIONS OVERVIEW

  Admin / Operator
       │
       ├── vSphere Client (GUI)
       │       └── Cluster → Monitor → vSAN
       │               ├── Health (Skyline Health)
       │               ├── Capacity
       │               ├── Resyncing Objects
       │               └── Performance
       │
       └── CLI / Automation
               │
               ├── PowerCLI (Windows/Linux)
               │       ├── Get-VsanClusterHealthSummary
               │       ├── Get-VsanDiskGroup
               │       ├── Get-VsanSpaceUsage
               │       └── Set-VsanClusterConfiguration
               │
               └── ESXi Shell (SSH)
                       ├── esxcli vsan cluster get
                       ├── esxcli vsan health cluster list
                       ├── esxcli vsan storage list
                       ├── esxcli vsan debug object list
                       ├── esxcli vsan debug resync summary get
                       └── esxcli vsan debug network test
                                │
                                ▼
                       vSAN Cluster Data Plane
                       (DOM / CLOM / LSOM / CMMDS)
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
