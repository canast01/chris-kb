# VMware Platform

<div class="kb-summary">
VMware platform knowledge base covering the full VMware stack — vCenter, ESXi, vSAN, NSX, VCF, VxRail, Horizon, SRM, vSphere Replication, and the Aria Suite. Includes architecture references, operational procedures, CLI commands, health checks, lifecycle management, and troubleshooting guides.
</div>

```powershell
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
