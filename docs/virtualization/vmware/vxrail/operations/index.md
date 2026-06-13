---
tags:
  - operations
  - vmware
  - vxrail
---
# VxRail — Operations

<div class="kb-summary">
Day-to-day operational reference for VxRail in the VMware product context. Covers plugin health, LCM upgrade sequencing, cluster expansion, and SupportAssist automation.

*Applies to: VxRail 7.x / 8.x*
</div>

```text
┌───────────────────────────────────────── VxRail — Operations ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         VxRail plugin daily health checks in vCenter; iDRAC hardware alarms monitoring        │   │
│   │        LCM bundle download and pre-check before upgrade; node-by-node upgrade sequence        │   │
│   │            FW + ESXi upgraded together per node in a single LCM operation per node            │   │
│   │        SupportAssist for proactive case creation on hardware alerts from iDRAC or OMIVV       │   │
│   │   Post-upgrade validation: vSAN health, ESXi version, iDRAC FW, and cluster stability checks  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch drift early · lifecycle upgrades per node · automation scales VxRail management    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │          Daily Ops          │  │          Lifecycle          │  │          Automation         │   │
│   │       VxRail plugin UI      │  │        LCM bundle DL        │  │        VxRail Mgr API       │   │
│   │         iDRAC alarms        │  │       Pre-check health      │  │         LCM REST API        │   │
│   │        ESXi connected       │  │       Node-by-node upg      │  │        PowerCLI vSAN        │   │
│   │       vSAN resync chk       │  │       FW+ESXi together      │  │       Dell automation       │   │
│   │          LCM status         │  │      Rebalance post-add     │  │        Ansible VxRail       │   │
│   │        SupportAssist        │  │          Post-check         │  │      SupportAssist API      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Daily ops catch issues early · lifecycle upgrades in sequence · automation handles at-scale changes│
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     CLI Ref      │    Health Chk    │     Procedures    │    Install/Up    │   Backup/Rest    │   │
│   │    VxRail API    │  Plugin: green   │    Daily checks   │  LCM bundle DL   │  Config export   │   │
│   │   LCM REST API   │    iDRAC: ok     │    Maint window   │  Pre-check run   │  vSAN config bk  │   │
│   │  PowerCLI vSAN   │  vSAN: resync=0  │     Node maint    │   Node-by-node   │   iDRAC config   │   │
│   │  Ansible VxRail  │ ESXi: connected  │   Expand cluster  │   Post-upg val   │  Restore redep   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Dell PowerEdge servers · NVMe/SSD/HDD · 25GbE NICs · iDRAC OOB · ToR switches                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VxRail Manager API  = REST API on VxRail Manager VM; used for LCM jobs, health queries, and config   │
│  LCM bundle          = Signed Dell upgrade package; FW + ESXi + vSAN versions tested and bundled      │
│  Pre-check           = Health validation run before LCM upgrade; blocks if vSAN or network issues     │
│  Node-by-node upgrade = LCM puts one node in maintenance, upgrades FW+ESXi, then moves to next node   │
│  SupportAssist       = Dell proactive support; auto-opens cases on hardware alert from iDRAC or OMIVV │
│  iDRAC               = Integrated Dell Remote Access Controller; hardware health, console, and OOB    │
│  OMIVV               = OpenManage Integration for VMware vCenter; shows Dell hardware alarms in       │
│  vSAN rebalance      = Redistributes vSAN objects evenly after a node is added to the cluster         │
│  Maintenance mode    = ESXi state that evacuates VMs via DRS before hardware or upgrade operations    │
│  FW update           = Firmware update applied to iDRAC, BIOS, NICs, and drives as part of LCM bundle │
│  PowerCLI            = VMware PowerShell module; used for vSAN health checks and cluster automation   │
│  Post-upgrade validation = Checks ESXi version, iDRAC FW, vSAN health, and cluster stability after LCM│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid">

<div class="kb-card">
<h3><a href="cli-reference/">CLI Reference</a></h3>
<p>VxRail Manager API, esxcli vSAN, iDRAC RACADM, and PowerCLI command reference.</p>
</div>

<div class="kb-card">
<h3><a href="health-checks/">Health Checks</a></h3>
<p>Daily and weekly health check routine — VxRail plugin, vSAN, iDRAC, and capacity.</p>
</div>

<div class="kb-card">
<h3><a href="procedures/">Procedures</a></h3>
<p>Node maintenance, expansion, disk replacement, and change readiness.</p>
</div>

<div class="kb-card">
<h3><a href="install-upgrade/">Install &amp; Upgrade</a></h3>
<p>VxRail LCM bundle upload, pre-check, node-by-node upgrade, and validation.</p>
</div>

<div class="kb-card">
<h3><a href="backup-restore/">Backup &amp; Restore</a></h3>
<p>VxRail Manager backup, vCenter VAMI backup, ESXi config export, and restore.</p>
</div>

<div class="kb-card">
<h3><a href="scripts/">Scripts</a></h3>
<p>PowerCLI and bash scripts for health checks, capacity, pre-upgrade validation.</p>
</div>

</div>
