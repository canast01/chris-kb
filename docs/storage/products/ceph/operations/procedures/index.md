---
tags:
  - ceph
  - operations
description: "Ceph operational procedures: add/replace/decommission OSDs, reweight for capacity balance, scrub management, PG repair, and controlled cluster maintenance..."
---
# Ceph — Procedures

<div class="kb-summary">
Ceph operational procedures: add/replace/decommission OSDs, reweight for capacity balance, scrub management, PG repair, and controlled cluster maintenance with noout/norebalance flags.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

OSD: "OSD" {shape: rectangle}
ADD: "Add new OSD · ceph orch daemon add" {shape: rectangle}
REPL: "Replace failed OSD · out → wait → purge → add" {shape: rectangle}
DECOM: "Decommission host · drain all OSDs" {shape: rectangle}
PGM: "PGM" {shape: rectangle}
REPAIR: "Repair inconsistent PG · ceph pg repair pgid" {shape: rectangle}
SCRUB: "Scrub scheduling · oscrub / nodeep-scrub flags" {shape: rectangle}
MAINT: "MAINT" {shape: rectangle}
NOOUT: "Set noout flag · prevent auto-out during work" {shape: rectangle}
NORB: "Set norebalance · pause data migration" {shape: rectangle}
CAP: "CAP" {shape: rectangle}
RWU: "reweight-by-utilization · move data off full OSDs" {shape: rectangle}
ADDNODE: "Add new node · ceph orch host add" {shape: rectangle}

OSD -> ADD
OSD -> REPL
OSD -> DECOM
PGM -> REPAIR
PGM -> SCRUB
MAINT -> NOOUT
MAINT -> NORB
CAP -> RWU
CAP -> ADDNODE
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Add a New OSD (Single Device)

```bash
# 1. Verify device is clean — no existing filesystem or partition
lsblk -f /dev/sdX

# 2. Wipe device if it has previous data
cephadm ceph-volume lvm zap /dev/sdX --destroy

# 3. Add OSD via cephadm
ceph orch daemon add osd <hostname>:/dev/sdX

# 4. Verify new OSD appears and cluster recovers
ceph osd tree                    # new OSD with correct weight
watch -n 10 ceph -s              # HEALTH_OK after rebalance completes
```


```text title="Expected output"
NAME MAJ:MIN RM SIZE RO TYPE MOUNTPOINTS
sdx    8:0    0 1.8T  0 disk 

Zapping: /dev/sdx
Zapping lvm member /dev/sdx
Zapping done for: /dev/sdx

Deploying daemon osd.12 on host ceph-node-03
Waiting for daemon osd.12 to deploy...
Deployed osd.12

ID CLASS WEIGHT   TYPE NAME           STATUS REWEIGHT PRI-AFFINITY
-1       1.80000 root default
-3       1.80000 host ceph-node-03
12   ssd 1.80000     osd.12              up  1.00000 1.00000

Every 10.0s: ceph -s                                    Mon Dec 19 14:32:15 2024
  cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_OK
  services:
    mon: 3 daemons, quorum ceph-mon-01,ceph-mon-02,ceph-mon-03 (age 2d)
    osd: 13 osds, 13 up, 13 in; 1 remapped pgs
  data:
    objects: 2.45M
    usage:   18.5 TiB / 23.4 TiB
    state:   active+clean
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: No such device /dev/sdX` | Replace `/dev/sdX` with the actual device name (e.g. `/dev/sdb`) and verify it exists with `lsblk`. |
    | `Error: OSD deployment failed: device /dev/sdx is already in use` | Run `cephadm ceph-volume lvm zap /dev/sdx --destroy` before attempting to add the OSD. |
    | `Error: host <hostname> not found in CRUSH map` | Ensure the hostname matches exactly what `ceph orch host ls` shows and the host is already added to the cluster. |
## Replace a Failed OSD

```bash
# 1. Identify failed OSD — note ID and host
ceph osd tree | grep down

# 2. Set noout before starting to avoid false alarms
ceph osd set noout

# 3. Mark OSD out — starts data migration away from failed disk
ceph osd out <id>

# 4. Wait for PGs to recover before touching hardware
watch -n 10 ceph -s              # wait until active+clean

# 5. Stop the OSD daemon
ceph orch daemon stop osd.<id>

# 6. Replace the physical disk on the host

# 7. Purge old OSD entry from cluster
ceph osd purge <id> --yes-i-really-mean-it

# 8. Add new OSD on the same host/device
ceph orch daemon add osd <hostname>:/dev/sdX

# 9. Remove noout
ceph osd unset noout

# 10. Verify
ceph osd tree                    # new OSD has correct weight
ceph -s                          # HEALTH_OK
```


