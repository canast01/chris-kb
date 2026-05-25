# Azure

<div class="kb-summary">
Microsoft Azure knowledge base covering compute, storage, networking, identity, monitoring, backup, security, governance, and cost management. Includes architecture references, operational procedures, CLI commands, and troubleshooting guides.
</div>

```text
┌──────────────────────────────────────── Azure Platform Stack ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Azure Management                                       │   │
│   │      Portal · Azure Monitor · Log Analytics · Cost Management · Resource Manager · Policy     │   │
│   │       Management Groups → Subscriptions → Resource Groups: hierarchical governance model      │   │
│   │           Entra ID: cloud identity for users, apps, and workloads across the tenant           │   │
│   │           az CLI · Azure PowerShell · ARM templates · Bicep: infrastructure as code           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Governance and policy enforcement span all subscriptions and resource groups                       │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │     Entra ID (Azure AD)     │  │           Compute           │  │          Networking         │   │
│   │  Users · groups · app regs  │  │   VMs: PAYG/reserved sizes  │  │   VNet: subnets · peering   │   │
│   │    RBAC: role assignments   │  │   VMSS: auto-scaling pool   │  │   NSG: stateful FW on NICs  │   │
│   │   PIM: just-in-time access  │  │   AKS: managed Kubernetes   │  │    Azure DNS: managed DNS   │   │
│   │   Conditional Access · MFA  │  │  Functions: serverless FaaS │  │    Front Door: global CDN   │   │
│   │   Service principals · MI   │  │    App Service: PaaS host   │  │    WAF · DDoS Protection    │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Entra ID controls access · VMs run inside VNets · NSGs enforce network policy                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │           Storage           │  │           Database          │  │    Security & Monitoring    │   │
│   │    Blob: hot/cool/archive   │  │   Azure SQL: managed MSSQL  │  │   Defender for Cloud: CSPM  │   │
│   │   Managed Disks: block VMs  │  │    Cosmos DB: multi-model   │  │    Sentinel: SIEM + SOAR    │   │
│   │     Azure Files: NFS/SMB    │  │    PostgreSQL: managed PG   │  │   Key Vault: secrets+certs  │   │
│   │   NetApp Files: enterprise  │  │    Redis Cache: in-memory   │  │   Policy: compliance scan   │   │
│   │     ADLS Gen2: analytics    │  │   Synapse: data warehouse   │  │   Monitor: metrics + logs   │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Storage, databases, and security services consumed as fully managed platform APIs                  │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                            Hybrid & Multi-Subscription Connectivity                           │   │
│   │         ExpressRoute: dedicated private circuit from on-premises to Azure (1/10 Gbps)         │   │
│   │               VPN Gateway: IPsec tunnels over the public internet to Azure VNets              │   │
│   │              VNet Peering: private routing between VNets within or across regions             │   │
│   │            Virtual WAN: hub-and-spoke WAN topology for global connectivity at scale           │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Azure global regions and availability zones; data centres owned and operated by Microsoft            │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Entra ID      = Azure Active Directory; cloud identity for users, devices, and service principals    │
│  RBAC          = Role-Based Access Control; Azure permission model using role assignments on scopes   │
│  PIM           = Privileged Identity Management; just-in-time privileged role activation              │
│  VNet          = Azure Virtual Network; isolated network with subnets, NSGs, and route tables         │
│  NSG           = Network Security Group; stateful firewall applied to subnets or individual NICs      │
│  VMSS          = Virtual Machine Scale Set; auto-scaling pool of identical VMs                        │
│  AKS           = Azure Kubernetes Service; managed Kubernetes control plane and node pools            │
│  Blob          = Azure Blob Storage; object store with hot, cool, and archive access tiers            │
│  Managed Disks = Azure block volumes for VMs; Premium SSD, Standard SSD, and Ultra Disk               │
│  ExpressRoute  = Dedicated private circuit from on-prem to Azure — bypasses public internet           │
│  Virtual WAN   = Azure hub-and-spoke WAN; connects VNets, branches, and on-premises at scale          │
│  Defender      = Microsoft Defender for Cloud; CSPM and workload protection for Azure resources       │
│  Sentinel      = Azure cloud-native SIEM; ingests logs, correlates alerts, automates response         │
│  Key Vault     = Azure managed secret store; stores keys, certificates, and connection strings        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-grid kb-grid-3">

<a class="kb-card" href="architecture/">
  <strong>Architecture</strong>
  <span>Overview, components, integrations, and standards.</span>
</a>

<a class="kb-card" href="operations/">
  <strong>Operations</strong>
  <span>CLI reference, health checks, procedures, lifecycle, backup, and scripts.</span>
</a>

<a class="kb-card" href="security/">
  <strong>Security</strong>
  <span>Authentication, access control, encryption, and hardening.</span>
</a>

<a class="kb-card" href="troubleshooting/">
  <strong>Troubleshooting</strong>
  <span>Common issues, diagnostics, and escalation.</span>
</a>

</div>
