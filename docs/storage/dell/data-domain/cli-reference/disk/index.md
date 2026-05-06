# Disk & Storage

> Part of the Dell Data Domain CLI Reference.

## Disk Status

```bash
# All disks with state (normal, unknown, suspect, failed)
disk show state

# Full hardware detail per disk
disk show hardware

# Disk performance statistics
disk show stats

# Disk error counts
disk show detail | grep -E "slot|error"
```

## Disk States

| State | Meaning | Action |
|---|---|---|
| `normal` | Healthy and in use | None |
| `spare` | Hot spare, available | None |
| `reconstructing` | Rebuilding RAID after failure | Monitor; do not remove disks |
| `failed` | Drive failure | Replace immediately |
| `unknown` | Newly inserted or not recognized | Check seating; may need `disk show hardware` to confirm |
| `absent` | Bay empty | Expected if slot unused |

## Enclosures and Shelves

```bash
# Enclosure hardware overview
enclosure show hardware

# All enclosures with status
enclosure show all

# Specific enclosure
enclosure show hardware enclosure <enc_id>
```

## Tier Management

Data Domain supports tiering to object storage (Cloud Tier) or tape:

```bash
# List all tiers (active, cloud)
tier list

# Detail on each tier (capacity, compression, usage)
tier show detail

# Cloud tier configuration (if licensed)
tier show detail cloud
```

## RAID Group Status

```bash
# RAID group state and disk members
raid show all
raid show detail

# RAID rebuilding progress (after disk replacement)
raid show detail | grep -E "Rebuilding|Complete"
```

## Replacing a Failed Disk

1. Identify the failed disk slot:
   ```bash
   disk show state | grep failed
   ```
2. Note the enclosure and slot number.
3. Physically replace the disk.
4. Verify the system picks up the new disk:
   ```bash
   disk show state
   ```
5. Monitor RAID rebuild:
   ```bash
   raid show detail | grep -i rebuild
   ```

## Capacity Summary

```bash
# Filesystem space usage
filesys show space

# Compressed vs logical usage
filesys show compression summary

# Tier capacity breakdown
tier show detail
```
