# Azure — Architecture

<div class="kb-summary">
Azure cloud platform architecture — management hierarchy, hub-and-spoke networking, compute options, HA patterns, and identity with Entra ID.
</div>

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>Management hierarchy, hub-spoke networking, compute, identity, HA, and DR patterns.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>ExpressRoute, on-premises connectivity, and third-party integrations.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Naming conventions, tagging policy, subscription design, and security baselines.</span></a>
</div>

| Layer | Service | Role |
|---|---|---|
| Identity | Entra ID (Azure AD) | Cloud identity plane; SSO, MFA, PIM, Conditional Access |
| Management | Management Groups / Policy | Governance hierarchy; RBAC and Policy inherited downward |
| Network | Hub VNet + Spoke VNets | Hub-and-spoke; Azure Firewall controls east-west and internet traffic |
| Compute | VMs, AKS, App Service | Lift-and-shift, containers, web apps |
| Storage | Blob, ADLS, Managed Disks | Object, data lake, and block storage |
| Observability | Azure Monitor + Log Analytics | Metrics, logs, alerts, dashboards |

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
