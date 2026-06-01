# Unity — Operations

<div class="kb-summary">
Unity — Operations reference: Health Checks, Procedures, CLI Reference, Install & Upgrade, and 2 more.
</div>

```
┌──────────────────────────────────────── Dell Unity Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Day-2 ops: SP health check, FAST VP job monitoring, snapshot lifecycle, replication      │   │
│   │            SP health: Unisphere health dashboard; uemcli /sys/general/health -list            │   │
│   │          FAST VP: schedule-driven tier moves; monitor via Unisphere Storage Pool view         │   │
│   │        Replication: async session monitoring; RPO check; failover / failback procedures       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Health check → FAST VP job review → snap schedule verify → replication lag → alert close           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Health / SP         │  │        Data Services        │  │         Replication         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       SP health check       │  │         FAST VP job         │  │        Session state        │   │
│   │         Drive health        │  │        Snap schedule        │  │         RPO monitor         │   │
│   │          Fan / PSU          │  │         Snap restore        │  │           Failover          │   │
│   │        Pool capacity        │  │         Snap expire         │  │           Failback          │   │
│   │        CloudIQ score        │  │       Pool shrink/grow      │  │         Repl resync         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SP status → FAST VP tier check → snap policy audit → replication RPO → capacity trend              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │       Tool       │        CLI        │    Frequency     │ Alert threshold  │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    SP health     │    Unisphere     │   uemcli health   │      Daily       │   Any degraded   │   │
│   │     FAST VP      │    Unisphere     │    uemcli tier    │      Weekly      │   Stalled job    │   │
│   │   Replication    │    Unisphere     │    uemcli repl    │      Daily       │   RPO exceeded   │   │
│   │     Capacity     │     CloudIQ      │    uemcli pool    │      Weekly      │    >80% used     │   │
│                                                                                                       │
│    Physical: Unisphere on embedded service processor; uemcli connects via HTTPS to SP IP              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    uemcli         = Unity CLI; REST API wrapper: uemcli /stor/prov/luns/lun -list                     │
│    FAST VP job    = Scheduled data migration between Flash, SAS, and NL-SAS tiers                     │
│    Snap schedule  = Automated snapshot rule; hourly/daily/weekly; max snap count limit                │
│    Snap restore   = Revert LUN or filesystem to snapshot state; overwrites current data               │
│    Snap expire    = Snapshot past retention date deleted automatically; capacity reclaimed            │
│    Pool capacity  = Storage pool usable space; alert at >80% used to avoid write failures             │
│    Repl session   = Unity async replication pairing; shows last sync time and transfer size           │
│    Failover       = Switch replication target to read/write; application moves to DR site             │
│    Failback       = Resync data back to primary Unity; resume original replication direction          │
│    Repl resync    = Re-establish replication after failback; delta sync not full reseed               │
│    CloudIQ score  = SaaS health score; receives data from Unity via SCG phone-home                    │
│    SP degraded    = One SP fault; remaining SP takes all I/O; repair SP immediately                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```text
┌──────────────────────────────────────── Dell Unity Operations ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Day-2 ops: SP health check, FAST VP job monitoring, snapshot lifecycle, replication      │   │
│   │            SP health: Unisphere health dashboard; uemcli /sys/general/health -list            │   │
│   │          FAST VP: schedule-driven tier moves; monitor via Unisphere Storage Pool view         │   │
│   │        Replication: async session monitoring; RPO check; failover / failback procedures       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Health check → FAST VP job review → snap schedule verify → replication lag → alert close           │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Health / SP         │  │        Data Services        │  │         Replication         │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       SP health check       │  │         FAST VP job         │  │        Session state        │   │
│   │         Drive health        │  │        Snap schedule        │  │         RPO monitor         │   │
│   │          Fan / PSU          │  │         Snap restore        │  │           Failover          │   │
│   │        Pool capacity        │  │         Snap expire         │  │           Failback          │   │
│   │        CloudIQ score        │  │       Pool shrink/grow      │  │         Repl resync         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SP status → FAST VP tier check → snap policy audit → replication RPO → capacity trend              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │       Tool       │        CLI        │    Frequency     │ Alert threshold  │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    SP health     │    Unisphere     │   uemcli health   │      Daily       │   Any degraded   │   │
│   │     FAST VP      │    Unisphere     │    uemcli tier    │      Weekly      │   Stalled job    │   │
│   │   Replication    │    Unisphere     │    uemcli repl    │      Daily       │   RPO exceeded   │   │
│   │     Capacity     │     CloudIQ      │    uemcli pool    │      Weekly      │    >80% used     │   │
│                                                                                                       │
│    Physical: Unisphere on embedded service processor; uemcli connects via HTTPS to SP IP              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    uemcli         = Unity CLI; REST API wrapper: uemcli /stor/prov/luns/lun -list                     │
│    FAST VP job    = Scheduled data migration between Flash, SAS, and NL-SAS tiers                     │
│    Snap schedule  = Automated snapshot rule; hourly/daily/weekly; max snap count limit                │
│    Snap restore   = Revert LUN or filesystem to snapshot state; overwrites current data               │
│    Snap expire    = Snapshot past retention date deleted automatically; capacity reclaimed            │
│    Pool capacity  = Storage pool usable space; alert at >80% used to avoid write failures             │
│    Repl session   = Unity async replication pairing; shows last sync time and transfer size           │
│    Failover       = Switch replication target to read/write; application moves to DR site             │
│    Failback       = Resync data back to primary Unity; resume original replication direction          │
│    Repl resync    = Re-establish replication after failback; delta sync not full reseed               │
│    CloudIQ score  = SaaS health score; receives data from Unity via SCG phone-home                    │
│    SP degraded    = One SP fault; remaining SP takes all I/O; repair SP immediately                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
</div>
