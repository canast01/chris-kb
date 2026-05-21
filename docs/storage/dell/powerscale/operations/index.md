# PowerScale — Operations


```
┌───────────────────────────────────── Dell PowerScale Operations ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Day-2 ops: cluster health, SyncIQ replication, SnapshotIQ lifecycle, quota management     │   │
│   │      isi status: cluster health overview; isi statistics: node/protocol/drive performance     │   │
│   │        SyncIQ: run/pause/resume policies; monitor RPO; failover and failback procedures       │   │
│   │         Quota alerts: track SmartQuota thresholds; isi quota list for space accounting        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    isi status → review alerts → SyncIQ policy check → quota review → snapshot expiry cleanup          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Cluster Health       │  │         Replication         │  │       Capacity / Data       │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │          isi status         │  │       isi sync policy       │  │        isi quota list       │   │
│   │         Drive state         │  │         isi sync job        │  │        SmartPool jobs       │   │
│   │          Node state         │  │       Failover policy       │  │        isi snap list        │   │
│   │       FlexProtect job       │  │       Failback policy       │  │         Snap delete         │   │
│   │          Event log          │  │          RPO alert          │  │        Capacity trend       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Cluster health → SyncIQ RPO check → quota threshold review → snapshot cleanup cycle                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │       Task       │     Command      │       Output      │    Frequency     │ Alert threshold  │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │      Health      │    isi status    │   Node/drive OK   │      Daily       │   Any degraded   │   │
│   │   SyncIQ check   │   isi sync job   │   Last run time   │      Daily       │   RPO exceeded   │   │
│   │   Quota check    │  isi quota list  │  Usage vs. limit  │      Weekly      │  >85% threshold  │   │
│   │   Snap cleanup   │ isi snap delete  │   Freed capacity  │     Monthly      │  Policy expired  │   │
│                                                                                                       │
│    Physical: SSH to any cluster node; isi commands run on OneFS and return cluster-wide data          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    isi status     = Cluster-wide health: node states, drive states, FlexProtect job status            │
│    isi statistics = Protocol throughput, node IOPS, latency, drive stats; -c for CSV                  │
│    isi sync policy= List/modify SyncIQ replication policies; target, schedule, throttle               │
│    isi sync job   = View running SyncIQ jobs; last run, bytes transferred, RPO gap                    │
│    isi quota list = Display directory quotas; hard limit, advisory, grace period status               │
│    isi snap list  = List snapshots; name, target directory, creation time, size                       │
│    FlexProtect job= Restripe job that repairs data after drive or node failure                        │
│    RPO alert      = SyncIQ replication behind schedule; data loss window exceeded target              │
│    SmartPool job  = Background tier migration; moves files between pools per file pool policy         │
│    Quota threshold= SmartQuota hard limit stops writes; advisory sends alert only                     │
│    Snap delete    = Remove expired or manual snapshots; reclaims capacity in snapshot delta           │
│    Failover policy= SyncIQ policy action to allow writes on target during source cluster outage       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">

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

<a class="kb-card" href="cli-reference/">
  <strong>CLI Reference</strong>
  <span>Commands, syntax, and quick reference.</span>
</a>

</div>
