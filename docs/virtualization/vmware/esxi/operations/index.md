---
tags:
  - esxi
  - operations
  - vmware
  - vsphere-8
---
# ESXi — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware ESXi. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.
</div>

```text
┌────────────────────────────────────────── ESXi — Operations ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ ESXi day-to-day operations: CLI commands, health checks, procedures, and lifecycle management │   │
│   │Daily: review host alarms in vCenter, check storage paths, confirm NTP sync and hardware health│   │
│   │   Lifecycle: patch via VUM/LCM baselines; apply host profiles; update ESXi image in cluster   │   │
│   │    Backup: no built-in VM backup; use VADP-based solutions; host config backed up via host    │   │
│   │ Automation: esxcli scripting, PowerCLI, REST API, Ansible VMware modules for at-scale changes │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    CLI gives direct host access · lifecycle keeps hosts patched · automation scales daily operations  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │     Host alarms: vCenter    │  │      VUM/LCM: baseline      │  │      esxcli: namespaces     │   │
│   │    Storage paths: esxcli    │  │     Host profile: apply     │  │     PowerCLI: host cmds     │   │
│   │    NTP drift: check sync    │  │    Patch: remediate task    │  │     Ansible: VMware mods    │   │
│   │     Hardware: iDRAC/iLO     │  │     Update planner tool     │  │      REST API: host ops     │   │
│   │     esxtop: perf monitor    │  │     Boot bank: validate     │  │     vSphere SDK scripts     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch drift early · lifecycle keeps hosts secure and current · automation reduces toil   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  esxcli system   │   Host: green?   │     Maint mode    │   VUM baseline   │  No native bkp   │   │
│   │  esxcli network  │   vSAN: resync   │    DRS evacuate   │  Image profile   │  VADP-based sol  │   │
│   │  esxcli storage  │   NTP: in sync   │    Host profile   │  Pre/post check  │ Host profile bk  │   │
│   │  vim-cmd vmsvc   │   HW: iDRAC ok   │  Patch remediate  │   Boot bank ok   │  Restore: redep  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server · CPUs · RAM DIMMs · PCIe HBAs/NICs · SAS/NVMe disks · iDRAC/iLO OOB management           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  esxcli        = ESXi CLI framework; namespaces: system, network, storage, vm, software, hardware     │
│  esxtop        = ESXi real-time performance monitor; displays CPU/memory/disk/network per VM          │
│  VUM           = vSphere Update Manager; baseline-based patching; scans, stages, and remediates       │
│  LCM           = Lifecycle Manager; image-based ESXi patching integrated into vCenter 7+              │
│  Host Profile  = Saved configuration template; applied to hosts to enforce configuration consistency  │
│  Maintenance mode = Host state that migrates VMs away before patching or hardware maintenance         │
│  Boot bank     = ESXi dual-bank boot; active and standby banks; rollback to standby if needed         │
│  VADP          = vStorage APIs for Data Protection; backup vendor interface for quiesced VM snapshots │
│  vim-cmd       = ESXi CLI for VM operations: power on/off, snapshot, register, unregister             │
│  vmkfstools    = ESXi CLI for VMDK operations: clone, resize, inflate, import/export                  │
│  iDRAC/iLO     = Out-of-band management; provides console access and hardware health independent of OS│
│  PowerCLI      = VMware PowerShell module for at-scale vSphere automation and reporting               │
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
