# Nexus Dashboard Architecture

## Overview

Cisco Nexus Dashboard (ND) is a centralised operations platform for Cisco ACI and NX-OS data centre fabrics. It provides unified management, health monitoring, policy orchestration, and network insights through a microservices-based architecture. Services including Nexus Dashboard Fabric Controller (NDFC) and Nexus Dashboard Insights (NDI) run on top of the ND platform and are independently licensed and deployed.

## Cluster Architecture

A Nexus Dashboard cluster consists of 3 or 5 nodes. All nodes are peers in a Raft-based cluster consensus model. A virtual IP (VIP) provides a single management entry point regardless of which node the client connects to.

```
          ┌─────────────────────────────────────────┐
          │          Management VIP                  │
          └────────────┬────────────────────────────┘
                       │
          ┌────────────┼──────────────┐
     ND Node 01    ND Node 02    ND Node 03
   (Master)      (Worker)       (Worker)
   [API GW]      [Services]    [Services]
   [UI]          [NDFC]        [NDI]
```

| Cluster Size | Use Case |
|---|---|
| 3 nodes | Standard production deployment (NDFC or NDI, not both at scale) |
| 5 nodes | High availability / multi-service deployment (NDFC + NDI at scale) |
| 1 node | Lab or development only — not supported for production |

## Deployment Modes

| Mode | Platform | Notes |
|---|---|---|
| Physical (Cisco UCS / Nexus Dashboard appliance) | Dedicated Cisco hardware | Highest performance; recommended for large fabrics |
| Virtual (VMware ESXi) | vSphere VM | Supported for production; check Cisco sizing guide |
| On-premises SaaS | Cisco managed | Available for some ND services |
| Cloud (AWS/Azure) | Hosted VM | Supported for hybrid use cases |

## Services on Nexus Dashboard

Services are installed on top of the base ND platform as microservice bundles.

| Service | Purpose |
|---|---|
| Nexus Dashboard Fabric Controller (NDFC) | Replaces DCNM; manages NX-OS fabric provisioning, VXLAN BGP-EVPN, and IP Fabric for Media |
| Nexus Dashboard Insights (NDI) | Fabric health scoring, anomaly detection, flow telemetry, compliance checking |
| Nexus Dashboard Orchestrator (NDO) | Multi-site ACI policy orchestration |

Services are installed and managed from **Admin > App Store** or via a downloaded service image.

## ACI Integration

For ACI fabrics, the ACI APIC cluster is added to Nexus Dashboard as a managed site. ND communicates with APIC via its northbound REST API.

```text
Admin > Sites > Add Site
- Site type: ACI
- APIC address: <APIC-cluster-VIP>
- Username/password: (read-only for monitoring, admin for NDFC/NDO)
```

## NX-OS / NDFC Integration

For NX-OS fabrics managed by NDFC, switches are discovered and onboarded via NDFC's fabric creation workflow. NDFC communicates with switches via SSH and SNMP.

## Node Communication

| Path | Protocol | Port | Purpose |
|---|---|---|---|
| ND cluster nodes (internal) | HTTPS | TCP 2379, 2380, 9200 | etcd / Elasticsearch cluster |
| Browser → ND VIP | HTTPS | TCP 443 | Web UI and REST API |
| ND → ACI APIC | HTTPS | TCP 443 | Policy management |
| ND → NX-OS switches | SSH | TCP 22 | Configuration and telemetry |
| ND → NX-OS switches | SNMP | UDP 161/162 | Fault and telemetry |
| ND → Syslog target | Syslog | UDP/TCP 514 | Event forwarding |

## Network Interfaces

Each ND node requires two network interfaces:
- **Management interface**: used for admin access and communication with managed devices
- **Data / cluster interface**: used for inter-node cluster communication (dedicated subnet recommended)
