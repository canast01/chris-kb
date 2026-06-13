---
tags:
  - operations
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware vSAN. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```text
┌────────────────────────────────────────── vSAN — Operations ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │  vSAN health service provides proactive monitoring of disk, network, HCL, and capacity status │   │
│   │ Daily: review disk group state, resync operations (target zero), capacity headroom (<70% used)│   │
│   │  Lifecycle: LCM upgrades ESXi and vSAN together; pre-check health before node-by-node upgrade │   │
│   │ Post-expansion: rebalance cluster after adding nodes; validate HCL compliance for new hardware│   │
│   │      Automation: vSAN REST API, RVC commands, PowerCLI vSAN module, esxcli vsan namespace     │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch drift · lifecycle keeps vSAN current · automation scales vSAN management tasks     │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │       vSAN health svc       │  │     LCM + ESXi together     │  │        vSAN REST API        │   │
│   │      Disk group: state      │  │       Pre-check health      │  │         RVC commands        │   │
│   │       Resync: 0 ideal       │  │       Node-by-node upg      │  │        PowerCLI vSAN        │   │
│   │        Capacity: <70%       │  │      Rebalance post-add     │  │         esxcli vsan         │   │
│   │      Policy compliance      │  │         HCL validate        │  │       Capacity report       │   │
│   │        Alarms review        │  │          Post-check         │  │           SPBM API          │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch resync and capacity issues · lifecycle upgrades node-by-node                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │   esxcli vsan    │ Health UI green  │     Maint mode    │    LCM bundle    │  vSAN no native  │   │
│   │    RVC vsan.*    │    Resync = 0    │    Add disk grp   │  Pre-check run   │  VM backup VADP  │   │
│   │     vSAN API     │  Capacity <70%   │   Expand cluster  │  Node upg order  │  Rep policy chk  │   │
│   │  PowerCLI vSAN   │  HCL compliant   │   Rebalance run   │   Post-upg chk   │  Witness backup  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers with NVMe/SSD/HDD · RAM DIMMs · 25GbE NICs (vSAN network) · Witness host · ToR switches  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vSAN health   = Built-in vCenter health service; checks HCL, network, disk, and capacity proactively │
│  Disk group    = OSA unit: one cache disk + up to 7 capacity disks; state must be healthy             │
│  FTT           = Failures To Tolerate; objects rebuild when a host enters maintenance mode            │
│  Resync        = Rebuild or rebalance of vSAN objects; high resync indicates degraded protection      │
│  Rebalance     = vSAN redistributes data across nodes after adding capacity to equalize usage         │
│  RVC           = Ruby vSphere Console; CLI tool with vSAN-specific commands for diagnostics           │
│  SPBM          = Storage Policy-Based Management; policy compliance check ensures FTT is satisfied    │
│  LCM           = Lifecycle Manager; image-based ESXi + vSAN upgrade integrated in vCenter 7+          │
│  HCL           = Hardware Compatibility List; vSAN requires certified disks and NICs at all times     │
│  Witness       = Tie-breaker node in stretched cluster; must be reachable from both data sites        │
│  OSA           = Original Storage Architecture; disk-group-based; cache+capacity tier design          │
│  ESA           = Express Storage Architecture; NVMe-only single-tier; vSAN 8.0+ required              │
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

</div>
