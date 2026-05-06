# Snapshots

> Part of the [Pure FlashBlade CLI Reference](../).

---

## Snapshots

```bash
# List snapshots
purefb snapshot show
purefb snapshot show --name <snapshot_name>

# Create snapshot
purefb snapshot create --source <filesystem_name> --name <snapshot_name>

# Restore
purefb snapshot copy --name <snapshot_name> --target <new_fs_name>

# Destroy / eradicate
purefb snapshot destroy --name <snapshot_name>
purefb snapshot eradicate --name <snapshot_name>

# Scheduled policies
purefb snapshot-rule show
```
