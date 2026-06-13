---
tags:
  - dell
  - operations
---
# PowerStore — Operations

<div class="kb-summary">
PowerStore day-to-day operations — volume/file provisioning, native replication, snapshots, and host connectivity.

*Applies to: PowerStore 3.x*
</div>

```text
┌───────────────────────────────────── Dell PowerStore Operations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Day-2 ops: snapshot lifecycle, replication monitoring, capacity, CloudIQ health review    │   │
│   │      Snapshots: policy-based volume/group snaps; scheduled or manual; thin pointer model      │   │
│   │     Replication: monitor lag, transfer rate, and RPO gap via PowerStore Manager dashboard     │   │
│   │      pstcli: REST-backed CLI; volume create, snap apply, replication policy, health check     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    CloudIQ alert → PowerStore Manager → check health → pstcli or GUI action → verify                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Snapshot Ops        │  │       Replication Ops       │  │      Health / Capacity      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Snap policy run       │  │        Repl lag check       │  │        CloudIQ score        │   │
│   │         Manual snap         │  │         RPO monitor         │  │        Capacity trend       │   │
│   │         Snap restore        │  │        Failover test        │  │         Drive health        │   │
│   │          Snap clone         │  │          Repl pause         │  │        Dedup savings        │   │
│   │         Snap expire         │  │         Repl resume         │  │         Alert review        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Snap policy schedules → replication RPO check → capacity headroom review → alert clear loop        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │       Tool       │        CLI        │    Frequency     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Health      │     CloudIQ      │   pstcli health   │      Daily       │   Check score    │   │
│   │     Snapshot     │    PS Manager    │    pstcli snap    │    Per policy    │ Verify gen count │   │
│   │   Replication    │    PS Manager    │    pstcli repl    │      Daily       │    RPO check     │   │
│   │     Capacity     │    PS Manager    │  pstcli vol list  │      Weekly      │    Alert >80%    │   │
│                                                                                                       │
│    Physical: SCG appliance or VM phone-home; PowerStore Manager on embedded service processor         │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    CloudIQ score  = Aggregate health score; checks capacity, performance, config, and replication     │
│    pstcli         = PowerStore command-line interface; wraps REST API for scripting                   │
│    Snap policy    = Rule defining snapshot schedule, retention, and naming for a volume/group         │
│    Snap clone     = Writable thin clone created from a snapshot for test/dev use                      │
│    Snap restore   = Revert a volume to a snapshot point-in-time state; overwrites current data        │
│    Repl lag       = Time difference between last replication sync and current; measures RPO gap       │
│    Failover test  = Switch writes to replication target; verify application continues; then fail back │
│    Dedup savings  = Ratio of logical data written to physical consumed; shown in PS Manager           │
│    SCG phone-home = SCG proxy sends appliance telemetry to Dell CloudIQ SaaS platform                 │
│    Volume group   = Logical grouping of volumes; snapped and replicated as consistent set             │
│    Snap expire    = Snapshot past retention date is automatically deleted per policy                  │
│    Drive health   = SSD wear indicator and error count; shown in PowerStore Manager hardware view     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>PowerStore CLI command reference with syntax and examples.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily checks, array health commands, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Change readiness, maintenance windows, and provisioning.</span>
</a>

<a class="kb-card" href="install-upgrade/">
  <strong>Install &amp; Upgrade</strong>
  <span>Software version matrix, upgrade paths, and lifecycle management.</span>
</a>

<a class="kb-card" href="backup-restore/">
  <strong>Backup &amp; Restore</strong>
  <span>Backup procedures and restore workflows.</span>
</a>

<a class="kb-card" href="scripts/">
  <strong>Scripts</strong>
  <span>Automation scripts for health checks and operations.</span>
</a>

</div>

