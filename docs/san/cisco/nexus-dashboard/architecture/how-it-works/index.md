# Nexus Dashboard — How It Works

```
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
