# NetApp Keystone — Operations


```
┌──────────────────────────────────── NetApp Keystone — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        Operations: daily ONTAP health checks, Collector upload status, capacity review        │   │
│   │        Daily: verify Collector upload, check EMS errors, confirm HA state, node health        │   │
│   │          Weekly: review Active IQ dashboard, burst usage trend, aggregate utilisation         │   │
│   │           Monthly: usage report export, billing reconciliation, ONTAP patch planning          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily checks -> weekly trend -> monthly billing -> quarterly KSM -> capacity plan                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Daily Checks        │  │         Weekly Tasks        │  │        Monthly Tasks        │   │
│   │       Collector upload      │  │        Active IQ dash       │  │         Usage report        │   │
│   │       EMS error review      │  │         Burst trend         │  │        Billing check        │   │
│   │         Node health         │  │       Aggr utilisation      │  │         Patch review        │   │
│   │           HA state          │  │        Volume growth        │  │          QoS review         │   │
│   │         Disk spares         │  │        Perf baselines       │  │        Capacity plan        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Alert thresholds: Collector offline >30 min = P2; aggr >85% = P1; HA fault = P1                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Task       │  Command / Tool  │     Frequency     │      Owner       │      Notes       │   │
│   │     HA check     │ storage failover │       Daily       │    StorageOps    │    Connected     │   │
│   │    Collector     │    ks status     │       Daily       │    StorageOps    │    Upload OK     │   │
│   │    Aggr util     │    aggr show     │       Weekly      │    StorageOps    │    <85% used     │   │
│   │     Billing      │   Active IQ UI   │      Monthly      │    FinanceOps    │  Match invoice   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: ONTAP cluster mgmt LIF accessible from ops jump host; Collector VM same net              │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    EMS             = Event Management System; ONTAP internal event/alert log                          │
│    HA state        = storage failover show; nodes must be Connected not Takeover                      │
│    Disk spare      = Unassigned disk; ONTAP uses to replace failed drives auto                        │
│    Aggregate util  = Physical used/total; above 85% risks out-of-space errors                         │
│    Burst trend     = Rate of committed + burst consumption; projected overage                         │
│    Collector status= ks status; connected, last upload <30 min ago                                    │
│    QoS review      = Check qos show for IOPS throttling events; adjust if needed                      │
│    Billing recon.  = Compare Active IQ invoice vs internal cost allocation                            │
│    Patch review    = Check NetApp PSIRT advisories; plan ONTAP NDU upgrade window                     │
│    NDU             = Non-Disruptive Upgrade; rolling upgrade without I/O interruption                 │
│    Volume growth   = Track FlexVol/FlexGroup growth rate; predict aggregate fill                      │
│    Perf baseline   = Weekly latency/IOPS averages; compare to service level SLO                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
<div class="kb-grid kb-grid-3">
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Routine checks, service validation, and status verification.</span></a>
<a class="kb-card" href="procedures/"><strong>Procedures</strong><span>Day-to-day operational tasks and how-to guides.</span></a>
<a class="kb-card" href="common-issues/"><strong>Common Issues</strong><span>Quick reference for common problems and resolutions.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Commands, syntax, and quick reference.</span></a>
<a class="kb-card" href="install-upgrade/"><strong>Install & Upgrade</strong><span>Installation, upgrade, patching, and decommission.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts and reusable code.</span></a>
<a class="kb-card" href="backup-restore/"><strong>Backup & Restore</strong><span>Backup configuration, restore procedures, and validation.</span></a>
</div>
