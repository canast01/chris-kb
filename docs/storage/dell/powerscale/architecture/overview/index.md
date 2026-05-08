# PowerScale — Architecture Overview

Dell PowerScale (formerly Isilon) is a scale-out NAS platform running the **OneFS** distributed operating system. All nodes in a cluster are peers — there is no dedicated metadata controller. The entire cluster presents a single namespace rooted at `/ifs` across all protocols (NFS, SMB, HDFS, S3, FTP). Clusters scale from a minimum of 3 nodes to 252 nodes, with each node added linearly contributing both capacity and throughput. PowerScale is available in all-flash (F-series), hybrid (H-series), and archive (A-series) node families.

## Scale-Out NAS Cluster

```mermaid
graph TB
  N1["Node 1"] & N2["Node 2"] & N3["Node 3"] & NN["Node N…"] --> INT["InfiniBand / 100GbE\nInternal Cluster Network"]
  INT --> SC["SmartConnect\n(DNS-based load balancing)"]
  SC --> NFS(["NFS v3/v4 Clients"])
  SC --> SMB(["SMB / CIFS Clients"])
  SC --> HDFS(["HDFS / S3 Clients"])
  classDef ctrl fill:#2563eb,stroke:#1d4ed8,color:#fff
  classDef net fill:#7c3aed,stroke:#6d28d9,color:#fff
  classDef host fill:#15803d,stroke:#166534,color:#fff
  class N1,N2,N3,NN ctrl
  class INT,SC net
  class NFS,SMB,HDFS host
```

---

## OneFS Distributed File System

OneFS is the operating system that runs identically on every node in the cluster. There is no single primary node or metadata controller — all nodes share responsibility for metadata, data, and client I/O. Key architectural properties:

### Single Global Namespace

All data lives under `/ifs`. There are no volumes, LUNs, or mount points within the cluster file system — the entire cluster is one flat namespace. Directories under `/ifs` can span multiple node pools and be managed with different protection levels, tiering policies, and quotas without any partitioning visible to clients.

### Distributed Metadata

File metadata (inode information, block maps, directory entries) is distributed across all nodes using the same erasure-coded protection as file data. No single node holds all the metadata for a directory — this is what prevents OneFS from having a metadata bottleneck as the cluster grows.

### Locking and Coherence

OneFS implements a distributed locking mechanism to maintain cache coherence. When a client modifies a file, the lock is held on a specific node (the owning node for that I/O operation), and data is written through to the cluster. NFS write caching and SMB opportunistic locks (oplocks) are managed within this distributed locking framework.

---

## HA Topology

OneFS implements redundancy at the file system level rather than through a primary/secondary controller model:

- **N+1 / N+2 / N+3 protection**: Data is protected using a distributed Reed-Solomon-like erasure coding scheme. Protection level (N+1 to N+4) is set per directory or at the pool level. N+2 can survive two simultaneous node or drive failures without data loss.
- **No single controller**: All nodes are symmetric. Losing a single node triggers a **SMARTFAIL** process where OneFS rebalances the data from the failed node across remaining nodes.
- **Intra-cluster network (back-end)**: Nodes are connected via a dedicated back-end InfiniBand or 10/25 GbE network for inter-node data and metadata traffic. This network must be isolated from client (front-end) traffic.
- **Quorum**: OneFS requires a strict majority of nodes to be online for write operations. Read access continues with fewer nodes, but write quorum must be maintained to prevent split-brain.
- **FlexProtect**: Dynamic protection rebalancing; continuously adjusts data layout as nodes are added, removed, or SmartFailed.

### Protection Levels

| Level | Survives | Overhead | Recommended Use |
|---|---|---|---|
| N+1 | 1 node or drive failure | ~33% (for 3-node cluster) | Minimum for any production cluster |
| N+2 | 2 simultaneous failures | Variable; lower on larger clusters | Standard recommendation for production |
| N+3 | 3 simultaneous failures | Higher; suitable for large clusters | High-value data; archive clusters |
| N+4 | 4 simultaneous failures | Highest | Regulatory or compliance data |
| 2x (mirroring) | Any 1 full copy lost | 100% | Small clusters or metadata-heavy workloads |

