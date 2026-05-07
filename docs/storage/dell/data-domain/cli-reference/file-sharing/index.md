# NFS & CIFS/SMB

> Part of the Dell Data Domain CLI Reference.
## NFS

Data Domain exports MTrees over NFS for backup applications that use the filesystem protocol (e.g., Networker, some Veeam configurations).

```bash
# List all NFS exports
nfs show exports

# NFS service status
nfs status

# NFS client connections
nfs show clients
```

### Managing NFS Exports

```bash
# Create an NFS export for an MTree
nfs add export /data/col1/<mtree_name> clients <ip_or_cidr>

# Allow multiple clients
nfs add export /data/col1/<mtree_name> clients <ip1>,<ip2>

# Modify export options (root squash, read-write)
nfs modify export /data/col1/<mtree_name> clients <ip> options rw,root-squash

# Remove a client from an export
nfs del export /data/col1/<mtree_name> clients <ip_or_cidr>

# Remove the entire export
nfs del export /data/col1/<mtree_name>
```

### NFS Options Reference

| Option | Meaning |
|---|---|
| `rw` | Read-write access |
| `ro` | Read-only access |
| `root-squash` | Map root user to anonymous (more secure) |
| `no-root-squash` | Root retains root privileges (needed for some backup apps) |
| `sync` | Synchronous writes — safer but slower |
| `async` | Asynchronous writes — faster but risk on crash |

## CIFS / SMB

```bash
# CIFS service status and configuration
cifs show

# Active client connections
cifs show clients

# All CIFS shares
cifs share show

# Create a CIFS share for an MTree
cifs share add /data/col1/<mtree_name>

# Remove a CIFS share
cifs share del /data/col1/<mtree_name>
```

### CIFS Share Options

```bash
# Restrict share access to specific AD groups
cifs share modify <share_name> add-writable-users <DOMAIN>\<group>

# View share permissions
cifs share show <share_name>
```

## NFS + CIFS Dual Protocol

An MTree can be exported over both NFS and CIFS simultaneously for mixed environments. Ensure access controls are configured on both protocols to avoid permission conflicts.

## Troubleshooting

| Issue | Check | Command |
|---|---|---|
| NFS mount fails | Export exists for client IP? | `nfs show exports` |
| Access denied on mount | `no-root-squash` needed? | `nfs modify export ... options no-root-squash` |
| CIFS share not visible | CIFS enabled? | `cifs show` |
| Slow NFS backup | `async` option enabled? | `nfs show exports` → check options |
