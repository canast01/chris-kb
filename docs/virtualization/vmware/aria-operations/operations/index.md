# Aria Operations — Operations

<div class="kb-summary">
Aria Operations daily operations — policy management, alert tuning, dashboard maintenance, and capacity reporting.
</div>

```text
┌──────────────────────────────────── Aria Operations — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Alert management and noise reduction: tune thresholds, suppress flapping, cancel false    │   │
│   │  Capacity optimization: review right-sizing recommendations; act on workload placement advice │   │
│   │   Report scheduling: cost management integration; automated PDF/CSV delivery to stakeholders  │   │
│   │  Cluster node health monitoring: verify all nodes stable; check adapter collection intervals  │   │
│   │     Lifecycle: upgrade wizard sequences node upgrades; pre-upgrade health check mandatory     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops review alerts and capacity · lifecycle keeps cluster current                             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │       Alert management      │  │       Upgrade planner       │  │           REST API          │   │
│   │      Capacity overview      │  │        Pre-upg health       │  │        PowerCLI vROps       │   │
│   │        Optim. actions       │  │        Node upg order       │  │          Alert API          │   │
│   │        Workload place       │  │        Adapter compat       │  │         Capacity API        │   │
│   │         Badge status        │  │          CMDB sync          │  │        Dashboard API        │   │
│   │       Report schedule       │  │          Cert renew         │  │          Report API         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch alert noise · lifecycle upgrades nodes in sequence · automation reduces manual toil│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  REST API calls  │  Cluster: green  │    Alert triage   │  Upgrade wizard  │  Config export   │   │
│   │  PowerCLI vROps  │  Nodes: healthy  │    Capacity rpt   │  Pre-chk health  │   Support.zip    │   │
│   │    Alert API     │   Adapters: ok   │  Add remote coll  │  Node upg order  │  Restore config  │   │
│   │   Capacity API   │  Collectors: up  │   Dashboard add   │   Post-upg val   │  Metric data bk  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 VMs (primary/replica/data/collector) · RAM DIMMs · Network NICs · vCenter/cloud connectivity     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Analytics cluster  = Primary + replica + data nodes; all must be healthy for full functionality      │
│  Remote collector   = Lightweight VM per site forwarding adapter metrics to the analytics cluster     │
│  Adapter instance   = Configured integration to a monitored product; collection interval configurable │
│  Alert definition   = Symptom-based rule firing notifications on threshold breach or anomaly          │
│  Capacity engine    = Forecasting subsystem projecting time-to-exhaustion for CPU, RAM, storage       │
│  Optimization action = Right-size, power-off, or migrate recommendation generated by analytics        │
│  Workload placement = DRS-aligned recommendation for optimal VM-to-host assignment                    │
│  Badge score        = 0-100 health/risk/efficiency score assigned to every monitored object           │
│  Right-sizing       = Reducing oversized vCPU/RAM allocations based on observed peak utilisation      │
│  Cost driver        = Resource consumer identified as a top contributor to capacity or cost usage     │
│  Upgrade planner    = Built-in wizard validating compatibility and sequencing node upgrade steps      │
│  support.zip bundle = Diagnostic package collected from Aria Ops for GSS case submission              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌──────────────────────────────────── Aria Operations — Operations ─────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Aria Operations Day-2 Operations — Health, Maintenance, and Housekeeping Tasks        │   │
│   │         Daily checks: cluster health · adapter status · alert queue depth · disk usage        │   │
│   │       Weekly tasks: review capacity forecasts · compliance report · stale alert cleanup       │   │
│   │       Monthly: log rotation · user audit · MP version check · certificate expiry review       │   │
│   │         Emergency: vracli restart service · cluster rejoin · support bundle collection        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Log the support bundle path before engaging VMware TAM: /data/support_bundle/                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         Daily Checks        │  │         Weekly Tasks        │  │        Monthly Tasks        │   │
│   │      Cluster health OK      │  │      Capacity forecast      │  │         Log rotation        │   │
│   │      Adapter status OK      │  │      Compliance report      │  │          User audit         │   │
│   │       Alert queue <500      │  │      Stale alert purge      │  │       MP version check      │   │
│   │        Disk <80% full       │  │       Dashboard review      │  │       Cert expiry scan      │   │
│   │     Collector reachable     │  │       Group membership      │  │        Backup verify        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Operations tasks performed via Aria Ops UI (HTTPS/443) or vracli SSH on master node                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vracli            = Aria Ops CLI: vracli cluster status · vracli services restart                    │
│  Cluster health    = UI indicator aggregating node status, service health, and Cassandra ring         │
│  Adapter status    = Green/Yellow/Red collector connectivity state in Administration > Adapters       │
│  Alert queue       = Count of active unacknowledged alerts; >500 requires triage                      │
│  Support bundle    = Compressed diagnostic archive: vracli support-bundle collect                     │
│  Log rotation      = Automated log file cycling to prevent disk exhaustion                            │
│  Stale alert purge = Cancelling alerts whose monitored object no longer exists                        │
│  Certificate expiry= TLS cert used by adapter or UI; must be renewed before expiry                    │
│  Compliance report = Scheduled export of policy violation counts per compliance pack                  │
│  MP version check  = Verifying Management Packs match vendor release notes                            │
│  User audit        = Review of local and AD-synced users for inactive or excessive roles              │
│  Cassandra ring    = Distributed DB health; vracli cassandra status shows ring state                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

<a class="kb-card" href="alert-management/">
  <strong>Alert Management</strong>
  <span>Alert design, severity classification, threshold tuning, noise reduction, and on-call routing.</span>
</a>

<a class="kb-card" href="dashboard-standards/">
  <strong>Dashboard Standards</strong>
  <span>Dashboard structure, metric selection, audience-based layouts, and naming conventions.</span>
</a>

<a class="kb-card" href="health-monitoring/">
  <strong>Health Monitoring</strong>
  <span>Infrastructure health monitoring standards — what to monitor, check cadence, and threshold references.</span>
</a>

<a class="kb-card" href="metrics-baseline/">
  <strong>Metrics Baseline</strong>
  <span>Establishing and maintaining performance baselines for CPU, memory, storage I/O, and network.</span>
</a>

<a class="kb-card" href="performance-baselining/">
  <strong>Performance Baselining</strong>
  <span>Methodology for capturing, storing, and comparing performance baselines across environments.</span>
</a>

<a class="kb-card" href="capacity-forecasting/">
  <strong>Capacity Forecasting</strong>
  <span>Capacity trend analysis, forecasting models, and runway calculations for compute and storage.</span>
</a>

<a class="kb-card" href="resource-optimization/"><strong>Resource Optimisation</strong><span>Right-sizing VMs and clusters, reclaiming unused resources, and cost/performance optimisation.</span></a>
<a class="kb-card" href="capacity/"><strong>Capacity</strong><span>Capacity utilization views, runway analysis, and trending across compute and storage.</span></a>
<a class="kb-card" href="alerts/"><strong>Alerts</strong><span>Alert management, threshold tuning, suppression rules, and notification configuration.</span></a>
<a class="kb-card" href="dashboards/"><strong>Dashboards</strong><span>Dashboard creation, widget configuration, and dashboard sharing.</span></a>
<a class="kb-card" href="reports/"><strong>Reports</strong><span>Scheduled and on-demand reports for capacity, health, and performance.</span></a>

</div>

## Daily Checklist

Run through these checks each morning before the ops team stand-up.

| Check | Location | Pass Criteria |
|---|---|---|
| Active Alerts review | Dashboards > Active Alerts | No unacknowledged Critical/Immediate alerts |
| Cluster node health | Admin > Cluster Management | All nodes show Online |
| Adapter collection status | Admin > Solutions | All adapters in Collecting state |
| Disk usage — analytics nodes | Admin > Cluster Management > [Node] > Disk | Below 80% used |
| Remote Collector status | Admin > Environment > Remote Collectors | All collectors Online |

Any failed check should be raised in the team channel and tracked in the ops log before the stand-up.

## Alert Triage Workflow

If a Remote Collector goes Offline, check:
- VM power state
- Network connectivity (TCP 443 to analytics cluster VIP)
- Collector service status: log into collector VM and run `systemctl status vmware-casa`

## Monthly Tasks

- Generate Monthly Executive Capacity Summary report and distribute
- Review alert noise: identify alert definitions with the highest fire frequency and tune thresholds
- Audit user accounts: Admin > Access Control > User Accounts — remove stale accounts
- Verify management pack versions are current (Admin > Solutions > check each adapter version)
- Review data node disk usage trend — project growth against retention policy
