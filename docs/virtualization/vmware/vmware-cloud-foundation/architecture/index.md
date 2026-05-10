# VCF — Architecture Overview

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

## Overview

VMware Cloud Foundation (VCF) is a full-stack SDDC platform that combines vSphere, vSAN, NSX, and SDDC Manager into a single integrated and lifecycle-managed platform.

Key concepts:
- **SDDC Manager** is the central orchestrator — it manages workload domains, lifecycle upgrades, password rotation, and certificate management across the entire stack
- **Management Domain** hosts the VCF management components (vCenter, NSX Manager, SDDC Manager themselves)
- **Workload Domains** are independently managed vSphere/vSAN/NSX instances provisioned by SDDC Manager for tenant or application workloads
- **Bill of Materials (BOM)** defines the validated, interoperable versions of all components for a given VCF release

---

## In this section

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="components/"><strong>Components</strong><span>Core components, services, and technical specifications.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with other platforms and external systems.</span></a>
<a class="kb-card" href="standards/"><strong>Standards</strong><span>Sizing guidelines, design standards, and best practices.</span></a>
</div>
