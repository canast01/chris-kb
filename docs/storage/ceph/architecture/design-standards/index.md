# Ceph — Design Standards

<div class="kb-summary">
Ceph cluster design: node and disk sizing, OSD-to-MON-to-MGR ratios, network separation (public vs cluster), CRUSH hierarchy for fault domains, and capacity planning rules.
</div>

```text
┌──────────────────────────────── Ceph — Design Standards ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Minimum production: 3 nodes × 4 OSDs; use 5 MONs for large clusters; 2 MGRs always         │    │
│   │   Network: public network (client I/O) and cluster network (replication) must be separate     │   │
│   │   CRUSH: define host-level failure domain; upgrade to rack if > 3 nodes per rack              │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Node Sizing           │  │      Network Design          │  │      Daemon Counts          │  │
│   │      ─────────────          │  │      ─────────────           │  │      ─────────────          │  │
│   │  Min: 3 OSD nodes           │  │  Public: client ↔ OSD       │  │  MON: 3 (up to 5+ nodes)   │    │
│   │  1 OSD per disk             │  │  Cluster: OSD ↔ OSD repl.   │  │  MGR: 2 (active/standby)   │    │
│   │  1 SSD/NVMe for WAL/DB      │  │  10 GbE public minimum      │  │  MDS: 1+ if CephFS          │   │
│   │  RAM: 4-6 GB per OSD        │  │  25 GbE+ cluster recommended│  │  RGW: 2+ if object storage  │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Node Sizing

| Role | Min Nodes | RAM Per Node | Notes |
|---|---|---|---|
| OSD nodes | 3 | 4–6 GB per OSD | 1 OSD per data disk; NVMe for WAL/DB |
| MON nodes | 3 | 16–32 GB | Separate nodes from OSD in production |
| MGR nodes | 2 | 16 GB | Run on MON nodes acceptable for small clusters |
| MDS nodes | 2+ | 32 GB+ | Memory scales with number of open files |
| RGW nodes | 2+ | 16 GB | Stateless; load-balance with HAProxy or DNS |

## Network Design

```text
Two networks required:
  Public network:   10.0.1.0/24   → client-to-OSD traffic (reads, writes)
  Cluster network:  10.0.2.0/24   → OSD-to-OSD replication and recovery

Why separate?
  Without a cluster network, recovery/replication traffic consumes client I/O bandwidth.
  Recovery after a disk failure can generate 100–500 Mbps per OSD.

Bandwidth guidelines:
  Public:  10 GbE minimum per OSD node; 25 GbE for NVMe-heavy clusters
  Cluster: 25 GbE minimum; 100 GbE for dense NVMe nodes (50+ OSDs per node)
```

## CRUSH Hierarchy Design

```bash
# Standard CRUSH hierarchy: datacenter → room → rack → host → OSD
# Minimum failure domain: host (3 hosts = 3 failure domains for replica=3)

# Example CRUSH rule for host-level failure domain
ceph osd crush rule create-replicated replicated_rule default host firstn

# Rack-level failure domain (better fault isolation)
ceph osd crush rule create-replicated rack_rule default rack firstn

# Assign pool to rack-level rule
ceph osd pool set rbd-pool crush_rule rack_rule

# Verify OSD placement
ceph osd crush tree
ceph osd df tree
```

## Capacity Planning

```text
Replicated pool (size=3):
  Raw capacity needed = usable × 3
  Safety threshold: never exceed 85% full (ceph warns at nearfull ratio)
  Full threshold: cluster stops writes at 95% (full ratio)

Erasure-coded pool (k=4, m=2):
  Raw capacity needed = usable × 1.5
  Better efficiency but slightly more complex recovery

OSD count formula:
  OSDs = Usable capacity target (TB) × replication factor / disk size (TB)
  Example: 100 TB usable, replica=3, 8 TB disks: (100 × 3) / 8 = 37.5 → 40 OSDs

PG count formula:
  PGs per pool = (Total OSDs × 100) / pool size (round to power of 2)
  Total PGs across all pools: aim for 100–200 per OSD
```
