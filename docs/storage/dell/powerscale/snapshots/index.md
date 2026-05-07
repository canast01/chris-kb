# PowerScale Snapshots

Snapshot management and recovery on Dell PowerScale using SnapshotIQ.
## Manual Snapshots

```bash
# Create a snapshot of a directory
isi snapshot snapshots create /ifs/data/project1 --name project1-$(date +%Y%m%d)

# List all snapshots
isi snapshot snapshots list
isi snapshot snapshots list -v

# View details of a snapshot
isi snapshot snapshots view <snap_id>

# Delete a snapshot
isi snapshot snapshots delete <snap_id>

# Delete by name
isi snapshot snapshots delete --name project1-20260101
```

## Snapshot Schedules

```bash
# List all schedules
isi snapshot schedules list

# View a schedule
isi snapshot schedules view <schedule_name>

# Create a daily schedule retaining 14 snapshots
isi snapshot schedules create daily-project1 \
    /ifs/data/project1 \
    --schedule "every 1 days at 00:00" \
    --retention 2W \
    --alias latest-project1

# Modify a schedule
isi snapshot schedules modify <schedule_name> --retention 1M

# Delete a schedule (does not delete existing snapshots)
isi snapshot schedules delete <schedule_name>
```

## Snapshot Aliases

```bash
# List aliases
isi snapshot aliases list

# View an alias
isi snapshot aliases view <alias_name>

# Update alias to point to a different snapshot
isi snapshot aliases modify <alias_name> --target <snap_id>
```

## Accessing Snapshot Data

Snapshot data is accessible read-only at the `.snapshot` directory within the filesystem:

```bash
# From the cluster shell
ls /ifs/data/project1/.snapshot/

# From a Linux NFS client (if .snapshot access is enabled on the export)
ls /mnt/project1/.snapshot/
cp /mnt/project1/.snapshot/project1-20260101/important_file.txt /restore/

# Enable .snapshot visibility on an NFS export
isi nfs exports modify <export_id> --snapshot-dir yes
```

## Recovering Files from a Snapshot

```bash
# Copy a specific file from snapshot back to live filesystem
cp -p /ifs/data/project1/.snapshot/project1-20260101/report.xlsx \
      /ifs/data/project1/report.xlsx

# Restore an entire directory
rsync -av /ifs/data/project1/.snapshot/project1-20260101/ \
          /ifs/data/project1/

# Restore via SnapshotIQ revert (rolls back entire path to snapshot state)
isi snapshot snapshots modify <snap_id> --set-expiration never   # Protect before reverting
isi snapshot snapshots revert <snap_id>
# WARNING: revert is destructive — all data written after the snapshot is lost
```

## Snapshot Capacity

```bash
# Total space consumed by snapshots
isi snapshot snapshots list | awk 'NR>1 { sum += $5 } END { print "Total snapshots:", sum/1024/1024/1024, "GB" }'

# Identify largest snapshots
isi snapshot snapshots list -v | sort -k5 -rn | head -10
```

## SnapshotIQ Lock and Expiration

```bash
# List snapshot locks (prevents deletion)
isi snapshot locks list <snap_id>

# Set expiration date on a snapshot
isi snapshot snapshots modify <snap_id> --set-expiration "2026-12-31"

# Remove expiration (snapshot persists until manually deleted)
isi snapshot snapshots modify <snap_id> --clear-expiration
```
