---
tags:
  - azure
  - certifications
description: "Azure Services Reference reference covering Compute Services, Networking Services, Identity Services, Storage Services, Monitoring Services and 1 more..."
---
# Azure Services Reference

<div class="kb-summary">
Azure Services Reference reference covering Compute Services, Networking Services, Identity Services, Storage Services, Monitoring Services and 1 more sections.
</div>

```d2
direction: down

compute_services: "Compute Services" {shape: rectangle}
networking_services: "Networking Services" {shape: rectangle}
identity_services: "Identity Services" {shape: rectangle}
storage_services: "Storage Services" {shape: rectangle}
monitoring_services: "Monitoring Services" {shape: rectangle}
study_checklist: "Study Checklist" {shape: rectangle}

compute_services -> networking_services: uses
networking_services -> identity_services: uses
identity_services -> storage_services: uses
storage_services -> monitoring_services: uses
monitoring_services -> study_checklist: uses
```

## Compute Services

| Service | Category | Key Facts |
|---|---|---|
| Azure Virtual Machines | IaaS | Full OS control; B-series for burstable, D-series for general, E-series for memory |
| Azure Virtual Machine Scale Sets (VMSS) | Auto-scaling VMs | Uniform or Flexible orchestration modes |
| Azure App Service | PaaS | Managed hosting for web apps, APIs; Windows and Linux |
| Azure Kubernetes Service (AKS) | Managed Kubernetes | Managed control plane; you manage node pools |
| Azure Container Instances (ACI) | Serverless containers | No cluster management; per-second billing |
| Azure Functions | Serverless | Event-driven; consumption plan scales to zero |
| Azure Batch | HPC batch | Large-scale parallel compute jobs |

## Networking Services

| Service | Purpose | Exam Notes |
|---|---|---|
| Virtual Network (VNet) | Isolated private network | Regional; subnets span the VNet |
| VNet Peering | VNet-to-VNet connectivity | Non-transitive; global peering across regions |
| VPN Gateway | Site-to-site / P2S VPN | Active-active for HA; requires GatewaySubnet |
| ExpressRoute | Private dedicated circuit | Not encrypted by default; 50Mbps–100Gbps |
| Azure Firewall | Managed stateful firewall | Layer 4 + Layer 7; FQDN rules; DNAT |
| Application Gateway | Layer 7 load balancer | WAF integration; path and host-based routing |
| Azure Load Balancer | Layer 4 load balancer | Internal or public; Standard vs Basic SKU |
| Azure Front Door | Global HTTP load balancer | CDN + WAF + global routing |
| Private Endpoint | Private access to PaaS | Puts a PaaS service on your VNet via private IP |
| Network Security Group (NSG) | Traffic filtering rules | Applied to subnet or NIC |

## Identity Services

| Service | Purpose |
|---|---|
| Microsoft Entra ID (Azure AD) | Cloud identity provider; SSO, MFA, Conditional Access |
| Entra ID B2B | Invite external partner/vendor identities to your tenant |
| Entra ID B2C | Customer-facing identity; social login, custom policies |
| Managed Identity | Service-to-service auth without credentials; system or user-assigned |
| Azure AD DS (Domain Services) | Managed Windows Server AD; Kerberos/LDAP for legacy apps |
| Privileged Identity Management (PIM) | Just-in-time privileged role activation with audit |

## Storage Services

| Service | Type | Use Case |
|---|---|---|
| Azure Blob Storage | Object | Unstructured data; Hot, Cool, Cold, Archive tiers |
| Azure Files | File (SMB/NFS) | Cloud file shares; Azure File Sync for hybrid |
| Azure Disk Storage | Block | Managed disks for VMs; Standard HDD, Standard SSD, Premium SSD, Ultra Disk |
| Azure NetApp Files | Enterprise NFS/SMB | High-performance file storage; SAP, Oracle workloads |
| Azure Data Lake Storage Gen2 | Hierarchical object | Big data analytics; ADLS is Blob with hierarchical namespace |
| Azure Queue Storage | Message queue | Simple async messaging between components |

## Monitoring Services

| Service | Purpose |
|---|---|
| Azure Monitor | Metrics, logs, alerts, dashboards — central monitoring platform |
| Log Analytics Workspace | Store and query log data; Kusto (KQL) query language |
| Application Insights | APM for apps; traces, exceptions, custom metrics |
| Azure Alerts | Trigger notifications or actions based on metrics or log queries |
| Network Watcher | Network diagnostics: packet capture, flow logs, topology |
| Azure Advisor | Cost, security, reliability, performance recommendations |

## Study Checklist

- [ ] Distinguish Application Gateway (Layer 7) from Azure Load Balancer (Layer 4)
- [ ] Know Managed Identity types (system-assigned vs user-assigned) and when to use each
- [ ] List Blob Storage access tiers and minimum storage durations
- [ ] Explain VNet Peering transitivity limitation and the solution (hub-and-spoke + Azure Firewall)
- [ ] Know the difference between NSG and Azure Firewall scope and capabilities
- [ ] Understand Log Analytics Workspace as the sink for Azure Monitor log data
