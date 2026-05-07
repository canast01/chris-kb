# Storage — Aggregates & Disks

> Part of the [NetApp ONTAP CLI Reference](../).
## Aggregates

An aggregate is the physical RAID group that holds one or more volumes.

```bash
# List all aggregates
storage aggregate show

# Only online aggregates
storage aggregate show -state online

# Aggregate detail — size, used, available, RAID type
storage aggregate show -fields aggr-name, node, size, availsize, usedsize, state

# Space breakdown including snapshot reserve
storage aggregate show-space

# Specific aggregate space
storage aggregate show-space -aggregate <aggr>
```

### Aggregate Capacity Thresholds

| Free Space | Action |
|---|---|
| > 20% | Healthy |
| 10–20% | Alert — add capacity or move volumes |
| < 10% | Emergency — volumes may go offline |

```bash
# Find aggregates below 20% free
storage aggregate show -fields aggr-name, node, availsize, usedpercent | \
    awk '$NF > 80 {print}'
```

### Aggregate Operations

```bash
# Rename an aggregate
storage aggregate rename -aggregate <old_name> -newname <new_name>

# Set maximum RAID group size
storage aggregate modify -aggregate <aggr> -maxraidsize 24

# Add disks to an aggregate
storage aggregate add-disks -aggregate <aggr> -diskcount <n>
```

## Disks

```bash
# All disk inventory
storage disk show

# Broken disks (failed or suspect)
storage disk show -broken

# Disk details — location, owner, type, size, bay
storage disk show -fields disk, bay, node, container-type, disk-type, rpm, size, position

# Spare disks available
storage disk show -container-type spare
```

### Disk States

| State | Meaning | Action |
|---|---|---|
| `raid_dp` | In a RAID-DP group | Normal |
| `spare` | Available for use | Normal |
| `broken` | Failed | Replace |
| `partner` | Owned by HA partner | Normal |
| `unknown` | Not recognized | Check cabling |

### Disk Operations

```bash
# Unfail a disk (re-add to aggregate after investigation)
storage disk unfail -disk <disk_name>

# Assign disk ownership
storage disk assign -disk <disk_name> -owner <node_name>

# Manually mark a disk as spare
storage disk assign -disk <disk_name> -owner <node_name> -container-type spare
```

## RAID Groups

```bash
# RAID group status per aggregate
storage aggregate show-raidtree -aggregate <aggr>

# RAID type (RAID-DP, RAID-TEC)
storage aggregate show -fields raidtype
```

## Shelf and Enclosure

```bash
# Disk shelves
storage shelf show

# Shelf module detail
storage shelf show -detail
```
