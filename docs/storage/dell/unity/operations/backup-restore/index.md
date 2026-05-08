# Unity — Backup & Restore

> Backup configuration, restore procedures, and validation for Dell Unity.

## Overview

Dell Unity supports multiple backup integration methods and native snapshot-based protection. This page covers the key approaches for protecting Unity-hosted data.

## Native Snapshots

Unity snapshots are space-efficient, redirect-on-write copies tied to the storage pool.

```bash
# Create a LUN snapshot
uemcli -d <ip> -u admin /prot/snap create \
    -name <snap_name> \
    -res <lun_id>

# Create a filesystem snapshot
uemcli -d <ip> -u admin /prot/snap create \
    -name <snap_name> \
    -res <fs_id>

# List all snapshots
uemcli -d <ip> -u admin /prot/snap show

# Restore a LUN or filesystem from snapshot
uemcli -d <ip> -u admin /prot/snap -id <snap_id> restore

# Delete a snapshot
uemcli -d <ip> -u admin /prot/snap -id <snap_id> delete
```

## Snapshot Schedules

```bash
# List snapshot schedules
uemcli -d <ip> -u admin /prot/snapSchedule show

# Create a daily snapshot schedule (retain 7 copies)
uemcli -d <ip> -u admin /prot/snapSchedule create \
    -name sched-daily \
    -type daily \
    -hour 2 \
    -keepFor 7

# Assign a schedule to a LUN
uemcli -d <ip> -u admin /stor/config/lun -id <lun_id> set \
    -snapSchedule <schedule_id>
```

## Backup Integration

| Backup Tool | Integration Method | Notes |
|---|---|---|
| Veeam Backup & Replication | Unity Storage Snapshots integration | Veeam triggers Unity snapshots at backup time; requires Veeam Enterprise or higher |
| CommVault | IntelliSnap snapshot API integration | Configure Unity array in CommVault as an IntelliSnap-capable array |
| Veritas NetBackup | NetBackup Snapshot Manager | Configure Unity as a snapshot array in NetBackup Snapshot Manager |
| NDMP (NAS backup) | NDMP protocol on NAS servers | Use any NDMP-compatible backup tool; configure via `uemcli /net/nas/ndmp` |

## Replication as DR

Unity asynchronous or synchronous replication to a remote Unity or PowerStore array provides RPO-based protection:

```bash
# List replication sessions and their last sync time
uemcli -d <ip> -u admin /prot/rep/session show -detail

# Trigger an immediate sync before maintenance
uemcli -d <ip> -u admin /prot/rep/session -id <session_id> sync
```

See the [CLI Reference](../cli-reference/) for full replication commands.

## Restore Validation

After any restore, confirm the following:

- [ ] Snapshot or replication restore completed without errors in Unisphere
- [ ] LUN or filesystem is accessible from the target host
- [ ] Application can read and write data from the restored volume
- [ ] Pool capacity is within acceptable range after the restore operation
