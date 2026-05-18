# ESXi — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware ESXi. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```
ESXi Operational Flow — Day-to-Day
┌─────────────────────────────────────────────────────┐
│  Daily                                              │
│  ├── Health checks (hardware, paths, services)      │
│  ├── Review vCenter alarms and recent tasks         │
│  └── Confirm NTP sync on all hosts                  │
│                                                     │
│  Maintenance Window                                 │
│  ├── Pre: check HA capacity, storage paths, DRS     │
│  ├── Enter maintenance mode → DRS evacuates VMs     │
│  ├── Perform work (patch / hardware / config)       │
│  ├── Exit maintenance mode                          │
│  └── Post: validate host, paths, vSAN, alarms       │
│                                                     │
│  Patch Cycle (quarterly)                            │
│  ├── vLCM: set desired cluster image                │
│  ├── Check Compliance → Remediate host-by-host      │
│  └── Wait 15–30 min between hosts                   │
│                                                     │
│  Incident Response                                  │
│  ├── Host Disconnected → restart hostd / vpxa       │
│  ├── Dead Paths → rescan HBAs, check fabric         │
│  ├── PSOD → collect core dump, open P1 case         │
│  └── High CPU / Memory → esxtop, DRS migrate        │
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
