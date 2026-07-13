---
tags:
  - architecture
  - azure
description: "How It Works reference covering Overview, Management Group Hierarchy, Identity Architecture."
---
# Azure — How It Works

<div class="kb-summary">
How It Works reference covering Overview, Management Group Hierarchy, Identity Architecture.

*Applies to: Azure*
</div>

## Overview

Microsoft Azure is a hyperscale public cloud platform. Resources are organised in a hierarchy: Tenant (Entra ID) → Management Groups → Subscriptions → Resource Groups → Resources. Azure Policy and RBAC applied at a Management Group are inherited by all child subscriptions. A hub-and-spoke network topology connects on-premises environments via ExpressRoute to a hub VNet, with workload spoke VNets peered to the hub.

## Management Group Hierarchy

```d2
direction: right

TENANT: "Azure Tenant\n(Entra ID" {shape: rectangle}
MG: "Management Groups\nCorp > Prod > Non-Prod" {shape: rectangle}
SUBP: "Production Subscription" {shape: rectangle}
SUBD: "Dev/Test Subscription" {shape: rectangle}
HUB: "Hub VNet\nFirewall · Bastion · VPN GW" {shape: rectangle}
SP1: "Spoke VNet 1\n(Workload A" {shape: rectangle}
SP2: "Spoke VNet 2\n(Workload B" {shape: rectangle}

TENANT -> MG
MG -> SUBP
MG -> SUBD
SUBP -> HUB
SUBP -> SP1
SUBP -> SP2
SP1 -> SP2
```

---

## See also

- [Azure — Design Standards](../design-standards/)
- [Azure — Integrations](../integrations/)
- [Azure — Deploy](../../deploy/)
