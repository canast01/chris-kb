---
tags:
  - azure
  - networking
---
# Azure Networking

<div class="kb-summary">
Azure Networking articles, operational checks, troubleshooting notes, and references.
</div>

```text
┌────────────────────────────────────── Azure Networking Overview ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           Azure Networking — VNet, NSG, Load Balancer, DNS, and Hybrid Connectivity           │   │
│   │      VNet: isolated network; CIDR /8–/29; subnets per AZ; hub-and-spoke via VNet peering      │   │
│   │   Security: NSG (stateful L4 rules per subnet/NIC) · Azure Firewall (stateful L4/L7 in hub)   │   │
│   │  Load balancing: Load Balancer (L4) · Application Gateway (L7 + WAF) · Traffic Manager (DNS)  │   │
│   │    Hybrid: ExpressRoute (private circuit) · VPN Gateway (IPsec) · Private Endpoints (PaaS)    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    VNet defines the network · NSG/Firewall secure it · Load Balancer distributes traffic              │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │        VNet & Subnets       │  │      Security Controls      │  │         Connectivity        │   │
│   │     VNet: CIDR /16 plan     │  │    NSG: allow/deny rules    │  │    ExpressRoute: private    │   │
│   │     Subnets: per AZ/tier    │  │    Firewall: hub central    │  │      VPN Gateway: IPsec     │   │
│   │     Peering: hub ↔ spoke    │  │    Network Watcher: diag    │  │    Private Endpoint: PaaS   │   │
│   │      Route tables: UDR      │  │      DDoS: Basic or std     │  │    Azure DNS: pub + priv    │   │
│   │      Service endpoints      │  │     Flow logs: NSG → LA     │  │     LB: internal+public     │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    VNet/subnets form the base · NSG/Firewall protect traffic                                          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       VNet       │     Subnets      │        NSG        │  Load Balancer   │   App Gateway    │   │
│   │    CIDR: plan    │    App subnet    │   Inbound rules   │   Backend pool   │  L7: path route  │   │
│   │   Peering: hub   │    DB subnet     │   Outbound rules  │   Health probe   │    WAF: OWASP    │   │
│   │  Flow logs: LA   │  GW subnet: /27  │   Priority: 100   │  LB rule: port   │ SSL termination  │   │
│   │   DNS: custom    │  Service endpt   │   NSG flow logs   │   Internal LB    │  Autoscale: min  │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure SDN fabric · Availability Zones · ExpressRoute physical circuits · VPN Gateway hardware        │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  VNet           = Virtual Network; isolated private network in a region; one or more CIDR address     │
│  Subnet         = Address range within a VNet; services and NSGs attached per subnet                  │
│  NSG            = Network Security Group; stateful L4 ACL; priority-ordered allow/deny rules on       │
│  VNet peering   = Private connectivity between VNets in same or different regions; low latency        │
│  UDR            = User Defined Route; custom route table overriding Azure defaults; force to firewall │
│  Azure Firewall = Managed stateful L4/L7 firewall in hub VNet; centralises egress and spoke traffic   │
│  Private Endpoint= Private IP in a VNet for accessing PaaS (Storage, SQL, Key Vault) without internet │
│  Service Endpoint= Optimised route from VNet to PaaS service; not a private IP; firewall-accessible   │
│  Application Gateway= L7 load balancer with URL routing, SSL offload, and optional WAF integration    │
│  Network Watcher = Diagnostics for connectivity, packet capture, NSG flow logs, and topology view     │
│  ExpressRoute   = Dedicated private 50 Mbps–10 Gbps circuit between on-premises and Azure             │
│  Azure DNS      = Managed DNS for public zones (internet) and private zones (VNet resolution)         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Articles

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="application-gateway/">
  <strong>Application Gateway</strong>
  <span>Layer 7 load balancer with WAF, SSL termination, URL routing, and session affinity.</span>
</a>

<a class="kb-card" href="azure-dns/">
  <strong>Azure DNS</strong>
  <span>Managed DNS hosting for public and private zones with Azure-integrated resolution.</span>
</a>

<a class="kb-card" href="expressroute/">
  <strong>ExpressRoute</strong>
  <span>Dedicated private connectivity from on-premises to Azure, bypassing the public internet.</span>
</a>

<a class="kb-card" href="load-balancer/">
  <strong>Load Balancer</strong>
  <span>Layer 4 load balancer for inbound and outbound traffic distribution across VM backends.</span>
</a>

<a class="kb-card" href="network-security-groups/">
  <strong>Network Security Groups</strong>
  <span>Stateful firewall rules applied to subnets or NICs to control inbound and outbound traffic.</span>
</a>

<a class="kb-card" href="network-watcher/">
  <strong>Network Watcher</strong>
  <span>Network diagnostics including connection troubleshoot, packet capture, and flow logs.</span>
</a>

<a class="kb-card" href="private-endpoints/">
  <strong>Private Endpoints</strong>
  <span>Private IP access to Azure PaaS services (Storage, Key Vault, SQL) within the VNet.</span>
</a>

<a class="kb-card" href="route-tables/">
  <strong>Route Tables</strong>
  <span>User-defined routes to override Azure default routing and direct traffic through NVAs or VPN.</span>
</a>

<a class="kb-card" href="subnets/">
  <strong>Subnets</strong>
  <span>VNet address space segmentation for workload isolation, NSG scope, and service delegation.</span>
</a>

<a class="kb-card" href="virtual-network/">
  <strong>Virtual Network</strong>
  <span>Core private network in Azure for resource connectivity, peering, DNS, and security boundaries.</span>
</a>

<a class="kb-card" href="vpn-gateway/">
  <strong>VPN Gateway</strong>
  <span>IPsec/IKE VPN tunnel between Azure VNet and on-premises or other Azure regions.</span>
</a>
</div>
