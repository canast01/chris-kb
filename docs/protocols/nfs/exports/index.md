# NFS Exports

```
        SERVER-SIDE EXPORT CONFIGURATION
┌──────────────────────────────────────────────────────────────┐
│  /etc/exports                                                │
│  ┌────────────────────────────────────────────────────────┐  │
│  │ /data/shared  192.168.10.0/24(rw,sync,no_subtree_check)│  │
│  │ /data/readonly  *(ro,sync,root_squash)                 │  │
│  └──────────────────────┬─────────────────────────────────┘  │
│                         │ exportfs -ra (reload without restart)│
│                         ▼                                    │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Active exports (exportfs -v)                          │  │
│  │  /data/shared  192.168.10.0/24(rw,sync,...)           │  │
│  │  /data/readonly  <world>(ro,sync,root_squash,...)      │  │
│  └──────────────────────┬─────────────────────────────────┘  │
│                         │ TCP 2049                            │
│                         ▼                                    │
│                    NFS clients mount                         │
└──────────────────────────────────────────────────────────────┘
```

## Overview

NFS exports are defined in `/etc/exports` on Linux servers. Each line specifies a directory, the clients allowed to mount it, and a set of options controlling access, security, and behavior. Changes take effect with `exportfs -ra` — no service restart required.

## /etc/exports Syntax

```
/path/to/export  client_spec(options)
```

```bash
# Examples
/data/shared     192.168.10.0/24(rw,sync,no_subtree_check)
/data/readonly   *(ro,sync,no_root_squash)
/home            10.0.0.0/8(rw,sync,root_squash,anonuid=65534,anongid=65534)
/srv/nfs4        *(rw,sync,fsid=0,no_subtree_check)           # NFSv4 pseudo-root
/srv/nfs4/data   *(rw,sync,bind=/data/shared,no_subtree_check) # NFSv4 bind mount
```

## Key Export Options

| Option | Meaning |
|--------|---------|
| `rw` | Read-write access |
| `ro` | Read-only access |
| `sync` | Write to disk before replying (safer) |
| `async` | Reply before write completes (faster, risk of data loss) |
| `no_root_squash` | Root on client retains root privileges |
| `root_squash` | Root on client mapped to anonymous UID (default) |
| `all_squash` | All users mapped to anonymous UID |
| `no_subtree_check` | Disable subtree checking (recommended for most cases) |
| `fsid=0` | Marks the NFSv4 pseudo-root |

## Applying Export Changes

```bash
# Reload exports without restarting NFS
exportfs -ra

# List currently active exports
exportfs -v

# Export a directory immediately (without editing /etc/exports)
exportfs -o rw,sync,no_subtree_check 192.168.10.50:/data/tmp

# Unexport a directory
exportfs -u 192.168.10.50:/data/tmp

# Restart NFS server (last resort)
systemctl restart nfs-server
```

## Verifying Exports from Client Side

```bash
# List exports available from a server
showmount -e 192.168.10.10

# Check which clients have mounted each export
showmount -a 192.168.10.10

# Verify NFS service is listening
rpcinfo -p 192.168.10.10 | grep nfs
```

## Known Issues

- `exportfs -ra` silently ignores malformed lines in `/etc/exports`. Check `journalctl -u nfs-server` or `exportfs -v` output to confirm an export actually loaded.
- Overlapping export paths (e.g. exporting both `/data` and `/data/sub` to the same client with different options) can produce unexpected option inheritance. Test with `exportfs -v` and verify the options shown for each path.
- `no_subtree_check` is recommended for directories that are entire filesystems; omitting it causes extra kernel overhead and occasional permission errors when files are opened by handle across export boundaries.
