---
tags:
  - architecture
  - vcf
  - vmware
---
# VCF — Architecture

<div class="kb-summary">
VMware Cloud Foundation (VCF) is a full-stack SDDC platform. SDDC Manager orchestrates vSphere, vSAN, and NSX as a validated, lifecycle-managed unit across a Management Domain and one or more Workload Domains.

*Applies to: VCF 4.x · 5.x*
</div>

![VCF Domain Architecture](../../../../../assets/vcf-architecture-overview.svg)

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

