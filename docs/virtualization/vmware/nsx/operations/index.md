---
tags:
  - nsx
  - nsx-4
  - operations
  - vmware
---
# NSX — Operations

<div class="kb-summary">
Day-to-day operational reference for VMware NSX. Covers CLI commands, health checks, routine procedures, lifecycle management, backup strategy, and automation scripts.

*Applies to: NSX-T 3.x / NSX 4.x*
</div>

```text
┌────────────────────────────────────────── NSX — Operations ───────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │        NSX operations: CLI commands, health checks, upgrade procedures, and automation        │   │
│   │ Daily: check Manager cluster health, Edge cluster state, transport node status, BGP peer state│   │
│   │  Health: verify DFW rule sync on all hosts; confirm MPA connectivity; review alarm dashboard  │   │
│   │   Lifecycle: upgrade via NSX coordinator (Manager → Edge → host transport nodes in sequence)  │   │
│   │     Automation: NSX Policy REST API, Terraform NSX provider, PowerCLI NSX, Ansible modules    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily checks catch control plane drift · lifecycle upgrades in sequence                            │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │     Manager: cluster ok     │  │       NSX coordinator       │  │       Policy REST API       │   │
│   │     Edge: cluster state     │  │     Manager upgrade 1st     │  │        Terraform NSX        │   │
│   │    Transport: node state    │  │       Edge upgrade 2nd      │  │       PowerCLI NSX mod      │   │
│   │     BGP: peer up/active     │  │     Host TN upgrade 3rd     │  │      Ansible: NSX role      │   │
│   │     DFW: rule count sync    │  │     Version compat check    │  │        nsxcli on edge       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch issues early · upgrade sequence prevents mismatch                                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │  nsxcli on edge  │  Manager: green  │    Add TN: prep   │   Coordinator    │  Config export   │   │
│   │    get routes    │ Edge: cluster ok │    BGP peer add   │ Mgr upgrade 1st  │  Policy API bkp  │   │
│   │get logical-router│   TN: state ok   │   Segment create  │   Edge upg 2nd   │  Restore: redep  │   │
│   │ set debug-level  │   BGP: peer up   │    DFW rule add   │ Host TN upg 3rd  │  Config backup   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 ESXi hosts · Edge VM nodes · ToR switches (BGP peers) · Physical NICs (TEP uplinks)              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  nsxcli        = NSX Edge CLI; access via SSH or console; commands: get, set, debug namespaces        │
│  NSX coordinator = Upgrade orchestrator built into NSX Manager; manages upgrade sequence and          │
│  MPA           = Management Plane Agent; runs on each transport node; communicates with Manager       │
│  Transport node = ESXi host or Edge VM enrolled in NSX; carries GENEVE overlay traffic                │
│  BGP peer      = ToR switch NSX peers with for T0 uplink routing; BFD tracks peer state               │
│  DFW rule sync = Verification that all hosts have the same distributed firewall rule count and policy │
│  Policy API    = NSX primary REST API (preferred over deprecated Manager API); intent-based config    │
│  Terraform NSX = HashiCorp Terraform provider for NSX-T; automates segment, DFW, and routing config   │
│  Edge cluster  = Group of Edge nodes providing routing/NAT/LB; HA active/standby or ECMP              │
│  Config backup = NSX Manager periodic backup to SFTP; restores Manager config not data plane state    │
│  Version compat = NSX and vSphere/vCenter version compatibility matrix; check before upgrade          │
│  Ansible NSX   = VMware Ansible collection modules for NSX policy, segments, DFW, and routing         │
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
