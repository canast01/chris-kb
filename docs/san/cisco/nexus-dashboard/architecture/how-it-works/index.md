# Nexus Dashboard — How It Works

## Overview

Cisco Nexus Dashboard (ND) is a unified management and operations platform for Cisco data centre infrastructure. It is a platform that hosts multiple Cisco-developed applications and provides shared services — identity, multi-site connectivity, API gateway, and a cluster management layer. Applications are deployed onto ND and consume its shared infrastructure, similar to how apps run on a Kubernetes cluster.

## Key Hosted Applications

| Application | Abbreviation | Role |
|---|---|---|
| Nexus Dashboard Fabric Controller | NDFC | SAN and LAN fabric management (successor to DCNM) |
| Nexus Dashboard Insights | NDI | Network assurance, anomaly detection, flow telemetry |
| Nexus Dashboard Orchestrator | NDO | Multi-site ACI and VXLAN fabric policy orchestration |
| Nexus Dashboard Data Broker | NDDB | OpenFlow-based network packet broker management |

For SAN environments, NDFC is the primary application.

## Deployment Topology

Nexus Dashboard is deployed as a 3-node or 5-node cluster for high availability.

```text
┌─────────────────────────────────────────────────────────────────┐
│                  Nexus Dashboard Cluster (3 nodes)               │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐               │
│  │  ND Node 1 │   │  ND Node 2 │   │  ND Node 3 │               │
│  └────────────┘   └────────────┘   └────────────┘               │
│  ┌──────────────────┐  ┌──────────────────┐                      │
│  │  NDFC (SAN/LAN)  │  │   NDI (Insights) │  (hosted apps)      │
│  └──────────────────┘  └──────────────────┘                      │
└─────────────────────────────────────────────────────────────────┘
         │                        │
  MDS SAN Fabric            ACI / Nexus Fabric
  (NDFC managed)            (NDI / NDO managed)
```

## Node Types

| Form Factor | Use Case | Notes |
|---|---|---|
| Physical appliance (UCS C220 M6) | Production with maximum performance | Preferred for large-scale deployments |
| VMware OVA | Smaller or lab environments | Supported for production with sizing guidelines |
| AWS (cloud nodes) | Multi-site with remote cloud sites | Requires ND connectivity between sites |

## Network Interfaces Per Node

| Interface | Purpose |
|---|---|
| Management (`mgmt0`) | UI access, REST API, external connectivity |
| Data (`data0`) | App-to-fabric communication (switch discovery, telemetry) |
| Cluster (`app0`) | Inter-node cluster communication and app replication |

## VM Sizing (OVA Deployment)

| Cluster Size | vCPU per Node | RAM per Node | Storage per Node | Notes |
|---|---|---|---|---|
| 3-node (standard) | 16 | 64 GB | 500 GB | Supports NDFC + NDI |
| 5-node (large) | 24 | 128 GB | 1 TB | Required for large-scale NDI |

## Multi-Site Architecture

A single ND cluster manages fabrics across multiple data centres. Each site is registered with the ND cluster and communicates via the data network.

```text
         ND Cluster (primary DC)
               │
    ┌──────────┴──────────┐
  Site A (DC1)         Site B (DC2)
  MDS SAN + ACI        MDS SAN + ACI
```

## Software Versioning

Nexus Dashboard uses independent version streams for the platform and hosted applications. Check the Cisco compatibility matrix before any upgrade to confirm ND platform version compatibility with each installed application version.

| Component | Example Version |
|---|---|
| Nexus Dashboard platform | 3.1.1 |
| NDFC application | 12.2.2 |
| NDI application | 6.3.1 |
