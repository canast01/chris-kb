# Nexus Dashboard — Overview

> Part of the [Nexus Dashboard](../../) reference.

---

## What Is Cisco Nexus Dashboard

Cisco Nexus Dashboard (ND) is a unified management and operations platform for Cisco data centre infrastructure. Rather than being a management application itself, it is a platform that hosts multiple Cisco-developed applications and provides shared services — identity, multi-site connectivity, API gateway, and a cluster management layer.

The platform follows an app-hosting model: applications are deployed onto ND and consume its shared infrastructure, similar to how apps run on a Kubernetes cluster. Nexus Dashboard is deployed as a 3-node or 5-node cluster for high availability, running on physical appliances (Cisco UCS), virtual machines (OVA), or on Amazon Web Services.

---

## Key Hosted Applications

| Application | Abbreviation | Role |
|---|---|---|
| Nexus Dashboard Fabric Controller | NDFC | SAN and LAN fabric management (successor to DCNM) |
| Nexus Dashboard Insights | NDI | Network assurance, anomaly detection, flow telemetry |
| Nexus Dashboard Orchestrator | NDO | Multi-site ACI and VXLAN fabric policy orchestration |
| Nexus Dashboard Data Broker | NDDB | OpenFlow-based network packet broker management |

For SAN environments, NDFC is the primary application. NDI provides additional telemetry and anomaly detection across SAN and LAN fabrics.

---

## Deployment Topology

```
┌─────────────────────────────────────────────────────────────────┐
│                  Nexus Dashboard Cluster (3 nodes)               │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐               │
│  │  ND Node 1 │   │  ND Node 2 │   │  ND Node 3 │               │
│  │ (primary)  │   │ (replica)  │   │ (replica)  │               │
│  └────────────┘   └────────────┘   └────────────┘               │
│         │                │                │                      │
│         └────────────────┴────────────────┘                      │
│                  Internal cluster fabric                         │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐                      │
│  │  NDFC (SAN/LAN)  │  │   NDI (Insights) │  (hosted apps)      │
│  └──────────────────┘  └──────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
         │                        │
┌────────▼────────┐    ┌──────────▼──────────┐
│  MDS SAN Fabric │    │  ACI / Nexus Fabric  │
│  (NDFC managed) │    │   (NDI / NDO managed)│
└─────────────────┘    └─────────────────────┘
```

Each ND cluster node runs a full set of platform services; the cluster provides active-active availability with quorum-based leader election.

---

## Nexus Dashboard Node Types

| Form Factor | Use Case | Notes |
|---|---|---|
| Physical appliance (UCS C220 M6) | Production with maximum performance | Preferred for large-scale deployments |
| VMware OVA | Smaller or lab environments | Supported for production with sizing guidelines |
| AWS (cloud nodes) | Multi-site with remote cloud sites | Requires ND connectivity between sites |

Mixed-form deployments (some physical, some virtual nodes) are supported but not recommended for simplicity.

---

## Network Interfaces Per Node

Each ND node has three logical networks:

| Interface | Purpose |
|---|---|
| Management (`mgmt0`) | UI access, REST API, external connectivity |
| Data (`data0`) | App-to-fabric communication (switch discovery, telemetry) |
| Cluster (`app0`) | Inter-node cluster communication and app replication |

The management and data networks must be reachable from managed sites. The cluster interface is used only between ND nodes and can be on an isolated network.

---

## VM Sizing (OVA Deployment)

| Cluster Size | vCPU per Node | RAM per Node | Storage per Node | Notes |
|---|---|---|---|---|
| 3-node (standard) | 16 | 64 GB | 500 GB | Supports NDFC + NDI |
| 5-node (large) | 24 | 128 GB | 1 TB | Required for large-scale NDI |

Nexus Dashboard uses all resources across all nodes. Thin provisioning is not recommended — use thick provisioning on production datastores.

---

## Supported Cisco Platforms (NDFC SAN)

When NDFC is deployed on Nexus Dashboard for SAN management, it supports:

| Platform | Role | Notes |
|---|---|---|
| MDS 9132T | 32G FC ToR switch | Fully managed |
| MDS 9148T | 32G FC ToR switch | Fully managed |
| MDS 9396T | 96-port 32G FC director | Fully managed |
| MDS 9706 / 9710 / 9718 | Modular 32G FC directors | Fully managed, ISSU |
| Nexus 93180YC-FX | FCoE-capable Nexus | FCoE fabric support |

---

## Relationship to DCNM

NDFC is DCNM 12.x. The same SAN management functionality (zoning, VSAN management, device aliases, image management, SAN Insights) is available in NDFC, but the deployment is fundamentally different:

| DCNM 11.x (standalone) | NDFC 12.x (on Nexus Dashboard) |
|---|---|
| Monolithic Java appliance | Application running on ND cluster |
| OVA or ISO deployment | ND cluster + NDFC app install |
| Standalone HA (2-node) | 3 or 5-node ND cluster |
| Direct switch communication | Via ND data network |
| Limited multi-site | Native multi-site via ND |
| EoL announced | Active development |

Migration from DCNM 11.x to NDFC requires re-deploying ND and re-discovering managed switches. Zone databases and device aliases can be exported from DCNM and re-imported into NDFC.

---

## Multi-Site Architecture

Nexus Dashboard supports multi-site deployments where a single ND cluster manages fabrics across multiple data centres. Each site is registered with the ND cluster and its managed switches communicate via the data network.

```
               ND Cluster (primary DC)
                     │
          ┌──────────┴──────────┐
     Site A                 Site B
  (DC1 Fabric)           (DC2 Fabric)
  MDS SAN + ACI          MDS SAN + ACI
```

Multi-site is supported for NDFC (SAN fabrics), NDO (ACI/VXLAN policy), and NDI (cross-site telemetry correlation).

---

## Software Versioning

Nexus Dashboard uses independent version streams:
- **Nexus Dashboard platform** version (e.g. 3.1.1)
- **NDFC** application version (e.g. 12.2.2)
- **NDI** application version (e.g. 6.3.1)

Platform and application versions are updated independently. Check the Cisco compatibility matrix (`cisco.com/go/nd-compat`) before any upgrade to confirm ND platform version compatibility with each installed application version.
