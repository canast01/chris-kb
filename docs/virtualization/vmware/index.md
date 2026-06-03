# VMware Platform

<div class="kb-summary">
VMware platform knowledge base covering the full VMware stack — vCenter, ESXi, vSAN, NSX, VCF, VxRail, Horizon, SRM, vSphere Replication, and the Aria Suite. Includes architecture references, operational procedures, CLI commands, health checks, lifecycle management, and troubleshooting guides.
</div>

```text
┌────────────────────────────────────── VMware Platform Landscape ──────────────────────────────────────┐
│                                                                                                       │
│   ┌────────────────────┐  ┌────────────────────┐  ┌───────────────────────────────────────────────┐   │
│   │      vCenter       │  │       VxRail       │  │                   Aria Suite                  │   │
│   │      (Manage)      │  │    (Appliance)     │  │    Ops/Logs   │   Automation  │Suite Lifecycle│   │
│   │    Web UI & API    │  │    Turnkey HCI     │  │ Monitor/Alert │  IaC / Deploy │ Patch/Upgrade │   │
│   │ SSO · Roles · LDAP │  │   Dell + VMware    │  │   Operations  │   Blueprints  │  Certificates │   │
│   │  vLCM · Licensing  │  │   All-in-one HCI   │  │     ↓ monitors & manages all layers below     │   │
│   └────────────────────┘  └────────────────────┘  └───────────────┴───────────────┴───────────────┘   │
│                                                                                                       │
│    vCenter/VxRail: control plane for vSphere  ·  Aria Suite: monitors all layers                      │
│                                                                                                       │
│             ▼                       ▼                                     ▼                           │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                  vSphere Cluster (ESXi Hosts)                                 │   │
│   │               Type-1 hypervisor: runs directly on hardware — no host OS required              │   │
│   │                     Cluster features: HA · DRS · vMotion · Fault Tolerance                    │   │
│   │                                                                                               │   │
│   │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────────────────────┐ │   │
│   │  │  ESXi-01   │  │  ESXi-02   │  │  ESXi-03   │  │  ESXi-04   │  │  Each host: 50-200+ VMs  │ │   │
│   │  │(Hypervisor)│  │(Hypervisor)│  │(Hypervisor)│  │(Hypervisor)│  │ Types: web, DB, app, AD  │ │   │
│   │  │  ┌─────┐   │  │  ┌─────┐   │  │  ┌─────┐   │  │  ┌─────┐   │  │ vMotion: live migration  │ │   │
│   │  │  │ VMs │   │  │  │ VMs │   │  │  │ VMs │   │  │  │ VMs │   │  │  HA: restart on failure  │ │   │
│   │  └──┴─────┴───┘  └──┴─────┴───┘  └──┴─────┴───┘  └──┴─────┴───┘  └──────────────────────────┘ │   │
│   │                                                                                               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Integrated into vSphere — part of the hypervisor, not separate appliances:                         │
│                                                                                                       │
│                         ▼                                                 ▼                           │
│                                                                                                       │
│   ┌────────────────────────────────────────────┐  ┌───────────────────────────────────────────────┐   │
│   │      vSAN (Software-Defined Storage)       │  │       NSX (Software-Defined Networking)       │   │
│   │        Pooled from ESXi local disks        │  │    Virtual switches + distributed firewall    │   │
│   │      Policy-based; no external array       │  │     Micro-segmentation & east-west routing    │   │
│   └────────────────────────────────────────────┘  └───────────────────────────────────────────────┘   │
│                                                                                                       │
│    Add-on products — licensed separately, deployed on top of vSphere:                                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        Horizon (VDI)        │  │    Site Recovery Manager    │  │     vSphere Replication     │   │
│   │          (Desktops)         │  │      (DR Orchestration)     │  │       (VM Replication)      │   │
│   │     VDI + app publishing    │  │     Failover + Failback     │  │    RPO-based replication    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                               VMware Cloud Foundation (VCF/SDDC)                              │   │
│   │              Packages & delivers the full SDDC: vSphere + vSAN + NSX + Lifecycle              │   │
│   │                                                                                               │   │
│   │  ┌───────────────────────────────────────────┐  ┌───────────────────────────────────────────┐ │   │
│   │  │                SDDC Manager               │  │        Tanzu (Kubernetes Platform)        │ │   │
│   │  │       Lifecycle orchestrator for VCF      │  │          Container Orchestration          │ │   │
│   │  │      Bringup · Upgrades · Compliance      │  │         Workload domain within VCF        │ │   │
│   │  └───────────────────────────────────────────┘  └───────────────────────────────────────────┘ │   │
│   │                                                                                               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  CPU cores · RAM (GBs to TBs per host) · NIC (10/25/100 GbE) · NVMe/SSD/HDD · Power & Cooling         │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VM      = a software-emulated computer; runs a full OS + apps inside a physical host                 │
│  ESXi    = Type-1 hypervisor; installed directly on bare metal — no host OS needed                    │
│  vSAN    = pools local server disks into shared storage — no separate SAN array needed                │
│  NSX     = software-defined networking; virtual switches, routers & distributed firewall              │
│  HA      = High Availability; vSphere auto-restarts VMs on another host if one fails                  │
│  DRS     = Distributed Resource Scheduler; auto-balances VM workload across ESXi hosts                │
│  vMotion = live migration of a running VM between ESXi hosts with zero downtime                       │
│  SSO     = Single Sign-On; central identity used by all vCenter/vSphere authentication                │
│  vLCM    = vSphere Lifecycle Manager; patches ESXi hosts and manages firmware baselines               │
│  VDI     = your desktop OS runs in the data centre; you stream it to any device remotely              │
│  SRM     = Site Recovery Manager; orchestrates DR failover using pre-defined recovery plans           │
│  vSR     = vSphere Replication; replicates VMs to a remote site; provides recovery point for SRM      │
│  HCI     = Hyper-Converged Infrastructure; compute + storage + networking in one appliance            │
│  SDDC Mgr= VCF lifecycle orchestrator; automates bringup, upgrades & compliance checks                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

```text
┌──────────────────────────── VMware Platform — Installation Sequence ──────────────────────────────────┐
│                                                                                                       │
│  Step 1 · Physical Infrastructure                                                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Rack and cable servers  ·  Confirm power + cooling capacity                                          │
│  Configure ToR switches — VLANs: Management | vMotion | vSAN | NSX TEP | VM Uplink                    │
│  MTU 9000 on vSAN + TEP switch ports  ·  Port channels / LAGs configured on uplinks                   │
│  IPMI / iDRAC: out-of-band management on every host  ·  Host firmware at minimum required version     │
│  DNS: A-records for all hosts + VIPs (vCenter FQDN, NSX Manager VIP, LCM, Edge nodes)                 │
│  NTP: two sources reachable from all hosts  ·  Time sync verified before any software deploy          │
│                                                                                                       │
│                                      │  install ESXi ISO on each host                                 │
│                                      ▼                                                                │
│  Step 2 · ESXi  (repeat for every host)                                                               │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Boot from ISO  ·  Set root password  ·  vmk0: management IP, subnet mask, default gateway            │
│  Set hostname + DNS suffix  ·  Configure NTP  ·  Enable SSH temporarily for initial setup             │
│  Verify HTTPS/443 reachable from jump host before continuing to the next host                         │
│  All hosts must be up and reachable on management VLAN before deploying vCenter                       │
│  Disable SSH on each host after initial config; re-enable only when needed for maintenance            │
│                                                                                                       │
│                                      │  deploy VCSA OVA to first ESXi host                            │
│                                      ▼                                                                │
│  Step 3 · vCenter Server (VCSA)                                                                       │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Deploy VCSA OVA — Stage 1: appliance config  ·  Stage 2: SSO domain + vCenter services               │
│  SSO domain: vsphere.local  ·  Assign management IP, hostname, DNS, NTP for the VCSA                  │
│  Create Datacenter + Cluster  ·  Add all ESXi hosts to cluster inventory                              │
│  Create vDS  ·  Migrate vmk0 (mgmt) to vDS  ·  Add vmk1 (vMotion) + vmk2 (vSAN) per host              │
│  Enable HA with admission control  ·  DRS: fully automated  ·  Create vLCM baseline image             │
│  Connect Active Directory as identity source  ·  Create admin roles  ·  Assign AD groups              │
│  Enable VCSA file-based backup to SFTP — schedule daily  ·  Confirm backup restores successfully      │
│                                                                                                       │
│      │  enable vSAN on cluster                                       │  deploy NSX Manager OVA (×3)   │
│      ▼                                                               ▼                                │
│  ┌──────────────────────────────────────────────┐  ┌──────────────────────────────────────────────┐   │
│  │  Step 4 · vSAN                               │  │  Step 5 · NSX                                │   │
│  │  Cluster → Configure → vSAN → Turn on        │  │  Deploy NSX Manager OVA ×3 (cluster VIP)     │   │
│  │  Claim disks: assign cache + capacity role   │  │  Register vCenter as compute manager         │   │
│  │  Disk groups: 1 cache SSD + 1–7 cap disks    │  │  Create Transport Zones: Overlay + VLAN TZ   │   │
│  │  Tag vmk2 for vSAN; verify unicast agents    │  │  Create Uplink Profile: MTU 9000, LAG mode   │   │
│  │  MTU test: vmkping -I vmk2 -d -s 8972        │  │  Config host transport nodes (TEP vmk)       │   │
│  │  Skyline Health: all checks green            │  │  Deploy Edge nodes ×2  ·  Edge Cluster       │   │
│  │  Create SPBM policies (FTT level, RAID type) │  │  T0 Gateway: BGP or static peer to router    │   │
│  │  Enable Performance Service                  │  │  T1 Gateway: connected to T0, NAT + LB       │   │
│  │  Enable dedup + compression if applicable    │  │  Create overlay segments for workloads       │   │
│  │  Verify object policy compliance: all green  │  │  DFW: define groups + firewall rule sets     │   │
│  └──────────────────────────────────────────────┘  └──────────────────────────────────────────────┘   │
│      │                                                               │                                │
│      └──────────────────────────────┬────────────────────────────────┘                                │
│                                     │  (optional) deploy monitoring layer                             │
│                                     ▼                                                                 │
│  Step 6 · Aria Suite  (optional — deploy after vCenter is stable)                                     │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  Deploy Aria Suite Lifecycle Manager (LCM) OVA first — LCM manages all Aria installs + upgrades       │
│  Via LCM → Aria Operations (vROps): register vCenter adapter, import vSAN + NSX mgmt packs            │
│  Via LCM → Aria Operations for Logs: deploy log agents on ESXi, configure syslog forwarding           │
│  Via LCM → Aria Automation: connect vCenter + NSX endpoints, create cloud accounts + blueprints       │
│  Via LCM → Aria Operations for Networks (optional): NSX flow analysis + physical switch visibility    │
│  Configure alert policies: capacity > 70%, health score < 80%, resync throughput, cert expiry         │
│                                                                                                       │
│                                     │  (optional) add-on products — any order after Step 3            │
│                                     ▼                                                                 │
│  Step 7 · Add-on Products                                                                             │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  SRM: deploy SRM appliance + vSphere Replication at both sites  ·  configure recovery plans           │
│  Horizon: deploy Connection Servers + Unified Access Gateway  ·  configure desktop + app pools        │
│  HCX: deploy HCX Manager  ·  activate licence  ·  pair sites  ·  create service mesh                  │
│  Tanzu: enable Workload Management on cluster  ·  deploy Supervisor  ·  create namespaces + classes   │
│                                                                                                       │
│  VCF path:    SDDC Manager automates steps 2–5 via a single guided bringup workflow                   │
│  VxRail path: Dell HCI appliance — VxRail Manager handles ESXi + vCenter + vSAN automatically         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="vcenter/">
  <strong>vCenter</strong>
  <span>Management control plane, inventory, RBAC, alarms, vLCM, and SSO.</span>
