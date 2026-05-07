# SnapMirror Resync

Resync re-establishes a SnapMirror relationship after it has been broken (intentionally for failover, or due to an error).

## When to Resync

- After a planned failover (`snapmirror break`) — resync to restore replication
- After data has diverged on both source and destination
- After re-establishing connectivity between clusters following an outage

## Standard Resync (Source → Destination)

```bash
# Re-establish replication from source to destination
snapmirror resync -source-path <src_svm:src_vol> \
    -destination-path <dest_svm:dest_vol>
```

Resync overwrites the destination with data from the source. Any writes to the destination since the break will be lost.

## Reverse Resync (After Failover)

When the original destination was activated (failed over to) and is now the active source:

```bash
# Step 1: Resync from destination (now active) back to the original source
snapmirror resync -source-path <dest_svm:dest_vol> \
    -destination-path <src_svm:src_vol>

# Step 2: Monitor until transfer completes
snapmirror show -destination-path <src_svm:src_vol>

# Step 3: After primary is ready to resume, break reverse relationship
snapmirror break -destination-path <src_svm:src_vol>

# Step 4: Re-establish original direction
snapmirror resync -source-path <src_svm:src_vol> \
    -destination-path <dest_svm:dest_vol>
```

## Monitor Resync Progress

```bash
snapmirror show -destination-path <dest_svm:dest_vol>
# Watch: transfer-progress field during active transfer

snapmirror show -destination-path <dest_svm:dest_vol> \
    -fields last-transfer-duration,last-transfer-size,state
```

## Resync Duration

Resync is incremental (uses common snapshot baseline) unless no common snapshot exists, in which case a full baseline transfer is required. Full baselines on large volumes can take hours to days.

## Common Issues

| Issue | Cause | Action |
|---|---|---|
| Resync fails — no common snapshot | Destination too diverged | Reinitialize instead |
| Resync overrides wanted destination writes | Failback not planned | Back up destination before resync |
| Slow resync | Large data delta or bandwidth | Schedule during low-utilization window |
| Resync completes but lag is high | Schedule not triggered | Run `snapmirror update` manually |
