---
tags:
  - dell
  - operations
---
# RecoverPoint — Operations



<div class="kb-summary">
RecoverPoint day-to-day operations — consistency group management, RPO monitoring, journal sizing, and test failover procedures.
</div>

```text
┌───────────────────────────────── RecoverPoint — Operations Overview ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Operational tasks: monitor CG replication lag, journal usage, RPA health, and link state   │   │
│   │         Daily: verify all CGs are Active/Synchronizing; check journal fill level < 70%        │   │
│   │              Weekly: test copy drill on non-prod CG; review RPO compliance report             │   │
│   │        Access via: RP Management Application (Unisphere for RP), vCenter plugin, or CLI       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Monitoring         │  │        CG Management        │  │         Maintenance         │   │
│   │       Replication lag       │  │        Add/remove VMs       │  │         RPA upgrade         │   │
│   │        Journal fill %       │  │         Set bookmark        │  │       Splitter update       │   │
│   │        RPA CPU/memory       │  │      Enable/disable CG      │  │        Journal resize       │   │
│   │        Link bandwidth       │  │      Change RPO policy      │  │          CG re-sync         │   │
│   │       Alarm dashboard       │  │      Image access test      │  │        Failover drill       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Physical: access Unisphere for RP via browser; RPA management port on dedicated management VLAN    │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Replication lag     = Time between source write and target journal apply; goal < 30 seconds        │
│    Journal fill %      = Percentage of journal VMDK consumed; alert at 70%; critical at 90%           │
│    CG state            = Active, Paused, Error, Initializing, or Transferring; check daily            │
│    Unisphere for RP    = Web GUI for RecoverPoint; manage CGs, view topology, run reports             │
│    Image access test   = Mount a CDP image non-disruptively; validate data integrity without failover │
│    RPO compliance      = Report showing whether actual lag stayed within configured RPO per CG        │
│    Bookmark            = Set before maintenance windows; provides a known-good recovery target        │
│    Re-sync             = After CG pause/error; resynchronises source and target without full rescan   │
│    Failover drill      = Scheduled test of full failover procedure; uses bubble network isolation     │
│    RPA health          = Check CPU, memory, fan, PSU status in Unisphere hardware dashboard           │
│    WAN bandwidth util  = Monitor replication link utilisation; alert if sustained >80% of allocated   │
│    Splitter state      = Verify splitter loaded on each ESXi host; alert if splitter unloaded         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>boxmgmt CLI and REST API command reference.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily checks, RPO compliance, and journal utilization monitoring.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Failover, recovery, maintenance windows, and change readiness.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install & Upgrade</strong>
  <span>Version matrix, upgrade path, and lifecycle planning.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup & Restore</strong>
  <span>Configuration backup and restore procedures.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for health checks, DR tests, and RPO reporting.</span>
</a>

</div>
