# Management Tools

```text
┌────────────────────────────────────── VMware — Management Tools ──────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Layered management toolstack for the VMware platform: compute, network, storage, lifecycle  │   │
│   │     Each tool manages a distinct layer; SDDC Manager orchestrates VCF lifecycle across all    │   │
│   │       Track: FQDN, version, admin URL, primary admin account, last upgrade date per tool      │   │
│   │    Access: all tools require LDAP/SSO + MFA; direct root is break-glass only, vault stored    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Compute/storage mgmt → network mgmt → operations and lifecycle management                          │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │      Compute & Storage      │  │      Network & Security     │  │       Ops & Lifecycle       │   │
│   │        vCenter Server       │  │         NSX Manager         │  │       Aria Operations       │   │
│   │        vSphere Client       │  │         NSX UI / API        │  │          Aria Logs          │   │
│   │        VxRail Manager       │  │        Aria Networks        │  │       Aria Automation       │   │
│   │         vSAN Skyline        │  │       NSX Intelligence      │  │        Aria Suite LCM       │   │
│   │         SDDC Manager        │  │       Load Balancer UI      │  │       Skyline Advisor       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Hardware access: iDRAC / RACADM — independent of ESXi and vCenter for OOB management               │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Tool       │       FQDN       │      Version      │    Admin URL     │   Last upgrade   │   │
│   │     vCenter      │   vcsa-prod-01   │       8.0 U3      │   https://vcsa   │     2025-03      │   │
│   │   NSX Manager    │    nsx-mgr-01    │       4.1.2       │   https://nsx    │     2025-03      │   │
│   │    VxRail Mgr    │    vxrail-mgr    │      8.0.300      │   https://vxrm   │     2025-04      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: management VMs on dedicated cluster · iDRAC on dedicated OOB network                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    vCenter Server  = Central management for ESXi clusters, VMs, storage, and networking               │
│    NSX Manager     = Control plane for NSX-T; manages segments, gateways, DFW policy                  │
│    VxRail Manager  = Dell VxRail appliance manager; Mystic service orchestrates LCM                   │
│    SDDC Manager    = VCF lifecycle orchestrator; manages domains, clusters, upgrades                  │
│    Aria Operations = vROps; monitors vSphere/vSAN/NSX with ML anomaly detection                       │
│    Aria Logs       = vRLI; log analytics for ESXi, vCenter, NSX, and infrastructure                   │
│    Aria Automation = vRA; IaC and self-service cloud automation; Terraform backed                     │
│    Aria Suite LCM  = Lifecycle Manager for Aria products; upgrades and cert rotation                  │
│    Skyline Advisor = Proactive support; flags known issues before they cause outages                  │
│    iDRAC           = Dell OOB management; hardware-level access independent of OS                     │
│    Aria Networks   = vRNI; network flow visibility and micro-segmentation planning                    │
│    Break-glass     = Emergency admin account in vault; used only when SSO/LDAP fails                  │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
> Part of the [Inventory](../index.md) reference.

---
## Overview

Document all management plane tools in the VMware environment — URLs, versions, credentials locations, and responsible owners. Update after any management platform upgrade or deployment change.

## Core Management Tools

| Tool | FQDN / URL | Version | IP Address | Credential Store | Owner | Notes |
|---|---|---|---|---|---|---|
| vCenter Server | vcsa-prod-01.example.com | 8.0 U3 | 10.10.10.5 | CyberArk | Infra Team | Primary production vCenter |
| vCenter Server (DR) | vcsa-dr-01.example.com | 8.0 U3 | 10.20.10.5 | CyberArk | Infra Team | DR site vCenter |
| NSX Manager | nsx-prod-01.example.com | 4.1.2 | 10.10.10.10 | CyberArk | Network/Infra Team | NSX-T cluster VIP |
| VxRail Manager | vxrail-prod-01.example.com | 8.0.300 | 10.10.10.15 | CyberArk | Infra Team | Integrated with vCenter |
| Aria Operations | aria-ops-01.example.com | 8.16 | 10.10.10.20 | CyberArk | Infra Team | Performance and capacity |
| Aria Automation | aria-auto-01.example.com | 8.16 | 10.10.10.21 | CyberArk | Infra/Cloud Team | Self-service, IaC |
| Aria Operations for Logs | aria-logs-01.example.com | 8.16 | 10.10.10.22 | CyberArk | Infra Team | Log aggregation and alerting |
| Aria Suite Lifecycle | aslcm-01.example.com | 8.16 | 10.10.10.23 | CyberArk | Infra Team | Lifecycle management for Aria |

## Backup and Data Protection

| Tool | FQDN / URL | Version | Notes |
|---|---|---|---|
| Veeam Backup & Replication | veeam-01.example.com | 12.1 | VM backups, vSAN integration |
| Veeam Backup for Microsoft 365 | veeam-m365-01.example.com | 7.x | M365 mailbox and SharePoint backup |

## Monitoring and Alerting

| Tool | FQDN / URL | Version | Notes |
|---|---|---|---|
| Aria Operations | aria-ops-01.example.com | 8.16 | Primary monitoring — see above |
| vSAN Skyline Health | Embedded in vCenter | — | In-product health checks |
| Dell SupportAssist | Embedded in VxRail Manager | — | Proactive support |

## Certificate Management

| Component | Certificate Authority | Expiry Tracking | Notes |
|---|---|---|---|
| vCenter HTTPS | Internal CA | Monitor in vCenter Certificates UI | Auto-renew enabled |
| NSX Manager | Internal CA | NSX Certificates view | |
| ESXi VMCA | VMCA (embedded) | vCenter Certificate Management | |

## Access URLs Quick Reference

| Tool | Access URL |
|---|---|
| vCenter | `https://vcsa-prod-01.example.com/ui` |
| NSX | `https://nsx-prod-01.example.com` |
| Aria Operations | `https://aria-ops-01.example.com` |
| Aria Automation | `https://aria-auto-01.example.com` |
| Aria Logs | `https://aria-logs-01.example.com` |
| VxRail Manager | `https://vxrail-prod-01.example.com` |
| Veeam | `https://veeam-01.example.com:9443` |

## Tool Registration and Integration Map

```text
vCenter <─── NSX Manager (integrated)
   │
   ├─── VxRail Manager (registered)
   │
   ├─── Aria Operations (collector/adapter)
   │         └─── Aria Operations for Logs (forwarding)
   │
   └─── Aria Automation (endpoint/cloud account)
             └─── Aria Suite Lifecycle (manages all Aria)
```
