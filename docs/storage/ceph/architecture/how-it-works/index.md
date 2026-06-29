---
tags:
  - architecture
  - ceph
---
# Ceph — How It Works

<div class="kb-summary">
Ceph's RADOS layer stores all data as objects. Clients calculate data placement directly via CRUSH without a central metadata server — enabling linear scale with no bottlenecks.

*Applies to: Red Hat Ceph Storage · Upstream Ceph*
</div>

```d2
direction: right

C: "C" {shape: rectangle}
CR: "CR" {shape: rectangle}
PG: "PG" {shape: rectangle}
PRI: "PRI" {shape: rectangle}
SEC1: "SEC1" {shape: rectangle}
SEC2: "SEC2" {shape: rectangle}
ACK: "ACK" {shape: rectangle}

C -> CR
CR -> PG
PG -> PRI
PRI -> SEC1
PRI -> SEC2
SEC1 -> ACK
SEC2 -> ACK
```

## Daemon Roles

| Daemon | Location | Count | Failure Impact |
|---|---|---|---|
| OSD | One per data disk | Scales with disk count | Single OSD failure: degraded; cluster recovers automatically |
| MON | Dedicated MON nodes | 3 (small), 5 (large) | Lose quorum → cluster freezes all writes; reads continue |
| MGR | Co-located with MON or standalone | 2 (active + standby) | Active MGR failure: standby promotes in seconds; no I/O impact |
| MDS | MDS nodes (CephFS only) | 1+ active, 1+ standby | Active MDS failure: standby takes over; brief CephFS pause |
| RGW | Gateway nodes | 2+ (behind load balancer) | Single RGW down: load balancer routes to survivor |
| CrashCollector | All nodes | 1 per host | Passive; collects crash dumps; no I/O impact if absent |

## BlueStore Internals

BlueStore is the default OSD backend since Ceph Nautilus. It writes directly to raw block devices — no filesystem layer.

```d2
direction: right

WAL: "WAL" {shape: rectangle}
DB: "DB" {shape: rectangle}
DATA: "DATA" {shape: rectangle}

WAL -> DB
DB -> DATA
```

| Component | Device | Size | Purpose |
|---|---|---|---|
| WAL | NVMe/SSD | 1–2 GB per OSD | Absorbs write bursts; prevents HDD seek storms |
| DB (RocksDB) | NVMe/SSD | 4–64 GB per OSD | Stores object metadata, OMAP keys, PG state |
| Data | HDD or SSD | Remaining capacity | Actual object data bytes |

If WAL/DB are co-located on the same SSD as data, performance degrades significantly under heavy write load. Always separate WAL/DB to NVMe for production HDD-based OSDs.

```bash
# Check BlueStore device layout for a specific OSD
ceph osd metadata osd.0 | grep -E 'bluefs|bluestore'

# Check BlueStore stats
ceph daemon osd.0 perf dump | grep bluefs
```

## PG Lifecycle

| State | Meaning | Operator Action |
|---|---|---|
| `active+clean` | All replicas present; normal operation | None |
| `active+degraded` | One or more replicas missing; I/O continues | Monitor; allow recovery unless persistent |
| `active+recovering` | Cluster is copying missing replicas | Allow to complete; avoid further OSD changes |
| `active+remapped` | PG has been remapped to new OSD set; backfill pending | Normal during OSD addition/removal |
| `active+backfilling` | New OSDs receiving data; cluster rebalancing | Normal; throttle with `osd_recovery_max_active` if needed |
| `peering` | OSDs establishing agreement on object history | Usually transient; persistent peering = OSD issue |
| `stale` | PG has not been reported to MON recently | Investigate OSD connectivity and logs |
| `inactive` | No primary OSD; clients blocked | Critical; check OSD and MON status immediately |
| `incomplete` | Not enough OSDs with PG history to form quorum | Requires manual recovery; possible data loss |
| `unclean` | PG has objects that are not in a clean state | Check for failed OSDs, CRUSH issues |

```bash
# PG health commands
ceph pg stat
ceph pg dump_stuck                      # show PGs stuck in non-clean state
ceph pg dump_stuck inactive
ceph pg dump_stuck unclean
ceph pg <pg-id> query                   # detailed PG state and peer list
ceph health detail                      # full breakdown of health warnings
```

## CRUSH Deep Dive

CRUSH (Controlled Replication Under Scalable Hashing) is a pseudo-random placement algorithm. Clients compute OSD targets locally — no central lookup.

**Bucket type hierarchy** (root → datacenter → rack → host → osd):

| Level | Type | Purpose |
|---|---|---|
| `root` | Top-level bucket | Entry point for CRUSH rules; one per storage tier (e.g., `ssd`, `hdd`) |
| `datacenter` | DC grouping | AZ-level fault isolation |
| `rack` | Rack grouping | Rack-level fault isolation; preferred in environments with ≥ 3 racks |
| `host` | Per-host | Default failure domain; minimum for production |
| `osd` | Leaf node | Individual OSD; weight = raw capacity in TB |

