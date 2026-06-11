# Amazon EVS — Design Standards

<div class="kb-summary">
EVS cluster sizing, AZ placement, CIDR planning, Direct Connect bandwidth requirements, and VPC design rules for production EVS deployments.
</div>

```text
┌──────────────────────────────────── Amazon EVS — Design Standards ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Minimum: 3 hosts (FTT=1 RAID-1); production: 4+ hosts; stretched: 6+ (3 per AZ + witness)  │    │
│   │   CIDR: reserve /20 for management + /20 for NSX-T VTEP + /16 for workload segments           │   │
│   │   Direct Connect: minimum 1 Gbps per 100 VMs being migrated with HCX                          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Host Sizing            │  │      Network Design          │  │      AZ Placement           │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  i4i.metal: 128vCPU/1TB    │  │  /20 management subnet       │  │  Single AZ: simplest        │   │
│   │  3 hosts min, 16 hosts max │  │  /20 VTEP overlay subnet     │  │  Multi-AZ: stretched vSAN   │   │
│   │  vSAN ESA on NVMe          │  │  /16+ for workload VMs       │  │  Witness: t3.medium in 3rd  │   │
│   │  Scale: add 1 host at time │  │  Avoid overlap with on-prem  │  │  AZ: DR isolation           │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  i4i.metal    = EVS bare-metal host; 128 vCPU, 1 TB RAM, 30 TB NVMe — standard choice                 │
│  i3en.metal   = Storage-heavy EVS host; 96 vCPU, 768 GB RAM, 60 TB NVMe                               │
│  FTT          = Failures to Tolerate; FTT=1 (RAID-1) needs 3 hosts; FTT=2 needs 5 hosts               │
│  vSAN ESA     = Express Storage Architecture; NVMe-optimised single tier; no cache/capacity split     │
│  HCI          = Hyper-Converged Infrastructure; compute + storage on the same bare-metal hosts        │
│  AZ           = Availability Zone; physically isolated AWS data center with independent power         │
│  Stretched cluster = vSAN across 2 AZs; requires witness VM in a third AZ for quorum                  │
│  Witness VM   = Lightweight t3.medium EC2 in 3rd AZ; holds tiebreaker vote; no data stored            │
│  VTEP subnet  = Dedicated /20 for NSX-T Geneve overlay tunnel endpoints on each host ENI              │
│  Direct Connect = Private dedicated link from on-prem to AWS; required for HCX production use         │
│  CIDR         = Plan 3 non-overlapping IP ranges: management / VTEP overlay / workload VMs            │
│  Admission control = vSphere HA policy reserving cluster capacity for host failure recovery           │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Host Type Selection

| Instance | vCPU | RAM | Raw Storage | Use Case |
|---|---|---|---|---|
| i3en.metal | 96 | 768 GB | 60 TB NVMe (15×4TB) | Large vSAN capacity |
| i4i.metal | 128 | 1024 GB | 30 TB NVMe (8×3.75TB) | High-performance (vSAN ESA) |
| r6i.metal | 128 | 1024 GB | EBS only (not vSAN) | External storage (NFS/iSCSI) |

- Start with i4i.metal for new deployments (vSAN ESA support)
- All hosts in a cluster must be the same instance type

## Cluster Sizing

```text
Minimum (dev/test):
  3 hosts × i4i.metal
  vSAN policy: RAID-1 FTT=1
  Usable capacity: ~50% raw (metadata + slack)

Production baseline:
  4 hosts — FTT=1 can survive 1 host failure
  Hosts: i4i.metal

Production recommended:
  6 hosts — allows FTT=2 (2 concurrent host failures tolerated)
  Or: FTT=1 with capacity headroom for host replacement without evacuation

Stretched (multi-AZ):
  6 hosts minimum: 3 in AZ-a, 3 in AZ-b
  1 witness appliance in AZ-c (t3.medium EC2 or dedicated)
  vSAN policy: RAID-1 FTT=1 (site-level) + FTT=0 host
```

## VPC and CIDR Design

```text
Subnet allocation per EVS cluster:

  10.0.0.0/20  — Management (vCenter, SDDC Manager, NSX Manager, ESXi mgmt VMkernel)
  10.0.16.0/20 — NSX-T VTEP (Geneve tunnel overlay; one ENI per host)
  10.0.32.0/20 — vMotion VMkernel (dedicated subnet recommended)
  10.0.48.0/20 — vSAN VMkernel (dedicated for performance isolation)
  10.1.0.0/16  — Workload VM segments (NSX-T logical networks, routed via T0)

Rules:
  - No overlap with on-premises CIDR ranges
  - VPC must be in the same region as the EVS cluster
  - Security groups on ENIs: allow VMware ports (443, 902, 8301, etc.)
  - VPC route table: workload subnets routed to ENI of T0 uplink
```

## Direct Connect Bandwidth

```text
Purpose                     Minimum bandwidth
────────────────────────────────────────────────────────────
Management reachability     10 Mbps (vCenter, SDDC access)
HCX cold migration          100 Mbps per concurrent migration
HCX vMotion (live)          1 Gbps per 100 VMs actively moving
HCX bulk migration (WAN opt)100 Mbps (compressed; effective rate higher)
Production workload access  Size for peak VM traffic + 30% headroom
````

Use Direct Connect dedicated connection (1 Gbps or 10 Gbps) for production. VPN is acceptable for small test clusters.

## Operational Design Rules

- **Maintenance windows**: host upgrades are one host at a time via vSAN evacuation; plan for 30-60 min per host
- **Replacement nodes**: when AWS replaces a failed host, vSAN rebuilds data automatically; time depends on data volume
- **vSAN slack**: keep ≥ 30% free capacity to allow host replacement without policy downgrade
- **NSX Edge sizing**: for high-throughput workloads use dedicated Edge cluster (separate hosts); don't co-locate Edge VMs on compute hosts
- **DNS**: create Route 53 private hosted zone or use on-premises DNS reachable via Direct Connect for VCF component names
