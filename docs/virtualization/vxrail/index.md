---
title: VxRail
tags:
  - vxrail
---

# VxRail

<div class="kb-summary">
Operational reference for Dell VxRail HCI. Covers architecture, lifecycle management, operations, CLI reference, troubleshooting, integration, and vendor support for VxRail clusters running vSphere and vSAN.
</div>

```text
┌──────────────────────────────────────── VxRail Platform Stack ────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                   VxRail Platform Management                                  │   │
│   │         VxRail Manager: node health, cluster expansion, and LCM upgrade orchestration         │   │
│   │        vCenter: VM and cluster management; integrated with VxRail for lifecycle events        │   │
│   │         Dell SupportAssist: automated diagnostics and proactive support case creation         │   │
│   │              CloudIQ: cloud analytics for capacity forecasting and health scoring             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VxRail Manager coordinates all cluster operations alongside vCenter                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Compute (Nodes)       │  │          Networking         │  │        Storage (vSAN)       │   │
│   │    P/E/S/V node families    │  │   vSAN: dedicated VMkernel  │  │      vSAN HCI datastore     │   │
│   │       Intel Xeon CPUs       │  │     Management VMkernel     │  │    Disk groups: cache+cap   │   │
│   │    iDRAC: BMC management    │  │   vMotion: live migration   │  │   Erasure coding: FTT=1/2   │   │
│   │  BIOS + firmware lifecycle  │  │    NSX-T: overlay network   │  │     Dedup + compression     │   │
│   │      NVMe/SSD/HDD tiers     │  │    10/25/100 GbE uplinks    │  │    Stretched cluster opt.   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Compute, networking, and storage are pre-validated on Dell HCI node hardware                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Lifecycle (LCM)       │  │          Operations         │  │         Integration         │   │
│   │   VxRail-specific bundles   │  │    Health: VxRail Manager   │  │    VCF: SDDC Manager mgd    │   │
│   │   HCL: compat. validation   │  │    vSAN health service UI   │  │   NSX-T: overlay+micro-seg  │   │
│   │   Non-disruptive upgrades   │  │  SupportAssist: log bundle  │  │     Tanzu: K8s on VxRail    │   │
│   │    Rolling: node by node    │  │    Syslog + SNMP alerting   │  │   Dell APEX: as-a-service   │   │
│   │   VC + VxRail compat. lock  │  │   Performance: vCenter UI   │  │      SRM: DR for VxRail     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    LCM, operational tooling, and integrations complete the VxRail platform picture                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       vSAN       │     vMotion      │     Management    │   iDRAC / BMC    │      NSX-T       │   │
│   │  HCI datastore   │ VM live migrate  │   Host/VM admin   │   Out-of-band    │   Overlay nets   │   │
│   │   iSCSI / RDMA   │  TCP dedicated   │    HTTPS / SOAP   │   IPMI + REST    │   Geneve/VXLAN   │   │
│   │    Witness VM    │ Encryption opt.  │    vCenter API    │   iDRAC web UI   │   Micro-seg FW   │   │
│   │    FTT policy    │   DRS-managed    │    Syslog fwd.    │  Lifecycle Ctrl  │  T-bit tagging   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  VxRail nodes · 10/25/100 GbE ToR switches · iDRAC BMC · Optional FC HBAs · Power                     │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VxRail  = Dell HCI appliance; vSphere + vSAN pre-validated on Dell hardware nodes                    │
│  LCM     = Lifecycle Manager; VMware/VxRail upgrade engine for rolling cluster upgrades               │
│  HCL     = Hardware Compatibility List; VMware list of validated vSAN hardware                        │
│  iDRAC   = Integrated Dell Remote Access Controller; out-of-band BMC for servers                      │
│  vSAN    = VMware hyperconverged storage; NVMe/SSD pools shared across cluster nodes                  │
│  FTT     = Failures to Tolerate; vSAN policy for data redundancy (FTT=1: 1 failure)                   │
│  Disk Group= vSAN unit: one NVMe/SSD cache device with 1-7 capacity devices per node                  │
│  Erasure Coding= RAID-5/6 over vSAN; more efficient than mirroring for FTT=1/2                        │
│  VCF     = VMware Cloud Foundation; full SDDC stack managed by SDDC Manager                           │
│  NSX-T   = VMware NSX; software-defined networking with distributed FW and LB                         │
│  SupportAssist= Dell automated diagnostics; sends logs to support on trigger                          │
│  CloudIQ = Dell cloud analytics SaaS; VxRail health, capacity, and performance                        │
│  SRM     = Site Recovery Manager; orchestrated DR failover for vSphere workloads                      │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌─────────────────────────────── VxRail Platform — Installation Sequence ───────────────────────────────┐
│                                                                                                       │
│  Step 1 · Physical Infrastructure                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Rack VxRail nodes  ·  Cable to ToR switches: mgmt, vSAN, vMotion, VM uplinks                         │
│  ToR: MTU 9000 on vSAN + vMotion ports  ·  LACP/LAG on uplinks if required                            │
│  iDRAC: dedicated management port on every node  ·  Out-of-band access confirmed                      │
│  DNS: A-records for all node FQDNs + VxRail Manager VIP + vCenter FQDN                                │
│  NTP: two sources reachable from management network  ·  Time sync verified                            │
│                                                                                                       │
│                                        │  update firmware on every node                               │
│                                        ▼                                                              │
│  Step 2 · iDRAC, BIOS & Firmware                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  iDRAC firmware at minimum required version per VxRail compatibility matrix                           │
│  BIOS: VT-x/AMD-V on  ·  Hyperthreading on  ·  C-states tuned for workload                            │
│  HBA/NIC firmware at VxRail-qualified levels — verify against VxRail HCL                              │
│  Boot order: local disk first  ·  PXE disabled  ·  RAID controller configured                         │
│  All nodes show healthy in iDRAC  ·  No outstanding hardware alerts                                   │
│                                                                                                       │
│                                        │  run VxRail first-run wizard                                 │
│                                        ▼                                                              │
│  Step 3 · VxRail Manager Bootstrap                                                                    │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Boot nodes from VxRail factory image  ·  Nodes receive management IPs                                │
│  Access VxRail Manager first-run wizard  ·  Set mgmt network, gateway, DNS, NTP                       │
│  Select deployment type: standard / stretched / two-node  ·  Choose vCenter mode                      │
│  Input vSAN disk configuration  ·  Wizard validates hardware + network prereqs                        │
│  Wizard provisions vCenter, SSO, vSAN, VxRail Manager — fully automated bringup                       │
│                                                                                                       │
│                                        │  vCenter available post-wizard                               │
│                                        ▼                                                              │
│  Step 4 · vCenter & Cluster Validation                                                                │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Login to vCenter  ·  All nodes joined cluster  ·  HA and DRS enabled                                 │
│  Licences applied  ·  SSO identity source configured (AD integration if needed)                       │
│  Distributed switch created by wizard  ·  Confirm port groups and uplinks                             │
│  vSAN health: all checks green  ·  Objects in compliance  ·  No disk warnings                         │
│  Alarm baselines set  ·  vCenter backup schedule configured                                           │
│                                                                                                       │
│                                        │  optional: add NSX overlay networking                        │
│                                        ▼                                                              │
│  Step 5 · NSX Integration (optional)                                                                  │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Deploy NSX Manager appliances via LCM or manually  ·  Register vCenter                               │
│  Configure transport zones and uplink profiles  ·  TEP pool assigned                                  │
│  Prepare all cluster hosts as host transport nodes  ·  Verify TEP connectivity                        │
│  Deploy Edge cluster  ·  Configure Tier-0/Tier-1 gateways  ·  BGP/static routing                      │
│  Micro-segmentation: review default DFW rules  ·  Enable IDS if licensed                              │
│                                                                                                       │
│                                        │  lifecycle management and day-2 operations                   │
│                                        ▼                                                              │
│  Step 6 · LCM, Monitoring & Day-2                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  VxRail LCM: download bundle from Dell  ·  Run pre-check  ·  Schedule window                          │
│  Register cluster with VMware Cloud (optional)  ·  Enable Skyline Health                              │
│  Aria Operations: add vCenter adapter  ·  Configure alert policies + dashboards                       │
│  Backup: vCenter DB schedule  ·  VxRail Manager backup  ·  NSX backup if deployed                     │
│  Support bundle path documented  ·  iDRAC call-home alerts enabled                                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-5">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Installation, initial configuration, and deployment procedures.</span>
</a>

<a class="kb-card" href="operations/"><strong>Operations</strong><span>Daily checks, health monitoring, maintenance tasks, and runbooks.</span></a>
<a class="kb-card" href="cli-reference/"><strong>CLI Reference</strong><span>Command reference by category with syntax and examples.</span></a>
<a class="kb-card" href="scripts/"><strong>Scripts</strong><span>Automation scripts for daily checks, health, incident triage, and validation.</span></a>
<a class="kb-card" href="troubleshooting/"><strong>Troubleshooting</strong><span>Common issues, diagnostic commands, log locations, and error codes.</span></a>
<a class="kb-card" href="integration/"><strong>Integration</strong><span>VMware, backup tools, monitoring, authentication, and API integration.</span></a>
<a class="kb-card" href="security/"><strong>Security</strong><span>Hardening checklist, RBAC, encryption, audit logging, and compliance.</span></a>
<a class="kb-card" href="vendor-support/"><strong>Vendor Support</strong><span>Opening a case, information to collect, support portal, and SLA tiers.</span></a>
<a class="kb-card" href="field-reference/"><strong>Field Reference</strong><span>Node part numbers, slot layout, LED codes, and drive replacement mapping.</span></a>
<a class="kb-card" href="health-checks/"><strong>Health Checks</strong><span>Cluster health, vSAN object status, node connectivity, and firmware compliance checks.</span></a>
<a class="kb-card" href="support-notes/"><strong>Support Notes</strong><span>Known issues, Dell support case tips, log bundle collection, and KB article links.</span></a>
<a class="kb-card" href="technical-deep-dive/"><strong>Technical Deep Dive</strong><span>Internal architecture, vSAN witness placement, network stack, and boot sequence detail.</span></a>
<a class="kb-card" href="vxrail-manager/"><strong>VxRail Manager</strong><span>VxRail Manager UI, API, upgrade orchestration, and credential management.</span></a>
<a class="kb-card" href="hardware/"><strong>Hardware</strong><span>Node families, part numbers, slot layout, LED codes, and drive replacement mapping.</span></a>
<a class="kb-card" href="rasr/"><strong>RASR</strong><span>Reset Appliance to Shipping Requirements — factory reset procedure and recovery workflow.</span></a>
</div>