Protection level is set on a directory basis using the `isi set` command:

```bash
# View the protection level of a directory
isi get -D /ifs/data/project1 | grep protection

# Set N+2 protection on a directory
isi set -R -p +2 /ifs/data/project1

# Set 2x mirroring on a directory (e.g., for metadata-heavy paths)
isi set -R -p 2x /ifs/data/critical-metadata/
```

### Node Pool and Tier Architecture

Nodes of the same hardware generation and type form a **node pool**. Multiple node pools of different types (SSD, SAS, SATA/NL-SAS) can be grouped into **tiers**. File pool policies (SmartPools) control which tier data is placed on based on access time, file type, or custom criteria.

```
Cluster
├── Tier: Performance
│   └── Node Pool: F-series NVMe (6 nodes)
├── Tier: Capacity
│   └── Node Pool: H-series SAS+SSD (12 nodes)
└── Tier: Archive
    └── Node Pool: A-series NL-SAS (6 nodes)
```

Data written to a directory is placed in the node pool designated by the file pool policy for that path. SmartPools automatically migrates data between tiers as it ages (based on last-access time or modification time).

---

## Network Architecture

### Front-End (Client) Network

Each node has one or more front-end network interfaces (10 GbE or 25 GbE) that carry client NFS, SMB, S3, and HDFS traffic. All front-end interfaces across all nodes participate in SmartConnect, which distributes client connections across nodes using DNS-based load balancing.

Front-end interfaces are assigned to **IP pools** within **subnets**. Each **access zone** is associated with one or more IP pools, creating a logical boundary between client groups.

```bash
# List all configured subnets
isi network subnets list

# List all IP pools and their zone assignments
isi network pools list

# List all network interfaces (front-end and back-end)
isi network interfaces list
```

### Back-End (Cluster) Network

The back-end network is dedicated to inter-node communication: distributed locking, metadata updates, data block replication, and management. This network must be on a physically separate switch or VLAN from client traffic. Back-end interfaces are not exposed to clients and are not configurable by the administrator once the cluster is built — they are managed entirely by OneFS.

| Generation | Back-End Technology |
|---|---|
| Gen 6 nodes (H600, F800, A2000 series) | 40 GbE or InfiniBand |
| Gen 7 nodes (H7000, F910, A300 series) | 25/100 GbE |
| Gen 8 / PowerScale F600, F900, H700, H7000 | 25/100 GbE |

### SmartConnect — DNS Load Balancing

SmartConnect uses DNS to distribute client connection requests across the IP addresses in a pool. When a client resolves the SmartConnect zone name (e.g., `nfs.lon.storage.example.com`), the cluster's DNS service returns one of the pool IPs based on the configured load balancing policy.

**Setup requirements:**
1. The parent DNS zone (e.g., `lon.storage.example.com`) must have an NS record delegating the SmartConnect sub-zone to the cluster's nodes.
2. The SmartConnect service runs on all cluster nodes — any node can answer DNS queries for the SmartConnect zone.
3. Each access zone must have at least one IP pool with at least 3 IPs for effective load balancing.

```bash
# View SmartConnect zone configuration for a pool
isi network pools view <pool_name>

# Test SmartConnect DNS resolution
nslookup nfs.lon.storage.example.com <cluster-node-ip>

# List all IP pools and their SmartConnect zone names
isi network pools list -v | grep -E "Name|SC Zone|Policy"
```

**Load balancing policies:**

| Policy | Behaviour | Best For |
|---|---|---|
| `round-robin` | Rotates IPs sequentially across DNS responses | General-purpose; equal workload distribution |
| `cpu-usage` | Directs new connections to the node with lowest CPU | CPU-bound workloads (heavy NFS operations) |
| `throughput` | Directs new connections to the lowest-throughput node | Throughput-bound workloads (large file transfers) |
| `connection-count` | Directs to the node with the fewest active connections | Many short-lived connections |

