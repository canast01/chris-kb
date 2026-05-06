# PowerScale NFS

NFS export management, configuration, and troubleshooting on Dell PowerScale.

## Export Management

```bash
# List all exports
isi nfs exports list
isi nfs exports list -v

# View a specific export
isi nfs exports view <export_id>

# Create an export
isi nfs exports create /ifs/data/myshare \
    --clients 10.0.0.0/24 \
    --read-write-clients 10.0.0.0/24 \
    --root-clients 10.0.1.5 \
    --description "Application data share"

# Modify an existing export
isi nfs exports modify <export_id> --addread-write-clients 10.0.2.0/24
isi nfs exports modify <export_id> --description "Updated description"

# Delete an export
isi nfs exports delete <export_id>

# Validate all exports for errors
isi nfs exports check
```

## Export Client Access Levels

| Client Type | Permission |
|---|---|
| `--clients` | Read-only access |
| `--read-write-clients` | Read/write access |
| `--root-clients` | Root access (uid 0 not squashed) |

## NFS Settings

```bash
# Global NFS settings
isi nfs settings global view

# Default export settings (applied to new exports)
isi nfs settings export view

# NFS service status
isi services nfs status

# Restart NFS service (with caution — disrupts active mounts)
isi services nfs restart
```

## NFS Zones (Access Zones)

```bash
# List access zones
isi zones list

# Create export in a specific access zone
isi nfs exports create /ifs/zone1/data \
    --zone Zone1 \
    --read-write-clients 10.1.0.0/24

# List exports by access zone
isi nfs exports list --zone Zone1
```

## NFS Aliases

```bash
# NFS aliases map a shorter path to a full /ifs path
isi nfs aliases list
isi nfs aliases create /exports/data /ifs/data/project1
```

## Troubleshooting NFS

```bash
# Check mount errors from client side (Linux)
showmount -e <powerscale-ip>
mount -t nfs <ip>:/ifs/data/share /mnt/test
dmesg | grep nfs | tail -10

# Check NFS stats on the cluster
isi statistics protocol list --protocol nfs3
isi statistics protocol list --protocol nfs4

# Check for NFS errors in events
isi event events list | grep -i nfs

# Verify export path exists
isi quota quotas list --path /ifs/data/share
ls -la /ifs/data/share   # (from cluster shell)
```

## Performance Tuning

```bash
# Increase NFS export throughput — disable attribute caching (for consistency-sensitive workloads)
isi nfs exports modify <export_id> --no-attribute-cache

# Block size for large sequential I/O
isi nfs exports modify <export_id> --block-size 524288

# Check current NFS client stats
isi statistics client list | grep nfs | sort -k3 -rn | head -10
```
