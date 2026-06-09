# Amazon EVS — How It Works

<div class="kb-summary">
Amazon EVS runs VMware Cloud Foundation on dedicated bare-metal EC2 instances inside your VPC. The cluster nodes are physical hosts you don't share with other tenants; VMware components run natively, not in VMs.
</div>

```text
┌────────────────────────────────────── Amazon EVS — How It Works ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   EVS = VCF on AWS bare-metal; runs in your VPC; treated like on-prem vSphere by VMware tools │   │
│   │   Bare-metal EC2 (i3en, i4i): dedicated physical hosts; ESXi installed by AWS on deploy       │   │
│   │   NSX-T overlay: separate VLAN + Geneve tunnel; uses ENIs on bare-metal hosts as uplinks      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   VPC                                                                                         │   │
│   │   ┌──────────────────────────┐    ┌──────────────────────────┐    ┌────────────────────────┐  │   │
│   │   │   ESXi Host 1 (i4i.metal)│    │   ESXi Host 2            │    │   ESXi Host 3+         │  │   │
│   │   │   ─────────────          │    │   ─────────────           │    │   ─────────────        │  │  │
│   │   │  vSAN disk groups        │    │  vSAN disk groups         │    │  vSAN disk groups      │  │  │
│   │   │  NSX-T vtep (ENI)        │    │  NSX-T vtep (ENI)         │    │  NSX-T vtep (ENI)      │  │  │
│   │   │  mgmt ENI (VPC-native)   │    │  mgmt ENI (VPC-native)    │    │  mgmt ENI (VPC-native) │  │  │
│   │   └──────────────────────────┘    └──────────────────────────┘    └────────────────────────┘  │   │
│   │                │                              │                               │                 │ │
│   │                └──────────────────────────────┴───────────────────────────────┘                 │ │
│   │                                     vSAN Cluster                                                │ │
│   │                                                                                                  ││
│   │   ┌─────────────────────────────┐  ┌─────────────────────────────────────────────────────────┐  │ │
│   │   │   VCF Management Domain     │  │   NSX-T Overlay                                         │  │ │
│   │   │   ─────────────             │  │   ─────────────                                          │  ││
│   │   │  vCenter (VM on ESXi)       │  │  NSX Manager (3-node cluster VM)                        │  │ │
│   │   │  SDDC Manager               │  │  Geneve tunnels between ESXi hosts                      │  │ │
│   │   │  NSX Manager                │  │  Distributed router + firewall                          │  │ │
│   │   │  vSAN datastore             │  │  T0 router → VPC subnet (BGP or static)                 │  │ │
│   │   └─────────────────────────────┘  └─────────────────────────────────────────────────────────┘  │ │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    EVS         = Amazon Elastic VMware Service; VCF running on bare-metal EC2 in your VPC             │
│    i4i.metal   = Common EVS host type; NVMe-based vSAN; 128 vCPU, 1 TB RAM per host                   │
│    ENI         = Elastic Network Interface; used for VMkernel and NSX-T VTEP traffic                  │
│    VTEP        = VXLAN Tunnel End Point; NSX-T overlay transport endpoint per host                    │
│    HCX         = VMware Hybrid Cloud Extension; live migration between on-prem and EVS                │
│    Direct Connect= Dedicated private network link from on-premises data center to AWS                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Bare-Metal Host Model

EVS allocates dedicated physical EC2 bare-metal instances (i3en.metal or i4i.metal) to the cluster. Each host:
- Runs ESXi directly on hardware (no hypervisor underneath)
- Has multiple ENIs: one for management/vMotion/vSAN, one or more for NSX-T VTEP overlay
- Contributes local NVMe disks to a vSAN cluster (HCI model, same as on-premises)
- Is billed per-hour; minimum 3 hosts required

## VPC Integration

```text
VPC → Subnet per VMkernel type:
  Management subnet: vCenter, SDDC Manager, ESXi DCUI, vSAN management VMkernel
  VTEP subnet:       NSX-T Geneve tunnel traffic between hosts
  VM network:        T1 router downlinks; workload VM traffic exits via T0 → ENI → VPC routing
  Transit Gateway:   Connect EVS VPC to other VPCs or on-premises via Direct Connect
```

## vSAN Architecture

```bash
# EVS uses vSAN OSA (Original Storage Architecture) or vSAN ESA (Express Storage Architecture)
# i4i.metal hosts with NVMe: recommended for vSAN ESA
# Minimum cluster: 3 hosts (RF=1 FTT) — production: 4+ hosts (RF=1, FTT=1 or FTT=2)

# Storage policy example for EVS workloads
# SPBM policy: RAID-1 FTT=1 (2 copies; 1 host failure tolerated)
# For stretched cluster: RAID-1 FTT=1 site + FTT=0 host (vSAN Stretched Cluster)
```

## NSX-T Overlay Network

```text
NSX-T on EVS uses Geneve tunnels over dedicated ENIs:

  On-premises DC → Direct Connect → AWS → VPC ENI (T0 uplink)
                                           T0 Router (BGP to VPC)
                                           T1 Routers (per tenant/segment)
                                           Logical Segments (VM networks)
                                           Distributed Firewall (micro-segmentation)

Key difference from on-prem: No physical switches managed by you.
AWS VPC routing tables = underlay network. NSX-T is pure overlay on top.
```

## VCF Component Versions

EVS runs a specific VCF version aligned with the AWS service launch. AWS manages:
- ESXi host OS provisioning (you do not install ESXi)
- AWS-side networking (VPC ENI attachment)
- Hardware failures (host replacement via AWS console or API)

You manage:
- VCF lifecycle (SDDC Manager upgrades)
- VM workloads
- NSX-T policies
- vSAN storage policies
