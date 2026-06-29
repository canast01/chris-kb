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

!!! danger "bucket rm --purge-objects deletes all objects — irreversible"
    `radosgw-admin bucket rm --purge-objects` permanently deletes every object in the bucket before removing it. There is no recycle bin or soft-delete. Confirm the bucket name and ensure no application is actively writing to it. Verify an offsite backup or snapshot exists before running.

```bash
radosgw-admin bucket rm --bucket=<name> --purge-objects
```

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

---

## See also

- [Ceph — Procedures](../procedures/)
- [Ceph — Scripts](../scripts/)
- [Ceph — Health Checks](../health-checks/)

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
