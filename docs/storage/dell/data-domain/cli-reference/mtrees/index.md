# MTrees (Data Management Units)

> Part of the Dell Data Domain CLI Reference.

MTrees are logical partitions of the Data Domain filesystem. Each MTree has its own quota, replication, and retention settings. All backup data lives under `/data/col1/`.
## List and View MTrees

```bash
# List all MTrees
mtree list

# Detail for a specific MTree
mtree show /data/col1/<mtree_name>

# All MTrees with usage stats
mtree list --verbose
```

## Create and Delete

```bash
# Create an MTree
mtree create /data/col1/<mtree_name>

# Delete an MTree (must be empty or use force)
mtree delete /data/col1/<mtree_name>
```

## Quotas

Quotas limit MTree disk usage and prevent one tenant from consuming all space:

```bash
# View current quotas
mtree quota show

# Set hard limit (backup fails when limit is reached)
mtree quota set hard-limit 10 TiB /data/col1/<mtree_name>

# Set soft limit (alert raised when exceeded)
mtree quota set soft-limit 8 TiB /data/col1/<mtree_name>

# Remove a quota
mtree quota reset /data/col1/<mtree_name>
```

## MTree Retention Lock (Compliance / Enterprise)

```bash
# Enable retention lock on an MTree
mtree retention-lock enable mode enterprise /data/col1/<mtree_name>

# Set minimum/maximum retention period
mtree retention-lock set min-retention-period 30days /data/col1/<mtree_name>
mtree retention-lock set max-retention-period 7years /data/col1/<mtree_name>

# View retention lock settings
mtree retention-lock status /data/col1/<mtree_name>
```

## MTree Replication

```bash
# Add an MTree as a replication source (see replication CLI ref for full setup)
replication add source mtree://<src_host>/data/col1/<mtree_name> destination mtree://<dst_host>/data/col1/<mtree_name>

# View replication contexts for this MTree
replication show all | grep <mtree_name>
```

## Capacity Summary

```bash
# Space used by each MTree
mtree list --verbose | grep -E "name|pre-comp|post-comp|quota"

# Compare pre-compression vs post-compression (dedup savings)
filesys show compression | grep -A5 "mtree"
```

## Common Operations Table

| Task | Command |
|---|---|
| Create MTree | `mtree create /data/col1/<name>` |
| Set hard quota | `mtree quota set hard-limit <size> TiB /data/col1/<name>` |
| View quotas | `mtree quota show` |
| Delete MTree | `mtree delete /data/col1/<name>` |
| Enable retention lock | `mtree retention-lock enable mode enterprise /data/col1/<name>` |
