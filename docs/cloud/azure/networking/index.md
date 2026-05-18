# Azure Networking

<div class="kb-summary">
Azure Networking articles, operational checks, troubleshooting notes, and references.
</div>

```
┌───────────────────────────────────────────────────────────────┐
│                  Azure Networking Overview                    │
│                                                               │
│  ┌───────────────────────────────────────────────────────┐    │
│  │  Virtual Network  (10.0.0.0/16)                       │    │
│  │                                                       │    │
│  │  ┌──────────────────┐    ┌──────────────────────────┐ │    │
│  │  │  Subnet-A        │    │  Subnet-B                │ │    │
│  │  │  10.0.1.0/24     │    │  10.0.2.0/24             │ │    │
│  │  │  NSG + Route tbl │    │  NSG + Route tbl         │ │    │
│  │  └──────────────────┘    └──────────────────────────┘ │    │
│  └──────────────────────────────────┬─────────────────────┘    │
│                                     │                         │
│          ┌──────────────────────────┼─────────────────┐       │
│          ▼                          ▼                 ▼       │
│  ┌──────────────┐         ┌──────────────┐   ┌──────────────┐ │
│  │  Load        │         │  VPN Gateway │   │  ExpressRoute│ │
│  │  Balancer    │         │  (IPsec S2S) │   │  (private)   │ │
│  └──────────────┘         └──────────────┘   └──────────────┘ │
└───────────────────────────────────────────────────────────────┘
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
