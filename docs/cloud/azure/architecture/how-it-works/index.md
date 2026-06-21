---
tags:
  - architecture
  - azure
---
# Azure — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Management Group Hierarchy, Identity Architecture.

*Applies to: Azure*
</div>
![Azure — How It Works](../../../../assets/cloud-azure-architecture-how-it-works-index.svg)


## Overview

Microsoft Azure is a hyperscale public cloud platform. Resources are organised in a hierarchy: Tenant (Entra ID) → Management Groups → Subscriptions → Resource Groups → Resources. Azure Policy and RBAC applied at a Management Group are inherited by all child subscriptions. A hub-and-spoke network topology connects on-premises environments via ExpressRoute to a hub VNet, with workload spoke VNets peered to the hub.

## Management Group Hierarchy

```mermaid
graph TB
  TENANT["Azure Tenant\n(Entra ID)"] --> MG["Management Groups\nCorp > Prod > Non-Prod"]
  MG --> SUBP["Production Subscription"]
  MG --> SUBD["Dev/Test Subscription"]
  SUBP --> HUB["Hub VNet\nFirewall · Bastion · VPN GW"]
  SUBP --> SP1["Spoke VNet 1\n(Workload A)"]
  SUBP --> SP2["Spoke VNet 2\n(Workload B)"]
  HUB <-->|"VNet peering"| SP1 & SP2
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef cloud fill:#0f766e,stroke:#0d5f58,color:#fff
  class TENANT,MG ctrl
  class SUBP,SUBD cloud
  class HUB,SP1,SP2 net
```


---

## See also

- [Azure — Design Standards](../design-standards/)
- [Azure — Integrations](../integrations/)
- [Azure — Deploy](../../deploy/)
