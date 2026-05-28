# Virtualization Health Checks

Reusable health checks for virtualization operations.

```text
Health Check Flows
═══════════════════════════════════════════════════════════

  DAILY (every morning, ~15 min)
  ┌──────────────────────────────────────────────────────┐
  │ vCenter alarms → Host status → vSAN health →        │
  │ Datastore space → VM state → Backup status           │
  └──────────────────────────────────────────────────────┘

  PRE-CHANGE (before any maintenance)
  ┌──────────────────────────────────────────────────────┐
  │ vCenter health → Active alarms → vSAN status →      │
  │ Snapshot count → Storage paths → Backup confirmed   │
  └──────────────────────────────────────────────────────┘

  POST-CHANGE (within 5 min of completion)
  ┌──────────────────────────────────────────────────────┐
  │ Host connectivity → HA/DRS → VM state →             │
  │ Datastore access → Monitoring → App owner sign-off  │
  └──────────────────────────────────────────────────────┘

  ALERT REVIEW (daily or on-demand)
  ┌─────────────┐   ┌─────────────┐   ┌──────────────┐
  │   vCenter   │   │    Aria     │   │   Pure1 /    │
  │   Alarms    │   │  Operations │   │   iDRAC      │
  └──────┬──────┘   └──────┬──────┘   └──────┬───────┘
         └─────────────────┼─────────────────┘
                           ▼
                  ┌────────────────┐
                  │ Priority Triage│
                  │ Assign owners  │
                  │ Escalate P1/P2 │
                  └────────────────┘
```
┌──────────────────────────────────── Virtualization Health Checks ─────────────────────────────────────┐
│                                                                                                       │
│    Structured checks across daily operations, capacity planning, and change management                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Daily (~15 min)       │  │      Capacity (weekly)      │  │      Pre / Post Change      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        vCenter alarms       │  │       CPU < 70% target      │  │        Alarms cleared       │   │
│   │      Host connectivity      │  │       RAM balloon = 0       │  │         vSAN healthy        │   │
│   │         vSAN health         │  │        Storage < 80%        │  │       Snapshots clear       │   │
│   │       Datastore space       │  │       Growth trend OK       │  │      Backups confirmed      │   │
│   │        VM state check       │  │       Forecast 90 days      │  │        HA/DRS active        │   │
│   │        Backup status        │  │       Licence headroom      │  │      App owner sign-off     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    HA         = High Availability; restarts VMs on surviving hosts when a host fails                  │
│    DRS        = Distributed Resource Scheduler; balances VM load across cluster hosts                 │
│    vSAN       = VMware hyper-converged storage; health = no resync, no degraded objects               │
│    Balloon    = VMware memory reclaim driver; non-zero = host under memory pressure                   │
│    Swap       = VM disk-based memory swap; non-zero = critical memory shortage on host                │
│    Datastore  = Storage volume presented to ESXi; monitor used % and provisioning ratio               │
│    VAMI       = vCenter Appliance Management Interface; port 5480; cert and patch mgmt                │
│    Alarm      = vCenter triggered alert; P1=red critical, P2=yellow warning, P3=info                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
┌──────────────────────────────────── Virtualization Health Checks ─────────────────────────────────────┐
│                                                                                                       │
│    Structured checks across daily operations, capacity planning, and change management                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Daily (~15 min)       │  │      Capacity (weekly)      │  │      Pre / Post Change      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │        vCenter alarms       │  │       CPU < 70% target      │  │        Alarms cleared       │   │
│   │      Host connectivity      │  │       RAM balloon = 0       │  │         vSAN healthy        │   │
│   │         vSAN health         │  │        Storage < 80%        │  │       Snapshots clear       │   │
│   │       Datastore space       │  │       Growth trend OK       │  │      Backups confirmed      │   │
│   │        VM state check       │  │       Forecast 90 days      │  │        HA/DRS active        │   │
│   │        Backup status        │  │       Licence headroom      │  │      App owner sign-off     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    HA         = High Availability; restarts VMs on surviving hosts when a host fails                  │
│    DRS        = Distributed Resource Scheduler; balances VM load across cluster hosts                 │
│    vSAN       = VMware hyper-converged storage; health = no resync, no degraded objects               │
│    Balloon    = VMware memory reclaim driver; non-zero = host under memory pressure                   │
│    Swap       = VM disk-based memory swap; non-zero = critical memory shortage on host                │
│    Datastore  = Storage volume presented to ESXi; monitor used % and provisioning ratio               │
│    VAMI       = vCenter Appliance Management Interface; port 5480; cert and patch mgmt                │
│    Alarm      = vCenter triggered alert; P1=red critical, P2=yellow warning, P3=info                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="daily-health-check/">
  <strong>Daily Health Check</strong>
  <span>Daily checks across vCenter, ESXi, vSAN, NSX, VxRail, and Aria.</span>
</a>

<a class="kb-card" href="pre-change-check/">
  <strong>Pre-Change Check</strong>
  <span>Checks before maintenance, patching, upgrades, migrations, or config changes.</span>
</a>

<a class="kb-card" href="post-change-validation/">
  <strong>Post-Change Validation</strong>
  <span>Validation after maintenance, upgrades, patching, or configuration changes.</span>
</a>

<a class="kb-card" href="capacity-review/">
  <strong>Capacity Review</strong>
  <span>Cluster, datastore, vSAN, CPU, memory, and growth review.</span>
</a>

<a class="kb-card" href="alert-review/">
  <strong>Alert Review</strong>
  <span>Review active alerts, stale alerts, ownership, and escalation needs.</span>
</a>

<a class="kb-card" href="management-access-check/">
  <strong>Management Access Check</strong>
  <span>vCenter, ESXi, VxRail Manager, NSX, and Aria access validation.</span>
</a>

</div>
