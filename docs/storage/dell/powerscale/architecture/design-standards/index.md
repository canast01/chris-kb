---
tags:
  - architecture
  - dell
---
# PowerScale — Standards


<div class="kb-summary">
Standards reference covering Sizing Guidelines, Naming Conventions, Build Baseline, Configuration Checklist.
</div>

```text
┌──────────────────────────── Dell PowerScale Architecture Design Standards ────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Design standards: minimum 4 nodes for production HA; FlexProtect N+2 for 3-node min      │   │
│   │    Network: separate front-end client network and back-end InfiniBand/Ethernet node fabric    │   │
│   │   SmartPool tiers: performance pool for hot data; archive pool for cold; policy-driven move   │   │
│   │         SyncIQ: RPO ≥ minutes; define bandwidth throttle; separate replication IP pool        │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Capacity model → node type selection → protection level → SmartPool policy → network design        │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Sizing Standards      │  │       Protection Stds       │  │      Network Standards      │   │
│   │      ─────────────────      │  │      ─────────────────      │  │      ─────────────────      │   │
│   │       4 nodes min prod      │  │        N+2:1 default        │  │       Front/back split      │   │
│   │       Mixed node pools      │  │        N+3:1 critical       │  │        25/100G front        │   │
│   │        Cap plan +20%        │  │       Mirror for WORM       │  │       InfiniBand back       │   │
│   │      F-series for perf      │  │       No degraded run       │  │       Separate repl IP      │   │
│   │       A-series archive      │  │        Resync on add        │  │       SmartConnect DNS      │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Node pool configured → FlexProtect set → SmartPool tier policy defined → test failover             │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   │     Standard     │       Rule       │     Rationale     │   Anti-pattern   │       Risk       │   │
│   │ ──────────────── │ ──────────────── │ ───────────────── │ ──────────────── │──────────────────│   │
│   │    Node count    │   4 nodes min    │    Tolerate N+2   │   3 nodes prod   │No failure margin │   │
│   │    Protection    │  N+2:1 default   │   Two-fault tol.  │    N+1:1 only    │ Single fault tol │   │
│   │     Network      │  Separate FE/BE  │   No contention   │  Shared fabric   │ Back-end impact  │   │
│   │     Capacity     │  +20% headroom   │   Space for jobs  │    Full pool     │ SmartPool stall  │   │
│                                                                                                       │
│    Physical: nodes on ToR switches; back-end IB or 25G switch; separate mgmt VLAN                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    N+2:1         = FlexProtect level; tolerates simultaneous failure of 2 drives or 1 node            │
│    N+3:1         = Three-fault-tolerant protection; for mission-critical or large node pools          │
│    FlexProtect   = OneFS auto-protection; dynamically balances protection across available drives     │
│    Front-end net = Client-facing Ethernet; SmartConnect IP pool for NFS/SMB client connections        │
│    Back-end net  = Node-to-node InfiniBand or 25/100G Ethernet; carries metadata and data traffic     │
│    Separate repl IP= SyncIQ uses dedicated IP pool; prevents replication from saturating client LAN   │
│    Cap plan +20% = Keep 20% free in SmartPool; SmartPool jobs and snapshots need space headroom       │
│    SmartPool stall= SmartPool tier migration stops when pool is 100% full; data at risk               │
│    Resync on add = After adding nodes, OneFS rebalances data across the expanded pool                 │
│    Mirror WORM   = SmartLock compliance volumes use mirroring for highest protection                  │
│    ToR switch    = Top of Rack switch; connects node front-end ports to client network                │
│    No degraded run= Do not operate cluster long-term in degraded state; add node or replace drive     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

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

## Naming Conventions

| Object | Convention | Example |
|---|---|---|
| Cluster name | `<site>-ps-<number>` | `lon-ps-01` |
| Access zone | `<business-unit>-zone` | `media-zone`, `hdfs-zone` |
| IP pool | `<zone>-pool-<number>` | `media-zone-pool-01` |
| SmartConnect zone DNS name | `<zone>.<site>.storage.example.com` | `media.lon.storage.example.com` |
| NFS export path | `/ifs/<env>/<bu>/<project>` | `/ifs/prod/media/editorial` |
| SMB share name | `<bu>_<project>` | `media_editorial` |
| SyncIQ policy name | `<src-path-slug>-to-<dst-cluster>` | `editorial-to-ams-ps-01` |
| Snapshot policy name | `<path-slug>-snap-<frequency>` | `editorial-snap-daily` |
| Quota path | Matches NFS export path | `/ifs/prod/media/editorial` |

## Build Baseline

Every new PowerScale cluster or access zone deployment must meet the following before handover:

- **OneFS version**: deploy at N-1 or current GA; patch level at latest available fix.
- **Back-end network**: dedicated VLAN or physical switch for intra-cluster traffic; no client traffic allowed on back-end.
- **SmartConnect**: DNS delegation confirmed and tested; connection balancing policy set to `Round Robin` or `CPU Usage` per workload.
- **Authentication**: Active Directory provider joined for each access zone requiring Windows/SMB clients; NIS or LDAP configured for Unix/NFS clients.
- **Protection level**: set to N+2 minimum on all production directories.
- **SmartPools**: tiering policy reviewed; `Requested protection` default set per node pool.
- **SyncIQ**: replication policies created for all production paths with RPO defined; initial seed complete.
- **Quotas**: advisory, soft, and hard quota thresholds applied to all shared directories before production data lands.
- **Snapshots**: SnapshotIQ policy configured with at minimum 7-day daily retention for each production path.
- **CloudIQ / SNMP**: monitoring integration confirmed; node-down and capacity alerts enabled.
- **NTP**: cluster NTP configured and synchronised — required for Kerberos authentication and SyncIQ consistency.

## Configuration Checklist

- [ ] Cluster registered in CMDB with serial numbers, site, and owning team
- [ ] Back-end network connectivity verified between all nodes (`isi network interfaces list`)
- [ ] Access zones created per business unit; correct IP pools assigned
- [ ] SmartConnect DNS delegation verified with `nslookup <sc-zone-dns-name>`
- [ ] Active Directory or LDAP authentication joined and tested per zone
- [ ] NFS exports created with correct client permissions and root squash settings
- [ ] SMB shares created with correct ACL inheritance and ABE settings
- [ ] Quotas applied to all project directories; hard limits tested
- [ ] SyncIQ policies running; first replication completed without error
- [ ] Snapshot policies active; snapshot accessibility tested via `.snapshot` path
- [ ] SNMP or CloudIQ monitoring confirmed; test alert received
- [ ] Firewall rules confirmed: NFS 2049, SMB 445, HDFS 8020 open as required