</a>

<a class="kb-card" href="esxi/">
  <strong>ESXi</strong>
  <span>Type-1 hypervisor, host configuration, networking, and storage.</span>
</a>

<a class="kb-card" href="vsan/">
  <strong>vSAN</strong>
  <span>Software-defined storage, disk groups, storage policies, and health.</span>
</a>

<a class="kb-card" href="nsx/">
  <strong>NSX</strong>
  <span>Software-defined networking, segments, gateways, and distributed firewall.</span>
</a>

<a class="kb-card" href="vmware-cloud-foundation/">
  <strong>VMware Cloud Foundation</strong>
  <span>Full SDDC stack delivery, SDDC Manager lifecycle, and workload domains.</span>
</a>

<a class="kb-card" href="vxrail/">
  <strong>VxRail</strong>
  <span>Dell HCI appliance, VxRail Manager, node expansion, and lifecycle.</span>
</a>

<a class="kb-card" href="aria-operations/">
  <strong>Aria Operations</strong>
  <span>Monitoring, alerting, capacity analytics, and vSAN dashboards.</span>
</a>

<a class="kb-card" href="aria-operations-for-logs/">
  <strong>Aria Operations for Logs</strong>
  <span>Log aggregation, analysis, and alerting across the VMware platform.</span>
</a>

