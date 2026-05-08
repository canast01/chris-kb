# Aria Operations — Components

## Cluster Node Roles

Aria Operations (formerly vROps) uses a distributed cluster architecture. Each node runs the same software but takes on a specific role during cluster formation.

| Node Role | Description |
|---|---|
| **Primary** | First node deployed; runs the cluster management UI, authentication, and analytics controller |
| **Primary Replica** | Hot standby for the Primary — automatically promoted if Primary fails |
| **Data** | Scale-out nodes for additional metric ingestion capacity and storage |
| **Remote Collector** | Lightweight proxy node deployed in remote sites or DMZs — forwards data to the cluster without joining it |
| **Cloud Proxy** | SaaS-hosted proxy for cloud (VMware Cloud on AWS) integrations |

---

## Sizing Guidelines

| Deployment Size | Nodes | vCPUs (per node) | RAM (per node) | Monitored Objects |
|---|---|---|---|---|
| Extra Small | Primary only | 4 | 16 GB | Up to 500 VMs |
| Small | Primary only | 8 | 32 GB | Up to 1,500 VMs |
| Medium | Primary + Replica | 16 | 48 GB | Up to 3,500 VMs |
| Large | Primary + Replica + 2 Data | 16 | 48 GB | Up to 10,000 VMs |
| Extra Large | Primary + Replica + 4+ Data | 24 | 64 GB | 10,000+ VMs |

Add a **Remote Collector** for each remote site or DMZ that cannot route management traffic directly to the cluster. Remote Collectors require 2 vCPUs and 4 GB RAM.

---

## Core Internal Services

| Service | Process / Unit | Role |
|---|---|---|
| Analytics | `vmware-vcops-analytics` | Core metric processing, anomaly detection, and capacity analytics |
| Collector | `vmware-vcops-collector` | Adapter framework — manages adapter instances and data collection |
| Web UI (Casa) | `vmware-casa` | REST API and web application server |
| GemFire | `vmware-vcops-gemfire` | In-memory distributed data grid — caches real-time metric data |
| Cassandra | `vmware-vcops-cassandra` | Long-term time-series metric storage |
| Postgres | `vmware-vcops-postgres` | Configuration, alert, and deployment metadata |
| Nginx | `nginx` | Front-end reverse proxy for HTTPS |
| Watchdog | `vmware-vcops-watchdog` | Service health monitor; restarts failed services automatically |

---

## Network Ports

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| 443 | TCP | Inbound | Web UI and REST API access |
| 22 | TCP | Inbound | SSH admin access (restrict to management network) |
| 4505 | TCP | Inbound | Salt master — Remote Collector registration and configuration |
| 4506 | TCP | Inbound | Salt master — Remote Collector data forwarding |
| 443 | TCP | Outbound | vCenter adapter, NSX adapter, cloud proxy |
| 9543 | TCP | Inbound (cluster-internal) | Cluster inter-node data replication |
| 10010 | TCP | Inbound (cluster-internal) | GemFire distributed data grid |
| 514 | UDP | Outbound | Syslog forwarding (optional) |

All cluster-internal ports must be open between all nodes (Primary, Replica, Data nodes). Remote Collectors only require outbound 443 to the cluster.

---

## Adapter Framework

Adapters (also called Solutions or Management Packs) extend Aria Operations to monitor additional technologies.

| Adapter | Source | Monitored Objects |
|---|---|---|
| vSphere Solution | Built-in | vCenter, ESXi, VMs, datastores, clusters |
| NSX-T Solution | Built-in / Marketplace | NSX-T managers, transport nodes, logical switches |
| Aria Ops for Logs | Built-in | Log Insight cluster health |
| Storage Devices | Management Pack | Pure Storage, NetApp, vSAN |
| Operating Systems | Management Pack | Windows, Linux via agent or WMI |
| AWS, Azure, GCP | Management Pack | Cloud resource monitoring |

Install management packs: **Administration → Solutions → Add Solution (PAK file)**.

---

## Persistent Storage Layout

| Path | Purpose | Minimum Size |
|---|---|---|
| `/storage/db` | Cassandra time-series metric data | 300 GB (large deployments) |
| `/storage/log` | Application and collector logs | 100 GB |
| `/storage/core` | OS and application binaries | 50 GB |
| `/dev/sdb` | Data disk (Cassandra) — add to expand capacity | As needed |

```bash
# Check storage usage on the primary node
df -h /storage/db /storage/log /storage/core

# Check Cassandra data directory sizes
du -sh /storage/db/cassandra/data/*
```
