# Dell Unity Storage Pools

Storage pool management, capacity monitoring, and disk group configuration on Dell Unity.
## Pool Overview

```bash
# List all pools
uemcli -d <ip> -u admin /stor/config/pool show
uemcli -d <ip> -u admin /stor/config/pool show -detail

# View a specific pool
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> show -detail
```

## Create a Pool

```bash
# Create a pool using an existing disk group (RAID5)
uemcli -d <ip> -u admin /stor/config/pool create \
    -name <pool_name> \
    -diskGroup <dg_id> \
    -raidType RAID5 \
    -stripeWidth 5

# Create with description
uemcli -d <ip> -u admin /stor/config/pool create \
    -name Production_Pool \
    -diskGroup dg_1 \
    -raidType RAID5 \
    -descr "Primary production pool - SAS SSD"
```

## Expand a Pool

```bash
# Add another disk group to an existing pool
uemcli -d <ip> -u admin /stor/config/pool -id <pool_id> set \
    -addDiskGroup <dg_id>

# Verify pool size after expansion
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

## Disk Groups

```bash
# List disk groups
uemcli -d <ip> -u admin /stor/config/dg show
uemcli -d <ip> -u admin /stor/config/dg show -detail

# Create a disk group
uemcli -d <ip> -u admin /stor/config/dg create \
    -diskType SAS \
    -diskCount 5 \
    -raidType RAID5

# View disks in a disk group
uemcli -d <ip> -u admin /stor/config/disk show | grep <dg_id>
```

## Capacity Monitoring

```bash
# Pool utilisation — flag if above 80%
uemcli -d <ip> -u admin /stor/config/pool show -detail | \
    grep -E "Name|Size|Used|Free|Health"

# Individual disk usage within pool
uemcli -d <ip> -u admin /stor/config/disk show -detail | \
    grep -E "Name|Pool|Health|State"
```

## Auto-Tiering (FAST VP)

If FAST VP (Fully Automated Storage Tiering) is licensed:

```bash
# View tiering policy on a LUN
uemcli -d <ip> -u admin /stor/config/lun show -detail | grep -i tier

# Set tiering policy on a LUN
uemcli -d <ip> -u admin /stor/config/lun -id <lun_id> set \
    -tieringPolicy autotier   # Options: autotier, highestAvailable, lowestAvailable, noData

# FAST VP relocation status
uemcli -d <ip> -u admin /storage/fastp/session show
```

## Pool Health Summary

| Metric | Healthy | Action Required |
|---|---|---|
| Pool health | OK | Any other value = investigate |
| Free space | > 20% | < 20% = alert; < 10% = emergency |
| Disk group health | OK | Degraded = drive failure, replace urgently |
| RAID rebuild | Not running | Rebuild running = do not make changes |