<a class="kb-card" href="aria-operations-for-networks/">
  <strong>Aria Operations for Networks</strong>
  <span>Network visibility, flow analysis, and security posture across NSX and physical.</span>
</a>

<a class="kb-card" href="aria-automation/">
  <strong>Aria Automation</strong>
  <span>IaC blueprints, self-service catalogue, and cloud template deployment.</span>
</a>

<a class="kb-card" href="aria-suite-lifecycle/">
  <strong>Aria Suite Lifecycle</strong>
  <span>Lifecycle orchestrator for deploying, patching, and upgrading the Aria Suite.</span>
</a>

<a class="kb-card" href="horizon/">
  <strong>Horizon</strong>
  <span>Virtual desktop infrastructure, application publishing, and Connection Server.</span>
</a>

<a class="kb-card" href="srm/">
  <strong>Site Recovery Manager</strong>
  <span>DR orchestration, recovery plans, failover, and failback.</span>
</a>

<a class="kb-card" href="vsphere-replication/">
  <strong>vSphere Replication</strong>
  <span>VM replication to secondary sites, RPO configuration, and recovery.</span>
</a>

<a class="kb-card" href="tanzu/">
  <strong>Tanzu</strong>
  <span>Kubernetes workload domains, cluster provisioning, and container platform.</span>
</a>

</div>
