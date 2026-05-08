# Data Domain — Backup & Restore

## Restore Methods

| Method | Protocol | When Used |
|---|---|---|
| DDBoost restore | DDBoost | NetBackup, Networker, Veeam using boost protocol |
| NFS restore | NFS | Direct file access to MTree from backup server |
| CIFS restore | SMB | Direct file access from Windows backup server |

## Validating Restore Readiness

Before a restore, confirm:

```bash
# 1. Filesystem is healthy and enabled
filesys status

# 2. MTree has data and correct quota
mtree list --verbose | grep <mtree_name>

# 3. NFS/CIFS export or DDBoost storage unit accessible
nfs show exports | grep <mtree_path>
ddboost storage-unit list

# 4. No active cleaning cycle (cleaning can slow restore I/O)
filesys clean status
```

## DDBoost Restore (Backup Application)

Restores are initiated from the backup application (NetBackup, Networker, Veeam). The Data Domain role is passive — it serves data to the backup server.

```bash
# Monitor DDBoost active connections during restore
ddboost show clients
ddboost show stats | grep -i read
```

## NFS Restore (Direct File Copy)

```bash
# Mount the MTree on the backup server
mount <dd_ip>:/data/col1/<mtree_name> /mnt/dd_restore

# Navigate to backup data
ls /mnt/dd_restore/

# Restore-specific files or directories
cp -r /mnt/dd_restore/<backup_path>/ /target/restore/path/
```

## Performance Expectations

| Scenario | Expected Throughput |
|---|---|
| DDBoost restore (with DSP) | 200–500 MB/s per stream |
| NFS restore | 100–300 MB/s (network and disk I/O bound) |
| Multiple concurrent restores | Shared bandwidth — plan accordingly |

## Troubleshooting Slow Restores

```bash
# Check DD CPU and I/O during restore
system show stats

# Check if cleaning is running (impacts read performance)
filesys clean status

# Check active restore clients
ddboost show clients --verbose
nfs show clients

# Network bandwidth to restore destination
# (Check on the backup server with iperf or similar)
```

## Tape-Out / CIFS Restores

If backup data was originally written via CIFS:

```bash
# Confirm CIFS share is accessible
cifs share show | grep <mtree_name>
cifs show clients
```
