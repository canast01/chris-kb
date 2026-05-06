# File Systems (NFS / SMB)

> Part of the [Pure FlashBlade CLI Reference](../).

---

## File Systems (NFS / SMB)

```bash
# List file systems
purefb filesystem show
purefb filesystem show --name <name>

# Create file system
purefb filesystem create --name <name> --size 10T --nfs --nfs-rules "*(rw,no_root_squash)"
purefb filesystem create --name <name> --size 10T --smb

# Resize
purefb filesystem update --name <name> --size 20T

# Destroy / eradicate
purefb filesystem destroy --name <name>
purefb filesystem eradicate --name <name>

# NFS exports
purefb filesystem show --name <name>
purefb filesystem update --name <name> --nfs-rules "<ip_or_cidr>(rw,no_root_squash)"

# SMB shares
purefb smb-share show
purefb smb-share create --name <share_name> --filesystem <fs_name>
purefb smb-share destroy --name <share_name>
```
