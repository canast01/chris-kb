# Linux — Backup & Restore

Veeam Agent for Linux backup jobs, restore procedures, and validation steps.

## Veeam Agent for Linux

Veeam Agent for Linux provides image-level and file-level backup for Linux physical and virtual machines.

### Installation

```bash
# Add Veeam repository (RHEL/CentOS)
curl -o /etc/yum.repos.d/veeam.repo https://repository.veeam.com/backup/linux/rhel/x86_64/veeam.repo
dnf install -y veeam

# Ubuntu/Debian
curl -s https://repository.veeam.com/backup/linux/dpkg/x86_64/Packages.key | apt-key add -
echo "deb https://repository.veeam.com/backup/linux/dpkg/x86_64 focal veeam" > /etc/apt/sources.list.d/veeam.list
apt update && apt install -y veeam

# Verify installation
veeam --version
veeamconfig ui   # Opens text-based configuration UI
```
┌────────────────────────────────────── Linux — Backup & Restore ───────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                                        Backup Strategy                                        │   │
│   │           3-2-1 rule: 3 copies · 2 different media · 1 offsite / cloud (S3/Glacier)           │   │
│   │         Full weekly + incremental daily; retention: 30 days local, 1 year tape/object         │   │
│   │        LVM snapshots: instant consistent point-in-time for live volumes before changes        │   │
│   │           Test restores: monthly drill to verify backup integrity and RTO compliance          │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Backup strategy must balance recovery time objective with storage cost                             │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               File-Level Tools               │  │              Enterprise Backup              │   │
│   │         rsync -avz: incremental sync         │  │          Bacula: client/director/SD         │   │
│   │         tar czf: archive + compress          │  │            Veeam Agent for Linux            │   │
│   │          dd if=/dev/sda: disk image          │  │          Amanda: open-source backup         │   │
│   │         duplicati: encrypted backup          │  │          Commvault: enterprise CBM          │   │
│   │          restic: dedup + encryption          │  │          NBU: NetBackup agent mode          │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86-64 servers · NAS/SAN storage · tape library · S3 object store · Power & Cooling                  │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  3-2-1 rule  = 3 copies of data on 2 different media with 1 copy offsite                              │
│  RTO         = Recovery Time Objective; max acceptable time to restore a service                      │
│  RPO         = Recovery Point Objective; max acceptable data loss measured in time                    │
│  LVM snapshot= CoW point-in-time copy of an LV; consistent backup without stopping service            │
│  rsync       = Remote sync tool; copies only changed blocks; supports SSH transport                   │
│  tar         = Tape ARchive; bundles files into a single stream; combined with gzip/bzip2             │
│  dd          = Data Duplicator; copies raw blocks; used for disk imaging and cloning                  │
│  restic      = Modern backup tool; content-addressable dedup with AES-256 encryption                  │
│  Bacula      = Open-source network backup; director/storage daemon/file daemon model                  │
│  Veeam Agent = Physical Linux backup agent; image-level backup to Veeam repository                    │
│  CBM         = Changed Block Monitoring; Commvault incremental-forever backup method                  │
│  NBU         = NetBackup; Veritas enterprise backup platform with agent and catalog                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

### Schedule Backup Jobs

```bash
# Set a daily schedule at 02:00
veeamconfig schedule set \
  --jobName "SERVER01-Daily" \
  --daily \
  --at 02:00

# Set a weekly schedule (Sunday at 03:00)
veeamconfig schedule set \
  --jobName "SERVER01-Daily" \
  --weekly \
  --dayOfWeek sunday \
  --at 03:00

# Enable the schedule
veeamconfig schedule enable --jobName "SERVER01-Daily"

# View schedule
veeamconfig schedule show --jobName "SERVER01-Daily"
```

### Run a Backup Job Manually

```bash
# Start a backup job immediately
veeamconfig job start --name "SERVER01-Daily"

# Monitor job progress
veeamconfig session list
veeamconfig session info --id <session-id>

# View logs for the last session
veeamconfig session log --id <session-id>

# Wait for job completion (useful in scripts)
while [[ $(veeamconfig session info --id <session-id> | grep "State:" | awk '{print $2}') == "Running" ]]; do
    sleep 30
done
echo "Backup complete"
```

### Backup Job Status

```bash
# List recent backup sessions
veeamconfig session list

# Show restore points available for a job
veeamconfig restorepoint list --jobName "SERVER01-Daily"

# Show session result (Success / Warning / Failed)
veeamconfig session info --id <session-id> | grep "Result:"
```

## Restore Procedures

### File-Level Restore

