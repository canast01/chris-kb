# Ceph — CLI Reference

<div class="kb-summary">
Essential Ceph CLI commands: ceph status and health, OSD management, pool operations, RBD image management, radosgw-admin for S3, and cephadm orchestration.
</div>

```text
┌──────────────────────────────── Ceph — CLI Reference ─────────────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │   ceph: admin CLI for cluster status, OSD, pool, PG, and auth management                     │    │
│   │   rbd: RBD image create/list/snap/map/resize; required for block storage operations           │   │
│   │   radosgw-admin: S3 user, bucket, quota, and zone management for RGW                          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Cluster Status

```bash
# Overall cluster status
ceph status         # summary
ceph health detail  # full health messages with codes

# Daemon status
ceph orch ps        # all daemon instances (cephadm-managed)
ceph mon stat       # MON quorum + leader
ceph mgr stat       # active MGR
ceph osd stat       # OSD up/in counts

# I/O and performance
ceph osd perf               # per-OSD commit/apply latency
ceph osd df                 # per-OSD capacity and utilization
ceph df                     # pool-level capacity summary
```

## OSD Management

```bash
# List OSDs
ceph osd tree           # topology with status (up/down, in/out)
ceph osd ls             # plain list of OSD IDs
ceph osd dump | grep osd  # full OSD map

# OSD out/in (move data away before maintenance)
ceph osd out osd.5      # stop assigning new PGs; triggers rebalance
ceph osd in osd.5       # restore OSD to cluster

# OSD down/rm (for permanent removal)
ceph osd down osd.5
ceph osd purge osd.5 --yes-i-really-mean-it

# Reweight OSD (adjust data placement weight)
ceph osd reweight osd.5 0.9  # 0.0-1.0; default 1.0

# Check OSD config at runtime
ceph config show osd.0
ceph tell osd.0 config show
```

## Pool Management

```bash
# List pools
ceph osd pool ls detail

# Pool settings
ceph osd pool get rbd all   # show all parameters
ceph osd pool set rbd size 3
ceph osd pool set rbd min_size 2
ceph osd pool set rbd pg_num 128    # adjust PG count (only increase; plan ahead)

# Rename pool
ceph osd pool rename old-pool new-pool

# Delete pool (requires confirmation twice)
ceph osd pool delete rbd rbd --yes-i-really-really-mean-it

# Quotas
ceph osd pool set-quota rbd max_objects 10000
ceph osd pool set-quota rbd max_bytes 10737418240   # 10 GB
```

## RBD (Block Storage)

```bash
# Create image
rbd create rbd/my-volume --size 100G

# List images
rbd ls rbd
rbd info rbd/my-volume

# Snapshot
rbd snap create rbd/my-volume@snap1
rbd snap ls rbd/my-volume
rbd snap rollback rbd/my-volume@snap1
rbd snap rm rbd/my-volume@snap1

# Clone from snapshot (thin provision)
rbd snap protect rbd/my-volume@snap1
rbd clone rbd/my-volume@snap1 rbd/my-clone

# Resize
rbd resize rbd/my-volume --size 200G

# Map on Linux (present as block device)
rbd map rbd/my-volume       # returns /dev/rbdX
rbd unmap /dev/rbd0
rbd showmapped
```

## radosgw-admin (Object Storage)

```bash
# User management
radosgw-admin user create --uid=testuser --display-name="Test User"
radosgw-admin user info --uid=testuser
radosgw-admin key create --uid=testuser --key-type=s3  # add access key

# Bucket management
radosgw-admin bucket list
radosgw-admin bucket stats --bucket=my-bucket
radosgw-admin bucket rm --bucket=my-bucket --purge-objects

# Quota management
radosgw-admin quota set --quota-scope=user --uid=testuser \
  --max-objects=100000 --max-size=10G
radosgw-admin quota enable --quota-scope=user --uid=testuser

# Usage stats
radosgw-admin usage show --uid=testuser --start-date=2026-01-01
```

## cephadm Orchestration

```bash
# Service management
ceph orch ls                  # list all services
ceph orch ps                  # list all daemon instances
ceph orch apply osd --all-available-devices
ceph orch daemon restart osd.5

# Host management
ceph orch host ls
ceph orch host add new-node 10.0.1.20
ceph orch host rm old-node

# Upgrade (see also Lifecycle page)
ceph orch upgrade status
ceph orch upgrade start --image quay.io/ceph/ceph:v18.2.0
```
