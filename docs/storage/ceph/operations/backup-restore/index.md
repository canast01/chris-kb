# Ceph — Backup & Restore

<div class="kb-summary">
Ceph backup: RBD snapshot export for VM disks, RBD mirroring for DR, cluster configuration backup, and crash dump collection. Note: Ceph itself is a redundant store — backup focus is on configuration and RBD images.
</div>

## RBD Snapshot and Export

```bash
# Create snapshot before changes
rbd snap create rbd/my-volume@backup-$(date +%F)
rbd snap ls rbd/my-volume

# Export snapshot to file (for off-cluster backup)
rbd export rbd/my-volume@backup-2026-06-07 /backup/my-volume-2026-06-07.img

# Export incremental (since last snapshot) — more efficient
rbd export-diff rbd/my-volume@snap-old rbd/my-volume@snap-new \
  /backup/my-volume-incremental.img

# Import and restore
rbd import /backup/my-volume-2026-06-07.img rbd/my-volume-restored

# Import incremental diff
rbd import-diff /backup/my-volume-incremental.img rbd/my-volume
```

## RBD Mirroring (DR / Async Replication)

```bash
# RBD mirroring replicates RBD images between two Ceph clusters asynchronously.
# Use case: DR site; RPO = configurable (journal-based or snapshot-based)

# Enable mirroring on pool
rbd mirror pool enable rbd image    # image mode (per-image enable)
# or:
rbd mirror pool enable rbd pool     # pool mode (all images mirrored)

# Enable mirroring on specific image
rbd mirror image enable rbd/my-volume journaling   # requires journaling feature

# On secondary cluster: create peer
rbd mirror pool peer bootstrap import rbd bootstrap-token

# Check mirror status
rbd mirror pool status rbd          # pool-level status
rbd mirror image status rbd/my-volume  # per-image sync status

# Failover: promote secondary image
rbd mirror image promote rbd/my-volume  # on DR site
rbd mirror image demote rbd/my-volume   # on primary (if accessible)
```

## Cluster Configuration Backup

```bash
# Back up all configuration keys
ceph config-key dump > /backup/ceph-configkeys-$(date +%F).json

# Back up auth keys (all users and capabilities)
ceph auth list > /backup/ceph-auth-$(date +%F).txt
ceph auth export > /backup/ceph-auth-$(date +%F).keyring

# Back up CRUSH map
ceph osd getcrushmap -o /backup/crush-$(date +%F).bin
crushtool -d /backup/crush-$(date +%F).bin -o /backup/crush-$(date +%F).txt

# Back up ceph.conf (on admin node)
cp /etc/ceph/ceph.conf /backup/ceph.conf.$(date +%F)

# OSD map
ceph osd dump > /backup/osd-dump-$(date +%F).txt
```

## Restore from Backup

```bash
# Restore CRUSH map
ceph osd setcrushmap -i /backup/crush-2026-06-07.bin

# Restore auth key for a specific user
ceph auth import -i /backup/ceph-auth-2026-06-07.keyring

# Restore RBD image from exported file
rbd import /backup/my-volume-2026-06-07.img rbd/my-volume-restored

# For full cluster recovery from scratch:
# 1. Deploy new cluster with cephadm bootstrap (same cluster FSID required)
# 2. Import auth keys
# 3. Re-add OSDs (existing data may be recoverable if disks intact)
# 4. Restore CRUSH map
# 5. Run: ceph osd repair; ceph pg repair
```
