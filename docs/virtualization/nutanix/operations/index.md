# Nutanix — Operations

<div class="kb-summary">
Day-to-day operations for Nutanix HCI — health monitoring, administrative procedures, backup and restore, CLI reference, and automation scripts. Covers both Prism Element and CLI-based operations.

*Applies to: AOS 6.x · AHV*
</div>

```text
┌───────────────────────── Nutanix Operations — Health Checks and Admin Tasks ──────────────────────────┐
│                                                                                                       │
│  Daily: NCC health checks, alert review, capacity monitoring; weekly: NCC full run,                   │
│  LCM check; as-needed: upgrades, disk repair, DR test.                                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Daily Operations               │  │              Weekly Operations              │   │
│   │        NCC: ncc health_checks run_all        │  │         NCC full: all plugin groups         │   │
│   │        Alerts: Prism alert dashboard         │  │            LCM: check for updates           │   │
│   │         Capacity: storage % consumed         │  │          Cluster health: HA status          │   │
│   │         Stargate: disk health green          │  │         Cluster history: any issues         │   │
│   │          CVM status: allssh status           │  │         Replication: Cerebro status         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  NCC result: PASS = healthy; WARN = investigate; FAIL = action required.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Administrative Tasks             │  │                CLI Reference                │   │
│   │         VM create: Prism or REST API         │  │           acli: AHV management CLI          │   │
│   │       Disk replace: hot-swap + repair        │  │         ncli: cluster + storage CLI         │   │
│   │           Node add: expand cluster           │  │           ncc: health check runner          │   │
│   │            Snapshot: per-VM or PD            │  │           allssh: run cmd all CVMs          │   │
│   │         DR test: Leap failover test          │  │          lcm: LCM CLI for upgrades          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Nutanix nodes with CVM on each; Prism Central VM for multi-cluster ops;                              │
│  10/25 GbE network; IPMI for OOB; Foundation VM for imaging.                                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NCC           = Nutanix Cluster Check; health check framework; 100+ plugins                          │
│  acli          = Acropolis CLI; AHV VM management (create/delete/update)                              │
│  ncli          = Nutanix CLI; cluster, storage, network management                                    │
│  allssh        = run command across all CVMs simultaneously                                           │
│  PD            = Protection Domain; group of VMs for snapshot/replication                             │
│  LCM           = Lifecycle Manager; AOS + AHV + firmware upgrade orchestrator                         │
│  Stargate      = storage I/O daemon; check health via Prism > Hardware                                │
│  CVM rolling restart= safe way to restart services across all CVMs                                    │
│  Leap          = Nutanix DR product; orchestrated failover to Nutanix cluster                         │
│  Cerebro       = replication engine in CVM; handles PD and Leap replication                           │
│  HA reserve    = capacity reserved for failed node; Prism > Cluster > HA                              │
│  Disk repair   = replace failed disk; CVM auto-rebuilds redundancy                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">
  <a class="kb-card" href="health-checks/">
    <strong>Health Checks</strong>
    <span>Daily and weekly cluster health routine — NCC checks, resilience, storage capacity, CVM and AHV host health.</span>
  </a>
  <a class="kb-card" href="procedures/">
    <strong>Procedures</strong>
    <span>Maintenance mode, LCM upgrades, adding/removing nodes, cloning VMs, snapshot management, protection domains.</span>
  </a>
  <a class="kb-card" href="cli-reference/">
    <strong>CLI Reference</strong>
    <span>Complete ncli, acli, ncc, allssh, genesis, nodetool, and curator_cli command reference.</span>
  </a>
  <a class="kb-card" href="backup-restore/">
    <strong>Backup & Restore</strong>
    <span>Native snapshots, Protection Domain replication, Nutanix DR policies, Veeam, and HYCU integration.</span>
  </a>
  <a class="kb-card" href="scripts/">
    <strong>Scripts</strong>
    <span>Reusable scripts for health snapshots, NCC automation, storage reports, VM inventory, and maintenance helpers.</span>
  </a>
</div>
