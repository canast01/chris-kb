# Nexus Dashboard — Architecture

<div class="kb-summary">
Cisco Nexus Dashboard is an app-hosting platform for Cisco data centre management. A 3-node or 5-node cluster provides shared identity, multi-site connectivity, and API gateway. NDFC (SAN/LAN), NDI (Insights), and NDO (Orchestrator) run as hosted applications on the cluster.
</div>

```text
┌──────────────────────────── Cisco Nexus Dashboard — Architecture Overview ────────────────────────────┐
│                                                                                                       │
│  Clustered platform hosting NDFC, NDI, and NDO as microservice apps on Kubernetes.                    │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Cluster Architecture             │  │             Hosted Applications             │   │
│   │           Primary: 3-node minimum            │  │         NDFC: SAN/LAN fabric control        │   │
│   │         Worker nodes: scale capacity         │  │       NDI: network insights/assurance       │   │
│   │        Kubernetes: container runtime         │  │         NDO: multi-site orchestrator        │   │
│   │        etcd: distributed state store         │  │         Apps deployed as Helm charts        │   │
│   │        Storage: Ceph or external NFS         │  │            Per-app RBAC isolation           │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  ND cluster provides platform; apps (NDFC/NDI/NDO) run independently on top                           │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │              Network Interfaces              │  │              HA and Resilience              │   │
│   │           Management: OOB Ethernet           │  │           Quorum: 2 of 3 nodes up           │   │
│   │          Data: in-band fabric VLAN           │  │          App restart: K8s self-heal         │   │
│   │           VIP: cluster virtual IP            │  │         Node failure: auto rebalance        │   │
│   │             App port: HTTPS 443              │  │          Backup: schedule to remote         │   │
│   │          Inter-node: cluster fabric          │  │        Upgrade: rolling node-by-node        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  UCS/virtual servers (3+ nodes) · management switch · ToR switches · NFS/Ceph storage                 │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  NDFC           = Nexus Dashboard Fabric Controller; manages SAN and LAN fabrics                      │
│  NDI            = Nexus Dashboard Insights; assurance and telemetry analytics                         │
│  NDO            = Nexus Dashboard Orchestrator; multi-site ACI policy orchestration                   │
│  Kubernetes     = Container orchestration platform underlying ND cluster                              │
│  etcd           = Distributed key-value store used by Kubernetes for cluster state                    │
│  Ceph           = Distributed storage system providing persistent volumes to apps                     │
│  VIP            = Virtual IP; single cluster entry point for management access                        │
│  Quorum         = Minimum node count (2 of 3) for cluster to remain operational                       │
│  Helm chart     = Kubernetes application packaging format used by ND apps                             │
│  OOB management = Out-of-Band network; separate from fabric data path                                 │
│  Worker node    = Additional ND node added beyond 3 primaries for scale                               │
│  Rolling upgrade= Upgrade one node at a time to maintain cluster availability                         │
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


