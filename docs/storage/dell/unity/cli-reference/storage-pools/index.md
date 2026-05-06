# Storage Pools

> Part of the Dell Unity CLI Reference (Unisphere CLI).

## List Pools

```bash
# All pools (summary)
uemcli -d <ip> -u admin /stor/config/pool show

# Detailed — name, size, used, free, health, RAID type
uemcli -d <ip> -u admin /stor/config/pool show -detail

# Specific pool by ID
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> show -detail
```

## Capacity Monitoring

```bash
# Pool utilisation
uemcli -d <ip> -u admin /stor/config/pool show -detail | \
    grep -E "Name|Size|Used|Free|Health"
```

| Free Space | Action |
|---|---|
| > 30% | Healthy — no action |
| 20–30% | Monitor closely |
| 10–20% | Alert — plan expansion |
| < 10% | Emergency — add capacity immediately |

## Create a Pool

```bash
# Create a pool using an existing disk group
uemcli -d <ip> -u admin /stor/config/pool create \
    -name <pool_name> \
    -diskGroup <dg_id> \
    -raidType RAID5 \
    -stripeWidth 5

# With description
uemcli -d <ip> -u admin /stor/config/pool create \
    -name Production_Pool \
    -diskGroup dg_1 \
    -raidType RAID5 \
    -descr "Primary production pool - SAS SSD"
```

## Expand a Pool

```bash
# Add a disk group to an existing pool
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> set \
    -addDiskGroup <dg_id>

# Verify size after expansion
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> show -detail | \
    grep -E "Size|Used|Free"
```

## Modify and Delete

```bash
# Rename a pool
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> set -name <new_name>

# Delete a pool (must be empty — no LUNs or file systems)
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> delete
```

## RAID Types

| RAID Type | Overhead | Protection | Use Case |
|---|---|---|---|
| RAID5 | 1 disk | 1 drive failure | General purpose SSD/SAS |
| RAID6 | 2 disks | 2 drive failures | High-capacity NL-SAS |
| RAID10 | 50% | 1 disk per mirrored pair | High IOPS workloads |
| RAID1/0 | 50% | 1 disk per pair | Critical databases |

## Pool Health States

| State | Meaning | Action |
|---|---|---|
| OK | Healthy | None |
| Degraded | A disk group is degraded | Check disk health |
| Minor | Non-critical condition | Review alerts |
| Major | Significant degradation | Immediate investigation |
| Critical | Service impacting | Emergency response |