**OSD weight** is set in TB of raw capacity. A 4 TB disk gets weight `4.0`; a 2 TB disk gets `2.0`. CRUSH distributes data proportionally to weight.

```bash
# View CRUSH tree
ceph osd crush tree --show-shadow

# Set OSD weight manually (use with caution — autoscale handles this)
ceph osd crush reweight osd.5 3.6

# Key CRUSH tunables
ceph osd crush show-tunables
# chooseleaf_descend_once: 1 = descent once per failure domain (faster, fewer retries)
# straw2: current default algorithm; provides best-balanced distribution

# Set optimal tunables for Luminous+
ceph osd crush tunables optimal

# Compile/decompile for manual CRUSH map editing
ceph osd getcrushmap -o crush.bin
crushtool -d crush.bin -o crush.txt
# Edit crush.txt to add/modify buckets and rules
crushtool -c crush.txt -o crush-new.bin
ceph osd setcrushmap -i crush-new.bin
```

## MON Quorum

MONs use the **Paxos** consensus protocol to maintain authoritative cluster maps. A majority must agree before any map update (OSD up/down, PG changes) is committed.

| MON Count | Tolerated Failures | Notes |
|---|---|---|
| 3 | 1 | Standard deployment; minimum for production |
| 5 | 2 | Large clusters or multi-site deployments |
| 1 | 0 | Lab only; any MON failure halts writes |

Quorum loss = cluster freezes all write operations. Existing reads may continue briefly from stale maps but will eventually stall.

```bash
# Verify MON quorum status
ceph mon stat
ceph mon dump
ceph quorum_status --format json-pretty

# Check MON clock skew (must be < 0.05 s; > 0.1 s causes quorum issues)
ceph time-sync-status

# Remove a failed MON
ceph mon remove <mon-id>
```

## OSD Heartbeat and Failure Detection

OSDs send heartbeat pings to their peers and to the MONs on a regular interval.

| Parameter | Default | Description |
|---|---|---|
| `osd_heartbeat_interval` | 6 s | How often an OSD pings its peers |
| `osd_heartbeat_grace` | 20 s | No response within this window → OSD marked **down** |
| `mon_osd_down_out_interval` | 600 s | Time after being marked down before being marked **out** (recovery starts) |
| `osd_recovery_max_active` | 3 | Max concurrent recovery operations per OSD |
| `osd_max_backfills` | 1 | Max concurrent backfill operations per OSD |

```bash
# Check OSD up/in status
ceph osd stat
ceph osd dump | grep -E 'up|down|in|out'

# Manually mark an OSD out (triggers recovery immediately)
ceph osd out osd.7

# Adjust recovery throttle (increase for faster recovery, lower for less I/O impact)
ceph tell osd.* injectargs '--osd-recovery-max-active 5'

# View OSD heartbeat peers
ceph daemon osd.0 dump_watchers
```

## Storage Pool Types

| Property | Replicated (size=3) | Erasure Coded (k=4 m=2) |
|---|---|---|
| Raw overhead | 3× | 1.5× |
| Minimum OSDs | 3 | 6 (k+m) |
| RBD support | Full (overwrites OK) | Requires `allow_ec_overwrites` |
| Recovery cost | Copy full object | Rebuild from k shards |
| IOPS impact | Low | Higher (CPU encode/decode) |
| Use case | VM disks, databases | Cold storage, backups |

```bash
# Replicated pool (default) — stores N copies
ceph osd pool create rbd-pool 64 replicated
ceph osd pool set rbd-pool size 3          # 3 replicas
ceph osd pool set rbd-pool min_size 2      # minimum replicas for writes

# Erasure-coded pool — stores data + parity chunks (like RAID)
ceph osd erasure-code-profile set my-ec k=4 m=2   # 4 data + 2 parity chunks
ceph osd pool create ec-pool 64 erasure my-ec

# Enable RBD overwrites on EC pool (requires BlueStore OSDs)
ceph osd pool set ec-pool allow_ec_overwrites true

# List pool details
ceph osd pool ls detail
ceph osd pool get rbd-pool all

# Set application tag (required for PG autoscaler to work correctly)
ceph osd pool application enable rbd-pool rbd
ceph osd pool application enable cephfs-data cephfs
```

## Cluster Health Quick Reference

```bash
# Overall status — always start here
ceph status
ceph health detail

# OSD status
ceph osd stat
ceph osd tree
ceph osd df                  # per-OSD utilisation %

# PG status
ceph pg stat
ceph pg dump_stuck           # PGs not in active+clean

# Pool usage
ceph df detail

# MON quorum
ceph mon stat
ceph quorum_status --format json-pretty

# Live I/O stats
ceph -w                      # watch real-time cluster events
```

## See also

- [Ceph — Design Standards](../design-standards/)
- [Ceph — Deploy](../../deploy/)
- [Ceph — Integrations](../integrations/)