```text title="Expected output"
# 1. Identify failed OSD
-2       0.87109 root default
-1       0.87109     host ceph-node-03
 0   ssd 0.29036         osd.0      up   1.00000 1.00000
 1   ssd 0.29036         osd.1      up   1.00000 1.00000
 4   ssd 0.29036         osd.4    down   1.00000 1.00000

# 2. Set noout
noout flag(s) set

# 3. Mark OSD out
marked out osd.4

# 4. Wait for PGs to recover
Every 10.0s: ceph -s
  cluster:
    id:     a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
    health: HEALTH_WARN
            1 osds down
            Degraded data redundancy: 128/384 objects degraded (33.3%), 64 pgs degraded
  services:
    mon: 3 daemons, quorum ceph-mon-01,ceph-mon-02,ceph-mon-03 (age 2h)
    mgr: ceph-mgr-01(active, since 1h), ceph-mgr-02(standby, since 1h)
    osd: 5 osds, 4 up, 1 down; 128 remapped pgs

# 5. Stop the OSD daemon
Scheduled daemon stop for osd.4 on host ceph-node-03

# 7. Purge old OSD entry
purged osd.4

# 8. Add new OSD
Created osd(s) 4 for ceph-node-03:/dev/sdX

# 10. Verify
-2       0.87109 root default
-1       0.87109     host ceph-node-03
 0   ssd 0.29036         osd.0      up   1.00000 1.00000
 1   ssd 0.29036         osd.1      up   1.00000 1.00000
 4   ssd 0.29036         osd.4      up   1.00000 1.00000

  cluster:
    id:     a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
    health: HEALTH_OK
    services:
      mon: 3 daemons, quorum ceph-mon-01,ceph-mon-02,ceph-mon-03 (age 2h)
      osd: 5 osds, 5 up, 0 down
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error ENOENT: osd.4 does not exist` | Verify the OSD ID is correct with `ceph osd tree` before attempting to purge. |
    | `Error: device /dev/sdX is already in use by osd.X` | Ensure the old OSD is fully purged and the device is wiped with `sgdisk --zap-all /dev/sdX` before re-adding. |
    **
## Decommission a Host (Remove All Its OSDs)

```bash
# 1. Set both noout and norebalance to control data migration
ceph osd set noout
ceph osd set norebalance

# 2. Identify all OSD IDs on the target host
ceph osd tree | grep <hostname>

# 3. Mark all host OSDs out
for i in <id1> <id2> <id3>; do ceph osd out $i; done

# 4. Unset norebalance to allow data to migrate away
ceph osd unset norebalance

# 5. Wait for all PGs to return to active+clean
watch -n 10 ceph -s

# 6. Drain and stop all daemons on the host
ceph orch host drain <hostname>

# 7. Purge each OSD from the cluster map
for i in <id1> <id2> <id3>; do
    ceph osd purge $i --yes-i-really-mean-it
done

# 8. Remove host from orchestrator
ceph orch host rm <hostname>

# 9. Unset noout
ceph osd unset noout
```


```text title="Expected output"
noout flag set
norebalance flag set
osd.2 host=storage-node-04 class=ssd
osd.5 host=storage-node-04 class=ssd
osd.8 host=storage-node-04 class=ssd
marked out osd.2
marked out osd.5
marked out osd.8
norebalance flag unset
    cluster 8a2f3c1e-9d4a-4f2b-b1c3-7e5d9f2a6c4b
     health HEALTH_OK
     monmap e12: 3 mons at {mon01=10.0.1.5:6789/0, mon02=10.0.1.6:6789/0, mon03=10.0.1.7:6789/0}
     osdmap e2847: 24 osds: 21 up, 21 in; 3 out
     pgmap v8934: 512 pgs: 512 active+clean; 2.4 TiB data, 6.8 TiB used, 18 TiB avail
Draining host storage-node-04...
Removed osd.2
Removed osd.5
Removed osd.8
Removed host storage-node-04
noout flag unset
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error EBUSY: osd.2 is still in use` | Wait longer for PGs to finish migrating before attempting purge, or check `ceph osd safe-to-destroy osd.2` first. |
    | `Error: host storage-node-04 still has daemons` | Ensure `ceph orch host drain` completes fully before removing the host; check `ceph orch ps` to verify all daemons are stopped. |
    | `Error ENOENT: osd.2 does not exist` | Do not re-run the purge loop; each OSD is removed only once, so verify the OSD ID is correct in the for loop. |
