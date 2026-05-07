# SnapMirror

> Part of the NetApp ONTAP CLI Reference.

## View Relationships

```bash
# List all relationships
snapmirror show

# Filter by destination
snapmirror show -destination-path <svm>:<vol>

# Show key health fields
snapmirror show -fields source-path,destination-path,state,lag-time,health

# Show unhealthy relationships only
snapmirror show -health false
```

## Create and Delete

```bash
# Create async DP relationship
snapmirror create \
    -source-path <src_svm>:<src_vol> \
    -destination-path <dest_svm>:<dest_vol> \
    -type DP \
    -policy MirrorAllSnapshots

# Delete relationship (destination side)
snapmirror delete -destination-path <svm>:<vol>

# Release source side (after delete)
snapmirror release -source-path <svm>:<vol> -destination-path <svm>:<vol>
```

## Operations

```bash
# Initialize (baseline transfer)
snapmirror initialize -destination-path <svm>:<vol>

# Manual update (force sync)
snapmirror update -destination-path <svm>:<vol>

# Quiesce (pause transfers)
snapmirror quiesce -destination-path <svm>:<vol>

# Break (make destination writable — for failover)
snapmirror break -destination-path <svm>:<vol>

# Resync (re-establish after break)
snapmirror resync -destination-path <svm>:<vol>

# Abort in-progress transfer
snapmirror abort -destination-path <svm>:<vol>
```

## Monitoring

```bash
# Transfer history
snapmirror history show -destination-path <svm>:<vol>

# Lag across all relationships
snapmirror lag show

# Show active transfers
snapmirror show -transfer-progress
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| Relationship unhealthy | State and error | Run `snapmirror update` |
| Lag exceeds RPO | Last transfer time | Check schedule; run manual update |
| Break fails | Relationship must be snapmirrored | Check state first |
| Initialize slow | Network bandwidth | Schedule baseline during off-peak |
