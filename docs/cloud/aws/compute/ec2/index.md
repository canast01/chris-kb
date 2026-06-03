# AWS EC2


<div class="kb-summary">
AWS EC2 reference covering Overview, Where It Fits, Daily Checks, Health Commands, Common Issues and 3 more sections.
</div>

```text
┌────────────────────────────────────────── AWS Compute — EC2 ──────────────────────────────────────────┐
│                                                                                                       │
│  Elastic Compute Cloud: instance types, purchasing options, networking, and storage.                  │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Instance Families               │  │              Purchasing Options             │   │
│   │         General: m7i, t3 (burstable)         │  │          On-demand: pay per second          │   │
│   │           Compute: c7i (high CPU)            │  │          Reserved: 1/3yr commitment         │   │
│   │            Memory: r7i (high RAM)            │  │          Spot: spare capacity, -90%         │   │
│   │          Storage: i4i (NVMe local)           │  │          Savings plan: flexible RI          │   │
│   │           Accelerated: p4/g5 (GPU)           │  │          Dedicated host: compliance         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Instance family chosen for workload type; purchasing model optimises cost                            │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                  Networking                  │  │                   Storage                   │   │
│   │          ENI: virtual network card           │  │              Root EBS: OS disk              │   │
│   │            Public IP: auto-assign            │  │          Data EBS: persistent block         │   │
│   │          Elastic IP: static public           │  │        Instance store: ephemeral NVMe       │   │
│   │         Enhanced networking: SR-IOV          │  │            EFS mount: shared NFS            │   │
│   │       Placement group: latency/spread        │  │          FSx: Windows/Lustre mount          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Nitro hypervisor · Nitro cards (network/storage) · physical host · AZ data centre                    │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ENI             = Elastic Network Interface; virtual NIC attachable to EC2                           │
│  Elastic IP      = Static public IPv4 address; persists across stop/start                             │
│  SR-IOV          = Single Root I/O Virtualisation; enables enhanced networking                        │
│  Placement group = Cluster (low latency) or spread (fault isolation) placement                        │
│  Spot instance   = Uses spare EC2 capacity; can be interrupted with 2-min notice                      │
│  Reserved instance= 1 or 3-year commitment for up to 72% discount                                     │
│  Savings plan    = Flexible commitment by $/hour; applies across instance families                    │
│  Dedicated host  = Physical server for BYOL or compliance isolation requirements                      │
│  Instance store  = NVMe SSD physically attached to host; lost on stop/terminate                       │
│  Burstable (t3)  = Accumulates CPU credits when idle; bursts above baseline                           │
│  Nitro hypervisor= AWS-built hypervisor offloading I/O to dedicated Nitro cards                       │
│  IMDS v2         = Instance Metadata Service v2; token-required for security                          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Overview

AWS EC2 notes for day-to-day infrastructure operations.

## Where It Fits

Use this page for build work, support checks, troubleshooting, standards, and operational review.

## Daily Checks

| Check | Command | Notes |
|---|---|---|
| Confirm service health. |  |  |
| Review alerts. |  |  |
| Check recent changes. |  |  |
| Confirm capacity and performance are within normal range. |  |  |

## Health Commands

```bash
# Add environment-specific commands here
```

## Common Issues

- Misconfiguration after change work.
- Missing access or permissions.
- Alert noise without clear ownership.
- Drift from documented standards.

## Operational Tasks

| Task | Command |
|---|---|
| Review current configuration. |  |
| Validate dependencies. |  |
| Record changes. |  |
| Confirm monitoring coverage. |  |

## Upgrade Notes

- Check release notes before upgrades.
- Validate backup or rollback options.
- Confirm maintenance window and communication plan.
- Test after the change.

## Best Practices

| Recommendation | Detail |
|---|---|
| Keep naming consistent. | Keep naming consistent. |
| Document ownership. | Document ownership. |
| Use least privilege access. | Use least privilege access. |
| Validate changes after implementation. | Validate changes after implementation. |

---

## EC2 Purchase Options

```text
┌────────────────────── EC2 Purchase Options — Discount and Commitment Comparison ──────────────────────┐
│                                                                                                       │
│    Six purchase options balance cost, flexibility, and availability guarantees.                       │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     On-Demand and Reserved                   │  │      Savings Plans                          │   │
│   │  On-Demand: no commitment, per-second        │  │  Compute SP: EC2+Fargate+Lambda             │   │
│   │  Full price; start/stop anytime              │  │  Any instance type/family/Region            │   │
│   │  Standard Reserved: 1 or 3 yr commit         │  │  Up to 66% discount; most flexible          │   │
│   │  Same type only; up to 72% discount          │  │  EC2 Instance SP: same family/Region        │   │
│   │  Convertible Reserved: exchange allowed      │  │  Up to 72% discount; less flexible          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Savings Plans and Reserved Instances both require upfront commitment for discount.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Spot Instances                           │  │      Dedicated Options                      │   │
│   │  Uses spare AWS capacity                     │  │  Dedicated Host: physical server            │   │
│   │  Up to 90% discount off On-Demand            │  │  BYOL licensing; full host control          │   │
│   │  2-minute interruption notice from AWS       │  │  Dedicated Instance: on dedicated HW        │   │
│   │  Not for critical/persistent workloads       │  │  Capacity Reservation: guarantee AZ         │   │
│   │  Spot Fleets: mix types for target cap       │  │  No discount; ensures capacity avail        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    EC2 runs on Nitro hypervisor · Nitro cards offload I/O · physical hosts in AZs                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    On-Demand         = Full price; no commitment; billed per second after first minute                │
│    Standard RI       = 1/3yr commit to specific type; up to 72% off; not exchangeable                 │
│    Convertible RI    = 1/3yr commit; can exchange instance family/OS/tenancy; 66% off                 │
│    Compute Savings Plan = $/hr commitment; applies to EC2/Fargate/Lambda; 66% off                     │
│    EC2 Instance SP   = $/hr for a specific family and Region; up to 72% off                           │
│    Spot              = Spare capacity; up to 90% off; can be reclaimed with 2-min notice              │
│    Spot interruption = AWS reclaims Spot with 2-minute warning; use checkpointing                     │
│    Dedicated Host    = Physical server; BYOL; see sockets/cores; compliance isolation                 │
│    Capacity Reservation= Reserve EC2 capacity in a specific AZ; no commitment discount                │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```



---

## EC2 Instance Type Families

```text
┌───────────────────────── EC2 Instance Type Families — Workload Optimisation ──────────────────────────┐
│                                                                                                       │
│    Instance family letter tells you the workload optimisation; generation number follows.             │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     General Purpose                          │  │      Compute Optimised                      │   │
│   │  m: balanced CPU/memory (m7i, m6i)           │  │  c: high compute-to-memory (c7i,c6i)        │   │
│   │  t: burstable with CPU credits (t3)          │  │  HPC, batch jobs, ML inference              │   │
│   │  Web servers, app servers, dev/test          │  │  Gaming, ad serving, media encode           │   │
│   │  a: ARM-based Graviton (cost-efficient)      │  │  c7g: Graviton3; best $/vCPU compute        │   │
│   │  mac: macOS dev environments (M1/M2)         │  │  Prefix c = compute optimised family        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Family letter = optimisation type; generation = newer hardware; suffix = features.                 │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Memory Optimised                         │  │      Storage / Accelerated Computing        │   │
│   │  r: high RAM (r7i up to 768 GiB)             │  │  i: NVMe SSD storage (i4i, i3en)            │   │
│   │  x: extra large memory (x2idn)               │  │  d: dense HDD storage (d3en)                │   │
│   │  z: high-freq core + memory (z1d)            │  │  p: GPU for ML training (p4d, p5)           │   │
│   │  In-memory DB, Redis, SAP HANA               │  │  g: GPU for ML inference (g5, g4dn)         │   │
│   │  Real-time big data analytics                │  │  trn: Trainium (AWS ML chip)                │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    Nitro hypervisor · Nitro cards · physical CPUs (Intel/AMD/Graviton) · NVMe/GPU                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Family          = Letter prefix (m, c, r, i, p, g) indicating workload optimisation                │
│    Generation      = Number after family (e.g., 7 in m7i); higher = newer hardware                    │
│    Processor       = Suffix: i=Intel, a=AMD, g=Graviton (AWS ARM); no suffix=any                      │
│    Size            = nano, micro, small, medium, large, xlarge, 2xlarge, etc.                         │
│    Burstable (t)   = Earns CPU credits when idle; bursts above baseline when credits exist            │
│    Graviton        = AWS-designed ARM chips (g suffix); up to 40% better price/performance            │
│    Nitro hypervisor= AWS-built hypervisor offloading storage/network to dedicated silicon             │
│    Bare metal       = Physical host access; no hypervisor; for licensing or performance               │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Compute Services Comparison

