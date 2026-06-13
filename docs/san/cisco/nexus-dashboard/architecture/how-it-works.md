---
tags:
  - architecture
  - san
---
# Nexus Dashboard — How It Works


<div class="kb-summary">
How It Works reference covering Overview, Key Hosted Applications, Deployment Topology, Node Types, Network Interfaces Per Node and 3 more sections.

*Applies to: Cisco MDS · Nexus*
</div>

```text
┌──────────────────────────────── Cisco Nexus Dashboard — How It Works ─────────────────────────────────┐
│                                                                                                       │
│  ND cluster discovers fabric sites, streams telemetry, and orchestrates multi-site policy.            │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Site Onboarding                │  │              Telemetry Pipeline             │   │
│   │            Add APIC/NDFC/switches            │  │         gRPC streaming from switches        │   │
│   │          Credentials: REST API auth          │  │         NDI: flow, latency, anomaly         │   │
│   │         Site health: continuous poll         │  │           Kafka bus: event routing          │   │
│   │          Reachability: ICMP + REST           │  │          Elasticsearch: query store         │   │
│   │         Discovered: fabric topology          │  │         Retention: configurable days        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Sites added to ND; apps query ND APIs to retrieve topology and telemetry data                        │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │          Policy Orchestration (NDO)          │  │               App Interactions              │   │
│   │          Template: define EPGs/BDs           │  │         NDFC: SAN zone push via REST        │   │
│   │         Deploy: push to remote APIC          │  │         NDI: anomaly alert webhooks         │   │
│   │         Delta: only changed objects          │  │           NDO: ACI multi-site sync          │   │
│   │         Rollback: prior template ver         │  │          Shared services: SSO/RBAC          │   │
│   │          Audit: deploy history log           │  │         API gateway: single endpoint        │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  ND cluster nodes · fabric switches (Nexus/MDS) · APIC cluster · management network                   │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  gRPC           = Google Remote Procedure Call; used for high-speed telemetry streaming               │
│  Kafka          = Distributed event streaming platform; routes telemetry within ND                    │
│  Elasticsearch  = Search/analytics engine storing historical telemetry for NDI                        │
│  APIC           = Application Policy Infrastructure Controller; ACI fabric controller                 │
│  EPG            = Endpoint Group; ACI policy construct grouping VMs or physical hosts                 │
│  BD             = Bridge Domain; Layer 2 forwarding domain in ACI                                     │
│  NDO template   = Policy definition object deployed to one or more APIC sites                         │
│  Delta deploy   = Only objects that changed since last deploy are pushed to APIC                      │
│  Rollback       = Revert site config to a previous NDO template version                               │
│  SSO            = Single Sign-On; shared auth across NDFC, NDI, NDO apps                              │
│  REST API       = HTTP-based interface used by ND to communicate with fabric sites                    │
│  API gateway    = Single HTTPS endpoint routing requests to correct ND app                            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Software Versioning

Nexus Dashboard uses independent version streams for the platform and hosted applications. Check the Cisco compatibility matrix before any upgrade to confirm ND platform version compatibility with each installed application version.

| Component | Example Version |
|---|---|
| Nexus Dashboard platform | 3.1.1 |
| NDFC application | 12.2.2 |
| NDI application | 6.3.1 |

## Multi-Site Fabric Management

Nexus Dashboard is the single pane of glass for multiple data centre fabrics operating in parallel. It abstracts each fabric as a **site** — a logical boundary that can represent an ACI pod, an NDFC-managed VXLAN fabric, or a standalone Nexus switch domain.

- **VXLAN EVPN fabrics** — ND discovers underlay topology and BGP EVPN overlays; NDFC manages full lifecycle.
- **ACI fabrics** — ND integrates with the APIC cluster; NDO orchestrates cross-site policy.
- **FabricPath / classical Ethernet** — managed via NDFC in LAN Classic mode.

Cross-site capabilities include stretched VRFs, inter-site L3Out, shared services, and coordinated maintenance windows across sites without touching individual fabric controllers directly.

## Nexus Dashboard Fabric Controller (NDFC)

NDFC is the successor to Cisco DCNM, rehosted as an application on the Nexus Dashboard platform from version 12.0 onward. It covers the full fabric lifecycle for NX-OS environments.

**Fabric modes supported:**

| Mode | Use Case |
|---|---|
| VXLAN EVPN | Modern underlay/overlay DC fabric; automated BGP and NVE provisioning |
| FabricPath | Legacy L2 fabric (migration path to VXLAN) |
| LAN Classic | Traditional L2/L3 NX-OS management without overlay |
| SAN | FC zoning and VSAN management for MDS switches |

NDFC automates underlay provisioning (IS-IS or OSPF, iBGP peering, loopbacks), overlay provisioning (VRFs, VLANs, VNIs, L3VNI), and day-2 operations including fabric recalculation after topology changes.

## Nexus Dashboard Insights

NDI is the telemetry and analytics application hosted on Nexus Dashboard. It collects streaming telemetry from Nexus switches via gRPC and provides:

- **Anomaly detection** — baseline learning over time; statistical deviation alerts for latency, packet drops, and interface errors.
- **Flow path analysis** — traces a packet flow hop-by-hop through the fabric; identifies where drops or delays occur.
- **Protocol-level diagnostics** — BGP neighbour state history, OSPF adjacency flaps, VXLAN tunnel health, and ARP/ND table anomalies.
- **Compliance** — checks running configuration against best-practice rules and flags deviations.

Telemetry data is stored in Elasticsearch on the ND cluster. Retention is configurable (default 30 days for flow data, longer for counters).

## Nexus Dashboard Orchestrator

NDO provides multi-site policy orchestration across ACI and NDFC fabrics from a single workflow. Key concepts:

- **Schema and templates** — policy is defined in a schema (collection of templates); each template is associated with one or more sites.
- **Stretched VRFs and EPGs** — the same VRF and endpoint group can span multiple ACI or NDFC sites; NDO pushes consistent policy to each site's controller.
- **Disaster recovery policy** — NDO coordinates which site is primary for a given VRF/EPG and can orchestrate failover policy changes across sites.
- **Delta deploy** — NDO tracks what has been pushed; only changed objects are sent to the remote APIC or NDFC on each deploy cycle.

NDO does not replace APIC or NDFC — it orchestrates them. Each site controller continues to enforce policy locally; NDO ensures consistency.

## High Availability Architecture

Nexus Dashboard runs as a 3-node or 5-node cluster. Each node is a physical appliance (UCS) or virtual machine (VMware ESXi / KVM).

| Role | Count | Function |
|---|---|---|
| Primary node | 1 | Cluster leader; hosts control-plane services |
| Worker nodes | 2 (or 4) | Run application workloads (NDFC, NDI, NDO) |

**Internal cluster mechanics:**

- **etcd** — distributed key-value store for cluster state; requires quorum (≥2 nodes healthy in a 3-node cluster).
- **Kubernetes** — all ND services and hosted apps run as containerised pods; Kubernetes schedules and restarts failed pods automatically.
- **Rolling upgrade** — upgrades proceed node-by-node; the cluster remains operational throughout. A node is drained, upgraded, and rejoined before moving to the next.
- **Persistent volumes** — application data (Elasticsearch indices, configuration database) resides on persistent volumes that survive node restarts.

A 3-node cluster tolerates the loss of one node. For upgrades, always upgrade the ND platform before upgrading hosted application versions.

```mermaid
graph TB
  subgraph ND["Nexus Dashboard Cluster (3 Nodes)"]
    N1["Node 1 — Primary\netcd leader · cluster control"]
    N2["Node 2 — Worker\napplication pods"]
    N3["Node 3 — Worker\napplication pods"]
  end

  NDFC["NDFC\nFabric lifecycle\nVXLAN / LAN / SAN"]
  NDI["NDI\nTelemetry &amp; insights\nAnomaly detection"]
  NDO["NDO\nMulti-site orchestration\nACI + NDFC policy"]

  FAB1["Data Centre Fabric A\nNexus switches · ACI"]
  FAB2["Data Centre Fabric B\nNexus switches · NDFC"]
  FAB3["SAN Fabric\nMDS switches"]

  N1 --- N2
  N2 --- N3
  N1 --- N3
  ND --> NDFC
  ND --> NDI
  ND --> NDO
  NDFC -->|"NX-API / POAP"| FAB1
  NDFC -->|"NX-API / POAP"| FAB2
  NDFC -->|"SNMP / SSH"| FAB3
  NDI -->|"gRPC telemetry"| FAB1
  NDI -->|"gRPC telemetry"| FAB2
  NDO -->|"REST to APIC"| FAB1
  NDO -->|"REST to NDFC"| FAB2

  classDef ndnode fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef svc fill:#15803d,stroke:#166534,color:#fff
  classDef fab fill:#b45309,stroke:#92400e,color:#fff
  class N1,N2,N3 ndnode
  class NDFC,NDI,NDO svc
  class FAB1,FAB2,FAB3 fab
```

---

## See also

- [Nexus Dashboard — Design Standards](design-standards/)
- [Nexus Dashboard — Integrations](integrations/)
- [Nexus Dashboard — Deploy](../deploy/)
