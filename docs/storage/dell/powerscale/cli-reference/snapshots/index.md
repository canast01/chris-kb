# Snapshots

> Part of the Dell PowerScale (Isilon) CLI Reference.

---

```bash
# List snapshots
isi snapshot snapshots list
isi snapshot snapshots view <snap_id>

# Create snapshot
isi snapshot snapshots create /ifs/<path> --name <snap_name>

# Delete snapshot
isi snapshot snapshots delete <snap_id>
isi snapshot snapshots delete --path /ifs/<path> --name <snap_name>

# Restore (copy back from snapshot)
cp -a /ifs/.snapshot/<snap_name>/<path>/* /ifs/<path>/

# Snapshot schedules
isi snapshot schedules list
isi snapshot schedules view <schedule_name>
isi snapshot schedules create <schedule_name> /ifs/<path> <frequency>

# Snapshot aliases
isi snapshot aliases list
```