```text
┌─────────────────────── AWS Compute Services — EC2 vs Containers vs Serverless ────────────────────────┐
│                                                                                                       │
│    Choose compute based on control needed, workload type, and management overhead.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      EC2 (IaaS — full control)               │  │      Lambda (FaaS — serverless)             │   │
│   │  Launch VMs; choose OS and instance          │  │  Event-driven; run code, not servers        │   │
│   │  You manage OS, patches, agents              │  │  15 minute max timeout per invocation       │   │
│   │  Persistent; auto scaling groups             │  │  Auto-scales to thousands instantly         │   │
│   │  Any workload: persistent, stateful          │  │  Pay per request + duration (ms)            │   │
│   │  Most control; most management effort        │  │  Supports Python, Node, Java, Go, etc       │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    EC2 = most control; Lambda = least management; containers sit in the middle.                       │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │      ECS / Fargate / EKS (containers)        │  │     Other Compute Services                  │   │
│   │  ECS: Docker on AWS; AWS control plane       │  │  Elastic Beanstalk: PaaS; deploy code       │   │
│   │  Fargate: serverless containers (ECS)        │  │  Lightsail: simple VPS for small apps       │   │
│   │  No EC2 management in Fargate mode           │  │  App Runner: deploy web app from code       │   │
│   │  EKS: managed Kubernetes on AWS              │  │  Batch: managed batch HPC computing         │   │
│   │  ECR: private container image registry       │  │  Outposts: EC2 + ECS on-premises            │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    Nitro hypervisor · container runtime on EC2 hosts · Lambda micro-VMs (Firecracker)                 │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    EC2             = Elastic Compute Cloud; virtual server; IaaS; full OS control                     │
│    Lambda          = Serverless function; event-triggered; no server management                       │
│    ECS             = Elastic Container Service; run Docker containers on AWS                          │
│    Fargate         = Serverless compute engine for ECS/EKS; no EC2 to manage                          │
│    EKS             = Elastic Kubernetes Service; managed K8s control plane on AWS                     │
│    Elastic Beanstalk= PaaS; upload code; AWS provisions EC2/LB/ASG/RDS automatically                  │
│    Lightsail       = Simple VPS with fixed monthly pricing; good for small workloads                  │
│    Firecracker     = AWS micro-VM technology powering Lambda and Fargate isolation                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## EC2 Auto Scaling and Load Balancing

```text
┌────────────────────── EC2 Auto Scaling + Elastic Load Balancing — Architecture ───────────────────────┐
│                                                                                                       │
│    ALB/NLB distribute traffic; Auto Scaling Group adjusts capacity automatically.                     │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Elastic Load Balancers                   │  │     Load Balancer Selection                 │   │
│   │  ALB: Layer 7 HTTP/HTTPS/gRPC                │  │  ALB: path/host routing; microservices      │   │
│   │  Path routing: /api to API target grp        │  │  ALB: WAF integration; TLS termination      │   │
│   │  Host routing: api.x.com to target grp       │  │  NLB: TCP/UDP/TLS; ultra-low latency        │   │
│   │  NLB: Layer 4 TCP/UDP; static Elastic        │  │  NLB: static IPs; for firewall rules        │   │
│   │  GWLB: inline L3 for virtual appliances      │  │  GWLB: transparent for IDS/IPS/FW           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    ALB is preferred for HTTP workloads; NLB for extreme performance or static IPs.                    │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │     Auto Scaling Group (ASG)                 │  │      Scaling Policies                       │   │
│   │  Min / Desired / Max capacity settings       │  │  Target Tracking: maintain CPU at 60%       │   │
│   │  Launch template: AMI + type + SGs           │  │  Step Scaling: scale by steps on alrm       │   │
│   │  Health check: LB or EC2 status              │  │  Scheduled: scale at known times            │   │
│   │  Multi-AZ: instances spread across AZs       │  │  Predictive: ML forecast future load        │   │
│   │  Warm pools: pre-warm instances quickly      │  │  Cool-down: prevent scale thrashing         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical Infrastructure (the hardware everything above runs on):                                   │
│    ALB/NLB nodes in each AZ · EC2 instances on Nitro hosts · Route 53 DNS                             │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    ALB             = Application Load Balancer; Layer 7; path/host/header routing                     │
│    NLB             = Network Load Balancer; Layer 4; static IPs; ultra-low latency                    │
│    GWLB            = Gateway Load Balancer; transparent inline Layer 3 for appliances                 │
│    Target Group    = Set of targets (EC2/Lambda/IP) that LB routes requests to                        │
│    Auto Scaling Group = EC2 fleet with min/desired/max; replaces unhealthy instances                  │
│    Launch Template = EC2 config snapshot (AMI, type, SG, user data) used by ASG                       │
│    Target Tracking = Scaling policy that adjusts capacity to hit a target metric                      │
│    Warm Pool       = Pool of pre-initialised instances to reduce scale-out latency                    │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
