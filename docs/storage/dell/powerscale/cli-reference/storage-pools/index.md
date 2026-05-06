# Storage Pools & Tiers

> Part of the Dell PowerScale (Isilon) CLI Reference. SmartPools (requires license) enables tiering across node pools with different media types.

## Node Pools

```bash
# List all node pools
isi storagepool nodepools list

# Detailed view of a node pool
isi storagepool nodepools view <pool_name>

# Check node pool capacity usage
isi storagepool nodepools list | awk '{print $1, $4, $5, $6}'
```

## Tiers

```bash
# List configured tiers
isi storagepool tiers list

# View a tier (shows which node pools are members)
isi storagepool tiers view <tier_name>

# Create a tier
isi storagepool tiers create <tier_name> --children <nodepool1>,<nodepool2>

# Delete a tier
isi storagepool tiers delete <tier_name>
```

## File Pool Policies

File pool policies control which files land in which tier based on age, size, path, or access pattern:

```bash
# List all file pool policies
isi filepool policies list

# View the default policy (applied to all files not matched by a specific policy)
isi filepool default-policy view

# View a specific policy
isi filepool policies view <policy_name>

# Create a policy — move files older than 30 days to archive tier
isi filepool policies create archive-old-files \
    --file-matching-pattern 'accessed:>30:days' \
    --set-data-storage-target <archive_tier> \
    --set-data-ssd-strategy avoid

# Modify the default policy
isi filepool default-policy modify \
    --set-data-storage-target <performance_tier>

# Delete a policy
isi filepool policies delete <policy_name>
```

## SmartPools Job

SmartPools runs periodically to move files between tiers according to file pool policies:

```bash
# Check SmartPools job status
isi job jobs list | grep SmartPool
isi job status | grep SmartPool

# Start SmartPools manually (e.g., after policy change)
isi job jobs start SmartPools

# View SmartPools job results
isi job history list | grep SmartPool
```

## Spillover Configuration

When a tier is full, files spill over to another tier:

```bash
# View spillover settings
isi storagepool settings view

# Enable spillover to a specific tier
isi storagepool settings modify \
    --spillover-enabled yes \
    --spillover-target <tier_name>
```

## SSD Strategy Options

| Strategy | Behaviour |
|---|---|
| `metadata` | SSD caches metadata only (default) |
| `metadata-write` | SSD caches metadata + write cache |
| `data` | SSD caches full file data |
| `avoid` | No SSD caching — use for cold/archive data |
