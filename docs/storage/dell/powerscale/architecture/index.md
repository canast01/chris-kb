# PowerScale Architecture
## Overview

Dell PowerScale (formerly Isilon) is a scale-out NAS platform running the **OneFS** distributed operating system. All nodes in a cluster are peers — there is no dedicated metadata controller. The entire cluster presents a single namespace rooted at `/ifs` across all protocols (NFS, SMB, HDFS, S3, FTP). Clusters scale from a minimum of 3 nodes to 252 nodes, with each node added linearly contributing both capacity and throughput. PowerScale is available in all-flash (F-series), hybrid (H-series), and archive (A-series) node families.

## Components

| Component | Description |
|---|---|
| OneFS Node | Individual server unit; contains CPU, RAM, NVMe/SSD/HDD storage, and network interfaces. Every node runs OneFS and participates in the distributed file system. |
| OneFS OS | Distributed OS running on all nodes; manages a single coherent namespace across the cluster. |
| SmartPools | Policy-based data tiering; automatically migrates files between node pools (SSD, SAS, SATA/NL-SAS) based on access time or custom criteria. |
| Access Zones | Virtual NAS partitions; each zone has its own IP pool, authentication provider, and export/share namespace. Used to multi-tenant the cluster. |
| SmartConnect | DNS-based connection load balancing; distributes NFS/SMB client connections across node IP addresses within a zone. |
| SyncIQ | Asynchronous replication engine; replicates directories to a remote PowerScale cluster at scheduled intervals or continuously. |
| SnapshotIQ | Per-directory point-in-time snapshots stored within `/ifs/.snapshot/` |
| SmartQuotas | Per-directory or per-user capacity quotas with advisory, soft, and hard thresholds. |
| CloudPools | Tiering of cold data to object stores (AWS S3, Azure Blob, ECS) as a transparent extension of `/ifs`. |
| InsightIQ | (Legacy) Performance analytics collector; replaced by CloudIQ in current deployments. |

## HA Topology

OneFS implements redundancy at the file system level rather than through a primary/secondary controller model:

- **N+1 / N+2 / N+3 protection**: Data is protected using a distributed Reed-Solomon-like scheme. Protection level (N+1 to N+4) is set per directory or at the pool level. N+2 can survive two simultaneous node or drive failures.
- **No single controller**: All nodes are symmetric. Losing a single node triggers a **SMARTFAIL** process where OneFS rebalances the data from the failed node across remaining nodes.
- **Intra-cluster network (back-end)**: Nodes are connected via a dedicated back-end InfiniBand or 10/25 GbE network for inter-node data and metadata traffic. This is separate from the front-end client network.
- **Quorum**: OneFS requires a strict majority of nodes to be online for writes. Read access continues with fewer nodes but write quorum must be maintained.
- **FlexProtect**: Dynamic protection rebalancing; continuously adjusts data layout as nodes are added or removed.

## Connectivity

| Protocol | Notes |
|---|---|
| NFS v3/v4 | Primary Unix/Linux client protocol; exposed per access zone |
| SMB 2.x/3.x | Windows file sharing; per access zone |
| HDFS | Hadoop workloads; maps `/ifs` paths as HDFS volumes |
| S3 | Object storage API over S3-compatible interface; per access zone |
| FTP/FTPS | Supported but not recommended for high-throughput workloads |

Network design:
- Front-end client network: 10 or 25 GbE per node; aggregate bandwidth scales linearly with nodes.
- Back-end cluster network: dedicated InfiniBand (older nodes) or 25/100 GbE; must be isolated from client traffic.
- SmartConnect DNS delegation: parent zone must delegate the SmartConnect zone to the cluster's back-end node IPs.

## Sizing Guidelines

| Dimension | Guidance |
|---|---|
| Minimum cluster size | 3 nodes (OneFS requires minimum 3 for quorum and N+1 protection) |
| Target capacity utilisation | Stay below 80% of usable capacity; OneFS performance degrades above 90% |
| Node type selection | F-series (all-NVMe) for high-IOPS workloads; H-series for mixed; A-series for archive and cold data |
| Protection level | N+2 or N+3 recommended for production clusters; N+1 minimum |
| SmartConnect zones | One IP pool per access zone; at least 3 IPs per pool for effective round-robin balancing |
| SyncIQ bandwidth | Size WAN link to sustain peak change rate; enable SyncIQ throttle for business hours |
| Snapshot retention | Limit snapshot count per policy; large snapshot counts on heavily-changed directories consume metadata space |
