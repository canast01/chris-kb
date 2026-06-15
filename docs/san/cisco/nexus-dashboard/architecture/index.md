---
tags:
  - architecture
  - san
---
# Nexus Dashboard — Architecture

<div class="kb-summary">
Cisco Nexus Dashboard is an app-hosting platform for Cisco data centre management. A 3-node or 5-node cluster provides shared identity, multi-site connectivity, and API gateway. NDFC (SAN/LAN), NDI (Insights), and NDO (Orchestrator) run as hosted applications on the cluster.

*Applies to: Cisco MDS · Nexus*
</div>

```text
┌──────────────────────────── Cisco Nexus Dashboard — App-Hosting Platform ─────────────────────────────┐
│                                                                                                       │
│  3-node or 5-node cluster with shared identity, multi-site connectivity, and API                      │
│  gateway; NDFC, NDI, and NDO run as hosted applications on the cluster.                               │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Cluster Architecture             │  │             Hosted Applications             │   │
│   │              3-node: HA quorum               │  │         NDFC: SAN+LAN fabric control        │   │
│   │       5-node: scale + apps separation        │  │            NDI: network insights            │   │
│   │        Kubernetes: shared app runtime        │  │         NDO: multi-site orchestrator        │   │
│   │          Etcd: cluster state store           │  │         Apps: install from app store        │   │
│   │          Shared: identity + secrets          │  │        License: per-app subscription        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Each app (NDFC/NDI/NDO) is independent; all share ND auth and multi-site links.                      │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Network Connectivity             │  │              Multi-Site and API             │   │
│   │        Data network: switch discovery        │  │          Multi-site: inter-ND link          │   │
│   │           Mgmt network: OOB access           │  │         REST API: per-app + platform        │   │
│   │            SSH/HTTPS to Nexus/MDS            │  │          SAML/LDAP: SSO integration         │   │
│   │             SNMP: trap receiving             │  │          Webhook: alert forwarding          │   │
│   │         NTP: all nodes sync required         │  │           Syslog: event forwarding          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  Nexus Dashboard hardware appliance (NDC) or VMware/KVM VMs; 3-node minimum;                          │
│  management + data networks; outbound HTTPS to Cisco app store for installs.                          │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  ND            = Nexus Dashboard; Cisco app-hosting platform for DC management                        │
│  NDFC          = Nexus Dashboard Fabric Controller; SAN/LAN fabric management                         │
│  NDI           = Nexus Dashboard Insights; telemetry + network assurance                              │
│  NDO           = Nexus Dashboard Orchestrator; ACI multi-site policy                                  │
│  3-node        = minimum HA cluster; tolerates 1 node failure                                         │
│  5-node        = production recommended; separates infra and app nodes                                │
│  Kubernetes    = ND runs K8s internally; apps are pods on the cluster                                 │
│  Etcd          = distributed KV for cluster state; used by ND Kubernetes                              │
│  Data network  = second NIC; device discovery + telemetry collection                                  │
│  Multi-site    = ND instances linked across sites for global view                                     │
│  App store     = Cisco app catalogue; install NDFC/NDI/NDO from UI                                    │
│  NDC           = Nexus Dashboard Cluster; Cisco hardware appliance option                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
![Cisco Nexus Dashboard Architecture](../../../../assets/cisco-nexus-dashboard-architecture-overview.svg)

<div class="kb-grid kb-grid-3">
<a class="kb-card" href="how-it-works/"><strong>How It Works</strong><span>How it works, integrations, and design standards.</span></a>
<a class="kb-card" href="integrations/"><strong>Integrations</strong><span>Integration with MDS SAN, ACI, VXLAN, and Nexus fabrics.</span></a>
<a class="kb-card" href="design-standards/"><strong>Design Standards</strong><span>Cluster sizing, form factor selection, and multi-site design standards.</span></a>
</div>

## Hosted Applications

| Application | Abbreviation | Role |
|---|---|---|
| Nexus Dashboard Fabric Controller | NDFC | SAN and LAN fabric management (successor to DCNM) |
| Nexus Dashboard Insights | NDI | Network assurance, anomaly detection, flow telemetry |
| Nexus Dashboard Orchestrator | NDO | Multi-site ACI and VXLAN fabric policy orchestration |

## Cluster Topology

