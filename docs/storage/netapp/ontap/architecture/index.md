# ONTAP Architecture
## Overview

NetApp ONTAP is a clustered storage operating system that abstracts physical hardware into logical constructs, enabling non-disruptive operations, multi-protocol data access, and built-in data protection. The hierarchy flows from cluster → nodes → aggregates → SVMs → volumes, with data served across NFS, SMB/CIFS, iSCSI, FC, FCoE, NVMe/FC, and S3 protocols simultaneously from a single cluster.

## Components

| Component | Description |
|---|---|
| Cluster | The top-level administrative domain; 2–24 nodes sharing a common namespace and management interface |
| Node | An individual controller (AFF/FAS/ONTAP Select) running ONTAP; each node owns aggregates and serves data |
| HA Pair | Two nodes configured as an active-active pair sharing disk shelves; each node can take over the other's storage |
| Aggregate | A collection of RAID groups built from physical disks or SSDs; the raw storage pool owned by a node |
| SVM (Storage VM) | A logical tenant with its own namespace, network interfaces, protocols, and security domain; equivalent to a vFiler |
| Volume | A FlexVol (or FlexGroup) within an SVM; the unit of storage presented to hosts and clients |
| LUN | A block device within a volume, mapped to hosts via iSCSI or FC using igroups |
| LIF (Logical Interface) | A virtual IP or WWN endpoint on a node port; SVMs have data LIFs, the cluster has a cluster-management LIF |
| WAFL | Write Anywhere File Layout — ONTAP's internal filesystem that handles all I/O, snapshots, and deduplication |
| ONTAP Mediator | An external Linux VM used to provide a quorum witness for SnapMirror Business Continuity (SMBC) automatic failover |

## HA Topology

ONTAP HA pairs are active-active: both nodes serve I/O simultaneously and each holds a full copy of the partner's NVRAM write log. In the event of a node failure, the surviving node performs an automatic storage failover (takeover) within ~45 seconds. Cluster interconnect links (100GbE or InfiniBand) carry the NVRAM mirroring and heartbeat traffic between HA partners.

```
  ┌──────────────────────────────────────────────────────────┐
  │                        Cluster                           │
  │                                                          │
  │   ┌─────────────┐  Cluster IC  ┌─────────────┐          │
  │   │   Node 01   │◄────────────►│   Node 02   │  HA Pair │
  │   │  (AFF A400) │              │  (AFF A400) │          │
  │   └──────┬──────┘              └──────┬──────┘          │
  │          │                            │                  │
  │          └────────────┬───────────────┘                  │
  │                       │                                  │
  │              Shared Disk Shelves                         │
  │              (NS224 NVMe or SAS)                         │
  └──────────────────────────────────────────────────────────┘
```

For larger clusters, multiple HA pairs share the same cluster network and management infrastructure but own separate aggregates. A 4-node cluster has two HA pairs; aggregates are not shared across pairs unless SyncMirror is used.

## Connectivity

| Layer | Detail |
|---|---|
| Cluster network | 10/25/100GbE dedicated switch fabric for intra-cluster traffic (NVRAM sync, HA heartbeat, volume moves) |
| Data network | 10/25GbE ports carrying NFS, SMB, iSCSI, and NVMe/TCP LIFs; LIF home ports assigned per node |
| FC fabric | 16G/32G FC HBAs with dual-fabric zoning for FC and FCoE SAN; LIFs represented as WWPNs |
| Management network | 1GbE dedicated management port per node plus the cluster-management LIF; used for CLI/API/System Manager access |
| Intercluster network | Dedicated intercluster LIFs on 10/25GbE for SnapMirror and cluster peering traffic |

## Sizing Guidelines

- **Nodes per cluster**: 2–24 nodes; AFF A-series for all-flash, FAS for hybrid; ONTAP Select for software-defined deployments
- **Aggregates**: Keep usable capacity below 90% to avoid WAFL metadata overhead and Snapshot spill-over; target 70–80% for production
- **Volumes per SVM**: Supported up to several thousand per cluster; practical limit depends on workload mix and management overhead
- **HA pair fan-out**: Each HA pair supports up to 12–24 disk shelves depending on platform; consult the NetApp Hardware Universe for exact limits
- **Protocols per SVM**: An SVM can serve multiple protocols simultaneously; for security and isolation, dedicated SVMs per protocol are common in regulated environments
- **QoS**: Set throughput floors (minimum) and ceilings (maximum) per volume or workload using adaptive QoS policies to prevent noisy-neighbor issues in mixed workload clusters
