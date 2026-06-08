# Ceph — Procedures

```text
┌──────────────────────────── Ceph — Operational Procedures Overview ───────────────────────────────────┐
│                                                                                                       │
│  Procedure Categories                                                                                 │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  ┌─────────────────────────┐  ┌─────────────────────────┐  ┌─────────────────────────┐                │
│  │  OSD Replacement        │  │  Cluster Expansion      │  │  Maintenance & Tuning   │                │
│  │  osd out → wait PG heal │  │  ceph orch apply osd    │  │  scrub scheduling       │                │
│  │  purge → physical swap  │  │  add nodes via cephadm  │  │  PG count adjustment    │                │
│  │  osd create new device  │  │  crush reweight balance │  │  reweight for load bal  │                │
│  │  verify recovery done   │  │  monitor data migration │  │  controlled maintenance │                │
│  └─────────────────────────┘  └─────────────────────────┘  └─────────────────────────┘                │
│                                                                                                       │
│  OSD Replacement — Safe Sequence                                                                      │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  1. Confirm OSD down: ceph osd tree | grep down                                                       │
│  2. Mark out: ceph osd out osd.<id>  — triggers data migration away from failed OSD                   │
│  3. Wait: watch ceph -s  — BytesToResync reaches 0 before physically replacing disk                   │
│  4. Stop daemon: systemctl stop ceph-osd@<id>  ·  replace disk  ·  re-run ceph-volume                 │
│  5. Verify: ceph osd tree — new OSD shows up/in; ceph -s — HEALTH_OK                                  │
│                                                                                                       │
│  Cluster Expansion — New Node                                                                         │
│  ─────────────────────────────────────────────────────────────────────────────────────────────────    │
│  cephadm bootstrap adds admin node; ceph orch host add <hostname> adds new node to cluster            │
│  ceph orch apply osd --all-available-devices — auto-deploys OSDs on new node's disks                  │
│  CRUSH weight adjusts automatically; monitor rebalance via ceph -s until clean                        │
│  Manual reweight: ceph osd crush reweight osd.<id> <float> — adjust placement if needed               │
│                                                                                                       │
│  GLOSSARY                                                                                             │
│  OSD       — Object Storage Daemon; one per disk; stores, replicates, and recovers data               │
│  PG        — Placement Group; logical shard unit; PGs map to OSDs via CRUSH                           │
│  cephadm   — Ceph's orchestrator for deploying and managing cluster daemons via containers            │
│  CRUSH     — Controlled Replication Under Scalable Hashing; Ceph's data distribution algorithm        │
│  reweight  — adjusting an OSD's relative capacity share in CRUSH map                                  │
│  scrub     — data integrity scan; deep-scrub includes checksum verification of stored objects         │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

<div class="kb-summary">
Ceph operational procedures: OSD replacement, adding new nodes, reweighting for load balance, scrub scheduling, pool PG count adjustment, and controlled cluster maintenance.
</div>

## OSD Replacement

```bash
# When a disk fails and needs replacement:

# 1. Confirm OSD is down
ceph osd tree | grep down

# 2. Mark OSD out (triggers data migration to remaining OSDs)
ceph osd out osd.5

# 3. Wait for PGs to recover (BytesToResync reaches 0)
watch -n 10 ceph -s

# 4. Remove OSD daemon
ceph orch daemon rm osd.5 --force

# 5. Remove OSD from CRUSH and cluster
ceph osd crush rm osd.5
ceph auth del osd.5
ceph osd rm 5

# 6. Physically replace the disk

# 7. Add new OSD (cephadm discovers new disk automatically)
ceph orch apply osd --all-available-devices
# Or specifically:
ceph orch daemon add osd ceph-node2:/dev/sdb
```

## Add New Node

```bash
# 1. Prepare the new node: install dependencies, configure networking
# 2. Copy SSH key
ssh-copy-id -f -i /etc/ceph/ceph.pub root@new-node

# 3. Add host to cluster
ceph orch host add new-node 10.0.1.30

# 4. Add OSDs from new node
ceph orch daemon add osd new-node:/dev/sdb
ceph orch daemon add osd new-node:/dev/sdc

# 5. Monitor rebalancing (data redistributes to new OSDs)
watch -n 10 ceph -s   # wait for HEALTH_OK

# 6. Adjust CRUSH weight if needed (should happen automatically)
ceph osd tree
```

## Scrub Management

```bash
# Ceph scrubs data to detect bitrot and inconsistencies.
# Deep scrub: reads all objects and verifies checksums (I/O intensive).

# Check last scrub time for each PG
ceph pg dump | awk '{print $1, $19}' | sort -t: -k2 -k3 | head -20

# Schedule scrub during maintenance window
ceph osd set noscrub           # disable automatic scrub
ceph osd set nodeep-scrub      # disable deep scrub

# Trigger scrub on specific pool
ceph osd pool scrub rbd
ceph osd pool deep-scrub rbd

# Re-enable automatic scrubbing
ceph osd unset noscrub
ceph osd unset nodeep-scrub

# Scrub time restriction (restrict to off-hours)
ceph config set osd osd_scrub_begin_hour 22
ceph config set osd osd_scrub_end_hour 6
```

## Adjusting PG Count

```bash
# Increase PG count for a pool (can only increase; plan ahead)
# Warning: triggers rebalancing — do during low I/O window
ceph osd pool set rbd pg_num 256         # increase PGs
ceph osd pool set rbd pgp_num 256        # apply new placement

# Monitor PG split progress
watch -n 5 "ceph -s | grep pgs"

# Auto-scaling (Nautilus+) — let Ceph manage PG count
ceph osd pool set rbd pg_autoscale_mode on
ceph osd pool autoscale-status
```

## Maintenance Mode

```bash
# Before maintenance on an OSD node:
# 1. Disable OSD device replacement alert temporarily
ceph osd set noout    # prevent OSDs from being marked out during maintenance

# 2. Perform maintenance (patch, reboot, hardware work)

# 3. Verify OSDs come back up after reboot
ceph osd stat   # all OSDs should be up+in

# 4. Remove noout flag
ceph osd unset noout

# Flags reference:
# noout     = don't mark OSDs out when they disconnect (maintenance safety)
# noin      = don't mark OSDs in when they reconnect
# norecover = suspend recovery
# nobackfill= suspend backfill
# norebalance= suspend rebalancing
```
