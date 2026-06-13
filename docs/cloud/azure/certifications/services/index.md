---
tags:
  - azure
  - certifications
---
# Azure Services Reference


<div class="kb-summary">
Azure Services Reference reference covering Compute Services, Networking Services, Identity Services, Storage Services, Monitoring Services and 1 more sections.
</div>
```text
┌──────────────────────────────────── Certifications Azure Services ────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                         Azure: Certifications Azure Services platform                         │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │                  Management: Certifications Azure Services management console                 │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Certifications Azure Services infrastructure · management network · monitoring           │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Azure              = Certifications Azure Services platform overview and core concepts             │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
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
