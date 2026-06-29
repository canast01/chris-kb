---
tags:
  - ceph
  - operations
---
# Ceph — CLI Reference

<div class="kb-summary">
Essential Ceph CLI commands: ceph status and health, OSD management, pool operations, PG management, RADOS object-level ops, RBD image management, radosgw-admin for S3, and cephadm orchestration.

*Applies to: Ceph Reef / Squid*
</div>

```d2
direction: right

CLI: "CLI" {shape: rectangle}
CEPH: "ceph · cluster management" {shape: rectangle}
RADOS: "rados · object ops" {shape: rectangle}
RBD: "rbd · block storage" {shape: rectangle}
RGW: "radosgw-admin · object gateway" {shape: rectangle}
CV: "ceph-volume · OSD provisioning" {shape: rectangle}
CADM: "cephadm · orchestration" {shape: rectangle}
C1: "status / health / log" {shape: rectangle}
C2: "osd / pool / pg mgmt" {shape: rectangle}
C3: "auth / config / crash" {shape: rectangle}
R1: "ls / stat / get / put" {shape: rectangle}
R2: "bench write/seq/rand" {shape: rectangle}
B1: "create / resize / rm" {shape: rectangle}
B2: "snap / clone / export" {shape: rectangle}
G1: "user / key management" {shape: rectangle}
G2: "bucket / quota / sync" {shape: rectangle}
V1: "lvm prepare/activate" {shape: rectangle}
V2: "zap / list" {shape: rectangle}
A1: "host add / rm / drain" {shape: rectangle}
A2: "daemon add / rm / restart" {shape: rectangle}

CLI -> CEPH
CLI -> RADOS
CLI -> RBD
CLI -> RGW
CLI -> CV
CLI -> CADM
CEPH -> C1
CEPH -> C2
CEPH -> C3
RADOS -> R1
RADOS -> R2
RBD -> B1
RBD -> B2
RGW -> G1
RGW -> G2
CV -> V1
CV -> V2
CADM -> A1
CADM -> A2
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Cluster Management

```bash
ceph -s                                              # status summary: health, OSDs, PGs, I/O
ceph -w                                              # live event stream (watch cluster log)
ceph health detail                                   # verbose health messages with error codes
ceph log last 50                                     # 50 most recent cluster log events
ceph config dump                                     # all non-default config values across cluster
ceph config get osd.0 osd_max_backfills              # read single config key for specific daemon
ceph config set global osd_recovery_op_priority 3   # runtime config change (no restart needed)

# Daemon status
ceph orch ps                                         # all daemon instances (cephadm-managed)
ceph mon stat                                        # MON quorum + leader
ceph mgr stat                                        # active MGR
ceph osd stat                                        # OSD up/in counts

# I/O and performance
ceph osd perf                                        # per-OSD commit/apply latency
ceph osd df                                          # per-OSD capacity and utilization
ceph df                                              # pool-level capacity summary
```


```text title="Expected output"
$ ceph -s
  cluster:
    id:     a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d
    health: HEALTH_OK
  services:
    mon: 3 daemons, quorum mon01,mon02,mon03 (age 2d)
    mgr: mgr01(active, since 8h), mgr02(standby)
    osd: 12 osds: 12 up, 12 in (since 3d)
  data:
    pools:   8 pools, 256 pgs
    objects: 1.24M objects, 847 GiB
    usage:   2.1 TiB used, 8.9 TiB / 11 TiB avail
    pgs:     256 active+clean

$ ceph health detail
HEALTH_OK

$ ceph log last 50
2024-01-15T14:32:18.456+0000 mon.mon01 (mon.0) 8192 : cluster [INF] Cluster is now healthy
2024-01-15T14:28:03.221+0000 osd.5 (osd.5) 4096 : cluster [WRN] slow request 30.456s
2024-01-15T14:15:47.889+0000 mgr.mgr01 (mgr.0) 2048 : cluster [INF] Scrub starts for pg 2.1a
...

$ ceph config dump
WHO     MASK LEVEL OPTION                          VALUE
global  -    file  mon_allow_pool_delete            true
global  -    file  osd_recovery_op_priority         3
osd     -    file  osd_max_backfills                4

$ ceph config get osd.0 osd_max_backfills
4

$ ceph config set global osd_recovery_op_priority 3
(no output — command completes silently)

