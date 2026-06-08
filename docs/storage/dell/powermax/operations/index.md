# PowerMax — Operations

<div class="kb-summary">
PowerMax day-to-day operations — SRDF management, storage group provisioning, performance monitoring, and host connectivity.
</div>

```text
┌────────────────────────────────────── Dell PowerMax Operations ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Day-2 operations: SRDF state management, TimeFinder copies, SLO rebalancing, capacity     │   │
│   │      SRDF suspend/resume, failover/failback, and swap-personality for planned maintenance     │   │
│   │        TimeFinder: create/restore snaps; snap schedules; VP Snap and Clone for test/dev       │   │
│   │      Health: Unisphere alerts, SYMAPI event logs, CloudIQ analytics, SCG-based reporting      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Monitor alerts → run health checks → execute SRDF or TimeFinder action → verify and close          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       SRDF Operations       │  │        TimeFinder Ops       │  │      Capacity / Health      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       Suspend / Resume      │  │        Snap establish       │  │       SRP utilization       │   │
│   │      Failover / Failbk      │  │         Snap restore        │  │        CloudIQ health       │   │
│   │       Swap personality      │  │         Clone split         │  │       Unisphere alerts      │   │
│   │      Group consistency      │  │        VP Snap mount        │  │        FE port stats        │   │
│   │       RDF link monitor      │  │        Snap schedule        │  │       Capacity trends       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    SRDF state check → TimeFinder snap/clone → SRP capacity review → alert remediation loop            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │       Tool       │    CLI command    │    Frequency     │      Notes       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    SRDF check    │      symrdf      │  symrdf -g query  │      Daily       │ Check link state │   │
│   │   Snap create    │     symsnap      │  symsnap -sg est  │   Per schedule   │ Verify gen count │   │
│   │    SRP usage     │    Unisphere     │  symcfg list -srp │      Weekly      │    Alert >80%    │   │
│   │  Health alerts   │     CloudIQ      │   REST API poll   │    Continuous    │   SCG required   │   │
│                                                                                                       │
│    Physical: Unisphere on embedded mgmt network; SCG phone-home for CloudIQ telemetry relay           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    symrdf         = SYMAPI CLI tool for SRDF state management (query, suspend, failover, swap)        │
│    symsnap        = SYMAPI CLI tool for TimeFinder/Snap operations (establish, restore, term)         │
│    symdg          = SYMAPI device group tool; groups volumes for consistent SRDF/snap ops             │
│    symsg          = SYMAPI storage group tool; list, modify, and provision storage groups             │
│    Swap personality = SRDF planned failover; R1 becomes R2 and vice versa at recovery site            │
│    VP Snap        = Virtual Provisioning Snap; pointer-based thin snap mounted on a host              │
│    RDF link       = Physical or virtual ISL between PowerMax arrays for SRDF traffic                  │
│    SCG            = Secure Connect Gateway; phone-home proxy for CloudIQ telemetry                    │
│    SRP utilization= Percentage of thin pool capacity consumed; alert threshold typically 80%          │
│    FE port stats  = Front-End director port I/O stats; check for hotspot or imbalance                 │
│    Snap schedule  = Automated TimeFinder snap generation policy (hourly/daily/weekly)                 │
│    Clone split    = Full physical copy created from Clone; independent of source after split          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>SYMCLI command reference for PowerMax administration.</span>
</a>

<a class="kb-card" href="health-checks/">
  <strong>Health Checks</strong>
  <span>Daily checks, array health commands, and status verification.</span>
</a>

<a class="kb-card" href="procedures/">
  <strong>Procedures</strong>
  <span>Change readiness, maintenance windows, provisioning, and masking views.</span>
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
  <span>Automation scripts for health checks, SRDF monitoring, and operations.</span>
</a>

</div>