## Reweight OSDs to Balance Capacity

```bash
# Check current utilization per OSD
ceph osd df tree

# Sort to find most-full OSDs
ceph osd df tree | sort -k8 -rn

# Automatic reweight: move data off OSDs more than 115% of average utilization
ceph osd reweight-by-utilization 115

# Manual reweight for a single OSD (lower value = less data placed on it)
ceph osd reweight <id> <0.0–1.0>

# Reweight all OSDs to match their actual device capacity (after adding larger disks)
ceph osd crush reweight-all

# Verify effect after rebalance
ceph osd df tree | sort -k8 -rn
```


```text title="Expected output"
ID  CLASS WEIGHT  TYPE NAME                STATUS REWEIGHT SIZE    RAW USE %USE VARS PGS
-1       259.72  root default
-3        86.57   host ceph-node-01
 0   ssd  10.82    osd.0                    up  1.00000 10.8T 8.2T 75.8  1.02 312
 1   ssd  10.82    osd.1                    up  1.00000 10.8T 9.1T 84.3  1.09 298
 2   ssd  10.82    osd.2                    up  1.00000 10.8T 9.5T 87.9  1.14 285
-5        86.57   host ceph-node-02
 3   ssd  10.82    osd.3                    up  1.00000 10.8T 7.9T 73.1  0.95 325
 4   ssd  10.82    osd.4                    up  1.00000 10.8T 8.8T 81.5  1.06 310
 5   ssd  10.82    osd.5                    up  1.00000 10.8T 9.3T 86.0  1.12 292
-7        86.58   host ceph-node-03
 6   ssd  10.82    osd.6                    up  1.00000 10.8T 6.2T 57.4  0.74 401
 7   ssd  10.82    osd.7                    up  1.00000 10.8T 7.1T 65.7  0.85 378
 8   ssd  10.82    osd.8                    up  1.00000 10.8T 8.9T 82.3  1.07 308

REWEIGHT_BY_UTILIZATION: reweighted 3 osds [2,5,1] by factor 0.95
(no output — command completes silently)
(no output — command completes silently)

ID  CLASS WEIGHT  TYPE NAME                STATUS REWEIGHT SIZE    RAW USE %USE VARS PGS
-1       259.72  root default
-3        86.57   host ceph-node-01
 0   ssd  10.82    osd.0                    up  1.00000 10.8T 8.1T 75.0  0.98 318
 1   ssd  10.82    osd.1                    up  0.95000 10.8T 8.6T 79.6  1.04 289
 2   ssd  10.82    osd.2                    up  0.95000 10.8T 8.9T 82.4  1.08 276
-5        86.57   host ceph-node-02
 3   ssd  10.82    osd.3                    up  1.00000 10.8T 7.8T 72.1  0.94 332
 4   ssd  10.82    osd.4                    up  1.00000 10.8T 8.7T 80.5
```
## Manage Scrub Operations

```bash
# Check scrub status across PGs
ceph pg dump | grep scrub

# Force immediate scrub on a specific PG
ceph pg scrub <pgid>

# Force scrub on all PGs in a pool
ceph osd pool scrub <pool>
ceph osd pool deep-scrub <pool>

# Disable scrub during maintenance window
ceph osd set noscrub
ceph osd set nodeep-scrub

# Re-enable after maintenance
ceph osd unset noscrub
ceph osd unset nodeep-scrub

# Restrict automatic scrub to off-hours
ceph config set osd osd_scrub_begin_hour 1
ceph config set osd osd_scrub_end_hour 5

# Per-pool scrub disable (does not affect other pools)
ceph osd pool set <pool> noscrub true
ceph osd pool set <pool> nodeep-scrub true
```