```bash
# List available restore points
veeamconfig restorepoint list --jobName "SERVER01-Daily"

# Mount a restore point (creates a read-only mount under /tmp/veeam/)
veeamconfig recoverypoints mount --restorePointId <restore-point-id>

# The mounted files will be available at a path like:
ls /tmp/veeam/<uuid>/

# Copy the needed files from the mount
cp -a /tmp/veeam/<uuid>/var/www/html/config.php /var/www/html/config.php.restored

# Unmount when done
veeamconfig recoverypoints umount --restorePointId <restore-point-id>
```

### Bare Metal Restore

For full system recovery, boot from the Veeam Recovery Media ISO.

```bash
# Create Veeam Recovery Media (run on a working system)
# Requires veeam-nosnap package
veeam --create-recovery-media --output /tmp/veeam-recovery.iso
# Write to USB
dd if=/tmp/veeam-recovery.iso of=/dev/sdX bs=4M status=progress

# Bare metal restore process (from Recovery Media boot):
# 1. Boot from Veeam Recovery Media
# 2. Select Restore Volumes or Restore Entire Machine
# 3. Browse to repository (NFS/SMB/Veeam repository)
# 4. Select restore point
# 5. Map to target disk(s)
# 6. Restore and reboot
```

### Volume-Level Restore to Alternate Location

```bash
# Mount the restore point and export to an image
veeamconfig recoverypoints export \
  --restorePointId <restore-point-id> \
  --targetDir /mnt/restore-output
```

## rsync-Based Backup (File Sync)

For file-level incremental backup without Veeam:

```bash
# Incremental backup to a remote host using rsync
rsync -avz --delete --link-dest=/backup/last \
  /data/ backupserver:/backup/$(date +%Y-%m-%d)/

# Rotate: create a symlink to the latest backup
ssh backupserver "ln -snf /backup/$(date +%Y-%m-%d) /backup/last"

# Exclude specific paths
rsync -avz --delete \
  --exclude="/data/tmp/" \
  --exclude="/data/cache/" \
  /data/ backupserver:/backup/data/

# Dry run first (shows what would be transferred)
rsync -avzn /data/ backupserver:/backup/data/
```

## Backup Validation

### Verify Backup Integrity

```bash
# Veeam — verify a restore point (checksum validation)
veeamconfig recoverypoints verify --id <restore-point-id>

# Manually verify an rsync backup by comparing checksums
# On source:
find /data -type f -exec md5sum {} \; | sort > /tmp/source-checksums.txt
# On backup target:
find /backup/data -type f -exec md5sum {} \; | sort > /tmp/backup-checksums.txt
# Compare
diff /tmp/source-checksums.txt /tmp/backup-checksums.txt
```

### Test Restore (Monthly)

```bash
# Mount the restore point and compare a sample of files
veeamconfig recoverypoints mount --restorePointId <restore-point-id>

# Verify key application files are intact
diff /var/www/html/index.php /tmp/veeam/<uuid>/var/www/html/index.php && echo "Match OK"

# Check database dump restorability
mysql -u testuser -p testdb < /tmp/veeam/<uuid>/var/backups/mysql-latest.sql
echo "DB restore test: $?"

# Unmount
veeamconfig recoverypoints umount --restorePointId <restore-point-id>
```

## Backup Monitoring

```bash
# Check Veeam Agent service status
systemctl status veeamservice veeamsnap

# View Veeam Agent logs
journalctl -u veeamservice -n 100
tail -f /var/log/veeam/Veeam.Backup.AgentManager.log

# Alert on failed backup sessions (add to monitoring/cron)
FAILED=$(veeamconfig session list | grep Failed | wc -l)
if [ "$FAILED" -gt 0 ]; then
    echo "WARNING: $FAILED Veeam backup session(s) failed" | mail -s "Backup Alert" alerts@corp.local
fi
```

## Backup Best Practices

| Practice | Detail |
|---|---|
| 3-2-1 rule | 3 copies, 2 different media, 1 offsite |
| Retention | Minimum 14 daily, 4 weekly, 3 monthly |
| Test restores | Perform file-level restore test monthly |
| Bare metal test | Test full BMR annually in DR exercise |
| Immutable backups | Enable immutability on repository to protect against ransomware |
| Encryption at rest | Enable Veeam backup encryption or use encrypted repository |
| Monitor alerts | Alert on failed jobs within the backup window |
| Log retention | Keep Veeam session logs for 90 days |

## Quick Reference

| Task | Command |
|---|---|
| List jobs | `veeamconfig job list` |
| Start job | `veeamconfig job start --name "JobName"` |
| List sessions | `veeamconfig session list` |
| List restore points | `veeamconfig restorepoint list --jobName "JobName"` |
| Mount restore point | `veeamconfig recoverypoints mount --restorePointId <id>` |
| Unmount restore point | `veeamconfig recoverypoints umount --restorePointId <id>` |
| Verify restore point | `veeamconfig recoverypoints verify --id <id>` |
| Veeam service status | `systemctl status veeamservice` |
| Veeam logs | `journalctl -u veeamservice` |
