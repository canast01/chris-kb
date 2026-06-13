---
title: VxRail Appliance
tags:
  - vmware
  - vxrail
---

# VxRail Appliance

<div class="kb-summary">
Technical and operational reference for Dell VxRail. Covers VxRail Manager, the First Run Wizard, vSAN auto-configuration, lifecycle upgrades via LCM, iDRAC hardware management, OMIVV integration, and cluster troubleshooting for VxRail HCI deployments.
</div>

```text
┌──────────────────────────────────────── VxRail Cluster Stack ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                    VxRail Manager — HCI Orchestration and Lifecycle Engine                    │   │
│   │    Deploys automatically during First Run Wizard · runs as VM on node 1 after cluster init    │   │
│   │     Owns: LCM upgrades · node expansion · health monitoring · SupportAssist integration       │   │
│   │     REST API: https://<vxm-ip>/rest/vxm/v1/  ·  Mystic local account for CLI/API access      │    │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                        │ manages and integrates with                                  │
│                                        ▼                                                              │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                  vCenter Server — Management Control Plane (embedded or external)             │   │
│   │     Embedded: deployed inside cluster during First Run Wizard (single-region only)            │   │
│   │     External: link to existing vCenter; required for cross-cluster or multi-site topologies   │   │
│   │     Hosts SSO domain · manages DRS · HA · vSphere Lifecycle Manager · OMIVV plugin            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                        │ runs on                                                      │
│                                        ▼                                                              │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       VxRail Node 01        │  │       VxRail Node 02        │  │     VxRail Node 03–08       │   │
│   │   ESXi hypervisor (VxRail   │  │   ESXi hypervisor (VxRail   │  │   ESXi hypervisor (VxRail   │   │
│   │       custom image)         │  │       custom image)         │  │       custom image)         │   │
│   │  vmk0: mgmt  vmk1: vMotion  │  │  vmk0: mgmt  vmk1: vMotion  │  │  vmk0: mgmt  vmk1: vMotion  │   │
│   │  vmk2: vSAN (MTU 9000)      │  │  vmk2: vSAN (MTU 9000)      │  │  vmk2: vSAN (MTU 9000)      │   │
│   │  iDRAC: OOB hardware mgmt   │  │  iDRAC: OOB hardware mgmt   │  │  iDRAC: OOB hardware mgmt   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                        │ storage contributed by all nodes                             │
│                                        ▼                                                              │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │             vSAN — Distributed Storage Layer (auto-configured by VxRail Manager)              │   │
│   │    OSA (Original Storage Architecture): cache + capacity tier disk groups per node            │   │
│   │    ESA (Express Storage Architecture): NVMe-only; single-tier; requires VxRail 8.x+           │   │
│   │    Policies: RAID-1 FTT=1 (minimum prod) · RAID-5/6 for capacity efficiency                  │    │
│   │    vSAN datastore visible in vCenter · SPBM policy assigned per VM or VMDK                    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware all layers above run on):                                      │
│  Dell PowerEdge servers (R-series or C6525)  ·  NVMe cache + SSD/NVMe capacity disks                  │
│  25GbE or 100GbE NICs  ·  Top-of-rack switches with VLAN 9000 MTU on vSAN/vMotion ports               │
│  iDRAC on dedicated OOB management port per node  ·  redundant PSUs + dual switch uplinks             │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VxRail Manager   = lifecycle and orchestration VM; owns First Run Wizard, LCM, expansion             │
│  First Run Wizard = browser-based initial cluster bringup; runs before vCenter exists                 │
│  iDRAC            = integrated Dell Remote Access Controller; OOB BMC for power/console/firmware      │
│  OMIVV            = OpenManage Integration for VMware vCenter; surfaces Dell hardware alerts in vC    │
│  SupportAssist    = Dell cloud-connected diagnostics; auto-uploads logs on detected failure           │
│  LCM              = Lifecycle Manager; VxRail-aware upgrade engine coordinating ESXi + vSAN + vC      │
│  Mystic           = local service account on VxRail Manager VM; used for REST API and CLI access      │
│  ESA              = Express Storage Architecture; NVMe-only vSAN mode; VxRail 8.x+ required           │
│  OSA              = Original Storage Architecture; cache + capacity disk groups; all VxRail versions  │
│  SPBM             = Storage Policy-Based Management; per-VM storage policy enforced by vSAN           │
│  FTT              = Failures to Tolerate; vSAN policy param controlling redundancy level              │
│  RACADM           = Remote RACADM CLI; manage iDRAC settings and passwords from the OS or OOB         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌──────────────────────────────── VxRail Cluster — Deployment Sequence ─────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Physical Readiness                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Rack and cable all nodes  ·  Connect 25GbE NICs to ToR switches per cabling guide                    │
│  iDRAC IP assigned on each node via DCUI F2 or iDRAC front-panel  ·  iDRAC reachable                  │
│  DNS: A + PTR records for VxRail Manager FQDN, vCenter FQDN, and all node FQDNs                       │
│  NTP server reachable from management VLAN  ·  Verify with ntpdate before wizard                      │
│  Switch: management, vMotion, vSAN, and VM VLANs configured  ·  MTU 9000 on vSAN+vMotion              │
│                                                                                                       │
│                                        │  browser to node1 iDRAC/management IP                        │
│                                        ▼                                                              │
│  Step 2 · First Run Wizard                                                                            │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Navigate to https://<node1-mgmt-ip>/  ·  Accept certificate warning                                  │
│  Enter initial network config (management IPs, vSAN IPs, vMotion IPs for all nodes)                   │
│  Choose vCenter deployment type: Embedded (auto-deploy) or External (provide vCenter FQDN)            │
│  Set SSO domain name (e.g. vsphere.local)  ·  Set admin and mystic passwords                          │
│  Wizard runs: discovers all nodes  ·  deploys VxRail Manager VM  ·  deploys embedded vCenter VM       │
│                                                                                                       │
│                                        │  VxRail Manager auto-configures                              │
│                                        ▼                                                              │
│  Step 3 · vCenter Integration                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Embedded: vCenter VCSA deployed automatically inside cluster on node 1 by VxRail Manager             │
│  External: VxRail Manager registers with external vCenter via vCenter plugin extension                │
│  SSO identity source configured  ·  VxRail Plugin visible in vCenter under Menu                       │
│  Cluster object created with DRS Fully Automated + HA enabled  ·  EVC mode set                        │
│                                                                                                       │
│                                        │  disk claim and policy creation                              │
│                                        ▼                                                              │
│  Step 4 · vSAN Configuration                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  VxRail Manager automatically claims all eligible disks  ·  assigns cache+capacity tiers              │
│  OSA: NVMe/SSD cache device + SSD/HDD capacity per disk group per node                                │
│  ESA (VxRail 8.x+): all NVMe — single tier; no explicit cache assignment                              │
│  vSAN health checks run automatically: network, disk, data, cluster health all green                  │
│  Create production SPBM policy: RAID-1 FTT=1 minimum  ·  apply to VxRail Manager VM                   │
│                                                                                                       │
│                                        │  validate VMkernel configuration                             │
│                                        ▼                                                              │
│  Step 5 · Network Validation                                                                          │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Verify vmk0 (management), vmk1 (vMotion), vmk2 (vSAN) present on ALL nodes                           │
│  MTU test: vmkping -I vmk2 -d -s 8972 <peer-vsan-vmk-ip>  ·  zero packet loss required                │
│  Verify OMIVV plugin installed in vCenter  ·  hardware inventory visible under each host              │
│  Confirm VxRail Plugin in vCenter shows cluster healthy                                               │
│                                                                                                       │
│                                        │  enable support and harden                                   │
│                                        ▼                                                              │
│  Step 6 · Post-Deploy Hardening                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────            │
│  Change VxRail Manager mystic password  ·  change all iDRAC passwords (default: root/Calvin)          │
│  Enable SupportAssist in VxRail Plugin  ·  configure Dell Connect (HTTPS outbound only)               │
│  Enable normal lockdown mode on all hosts  ·  disable SSH post-config                                 │
│  Configure vCenter VAMI file-based backup (daily, retain 3)  ·  set up LCM upgrade baseline           │
│  Take VM-level snapshot/backup of VxRail Manager VM  ·  document final IP and DNS inventory           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>How it works, node types, deployment models, and integrations.</span>
</a>

<a class="kb-card" href="deploy/">
  <strong>Deploy</strong>
  <span>Step-by-step initial VxRail cluster deployment using the First Run Wizard.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, LCM upgrades, expansion, and backup.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and Dell escalation.</span>
</a>

</div>
