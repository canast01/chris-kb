# VCF — Architecture

<div class="kb-summary">
VMware Cloud Foundation (VCF) is a full-stack SDDC platform. SDDC Manager orchestrates vSphere, vSAN, and NSX as a validated, lifecycle-managed unit across a Management Domain and one or more Workload Domains.
</div>

```
┌───────────────────────────────────────── VCF — Architecture ──────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │ VMware Cloud Foundation = SDDC Manager + Cloud Builder + vSphere + vSAN + NSX bundled together│   │
│   │ Workload domains isolate workloads; BOM ensures component compatibility across the full stack │   │
│   │ Automated bring-up via Cloud Builder; Management domain deployed first, VI domains added after│   │
│   │    SDDC Manager orchestrates lifecycle: patching, password rotation, certificate management   │   │
│   │     NSX per domain provides overlay networking; vCenter per domain for workload management    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    How-it-works defines domain architecture · integrations connect stack components                   │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │         How It Works        │  │         Integrations        │  │       Design Standards      │   │
│   │       SDDC Manager UI       │  │       vSphere+vSAN+NSX      │  │      Mgmt domain first      │   │
│   │    Cloud Builder: deploy    │  │       Aria Suite intg       │  │     VI domains: isolated    │   │
│   │       Workload domains      │  │      vCenter per domain     │  │        NSX per domain       │   │
│   │       BOM: version set      │  │        NSX per domain       │  │       SDDC user roles       │   │
│   │     VI domain: workload     │  │       Identity Manager      │  │      BOM compat matrix      │   │
│   │      Mgmt domain: core      │  │         SIEM syslog         │  │      Subscription model     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    How-it-works covers domain model · integrations connect stack and identity                         │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   How It Works   │   Integrations   │    Design Stds    │    Deployment    │     Key Stds     │   │
│   │   SDDC Manager   │   vSphere+vSAN   │  Mgmt domain 1st  │  Cloud Builder   │    BOM matrix    │   │
│   │ Workload domains │  NSX per domain  │     VI domains    │ Automated deploy │  Domain naming   │   │
│   │  BOM lifecycle   │ Aria Suite intg  │     SDDC RBAC     │  Pre-check reqs  │    SDDC roles    │   │
│   │  Cloud Builder   │   Identity Mgr   │    NSX overlay    │ Post-deploy val  │   Password std   │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 servers · PCIe NICs · ToR switches · SAN/vSAN storage · OOB management network                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  SDDC Manager  = VCF control plane; orchestrates domain lifecycle, LCM upgrades, password rotation    │
│  Cloud Builder = Automated bring-up appliance; validates prerequisites and deploys Management domain  │
│  Workload domain = Isolated vSphere+vSAN+NSX unit; separate vCenter, NSX Manager, and cluster         │
│  Management domain = First VCF domain; hosts SDDC Manager, vCenter, and shared infrastructure         │
│  VI domain     = Virtual Infrastructure workload domain; runs production VMs separate from management │
│  BOM (Bill of Materials) = Validated version matrix for all VCF components; ensures stack             │
│  SDDC bring-up = Cloud Builder automated deployment of Management domain from JSON spec               │
│  NSX per domain = Each VCF workload domain gets its own NSX Manager cluster for isolation             │
│  vCenter per domain = Each VCF domain has a dedicated vCenter for workload management and HA/DRS      │
│  LCM (Lifecycle Manager) = SDDC Manager component for orchestrating upgrades across VCF stack         │
│  SoS tool      = Support and Serviceability tool; runs health checks across all VCF components        │
│  VCF subscription = Licensing model for VCF; covers all included components under one SKU             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

| Domain Type | Purpose | Components |
|---|---|---|
| Management Domain | Hosts VCF management stack | SDDC Manager, vCenter, NSX, vSAN |
| VI Workload Domain | General-purpose vSphere workloads | vCenter, NSX, vSAN (per domain) |
| VVF Workload Domain | Cloud-native / Tanzu workloads | vCenter, NSX, vSAN + TKGs |
| Consolidated Architecture | Small deployments — management + workload combined | All on 4 hosts |

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>SDDC Manager, deployment domains, BOM, lifecycle management, passwords, certificates, and network pools.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Aria Operations, Aria Automation, Active Directory, NSX Federation, backup, and SIEM.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Management domain sizing, naming conventions, network requirements, password policy, and HCL requirements.</span></a>
</div>

## VCF Domain Architecture

![VCF Domain Architecture](../../../../assets/vcf-architecture-overview.svg)

