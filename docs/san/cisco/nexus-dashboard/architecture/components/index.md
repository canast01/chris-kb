# Nexus Dashboard — Components

> Part of the [Nexus Dashboard](../../) reference.

---

## Overview

Nexus Dashboard is a Kubernetes-based platform. Each cluster node runs a set of core platform services plus the installed application workloads. This page covers the platform components, how they interact, and the ports required for infrastructure teams.

---

## Platform Layer Components

| Component | Role |
|---|---|
| Kubernetes control plane | Cluster management, pod scheduling, service discovery |
| etcd | Distributed key-value store for cluster state |
| Kafka | Internal event bus between platform services and apps |
| Elasticsearch | Log aggregation and search for platform and app logs |
| PostgreSQL | Platform configuration and identity data |
| Nginx (ingress) | HTTP/HTTPS routing to application services |
| Keycloak | Identity provider for ND UI and API authentication |
| MinIO | Object storage for backups and app-generated artifacts |
| Cilium | CNI for pod networking and network policy enforcement |

These services run across all three (or five) cluster nodes with replication. Loss of one node does not cause service interruption — quorum requires at least two nodes.

---

## Application Layer: NDFC (Nexus Dashboard Fabric Controller)

NDFC is the SAN and LAN fabric controller application. When installed on ND, it replaces standalone DCNM 11.x.

### NDFC Services

| Service | Role |
|---|---|
| NDFC Server | Core fabric management logic, REST API, GUI backend |
| Discovery Manager | SSH + SNMP based switch discovery and topology crawl |
| Performance Manager | SNMP MIB polling for interface counters |
| Event Manager | SNMP trap and syslog processing |
| Image Management | NX-OS firmware repository and staged upgrade engine |
| SAN Insights engine | Fibre Channel flow telemetry analysis (SAN Insights feature) |
| Zone Manager | Zone and device alias lifecycle management |

### NDFC SAN Insights

SAN Insights is a licensed feature within NDFC that correlates FC flow telemetry from MDS switches. It provides:
- Per-initiator-target-LUN I/O analytics (IOPS, throughput, latency)
- Slow-drain device identification
- Historical trending with anomaly detection
- Integration with NDI for cross-domain correlation

SAN Insights requires MDS switches running NX-OS 8.4(1a)+ and a SAN Insights license applied to NDFC.

---

## Application Layer: Nexus Dashboard Insights (NDI)

NDI provides network assurance and anomaly detection across ACI, VXLAN, and SAN fabrics.

### NDI Components

| Service | Role |
|---|---|
| Flow collector | Receives flow telemetry from managed fabrics |
| Anomaly engine | Machine-learning anomaly detection on topology and flows |
| Compliance engine | Policy compliance checking against defined intents |
| Change analysis | Tracks configuration changes and correlates with anomalies |
| Bug catalog | Matches running software versions against known bug databases |
| Dashboard renderer | Visualization layer for the NDI UI |

NDI requires a dedicated streaming telemetry connection from managed switches — ACI fabrics via APIC, Nexus via NX-OS streaming telemetry, MDS SAN via NDFC.

---

## Port Reference

### External (Client to ND Cluster)

| Port | Protocol | Service |
|---|---|---|
| 443 | HTTPS | ND UI, REST API, NDFC UI/API, NDI UI |
| 22 | SSH | ND cluster node CLI (ndadmin access) |

### ND Cluster Internal

| Port | Protocol | Service |
|---|---|---|
| 2380, 2379 | TCP | etcd (cluster state) |
| 6443 | TCP | Kubernetes API server |
| 9092 | TCP | Kafka event bus |
| 5432 | TCP | PostgreSQL |
| 9200 | TCP | Elasticsearch |
| 9000 | TCP | MinIO object storage |

Internal ports are not externally accessible; they are used only between ND cluster nodes.

### ND to Managed Infrastructure

| Port | Protocol | Direction | Purpose |
|---|---|---|---|
| 22 | SSH | ND → switch | NDFC switch management, config push |
| 161 | UDP | ND → switch | SNMP polling (NDFC Performance Manager) |
| 162 | UDP | Switch → ND | SNMP trap reception |
| 514 | UDP | Switch → ND | Syslog from managed switches |
| 443 | HTTPS | ND → APIC | ACI fabric management (NDO/NDI) |
| 443 | HTTPS | ND → switch | NX-OS REST API |
| 5640 | TCP | Switch → ND | Streaming telemetry (NDI) |

### ND to External Services

| Port | Protocol | Purpose |
|---|---|---|
| 636 | LDAPS | Active Directory / LDAP authentication |
| 49 | TCP | TACACS+ authentication |
| 1812 | UDP | RADIUS authentication |
| 123 | UDP | NTP |
| 25 / 587 | TCP | SMTP (email alerts) |
| 443 | HTTPS | Cisco Intersight connectivity |

---

## Cluster Health Indicators

The ND cluster health can be assessed from the UI and CLI:

### UI

Navigate to **Nexus Dashboard > Admin > System > Nodes**:
- All nodes should show **Healthy** status
- CPU and memory usage per node should be below 80%
- No nodes in **Unknown**, **Offline**, or **Degraded** state

### CLI (ndadmin)

```bash
# SSH to any ND cluster node
ssh ndadmin@nd-node1.corp.example.com

# Show cluster status
acs health
# Expected: all nodes healthy, services running

# Show node summary
acs nodes list

# Show app deployment status
acs apps status

# Show Kubernetes pod health (all pods should be Running)
kubectl get pods --all-namespaces | grep -v Running | grep -v Completed
# Zero output = all pods healthy
```

---

## Backup and Storage Components

| Component | Storage Location | Purpose |
|---|---|---|
| Platform backup | External SCP/SFTP (configured by admin) | Full cluster state backup |
| App data (NDFC) | Kubernetes persistent volumes on each node | NDFC database, zone databases |
| App data (NDI) | Elasticsearch + MinIO | Flow telemetry and anomaly data |
| MinIO object store | `/data/minio` on each node | App-generated files, backup archives |

Nexus Dashboard uses distributed storage via Rook/Ceph or local persistent volumes depending on the deployment type. Physical appliance deployments use local NVMe SSDs with replication across nodes.

---

## NDFC Deployment Modes on ND

NDFC on Nexus Dashboard supports three persona modes, selected at install time:

| Mode | Description |
|---|---|
| SAN Controller | Pure SAN (MDS FC fabric) management — zoning, VSAN, device alias, image management |
| LAN Controller | Pure LAN (Nexus VXLAN / BGP EVPN) fabric management |
| SAN + LAN | Combined SAN and LAN management on a single NDFC instance |

For SAN-only environments, deploy NDFC in **SAN Controller** mode to minimise resource consumption and operational complexity.
