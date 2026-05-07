# File Systems (NFS / SMB)

> Part of the Pure FlashBlade CLI Reference.

## List File Systems

```bash
purefb filesystem show
purefb filesystem show --name <name>
purefb filesystem show --all    # includes destroyed
```

## Create a File System

```bash
# NFS file system with export rules
purefb filesystem create \
    --name <name> \
    --size 10T \
    --nfs \
    --nfs-rules "*(rw,no_root_squash)"

# SMB file system
purefb filesystem create --name <name> --size 10T --smb

# Both NFS and SMB
purefb filesystem create \
    --name <name> \
    --size 10T \
    --nfs --nfs-rules "*(rw,no_root_squash)" \
    --smb
```

## Resize a File System

```bash
purefb filesystem update --name <name> --size 20T
```

## Update NFS Export Rules

```bash
# Restrict to specific network
purefb filesystem update \
    --name <name> \
    --nfs-rules "<ip_cidr>(rw,no_root_squash)"

# Multiple rules
purefb filesystem update \
    --name <name> \
    --nfs-rules "10.0.1.0/24(rw,no_root_squash):10.0.2.0/24(ro)"
```

## SMB Shares

```bash
# List SMB shares
purefb smb-share show

# Create an SMB share
purefb smb-share create --name <share_name> --filesystem <fs_name>

# Delete an SMB share
purefb smb-share destroy --name <share_name>
```

## Destroy and Eradicate

```bash
# Destroy (recoverable for 24 hours)
purefb filesystem destroy --name <name>

# Permanently eradicate
purefb filesystem eradicate --name <name>

# Recover a destroyed file system
purefb filesystem recover --name <name>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| NFS mount refused | Export rules | Verify client IP is in NFS rules |
| SMB share not visible | SMB enabled | Ensure `--smb` flag was used at create |
| File system full | Capacity | `purefb filesystem update --size` |
| Cannot destroy | Not empty (NFS mounts active) | Unmount all clients first |
