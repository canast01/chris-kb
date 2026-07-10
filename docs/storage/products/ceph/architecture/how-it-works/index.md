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


```text title="Expected output"
bluefs_db_total_bytes: 10737418240
bluefs_db_used_bytes: 2147483648
bluefs_log_total_bytes: 1073741824
bluefs_log_used_bytes: 536870912
bluefs_wal_total_bytes: 5368709120
bluefs_wal_used_bytes: 3221225472
bluefs_alloc_unit: 4096
bluefs_fragmentation: 0.15
bluestore_allocated: 8589934592
bluestore_stored: 7516192768
bluestore_compressed: 1073741824
bluestore_compression_ratio: 0.875
```

!!! warning "Common errors"
    **`Error: osd.0 does not exist`** — Verify the OSD ID is correct with `ceph osd tree` and ensure the OSD is up.
    **`Error connecting to daemon socket: No such file or directory`** — Start the OSD daemon with `systemctl start ceph-osd@0` or check that the OSD process is running.
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


```text title="Expected output"
PGS_BY_STATE       TOTAL  ACTIVE+CLEAN  ACTIVE+DEGRADED  PEERING
                    2048         2041              5           2
TOTAL_USED         TOTAL_AVAIL    TOTAL
1.2 TiB            8.8 TiB        10 TiB

PG_STAT OBJECTS  MISSING_ON  DEGRADED  MISPLACED  UNFOUND
1.45M    0         0          12        8          0

stuck pg query (inactive):
1.a2f
2.1c4
3.5e8

stuck pg query (unclean):
1.a2f
2.1c4
3.5e8
4.2b1

PG 1.a2f query:
{
  "state": "peering",
  "snap_trimq": "[]",
  "epoch": 847,
  "up": [2,0,1],
  "acting": [2,0],
  "acting_primary": 2,
  "up_primary": 2,
  "peer_missing": {
    "0": {"oid": 1024}
  }
}

HEALTH_WARN 2 pgs peering; 1 pg stuck inactive; 3 pgs degraded
    PG_AVAILABILITY Reduced data availability: 1 pg inactive
    PG_DEGRADATION Some data degraded: 3 pgs degraded
```

!!! warning "Common errors"
    **`Error ENOENT: pg 1.xyz not found`** — Verify the PG ID format matches output from `ceph pg stat` (use dot notation like `1.a2f`).
    **`Error: health detail requires a connected monitor`** — Ensure the Ceph cluster is running and your `ceph.conf` points to a valid monitor address.
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


```text title="Expected output"
ID    CLASS WEIGHT  TYPE NAME
-1           10.80 root default
-2            3.60   host node-01
 0    ssd  1.80       osd.0
 1    ssd  1.80       osd.1
-3            3.60   host node-02
 2    ssd  1.80       osd.2
 3    ssd  1.80       osd.3
-4            3.60   host node-03
 4    ssd  1.80       osd.4
 5    ssd  1.80       osd.5

reweighted item id 5 to weight 3.6
chooseleaf_descend_once: 1
straw2: 1
chooseleaf_vary_r: 0
chooseleaf_stable: 1
adjusted tunables to optimal values
got crush map from cluster
# begin crush map
tunable choose_local_tries 0
tunable choose_local_fallback_tries 0
tunable choose_total_tries 50
tunable chooseleaf_descend_once 1
tunable chooseleaf_vary_r 1
tunable chooseleaf_stable 1
tunable straw_calc_version 1
tunable allowed_bucket_algs 54
# devices
# types
# buckets
# rules
# end crush map
updated crush map
```

!!! warning "Common errors"
    **`Error EINVAL: invalid crush map`** — Verify the crush.txt syntax by running `crushtool -d crush.bin -o crush.txt` again and check for malformed bucket or rule definitions.
    **`Error: osd.5 does not exist`** — Confirm the OSD ID is valid by running `ceph osd tree` before attempting to reweight.
    **`Error EACCES: permission denied`** — Ensure you have admin privileges by running commands with `sudo` or as a user in the `ceph` group.
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


```text title="Expected output"
+++ quorum service is up-to-date +++
monmaps e3: 3 mons at {mon0=10.0.1.5:6789/0,mon1=10.0.1.6:6789/0,mon2=10.0.1.7:6789/0}
election epoch 42, quorum 0,1,2 mon0,mon1,mon2
fsid 550e8400-e29b-41d4-a716-446655440000
rank 0 (mon0) has 256 GB
rank 1 (mon1) has 256 GB
rank 2 (mon2) has 256 GB
{
  "election_epoch": 42,
  "quorum": [
    0,
    1,
    2
  ],
  "quorum_names": [
    "mon0",
    "mon1",
    "mon2"
  ],
  "quorum_age": 3600
}
mon.mon0: HEALTH_OK clock skew 0.012s
mon.mon1: HEALTH_OK clock skew 0.008s
mon.mon2: HEALTH_OK clock skew 0.031s
removed mon.mon3
```

!!! warning "Common errors"
    **`Error: mon.mon3 does not exist or not in monmap`** — Verify the MON ID exists with `ceph mon dump` before attempting removal.
    **`Error: cannot remove mon, not enough monitors in quorum`** — Ensure at least 2 MONs remain healthy; add a replacement MON before removing the failed one.
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


