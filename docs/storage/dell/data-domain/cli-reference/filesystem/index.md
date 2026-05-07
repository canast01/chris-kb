# Filesystem

> Part of the Dell Data Domain CLI Reference.

The Data Domain filesystem (DDFS) manages all deduplication and compression. All user data lives in the active tier under `/data/col1/`.
## Filesystem Status

```bash
# Filesystem state (enabled/disabled)
filesys status

# Full status overview
filesys show

# Compression and deduplication statistics
filesys show compression

# Space usage breakdown (pre-comp, post-comp, physical)
filesys show space
```

## Enable and Disable

```bash
# Enable the filesystem (required before accepting backup data)
filesys enable

# Disable the filesystem (maintenance only — stops all I/O)
filesys disable
```

## Cleaning (Garbage Collection)

Cleaning reclaims space from deleted or expired files. It runs automatically but can be triggered manually:

```bash
# Start a cleaning cycle
filesys clean start

# Show cleaning status
filesys clean status

# Stop an in-progress clean
filesys clean stop
```

Cleaning is I/O intensive. Schedule during off-peak hours if running manually.

## Capacity and Compression Analysis

```bash
# Overall capacity summary
filesys show space

# Compression ratio and savings
filesys show compression summary

# Per-MTree compression
filesys show compression | grep -A5 "mtree"

# Logical vs physical usage
filesys show space | grep -E "Used|Available|Total"
```

## Compression Ratio Fields

| Field | Meaning |
|---|---|
| Pre-comp | Total logical data written (before dedup/compression) |
| Post-comp | Physical space used on disk |
| Global comp factor | Overall compression ratio |
| Local comp factor | Per-stream compression ratio |
| Dedup savings | Percentage saved by deduplication |

## Space Recovery Actions

```bash
# Expire old backup data (via backup application policy — not DD CLI)
# Data Domain only deletes data when the backup app marks it expired

# After deletions, run cleaning to reclaim space
filesys clean start

# Monitor reclaim progress
filesys clean status
filesys show space   # compare before/after
```

## Filesystem Checks

```bash
# Check filesystem integrity
filesys check

# View filesystem event log
filesys show log
```