---

## Access Zones

Access zones are logical partitions of the cluster namespace. Each access zone has:

- Its own root path under `/ifs`
- Its own set of NFS exports, SMB shares, and HDFS settings
- Its own authentication providers (AD, LDAP, local)
- Its own IP pool assignment (SmartConnect zone)

Access zones enable multi-tenancy on a single physical cluster without requiring separate hardware per tenant.

```bash
# List all access zones
isi zone zones list

# View an access zone configuration
isi zone zones view <zone_name>

# Create an access zone
isi zone zones create MediaZone --path /ifs/media

# Assign an IP pool to an access zone
isi network pools modify <pool_name> --access-zone MediaZone
```

Typical access zone design:

| Zone | Path | Clients | Auth Provider |
|---|---|---|---|
| `System` | `/ifs` | Administrators | Local OneFS |
| `MediaZone` | `/ifs/media` | Media production hosts | AD: MEDIA.EXAMPLE.COM |
| `AnalyticsZone` | `/ifs/analytics` | Hadoop cluster | LDAP |
| `BackupZone` | `/ifs/backup` | Backup servers | AD: CORP.EXAMPLE.COM |

---

## Data Path

When a client performs a write operation over NFS or SMB:

1. The client connects to a node IP from the SmartConnect pool (via DNS).
2. The receiving node (the **initiator node**) accepts the request and determines which nodes hold the stripes for the target file based on the current data layout.
3. The initiator node distributes data blocks to the appropriate **storage nodes** across the cluster via the back-end network.
4. Parity blocks are computed and written to additional nodes per the configured protection level.
5. When all stripes and parity blocks are confirmed written, the write is acknowledged to the client.

For read operations, the initiator node fetches data from whichever nodes hold the relevant stripes and returns the data to the client. If a node holding required stripes is unavailable, OneFS reconstructs the data from the parity blocks on the remaining nodes.

---

## Connectivity

| Protocol | Port | Notes |
|---|---|---|
| NFS v3 | TCP/UDP 2049 | Primary Unix/Linux client protocol; exposed per access zone |
| NFS v4 | TCP 2049 | NFSv4 with optional Kerberos security flavors |
| SMB 2.x/3.x | TCP 445 | Windows file sharing; per access zone |
| HDFS | TCP 8020 | Hadoop workloads; maps `/ifs` paths as HDFS volumes |
| S3 | TCP 9020 (HTTP) / 9021 (HTTPS) | Object storage API; per access zone |
| FTP/FTPS | TCP 21 / 990 | Supported but not recommended for high-throughput workloads |
| Management API (PAPI) | TCP 8080 (HTTP) / 8081 (HTTPS) | REST API for automation and management |
| SSH | TCP 22 | CLI access; restrict to management VLAN |
| SNMP | UDP 161 | Monitoring integration; use SNMP v3 only |
| SyncIQ | TCP 7722 | Cluster-to-cluster replication traffic |

### Network Design Summary

- Front-end client network: 10 or 25 GbE per node; aggregate bandwidth scales linearly with node count.
- Back-end cluster network: dedicated InfiniBand (older nodes) or 25/100 GbE; must be isolated from client traffic.
- SmartConnect DNS delegation: parent zone must have an NS record delegating the SmartConnect zone to the cluster's node IPs.
- Management network: separate or shared with front-end; restrict access via firewall to management VLAN source IPs.

---

## Node Hardware Families

| Family | Storage Type | Primary Use Case |
|---|---|---|
| F-series (F600, F900) | All-NVMe SSD | High-IOPS workloads: EDA, genomics, databases |
| H-series (H700, H7000) | NVMe + SAS HDD hybrid | Mixed workloads: home directories, general NAS |
| A-series (A300, A3000) | NL-SAS (high-density) | Archive and cold data; long-term retention |
| B-series (B100) | Balanced hybrid | Entry-level; smaller deployments |

Node pools must contain at least 3 nodes of the same hardware type. Mixing node types within a pool is not supported; mixed-type clusters use separate pools per hardware type.
