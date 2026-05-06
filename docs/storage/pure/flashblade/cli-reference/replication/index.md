# Replication (ActiveDR)

> Part of the [Pure FlashBlade CLI Reference](../).

Pure FlashBlade supports asynchronous replication (snapshot-based) and ActiveDR (near-synchronous) for NFS/SMB file replication.

## Remote Array (Replication Target)

```bash
# List configured remote arrays
purefb remote-array show

# Add a replication target
purefb remote-array create \
    --name <target_name> \
    --management-address <target_management_ip>

# The target FlashBlade must also trust this array (reciprocal)
```

## File System Replica Links

Replica links replicate file systems between source and target arrays:

```bash
# List all replica links
purefb fs-replica-link show

# Detailed view — state, lag, direction
purefb fs-replica-link show --detailed

# Create a replica link
purefb fs-replica-link create \
    --local-filesystem <local_fs_name> \
    --remote-filesystem <remote_fs_name> \
    --remote-array <target_name>
```

## Replication Status

| Status | Meaning |
|---|---|
| `replicating` | Data actively syncing |
| `idle` | Up to date — no new changes |
| `paused` | Manually suspended |
| `broken` | Link failed — investigate |

## Pause and Resume

```bash
# Pause replication
purefb fs-replica-link update \
    --paused true \
    --local-filesystem <fs_name> \
    --remote-filesystem <remote_fs_name> \
    --remote-array <target_name>

# Resume replication
purefb fs-replica-link update \
    --paused false \
    --local-filesystem <fs_name> \
    --remote-filesystem <remote_fs_name> \
    --remote-array <target_name>
```

## Delete a Replica Link

```bash
purefb fs-replica-link delete \
    --local-filesystem <fs_name> \
    --remote-filesystem <remote_fs_name> \
    --remote-array <target_name>
```

## Monitoring Lag

```bash
# Replication lag (time behind)
purefb fs-replica-link show --detailed | grep -i lag
```

## Object Store Replication (Buckets)

```bash
# List object replica links
purefb os-replica-link show

# Create bucket replication
purefb os-replica-link create \
    --local-bucket <bucket_name> \
    --remote-bucket <remote_bucket_name> \
    --remote-array <target_name>
```
