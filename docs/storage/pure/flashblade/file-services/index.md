# FlashBlade File Services

FlashBlade provides NFS and SMB file services through managed file systems.

## List File Systems

```bash
purefb fs list
purefb fs list --all    # includes destroyed
```

## Create a File System

```bash
# NFS file system
purefb fs create --name <fs_name> --size 10T --nfs-v3-enabled true --nfs-v4-1-enabled true

# SMB file system
purefb fs create --name <fs_name> --size 10T --smb-enabled true
```

## Manage NFS Exports

```bash
# Show NFS export rules for a file system
purefb fs list <fs_name> --nfs

# Set NFS export rules
purefb fs update <fs_name> \
    --nfs-rules "*(rw,no_root_squash)" \
    --nfs-v3-enabled true \
    --nfs-v4-1-enabled true
```

## Manage SMB Shares

```bash
# Enable SMB on a file system
purefb fs update <fs_name> --smb-enabled true

# SMB shares are accessible at \\<VIP_FQDN>\<fs_name>
```

## Resize a File System

```bash
purefb fs update <fs_name> --size 20T
```

## Mount Points (Client Side)

```bash
# NFS mount from a Linux client
mount -t nfs <FlashBlade_VIP>:/<fs_name> /mnt/<mountpoint>

# NFSv4.1 mount
mount -t nfs4 -o minorversion=1 <FlashBlade_VIP>:/<fs_name> /mnt/<mountpoint>
```

## Snapshot-Enabled File Systems

```bash
# Enable snapshots (required for file system snapshots)
purefb fs update <fs_name> --snapshot-enabled true
```

## Destroy and Eradicate a File System

```bash
# Destroy (recoverable for 24 hours)
purefb fs destroy <fs_name>

# Eradicate permanently
purefb fs eradicate <fs_name>
```

## Common Issues

| Issue | Check | Action |
|---|---|---|
| NFS mount fails | Export rules | Verify client IP matches export rule |
| SMB share inaccessible | SMB enabled | `purefb fs update --smb-enabled true` |
| File system full | Capacity | Resize with `purefb fs update --size` |
| Snapshot missing | Snapshots enabled? | Enable with `--snapshot-enabled true` |