```text title="Expected output"
PG_STAT OBJECTS MISSING_ON_PRIMARY DEGRADED MISPLACED VERSION STATE
1.0        1024                  0        0         0   12'34 active+clean
1.1        2048                  0        0         0   11'28 active+clean+scrubbing
1.2        512                   0        0         0   10'15 active+clean
1.3        1536                  0        0         0   12'40 active+clean+deep-scrubbing
1.4        2560                  0        0         0   11'32 active+clean
...
instructing pg 1.1 to scrub
instructing pg 1.3 to scrub
instructing pg 1.4 to scrub
instructing pg 1.5 to scrub
instructing pg 1.6 to scrub
...
noscrub,nodeep-scrub set
osd_scrub_begin_hour = 1
osd_scrub_end_hour = 5
set pool 3 noscrub to true
set pool 3 nodeep-scrub to true
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error EINVAL: invalid pool name '<pool>'` | Replace `<pool>` with an actual pool name like `rbd` or `cephfs_data`, or list pools with `ceph osd pool ls`. |
    | `Error ENOENT: pool does not exist` | Verify the pool exists and is not being deleted; check with `ceph osd pool ls`. |
## Repair an Inconsistent PG

```bash
# 1. Identify inconsistent PGs
ceph health detail | grep inconsistent

# 2. Trigger repair on the affected PG
ceph pg repair <pgid>

# 3. Monitor repair progress
watch -n 10 "ceph pg <pgid> query | python3 -m json.tool | grep state"

# 4. Confirm PG returns to active+clean
ceph pg stat

# If repair fails — identify which OSD has the bad object copy
ceph pg <pgid> query | python3 -m json.tool | grep acting

# Pull the object from the good OSD manually
rados get -p <pool> <object> /tmp/recovered-object
rados put -p <pool> <object> /tmp/recovered-object
```


```text title="Expected output"
HEALTH_ERR 1 pg inconsistent
    pg 2.4c is inconsistent

PG_STATE_INCONSISTENT

Every 10.0s: ceph pg 2.4c query | python3 -m json.tool | grep state

    "state": "recovering+inconsistent",
    "state": "recovering",
    "state": "active+clean",

PG_STAT objects 1024 bytes 4194304 log 512
    2.4c: active+clean [3,1,2] r=0 lpr=512 pi=256..512 lpr=512 pi=256..512 cdhr=513 lis=512 empty_epoch=0

    "acting": [3, 1, 2],
    "acting_primary": 3,

object recovered-object retrieved from pool default.rgw.buckets.data
object recovered-object written to pool default.rgw.buckets.data
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `error: pg 2.4c query: No such file or directory` | Verify the PG ID format is correct (use `ceph pg ls` to list valid PGs) and ensure the cluster is in a queryable state. |
    | `error: [Errno 2] No such file or directory: '/tmp/recovered-object'` | Create the temporary directory first with `mkdir -p /tmp` or use a writable path like `$HOME/recovered-object`. |
    | `Error: pool <pool> does not exist` | Confirm the pool name with `ceph osd pool ls` and substitute the correct pool name in the rados commands. |
## OSD Replacement (Original Procedure — ceph orch)

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


```text title="Expected output"
osd.5 down                                    1        1.0          1.0B        0 B        0 B 0 B
cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_WARNING
            Degraded data redundancy: 342 pgs degraded
    
    services:
      mon: 3 daemons, quorum ceph-mon1,ceph-mon2,ceph-mon3 (age 2h)
      mgr: ceph-mgr1(active, since 45m), ceph-mgr2
      osd: 12 osds: 11 up, 1 down; 11 in, 1 out
    
    data:
      pools:   8 pools, 256 pgs
      objects: 1.24M objects, 4.2 TiB
      usage:   8.9 TiB used, 31 TiB / 40 TiB avail
      pgs:     342 degraded+undersized+peering
      BytesToResync: 0 B

osd.5 marked out.
osd.5 removed.
osd.5 deleted.
Removed /var/lib/ceph/osd/ceph-5

