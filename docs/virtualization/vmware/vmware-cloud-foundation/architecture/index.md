# VCF — Architecture Overview

VMware Cloud Foundation (VCF) is a full-stack SDDC platform. SDDC Manager orchestrates vSphere, vSAN, and NSX as a validated, lifecycle-managed unit across deployment domains.

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

---

## SDDC Stack Architecture

```mermaid
graph TB
  SDDC["SDDC Manager\n(VCF orchestration)"] --> MGMT["Management Domain\nvCenter · NSX · vSAN"]
  SDDC --> WL1["Workload Domain I\n(VI workloads)"]
  SDDC --> WL2["Workload Domain II\n(VVF cloud workloads)"]
  MGMT --> EMH["ESXi Mgmt Hosts\n(4 minimum)"]
  WL1 --> EWH["ESXi Workload Hosts"]
  SDDC --> CLOUD["VMware Cloud\n(optional hybrid)"]

  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef mgmt fill:#b45309,stroke:#92400e,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff

  class SDDC mgmt
  class MGMT,WL1,WL2 ctrl
  class EMH,EWH host
  class CLOUD cloud
```
