# Ceph — How It Works

<div class="kb-summary">
Ceph's RADOS layer stores all data as objects. Clients calculate data placement directly via CRUSH without a central metadata server — enabling linear scale with no bottlenecks.
</div>

```text
┌──────────────────────────────────── Ceph — How It Works ──────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   CRUSH: clients compute OSD placement locally; no central metadata lookup required            │  │
│   │   OSDs self-heal: when an OSD fails, peers detect it and begin replicating lost copies        │   │
│   │   PG (Placement Group): unit of replication; each PG maps to a set of OSDs via CRUSH          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   Client I/O path (block/file/object all converge here):                                      │   │
│   │                                                                                               │   │
│   │   Client → CRUSH(object, pool, CRUSH map) → PG ID → OSD set                                  │    │
│   │        → Primary OSD (accepts write)                                                          │   │
│   │        → Replicates to secondary OSDs (if replicated pool)                                    │   │
│   │        → Returns ACK to client when all replicas confirm                                      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    RADOS   = Reliable Autonomic Distributed Object Store; the storage engine underlying all Ceph      │
│    OSD     = Object Storage Daemon; one per disk; stores objects, handles replication + recovery      │
│    MON     = Monitor; maintains cluster maps (CRUSH, OSD, PG maps); 3 or 5 per cluster for quorum     │
│    MGR     = Manager; metrics, orchestration, dashboard; at least 2 per cluster (active/standby)      │
│    MDS     = Metadata Server; required for CephFS only; manages file system namespace                 │
│    PG      = Placement Group; unit of data distribution; typically 128-256 per OSD                    │
│    CRUSH   = Controlled Replication Under Scalable Hashing; placement algorithm; no metadata needed   │
│    BlueStore= Default OSD backend (since Nautilus); raw block device; no filesystem underneath        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Daemon Roles

| Daemon | Count | Purpose |
|---|---|---|
| OSD | 1 per disk | Stores objects; handles replication, recovery, rebalancing |
| MON | 3 or 5 | Maintains cluster maps; quorum required for writes |
| MGR | 2 (active + standby) | Metrics, orchestration, dashboard, alert manager |
| MDS | 1+ (for CephFS only) | CephFS namespace; active/standby HA supported |
| RGW | 1+ (for object storage) | S3/Swift-compatible object storage gateway |

## CRUSH Algorithm

```bash
# CRUSH map defines:
# 1. Devices (OSDs) with weight proportional to disk size
# 2. Buckets (hosts, racks, rows, DCs) — failure domains
# 3. Rules — how PGs are distributed across failure domains

# View current CRUSH map
ceph osd crush tree --show-shadow
ceph osd crush rule list
ceph osd crush rule dump

# Compile and decompile CRUSH map for editing
ceph osd getcrushmap -o crush.bin
crushtool -d crush.bin -o crush.txt
# Edit crush.txt
crushtool -c crush.txt -o crush-new.bin
ceph osd setcrushmap -i crush-new.bin
```

## Placement Groups (PGs)

```bash
# PG count rules of thumb:
# Target: ~100 PGs per OSD
# Formula: (OSDs × 100) / pool_size (round to nearest power of 2)
# Example: 30 OSDs, replica=3: (30 × 100) / 3 = 1000 → 1024 PGs

# Check PG status
ceph pg stat
ceph pg dump_stuck    # show stuck PGs (inactive, unclean, degraded)

# PG states meaning:
# active+clean    = Normal; all replicas present
# active+degraded = Some replicas missing; cluster is recovering
# inactive        = PG has no primary OSD; clients cannot access data
# backfilling     = New OSDs receiving backfill copies
# peering         = OSDs establishing agreement on object history
```

## Storage Pool Types

```bash
# Replicated pool (default) — stores N copies
# Pros: better performance; Cons: 3× storage overhead
ceph osd pool create rbd-pool 64 replicated
ceph osd pool set rbd-pool size 3          # 3 replicas
ceph osd pool set rbd-pool min_size 2      # minimum replicas for writes

# Erasure-coded pool — stores data + parity chunks (like RAID)
# Pros: ~1.5× overhead (vs 3× for replica); Cons: slower writes, no RBD overwrites
ceph osd erasure-code-profile set my-ec k=4 m=2   # 4 data + 2 parity chunks
ceph osd pool create ec-pool 64 erasure my-ec
```
