---
title: VxRail
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

<div class="kb-grid kb-grid-5">
<a class="kb-card" href="architecture/"><strong>Architecture</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, build baseline, and configuration checklist.</span></a>
<a class="kb-card" href="lifecycle/"><strong>Lifecycle</strong><span>Version matrix, upgrade paths, EOL tracking, and refresh planning.</span></a>
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
</div>