$ ceph orch ps
NAME                                 HOST      STATUS        REFRESHED  AGE  VERSION  IMAGE ID      CONTAINER ID
alertmanager.host01                  host01    running (2h)  2m ago     3d   0.24.0   a1b2c3d4e5f6  abc123def456
ceph-exporter.host02                 host02    running (2h)  2m ago     3d   17.2.5   f6e5d4c3b2a1  xyz789uvw012
mon.mon01                            host01    running (2h)  2m ago     3d   17.2.5   f6e5d4c3b2a1  abc123def456
mgr.mgr01                            host01    running (2h)  2m ago     3d   17.2.5   f6e5d4c3b2a1  abc123def457
osd.0                                host02    running (2h)  2m ago     3d   17.2.5   f6e5d4c3b2a1  abc123def458
...

$ ceph mon stat
e4: 3 mons at {mon01=10.0.
```
## OSD Management

```bash
ceph osd ls                                          # list all OSD IDs
ceph osd tree                                        # topology with weights and up/in state
ceph osd stat                                        # up/in/down counts
ceph osd find <id>                                   # which host an OSD lives on
ceph osd dump | grep osd                             # full OSD map entries

ceph osd set noout                                   # prevent OSDs going out during maintenance
ceph osd unset noout
ceph osd reweight <id> <weight>                      # adjust OSD weight (0.0–1.0); default 1.0
ceph osd crush reweight-all                          # reweight all OSDs to match current capacity
ceph osd out <id>                                    # mark OSD out — starts data migration away
ceph osd in <id>                                     # mark OSD in — triggers rebalance back onto OSD
ceph osd down <id>                                   # mark OSD down (stops it if running)
ceph osd purge <id> --yes-i-really-mean-it           # fully remove OSD: crush entry, auth key, map

# Config at runtime
ceph config show osd.0
ceph tell osd.0 config show
```


```text title="Expected output"
0
1
2
3
4

ID WEIGHT  TYPE NAME             UP/DOWN REWEIGHT PRI-AFF 
-1       root default           
-2   3.00     host ceph-node-01  
 0   1.00         osd.0              up  1.00000 1.00000 
 1   1.00         osd.1              up  1.00000 1.00000 
 2   1.00         osd.2              up  1.00000 1.00000 
-3   3.00     host ceph-node-02  
 3   1.00         osd.3              up  1.00000 1.00000 
 4   1.00         osd.4              up  1.00000 1.00000 

    5 osds: 5 up, 5 in

{
  "osd": 2,
  "host": "ceph-node-01",
  "rack": "rack-a",
  "datacenter": "us-west-2a",
  "root": "default"
}

osd.0 up   in weight 1.0 at [192.168.1.10]:6800/2567
osd.1 up   in weight 1.0 at [192.168.1.11]:6800/2568
osd.2 up   in weight 1.0 at [192.168.1.12]:6800/2569

noout flag(s) set
noout flag(s) unset
reweighted osd.1 to 0.5
reweighted all osds
marked down osd.3
marked in osd.3
marked down osd.2
purged osd.4

[osd.0]
  admin_socket = /var/run/ceph/ceph-osd.0.asok
  osd_memory_target = 4294967296
  osd_max_backfills = 1

{
  "admin_socket": "/var/run/ceph/ceph-osd.0.asok",
  "osd_memory_target": 4294967296,
  "osd_max_backfills": 1
}
```

!!! warning "Common errors"
    **`Error ENOENT: osd.99 does not exist`** — Verify the OSD ID exists with `ceph osd ls` before running commands against it.
    **`Error EINVAL: invalid weight`** — Ensure reweight values are between 0.0 and 1.0, or use `ceph osd crush reweight-all` to auto-reweight based on capacity.
    **`Error EPERM: insufficient permissions`** — Run ceph commands with appropriate privileges (typically as root or with sudo) or ensure your user is in the ceph group.
## Pool Management

```bash
ceph osd pool ls detail                              # list pools with PG count, size, and flags
ceph osd pool get <pool> all                         # all pool parameters
ceph osd pool set <pool> size 3                      # replica count
ceph osd pool set <pool> min_size 2                  # minimum replicas for I/O
ceph osd pool set <pool> pg_autoscale_mode on        # enable automatic PG scaling
ceph osd pool rename <old> <new>
ceph osd pool delete <pool> <pool> --yes-i-really-really-mean-it

# PG count (manual — only increase; plan ahead)
ceph osd pool set rbd pg_num 256
ceph osd pool set rbd pgp_num 256

# Quotas
ceph osd pool set-quota rbd max_objects 10000
ceph osd pool set-quota rbd max_bytes 10737418240    # 10 GiB
```


```text title="Expected output"
NAME                     ID     PIGP      PGS STATE    TYPE REP CLASS RBYTES RBYTES RBYTES MINSIZE DCACHE AUID COMPRESSION
rbd                      0      32        128 active+clean replicated   3   0        0        0       2       -1 none
metadata                 1      32        32  active+clean replicated   3   0        0        0       2       -1 none
cephfs_data              2      32        64  active+clean replicated   3   0        0        0       2       -1 none
cephfs_metadata          3      32        32  active+clean replicated   3   0        0        0       2       -1 none

size 3
min_size 2
pg_autoscale_mode on
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error ENOENT: pool 'rbd' does not exist`** — Verify the pool name with `ceph osd pool ls` before running pool commands.
    **`Error EINVAL: pg_num 256 <= current pg_num 256`** — Only increase pg_num to a higher value; decreasing PGs is not allowed.
    **`Error EPERM: pool deletion not confirmed; use --yes-i-really-really-mean-it flag`** — Include both pool name arguments and the confirmation flag exactly as shown in the command.
## PG Management

```bash
ceph pg stat                                         # PG count and state summary
ceph pg dump_stuck                                   # list stuck/unclean PGs
ceph pg <pgid> query                                 # detailed PG state, acting set, history
ceph pg repair <pgid>                                # trigger repair on inconsistent PG
ceph pg scrub <pgid>                                 # scrub specific PG on demand

ceph osd pool set <pool> noscrub true                # disable scrub for pool (maintenance)
ceph osd pool set <pool> nodeep-scrub true           # disable deep-scrub for pool

# Cluster-wide scrub control
ceph osd set noscrub
ceph osd unset noscrub
ceph osd set nodeep-scrub
ceph osd unset nodeep-scrub

# Autoscale status
ceph osd pool autoscale-status
```


```text title="Expected output"
PG_STAT OBJECTS MISSING_ON_PRIMARY DEGRADED MISPLACED UNFOUND BYTES LOG STATE_PERF_MOD
       1234567          0           0        0        0       0 8.2G      ok
pgs: 256 active+clean; 0 B data, 12 GiB used, 488 GiB / 500 GiB avail

stuck pg query (empty)

{
  "state": "active+clean",
  "snap_trimq": "[]",
  "acting": [0, 2, 1],
  "acting_primary": 0,
  "up": [0, 2, 1],
  "up_primary": 0,
  "epoch": 1847,
  "last_epoch_clean": 1847,
  "last_deep_scrub_stamp": "2024-01-15T09:22:14.123456+0000"
}

set pool 'rbd' property noscrub to true
set pool 'rbd' property nodeep-scrub to true
noscrub set
noscrub unset
nodeep-scrub set
nodeep-scrub unset

POOL                 SIZE  TARGET_SIZE  RATE  RAW_USED  RAW_USED_PCT  EFFECTIVE_BYTES_USED  AUTOSCALE  BULK
rbd                    32           32  1.0   2.1 GiB         0.42           2.1 GiB  on         False
cephfs_data            64           64  1.0   4.8 GiB         0.76           4.8 GiB  on         False
cephfs_metadata         8            8  1.0   512 MiB         0.80           512 MiB  on         False
```

!!! warning "Common errors"
    **`Error ENOENT: pg 1.2a3 does not exist`** — Verify the PG ID format is correct (use `ceph pg ls` to list valid PGs) and the PG exists in the cluster.
    **`Error EPERM: pool 'mypool' does not exist`** — Confirm the pool name is spelled correctly with `ceph osd pool ls`.
    **`Error EBUSY: scrub already in progress on pg 2.1f`** — Wait for the current scrub to complete before triggering another one, or check `ceph pg stat` for PG state.
## rados (Object-Level)

```bash
rados ls -p <pool>                                   # list all objects in a pool
rados stat -p <pool> <object>                        # object metadata: size and mtime
rados get -p <pool> <object> /tmp/out                # download object to file
rados put -p <pool> <object> /tmp/in                 # upload file as object

# Benchmarking
rados bench -p <pool> 30 write --no-cleanup          # write benchmark for 30 seconds
rados bench -p <pool> 30 seq                         # sequential read benchmark
rados bench -p <pool> 30 rand                        # random read benchmark
rados cleanup -p <pool>                              # remove bench objects after testing
```


```text title="Expected output"
$ rados ls -p rbd
rbd_data.1a2b3c4d5e6f7g8h.0000000000000001
rbd_data.1a2b3c4d5e6f7g8h.0000000000000002
rbd_data.1a2b3c4d5e6f7g8h.0000000000000003
vm-disk-backup.snap
metadata.json
...

$ rados stat -p rbd rbd_data.1a2b3c4d5e6f7g8h.0000000000000001
size 4194304
mtime 2024-01-15T09:42:17.123456+0000

$ rados get -p rbd metadata.json /tmp/out
$ rados put -p rbd metadata.json /tmp/in
(no output — command completes silently)

$ rados bench -p rbd 30 write --no-cleanup
  sec Cur ops   started  finished  avg MB/s  cur MB/s last lat(ms) avg lat(ms)
    0       0         0         0         0         0           -           0
   10      16       512       496    16.53    16.53      124.5      128.3
   20      12       768       756    12.67    12.67      156.2      142.1
   30       0      1024      1024    11.42    11.42      148.9      139.7
Total time run:       30.245
Total writes made:    1024
Write size:           4194304
Bandwidth (MB/sec):   135.42

$ rados cleanup -p rbd
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: pool <pool> does not exist`** — Verify the pool name with `ceph osd pool ls` and ensure the pool has been created.
    **`Error: object not found`** — Confirm the object exists in the pool using `rados ls -p <pool>` before attempting stat or get operations.
    **`Error: permission denied`** — Ensure your user has read/write permissions to the pool by checking `ceph auth list` and applying appropriate capabilities.
## RBD (Block Storage)

```bash
rbd ls -p <pool>                                     # list RBD images in pool
rbd info <pool>/<image>                              # image metadata: features, size, format
rbd create <pool>/<image> --size 100G
rbd resize <pool>/<image> --size 200G

# Snapshots
rbd snap create <pool>/<image>@<snapname>
rbd snap ls <pool>/<image>
rbd snap rollback <pool>/<image>@<snapname>          # in-place revert
rbd snap rm <pool>/<image>@<snapname>

# Clone (thin provision from snapshot)
rbd snap protect <pool>/<image>@<snapname>
rbd clone <pool>/<image>@<snapname> <pool>/<clone>

# Export / import
rbd export <pool>/<image> /tmp/export.img
rbd export-diff --from-snap <prev> <pool>/<image>@<snap> /tmp/diff.img
rbd import /tmp/export.img <pool>/<image>
rbd import-diff /tmp/diff.img <pool>/<image>

rbd rm <pool>/<image>

# Map on Linux
rbd map <pool>/<image>                               # returns /dev/rbdX
rbd unmap /dev/rbd0
rbd showmapped
```


```text title="Expected output"
$ rbd ls -p volumes
volume-001
volume-002
vm-backup-prod
test-image

$ rbd info volumes/volume-001
rbd image 'volume-001':
	size 100 GiB
	objects 25600
	order 22 (4 MiB objects)
	snapshot_count 2
	id: 1a2b3c4d5e6f7g8h
	block_name_prefix: rbd_data.1a2b3c4d5e6f7g8h
	format: 2
	features: layering, striping, exclusive-lock, object-map, fast-diff, deep-flatten
	op_features: 
	flags: 
	create_timestamp: Thu Jan 12 14:23:45 2024
	access_timestamp: Thu Jan 12 16:45:12 2024
	modify_timestamp: Thu Jan 12 16:45:12 2024

$ rbd snap ls volumes/volume-001
SNAPID NAME                 SIZE TIMESTAMP
     4 daily-2024-01-12  100 GiB Thu Jan 12 14:30:00 2024
     5 daily-2024-01-11  100 GiB Wed Jan 11 14:30:00 2024

$ rbd map volumes/volume-001
/dev/rbd0

$ rbd showmapped
id pool      image        snap dev    
0  volumes   volume-001   -    /dev/rbd0
```

!!! warning "Common errors"
    **`rbd: error opening image volume-001: (2) No such file or directory`** — Verify the pool name and image name are correct with `rbd ls -p <pool>`.
    **`rbd: snap 'daily-backup' is not protected`** — Protect the snapshot before cloning with `rbd snap protect <pool>/<image>@<snapname>`.
    **`rbd: error: image still has 2 snapshots`** — Delete all snapshots before removing the image using `rbd snap rm <pool>/<image>@<snapname>` for each snapshot.
## radosgw-admin (Object Gateway)

```bash
radosgw-admin user list
radosgw-admin user info --uid=<user>
radosgw-admin user create --uid=<user> --display-name="<name>"
radosgw-admin key create --uid=<user> --key-type=s3   # generate S3 access/secret key pair

radosgw-admin bucket list --uid=<user>
radosgw-admin bucket stats --bucket=<name>
radosgw-admin quota set --uid=<user> --quota-type=user --max-size=50G
radosgw-admin quota enable --uid=<user> --quota-type=user
radosgw-admin usage show --uid=<user> --start-date=2026-01-01
```


```text title="Expected output"
[
  "testuser",
  "admin",
  "s3-app-user"
]
{
  "user_id": "testuser",
  "display_name": "Test User",
  "email": "",
  "suspended": 0,
  "max_buckets": 1000,
  "auid": 0,
  "subusers": [],
  "keys": [
    {
      "user": "testuser",
      "access_key": "AKIAIOSFODNN7EXAMPLE",
      "secret_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    }
  ],
  "swift_keys": [],
  "caps": [],
  "op_mask": "read, write, delete",
  "default_placement": "",
  "default_storage_class": "",
  "placement_tags": [],
  "bucket_quota": {
    "enabled": false,
    "check_on_raw": false,
    "max_size": -1,
    "max_size_kb": 0,
    "max_objects": -1
  },
  "user_quota": {
    "enabled": false,
    "check_on_raw": false,
    "max_size": 53687091200,
    "max_size_kb": 52428800,
    "max_objects": -1
  },
  "temp_url_keys": [],
  "type": "rgw"
}
{
  "user_id": "newapp",
  "display_name": "New Application",
  "email": "",
  "suspended": 0,
  "max_buckets": 1000,
  "auid": 0,
  "subusers": [],
  "keys": [
    {
      "user": "newapp",
      "access_key": "AKIAJ5XAMPLE2ABCDEF",
      "secret_key": "bKzlrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    }
  ],
  "swift_keys": [],
  "caps": [],
  "op_mask": "read, write, delete",
  "default_placement": "",
  "default_storage_class": "",
  "placement_tags": [],
  "bucket_quota": {
    "enabled": false,
    "check_on_raw": false,
    "max_size": -1,
    "max_size_kb": 0,
    "max_objects": -1
  },
  "user_quota": {
    "enabled": false,
    "check_on_raw": false,
    "max_size": -1,
    "max_size_kb": 0,
    "max_objects": -1
  },
  "temp_url_keys": [],
  "type": "rgw"
}
{
  "user": "newapp",
  "access_key": "AKIA7XAMPLE3GHIJKL",
  "secret_key": "cKzlrXUtnFEMI/K7MDENG/bPxRfi
```
!!! danger "bucket rm --purge-objects deletes all objects — irreversible"
    `radosgw-admin bucket rm --purge-objects` permanently deletes every object in the bucket before removing it. There is no recycle bin or soft-delete. Confirm the bucket name and ensure no application is actively writing to it. Verify an offsite backup or snapshot exists before running.

```bash
radosgw-admin bucket rm --bucket=<name> --purge-objects
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`error: bucket '<name>' does not exist`** — Verify the bucket name is correct and exists by running `radosgw-admin bucket list`.
    **`error: unable to remove bucket, it is not empty`** — Remove the `--purge-objects` flag if you want to keep objects, or ensure the bucket truly has no versioned/deleted object markers with `radosgw-admin bucket check --bucket=<name>`.
## cephadm Orchestration

```bash
# Service management
ceph orch ls                                         # list all services
ceph orch ps                                         # list all daemon instances
ceph orch apply osd --all-available-devices          # deploy OSDs on all available disks
ceph orch daemon restart osd.5
ceph orch daemon stop osd.5
ceph orch daemon add osd <hostname>:/dev/sdX         # add single OSD on specific device

# Host management
ceph orch host ls
ceph orch host add new-node 10.0.1.20
ceph orch host drain <hostname>                      # gracefully remove all daemons from host
ceph orch host rm <hostname>

# Upgrade
ceph orch upgrade status
ceph orch upgrade start --image quay.io/ceph/ceph:v18.2.0

# Crash reports
ceph crash ls                                        # list recorded daemon crashes
ceph crash info <crash-id>                           # full backtrace and context
ceph crash archive <crash-id>                        # mark crash as acknowledged
ceph crash archive-all                               # clear all crash alerts
```


```text title="Expected output"
NAME                 PORTS   RUNNING  REFRESHED  AGE  VERSION  IMAGE NAME                                IMAGE ID      
osd                  -       12/12    2m ago     8d   18.2.0   quay.io/ceph/ceph:v18.2.0               a1b2c3d4e5f6  
mon                  -       3/3      2m ago     8d   18.2.0   quay.io/ceph/ceph:v18.2.0               a1b2c3d4e5f6  
mgr                  -       2/2      2m ago     8d   18.2.0   quay.io/ceph/ceph:v18.2.0               a1b2c3d4e5f6  

NAME                 HOST           DAEMON         ID    VERSION  STATUS      REFRESHED  AGE  MEM USE  MEM LIM  PORTS  
osd.0                ceph-node-01   osd            0     18.2.0   running     2m ago     8d   512M     4G      6800-6820  
osd.1                ceph-node-02   osd            1     18.2.0   running     2m ago     8d   498M     4G      6800-6820  
osd.2                ceph-node-03   osd            2     18.2.0   running     2m ago     8d   521M     4G      6800-6820  
...

HOSTNAME      STATUS  LABELS  CEPH_VERSION  
ceph-node-01  online  -       18.2.0        
ceph-node-02  online  -       18.2.0        
ceph-node-03  online  -       18.2.0        
new-node      online  -       18.2.0        

Scheduled upgrade to quay.io/ceph/ceph:v18.2.0
Progress: 8/12 daemons upgraded
Remaining: mon.a, osd.4, osd.5, osd.11

ID                                    TIMESTAMP           ENTITY      MESSAGE  
20240115_143022_a1b2c3d4-e5f6-7890   2024-01-15 14:30:22  osd.3       Segmentation fault in BlueStore::_do_write_small  
20240114_091547_b2c3d4e5-f6a7-8901   2024-01-14 09:15:47  mon.b       Assertion `!m_lock.is_locked()' failed
```

!!! warning "Common errors"
    **`Error ENOENT: unrecognized service 'osd'`** — Verify the service name matches exactly (e.g., `osd.0` for a specific daemon) or use `ceph orch ls` to list available services.
    **`Error EINVAL: host 'new-node' is not in the cluster`** — Ensure the hostname is resolvable and the host has been bootstrapped with `ceph orch host add` before deploying daemons to it.
    **`Error EBUSY: host 'ceph-node-02' still has running daemons`** — Run `ceph orch host drain <hostname>` before removing the host to gracefully
## Auth Management

```bash
ceph auth ls                                         # list all CephX users and capabilities
ceph auth get client.admin                           # show key and caps for a user
ceph auth get-or-create client.rbd mon 'allow r' osd 'allow rwx pool=rbd'
ceph auth caps client.rbd mon 'allow r' osd 'allow rw pool=rbd'   # update caps
ceph auth del client.rbd                             # remove user
ceph auth export client.admin > /backup/admin.keyring
ceph auth import -i /backup/admin.keyring
```


```text title="Expected output"
installed auth entries:

client.admin
	key: AQC7VPdnK8J3ExAA1b2Z9mK4vL5pQ6rS7tU8Vw==
	caps mon: "allow *"
	caps osd: "allow *"
	caps mds: "allow *"

client.rbd
	key: AQDmWQdoL9K2FxBB2c3a0nL5wM6qR7sT8uV9Wx==
	caps mon: "allow r"
	caps osd: "allow rwx pool=rbd"

[client.admin]
	key = AQC7VPdnK8J3ExAA1b2Z9mK4vL5pQ6rS7tU8Vw==
	caps mon = "allow *"
	caps osd = "allow *"
	caps mds = "allow *"

imported keyring
```

!!! warning "Common errors"
    **`Error EACCES: permission denied`** — Ensure you have admin privileges (run with `sudo` or as the ceph user) and the Ceph cluster is accessible.
    **`Error EINVAL: invalid value`** — Verify the pool name exists and the capability syntax is correct (e.g., `'allow rwx pool=poolname'` with proper quoting).
    **`Error ENOENT: No such file or directory`** — Check that the keyring file path is correct and readable before importing with `ceph auth import`.
---

## See also

- [Ceph — Procedures](../procedures/)
- [Ceph — Scripts](../scripts/)
- [Ceph — Health Checks](../health-checks/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
