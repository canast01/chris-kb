# File Systems (NAS)

> Part of the Dell Unity CLI Reference (Unisphere CLI).
## NAS Servers

```bash
# List NAS servers
uemcli -d <ip> /net/nas/server show
uemcli -d <ip> /net/nas/server show -detail

# Create a NAS server
uemcli -d <ip> /net/nas/server create \
    -name <nas_name> \
    -sp <sp_id> \
    -pool <pool_id>
```

## File Systems

```bash
# List file systems
uemcli -d <ip> /stor/config/fs show
uemcli -d <ip> /stor/config/fs show -detail

# Create a file system
uemcli -d <ip> /stor/config/fs create \
    -name <fs_name> \
    -nasServer <nas_id> \
    -pool <pool_id> \
    -size 1T

# Resize a file system
uemcli -d <ip> /stor/config/fs -id <fs_id> set -size 2T

# Delete a file system
uemcli -d <ip> /stor/config/fs -id <fs_id> delete
```

## NFS Shares

```bash
# List NFS shares
uemcli -d <ip> /stor/config/nfs show

# Create an NFS share
uemcli -d <ip> /stor/config/nfs create -fs <fs_id> -path / -nfsVersion NFSv3

# Set host access
uemcli -d <ip> /stor/config/nfs -id <nfs_id> set -hostAccess "<ip>(rw)"

# Delete an NFS share
uemcli -d <ip> /stor/config/nfs -id <nfs_id> delete
```

## CIFS Shares

```bash
# List CIFS shares
uemcli -d <ip> /stor/config/cifs show

# Create a CIFS share
uemcli -d <ip> /stor/config/cifs create -name <share_name> -fs <fs_id> -path /

# Delete a CIFS share
uemcli -d <ip> /stor/config/cifs -id <cifs_id> delete
```

## File System Snapshots

```bash
# List snapshots for a file system
uemcli -d <ip> /prot/snap show -res <fs_id>

# Create a snapshot
uemcli -d <ip> /prot/snap create -name <snap_name> -res <fs_id>

# Restore
uemcli -d <ip> /prot/snap -id <snap_id> restore

# Delete
uemcli -d <ip> /prot/snap -id <snap_id> delete
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| NFS mount fails | NFS share access | Set `-hostAccess` with correct IP |
| File system full | Capacity | Resize with `-size` |
| NAS server not responding | SP health | Check SP status in Unisphere |
| CIFS share inaccessible | AD join | Verify NAS server AD status |
