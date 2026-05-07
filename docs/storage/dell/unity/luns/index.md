# Dell Unity LUNs

LUN lifecycle management on Dell Unity — create, map, expand, and manage snapshots.
## LUN Overview

```bash
# List all LUNs
uemcli -d <ip> -u admin /stor/config/lun show
uemcli -d <ip> -u admin /stor/config/lun show -detail

# View a specific LUN
uemcli -d <ip> -u admin /stor/config/lun -id <lun_id> show -detail
```

## Create a LUN

```bash
# Create a basic thin LUN in a pool
uemcli -d <ip> -u admin /stor/config/lun create \
    -name <lun_name> \
    -pool <pool_id> \
    -size 500G

# Create with a description
uemcli -d <ip> -u admin /stor/config/lun create \
    -name db-prod-01 \
    -pool pool_1 \
    -size 1T \
    -descr "Production database LUN"

# Create with a host access directly
uemcli -d <ip> -u admin /stor/config/lun create \
    -name app-lun-01 \
    -pool pool_1 \
    -size 200G \
    -host <host_id> \
    -accessMask nohostaccess   # assign access separately
```

## Modify and Expand

```bash
# Expand LUN size (can only increase)
uemcli -d <ip> -u admin /stor/config/lun -id <lun_id> set -size 2T

# Rename a LUN
uemcli -d <ip> -u admin /stor/config/lun -id <lun_id> set -name <new_name>

# Change description
uemcli -d <ip> -u admin /stor/config/lun -id <lun_id> set -descr "Updated description"
```

## Host Access (LUN Mapping)

```bash
# Grant host access to a LUN
uemcli -d <ip> -u admin /stor/config/lunacl create \
    -lun <lun_id> \
    -host <host_id>

# List current host access
uemcli -d <ip> -u admin /stor/config/lunacl show

# Remove host access
uemcli -d <ip> -u admin /stor/config/lunacl -id <acl_id> delete
```

## LUN Snapshots

```bash
# List snapshots for a LUN
uemcli -d <ip> -u admin /prot/snap show -res <lun_id>

# Create a snapshot
uemcli -d <ip> -u admin /prot/snap create \
    -name <snap_name> \
    -res <lun_id>

# Restore LUN from snapshot
uemcli -d <ip> -u admin /prot/snap -id <snap_id> restore

# Delete a snapshot
uemcli -d <ip> -u admin /prot/snap -id <snap_id> delete

# Attach snapshot as read-only to another host
uemcli -d <ip> -u admin /prot/snap -id <snap_id> copy \
    -name <snap_copy_name>
```

## Delete a LUN

```bash
# Delete requires all host access and snapshots to be removed first
# 1. Remove host access
uemcli -d <ip> -u admin /stor/config/lunacl -id <acl_id> delete

# 2. Delete snapshots
uemcli -d <ip> -u admin /prot/snap show -res <lun_id>
uemcli -d <ip> -u admin /prot/snap -id <snap_id> delete

# 3. Delete the LUN
uemcli -d <ip> -u admin /stor/config/lun -id <lun_id> delete
```

## Host-Side Validation (After Mapping)

```bash
# Linux — rescan and discover new LUN
rescan-scsi-bus.sh
multipath -ll

# Windows — rescan disks
Get-Disk | Where-Object OperationalStatus -eq "Offline"
Set-Disk -Number <n> -IsOffline $false
Initialize-Disk -Number <n>
New-Partition -DiskNumber <n> -UseMaximumSize -AssignDriveLetter
Format-Volume -DriveLetter <X> -FileSystem NTFS
```
