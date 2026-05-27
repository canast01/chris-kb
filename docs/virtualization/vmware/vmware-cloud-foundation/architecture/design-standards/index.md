# VCF — Design Standards

```text
VCF Physical and Logical Design Requirements
┌─────────────────────────────────────────────────────┐
│  Underlay Network (physical)                        │
│                                                     │
│  ToR Switch A ─────────────── ToR Switch B          │
│       │   (dual uplinks, LACP or active-active)     │
│       └────────── ESXi Hosts ─────────────┘         │
│                   vmk0  vmk1  vmk2  vmkX            │
│                   Mgmt  vMot  vSAN  TEP             │
│                   VLAN  VLAN  VLAN  VLAN            │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  VMkernel Requirements (per host)                   │
│                                                     │
│  vmk0  Management      ≥ 1 GbE   VCF-managed VDS    │
│  vmk1  vMotion         ≥ 10 GbE  VCF-managed VDS    │
│  vmk2  vSAN            ≥ 10 GbE  VCF-managed VDS    │
│  vmkX  NSX TEP         ≥ 10 GbE  VCF-managed VDS    │
│                                                     │
│  Standard vSwitches are NOT supported               │
└─────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Management Domain Minimum Build                    │
│                                                     │
│  4 x ESXi hosts (vSAN-Ready Node, HCL-validated)    │
│  SDDC Manager   4 vCPU / 16 GB  (8/24 recommended)  │
│  vCenter        small 14 GB RAM (medium 24 GB)      │
│  NSX Manager    3-node cluster                      │
│                                                     │
│  DNS: forward + reverse for all FQDNs before deploy │
│  NTP: all components synchronised                   │
└─────────────────────────────────────────────────────┘
```
┌───────────────────────────── VMware Cloud Foundation — Design Standards ──────────────────────────────┐
│                                                                                                       │
│  VCF design standards define domain layout, host sizing, VLAN scheme, NSX topology,                   │
│  and upgrade sequencing following VMware VCF design guidance.                                         │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Domain Design                 │  │                Network Design               │   │
│   │          1 mgmt domain: min 4 hosts          │  │           VLANs: mgmt/vSAN/vMotion          │   │
│   │             1+ workload domains              │  │          NSX overlay: VXLAN/GENEVE          │   │
│   │            Separate VC per domain            │  │            25GbE minimum uplinks            │   │
│   │           NSX: shared or dedicated           │  │             MTU 9000: all VLANs             │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Mgmt domain hosts VCF tooling; workload domains host applications.                                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Upgrade Standards               │  │               Sizing Standards              │   │
│   │           SDDC Mgr: upgrade via UI           │  │            Mgmt hosts: 512GB RAM+           │   │
│   │         Bundle: download from depot          │  │         Workload: right-size for app        │   │
│   │          Upgrade order: VCF defined          │  │             vSAN: HCL disks only            │   │
│   │         Pre-check: run before apply          │  │             NVMe/SSD: ESA or OSA            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Servers must be on VCF HCL; 25GbE TOR switches; dedicated management network;                        │
│  separate OOB management (iDRAC/iLO) for host lifecycle.                                              │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Management domain= first VCF domain; hosts SDDC Manager + shared infra                               │
│  Workload domain = application cluster; separate lifecycle from mgmt                                  │
│  SDDC Manager  = automation hub; upgrade bundles applied here                                         │
│  Bundle        = VCF update package; downloaded from VMware depot                                     │
│  Pre-check     = automated readiness validation before applying bundle                                │
│  NSX shared    = one NSX manager serving multiple domains                                             │
│  NSX dedicated = per-domain NSX manager for isolation                                                 │
│  GENEVE        = NSX-T overlay protocol; replaced VXLAN                                               │
│  MTU 9000      = jumbo frames; required for all VCF network segments                                  │
│  OOB           = Out-of-Band management; iDRAC/iLO for host power/BIOS                                │
│  HCL           = Hardware Compatibility List; VCF-specific requirements                               │
│  Upgrade order = VCF prescribes sequence; SDDC Mgr → vCenter → ESXi → NSX                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Supported Configurations

| Feature | Supported | Notes |
|---|---|---|
| vSAN ESA (Express Storage Architecture) | VCF 5.1+ | Requires NVMe drives |
| vSAN OSA (Original Storage Architecture) | All versions | Hybrid and all-flash |
| Stretched clusters | Yes | Requires witness host |
| NSX Federation | VCF 4.3+ | Cross-site policy management |
| Workload domains with FC storage | No | VCF uses vSAN only for principal storage |

## Compliance Checks in SDDC Manager

```bash
# SDDC Manager UI — run before any upgrade:
# Lifecycle Management → Precheck

# Precheck validates:
# - DNS resolution for all components
# - NTP synchronisation
# - Certificate expiry
# - vSAN health
# - Network pool capacity
# - Password rotation status
```