Scheduled osd.6 addition for ceph-node2:/dev/sdb
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error ENOENT: osd.5 does not exist` | Verify the OSD number is correct and the daemon hasn't already been removed with `ceph osd tree`. |
    | `Error: OSD osd.5 is still in (in the cluster); must be marked out first` | Run `ceph osd out osd.5` before attempting to remove the OSD. |
    | `Error: Device /dev/sdb is already in use or has an existing LVM/partition table` | Wipe the disk with `sgdisk -Z /dev/sdb` or `dd if=/dev/zero of=/dev/sdb bs=1M count=100` before re-adding it to the cluster. |
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


```text title="Expected output"
/usr/bin/ssh-copy-id: INFO: Source of key(s) to be installed: "/etc/ceph/ceph.pub"
/usr/bin/ssh-copy-id: INFO: attempting to log in with the following key(s):
/usr/bin/ssh-copy-id: INFO: 1 key sent to root@new-node, trying passwd authentication.
Number of key(s) added: 1

Added host 'new-node' with addr '10.0.1.30'

Scheduling osd.4 (device /dev/sdb) on host 'new-node'
Scheduling osd.5 (device /dev/sdc) on host 'new-node'

Every 10.0s: ceph -s                                                    Mon Jan 15 14:32:45 2025

  cluster:
    id:     a1b2c3d4-e5f6-7890-abcd-ef1234567890
    health: HEALTH_WARN
    
  services:
    mon: 3 daemons, quorum ceph-mon01,ceph-mon02,ceph-mon03 (age 2h)
    mgr: ceph-mgr01(active, since 1h), ceph-mgr02(standby, since 1h)
    osd: 6 osds: 6 up, 6 in; 145 GiB data, 892 GiB total, 747 GiB avail
    
  data:
    pools:   3 pools, 96 pg
    objects: 45.2k objects, 142 GiB
    usage:   145 GiB used, 747 GiB / 894 GiB avail
    pgs:     96 active+clean

ID  CLASS  WEIGHT   TYPE NAME          STATUS REWEIGHT PRI-AFF
-1         0.87500  root default
-3         0.87500      host ceph-node01
 0    ssd  0.43750          osd.0        up  1.00000 1.00000
 1    ssd  0.43750          osd.1        up  1.00000 1.00000
-5         0.87500      host new-node
 4    ssd  0.43750          osd.4        up  1.00000 1.00000
 5    ssd  0.43750          osd.5        up  1.00000 1.00000
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `ssh-copy-id: ERROR: failed to open ID file '/etc/ceph/ceph.pub': No such file or directory` | Generate the SSH key pair on the admin node with `ssh-keygen -t rsa -f /etc/ceph/ceph -N ''` before copying. |
    | `Error EINVAL: osd.X: device /dev/sdb does not exist or is not usable` | Verify the device exists on the target node with `ssh root@new-node lsblk` and ensure it is not already partitioned or in use. |
    | `Error: host 'new-node' not found in CRUSH map` | Confirm the host was successfully added with `ceph orch host ls` and check network connectivity to the new node. |
## Maintenance Mode

```bash
# Before maintenance on an OSD node:
ceph osd set noout        # prevent OSDs from being marked out during maintenance

# Perform maintenance (patch, reboot, hardware work)

# Verify OSDs come back up after reboot
ceph osd stat             # all OSDs should be up+in

# Remove noout flag
ceph osd unset noout

# Flags reference:
# noout      = don't mark OSDs out when they disconnect (maintenance safety)
# noin       = don't mark OSDs in when they reconnect
# norecover  = suspend recovery
# nobackfill = suspend backfill
# norebalance= suspend rebalancing
```


```text title="Expected output"
set noout
    osdmap e847: 24 osds: 24 up, 24 in
        flags noout
    pools:   8
    objects: 2.34M
    usage:   847 GiB / 960 GiB avail
    pgs:     672 active+clean

unset noout
    osdmap e851: 24 osds: 24 up, 24 in
        flags 
    pools:   8
    objects: 2.34M
    usage:   849 GiB / 960 GiB avail
    pgs:     672 active+clean
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error EACCES: access denied` | Ensure you have admin-level ceph credentials (typically run with `sudo` or as the `ceph` user with proper keyring permissions). |
    | `Error EINVAL: invalid command` | Verify the cluster is healthy and reachable; check that `ceph.conf` is present and `MON_HOST` is correctly configured. |
    | `Error: no monitors available` | Confirm at least one monitor is running and network connectivity exists to the monitor nodes (check firewall rules and DNS resolution). |
---

## See also

- [Ceph — Health Checks](../health-checks/)
- [Ceph — Common Issues](../../troubleshooting/common-issues/)
- [Ceph — CLI Reference](../cli-reference/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