```text title="Expected output"
osd: 12 up, 12 in
        flags sortbitwise,recovery_deletes_unfound
     osd.0 up   in weight 1.00000 up_from 142 up_thru 156 down_thru 0 last_clean_interval [1-155] last_epoch_clean 156 flags live
     osd.1 up   in weight 1.00000 up_from 138 up_thru 156 down_thru 0 last_clean_interval [1-155] last_epoch_clean 156 flags live
     osd.7 up   in weight 1.00000 up_from 145 up_thru 156 down_thru 0 last_clean_interval [1-140] last_epoch_clean 156 flags live
     osd.11 up  in weight 1.00000 up_from 151 up_thru 156 down_thru 0 last_clean_interval [1-155] last_epoch_clean 156 flags live
marked osd.7 out
2024-11-15T09:42:31.234567+00:00 osd.0 osd.0 10.0.1.45:6800/12345 _ log [INF] : osd.7 out
{
  "num_watchers": 3,
  "watchers": [
    {"address": "10.0.1.46:6800/12346", "name": "osd.1", "cookie": 1},
    {"address": "10.0.1.47:6800/12347", "name": "osd.2", "cookie": 2},
    {"address": "10.0.1.48:6800/12348", "name": "osd.3", "cookie": 3}
  ]
}
```

!!! warning "Common errors"
    **`Error ENOENT: osd.7 does not exist`** — Verify the OSD number exists with `ceph osd tree` before attempting to mark it out.
    **`Error: admin_socket: stat failed on '/var/run/ceph/ceph-osd.0.asok': No such file or directory`** — Ensure the OSD daemon is running with `systemctl status ceph-osd@0` and the socket path is correct.
    **`Error EPERM: you do not have permission to perform this operation`** — Run commands with appropriate privileges (sudo or as ceph user) or ensure your keyring has admin capabilities.
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


```text title="Expected output"
pool 'rbd-pool' created
pool size set to 3
pool min_size set to 2
created erasure code profile my-ec
pool 'ec-pool' created
set pool 64 allow_ec_overwrites to true
pool 'rbd-pool' flags: hashpspool
pool 'ec-pool' flags: hashpspool
pool rbd-pool application rbd enabled
pool cephfs-data application cephfs enabled
pools:
  - name: rbd-pool
    id: 1
    type: replicated
    pg_num: 64
    pgp_num: 64
    size: 3
    min_size: 2
  - name: ec-pool
    id: 2
    type: erasure
    pg_num: 64
    pgp_num: 64
    erasure_code_profile: my-ec
```

!!! warning "Common errors"
    **`Error ENOENT: pool 'rbd-pool' does not exist`** — Run the pool creation command before attempting to set pool parameters.
    **`Error EINVAL: allow_ec_overwrites requires BlueStore`** — Verify all OSDs use BlueStore backend with `ceph osd metadata | grep osd_objectstore`.
    **`Error ERANGE: invalid erasure code profile: k=4 m=2 requires at least 6 OSDs`** — Ensure your cluster has at least k+m OSDs available before creating the erasure-coded pool.
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


```text title="Expected output"
$ ceph status
  cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_OK
  services:
    mon: 3 daemons, quorum ceph-mon01,ceph-mon02,ceph-mon03 (age 2d)
    mgr: ceph-mgr01(active, since 8d), ceph-mgr02(standby, since 8d)
    osd: 12 osds: 12 up, 12 in (since 3d)
  data:
    pools:   8 pools, 256 pgs
    objects: 1.24M objects, 847 GiB
    usage:   2.5 TiB used, 7.5 TiB / 10 TiB avail
    pgs:     256 active+clean

$ ceph health detail
HEALTH_OK

$ ceph osd stat
12 osds: 12 up, 12 in; epoch e847

$ ceph osd tree
ID  CLASS WEIGHT  TYPE NAME          STATUS REWEIGHT PRI-AFF
-1        10.0000 root default
-3         5.0000   host ceph-osd01
  0   ssd  1.0000     osd.0            up  1.00000 1.00000
  1   ssd  1.0000     osd.1            up  1.00000 1.00000
  2   ssd  1.0000     osd.2            up  1.00000 1.00000
  3   ssd  1.0000     osd.3            up  1.00000 1.00000
  4   ssd  1.0000     osd.4            up  1.00000 1.00000
-5         5.0000   host ceph-osd02
  5   ssd  1.0000     osd.5            up  1.00000 1.00000
...

$ ceph osd df
ID CLASS WEIGHT  REWEIGHT SIZE    RAW USE %USE VARS PGID STATUS
 0   ssd 1.00000  1.00000  1.0 T  847 G 84.7  1.02   ?   up
 1   ssd 1.00000  1.00000  1.0 T  823 G 82.3  0.98   ?   up
 2   ssd 1.00000  1.00000  1.0 T  856 G 85.6  1.05   ?   up
...
                   TOTAL 10.0 T  2.5 T 25.0

$ ceph pg stat
256 pgs: 256 active+clean; 0 B/s rd, 1.2 MB/s wr; 0 op/s

$ ceph pg dump_stuck
(no output — all PGs healthy)

$ ceph df detail
RAW STORAGE:
    CLASS     SIZE    AVAIL     USED RAW USED %RAW USED
    ssd    10.0 T    7.5 T    2.5 T    2.5 T     25.00
POOLS
```
## See also

- [Ceph — Design Standards](../design-standards/)
- [Ceph — Deploy](../../deploy/)
- [Ceph — Integrations](../integrations/)
