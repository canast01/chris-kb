# MTree Operations

MTrees are the primary logical partitions on a Data Domain system. Each MTree maps to a directory under `/data/col1/` and can have independent quotas, replication, and retention lock settings.
## Capacity and Usage

```bash
# List all MTrees with usage
mtree list --verbose

# Check MTree quota utilisation
mtree quota show

# Compare pre-compression vs post-compression per MTree
filesys show compression | grep -B2 -A5 "mtree"
```

## MTree Space Actions

```bash
# Reduce quota if an MTree is over-allocated
mtree quota set hard-limit <new_size> TiB /data/col1/<mtree_name>

# Remove quota entirely (no limit)
mtree quota reset /data/col1/<mtree_name>
```

## Replication State

```bash
# Check which MTrees are replicating and their state
replication show all | grep <mtree_name>

# Show replication lag for a specific MTree
replication show stats | grep <mtree_name>
```

## Retention Lock Review

```bash
# Check if retention lock is enabled on an MTree
mtree retention-lock status /data/col1/<mtree_name>

# List MTrees with retention lock enabled
mtree list --verbose | grep -E "mtree|retention"
```

## Creating MTrees for New Backup Applications

```bash
# Step 1 — create the MTree
mtree create /data/col1/<application>_backup

# Step 2 — set a quota (prevent runaway growth)
mtree quota set hard-limit 5 TiB /data/col1/<application>_backup
mtree quota set soft-limit 4 TiB /data/col1/<application>_backup

# Step 3 — create an NFS export or DDBoost storage unit
nfs add export /data/col1/<application>_backup clients <backup_server_ip>
# OR
ddboost storage-unit create <application>_backup

# Step 4 — verify
mtree show /data/col1/<application>_backup
mtree quota show
```

## Decommissioning an MTree

```bash
# Step 1 — confirm backup data has been expired in the backup application
# Step 2 — remove the NFS export or DDBoost storage unit
nfs del export /data/col1/<mtree_name>
# OR
ddboost storage-unit delete <storage_unit_name>

# Step 3 — delete the MTree
mtree delete /data/col1/<mtree_name>

# Step 4 — run cleaning to reclaim space
filesys clean start
filesys clean status
```

## Health Summary

| Metric | Target | Check |
|---|---|---|
| MTree quota used | < 85% | `mtree quota show` |
| Replication lag | < 4 hours | `replication show stats` |
| Retention lock as expected | Per policy | `mtree retention-lock status` |
| DDBoost storage unit exists | Configured | `ddboost storage-unit list` |
