# Snapshots

> Part of the [Pure FlashBlade CLI Reference](../).

FlashBlade snapshots are instant point-in-time copies of file systems or object store buckets. They are read-only and space-efficient (copy-on-write).
## List Snapshots

```bash
# List all snapshots
purefb snapshot show

# Snapshots for a specific file system
purefb snapshot show --source <filesystem_name>

# Snapshot detail — size, creation time, source
purefb snapshot show --name <snapshot_name>
```

## Create a Snapshot

```bash
# Manual snapshot of a file system
purefb snapshot create \
    --source <filesystem_name> \
    --name <snapshot_name>

# Example: pre-change snapshot
purefb snapshot create --source prod-nfs --name pre-maint-20260506
```

## Restore from Snapshot

Restore creates a new file system from a snapshot (non-destructive — original snapshot preserved):

```bash
# Restore (copy) a snapshot to a new file system
purefb snapshot copy \
    --name <snapshot_name> \
    --target <new_filesystem_name>

# The new file system is writable — export via NFS/SMB to complete recovery
```

## Destroy and Eradicate

FlashBlade uses a two-step deletion model:

```bash
# Step 1 — destroy (moves to pending eradication)
purefb snapshot destroy --name <snapshot_name>

# Step 2 — eradicate (permanently deletes — 24-hour hold by default)
purefb snapshot eradicate --name <snapshot_name>

# List pending eradication items
purefb snapshot show --pending-only
```

## Scheduled Snapshot Policies

```bash
# List snapshot policies
purefb snapshot-rule show

# Create a snapshot policy
purefb snapshot-rule create \
    --name <rule_name> \
    --keep-for <duration>   # e.g., 7d, 30d

# Attach a policy to a file system
purefb fs-snapshot-rule create \
    --filesystem <fs_name> \
    --rule <rule_name>
```

## Accessing Snapshots from NFS

FlashBlade exposes snapshots via the `.snapshot` directory on the NFS export:

```bash
# From NFS client
ls /mnt/nfs_export/.snapshot/

# Restore a file from snapshot
cp /mnt/nfs_export/.snapshot/<snapshot_name>/path/to/file /mnt/nfs_export/path/to/file
```

## Capacity Monitoring

```bash
# Snapshot space usage
purefb snapshot show | grep -i size

# Total space used by snapshots vs live data
purefb array show | grep -i snap
```
