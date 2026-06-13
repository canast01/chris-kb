---
tags:
  - operations
  - pure
---
# FlashBlade — Backup & Restore


<div class="kb-summary">
Backup & Restore reference covering Snapshot-Based Backup Overview, Snapshot Management, File Restore Procedures, Object Store Restore Procedures, Veeam Backup & Replication Integration and 4 more sections.
</div>

```text
FlashBlade Data Protection Tiers
  ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  Local Snapshots (filesystem / bucket)                     │
  │  Snapshot policy schedule ──► point-in-time copies         │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                          │  async replication
  ┌────────────────────────────────────────────────── ▼ ──────────────────────────────────────────────────┐
  │  ActiveDR Replication                                      │
  │  Filesystem/bucket ──► remote FlashBlade (RPO: minutes)    │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                          │  backup integration
  ┌────────────────────────────────────────────────── ▼ ──────────────────────────────────────────────────┐
  │  Application Backup to FlashBlade (target)                 │
  │  Veeam / Commvault ──► NFS or S3 backup target on FB      │
  └───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Restore: snapshot → create clone → mount → validate → promote
```

> Part of the [FlashBlade Operations](../index.md) reference.

---

This page covers FlashBlade snapshot-based data protection, integration with enterprise backup tools, and restore procedures for filesystems and object store buckets.

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Snapshot-Based Backup Overview

FlashBlade uses space-efficient, redirect-on-write snapshots as the foundation for all data protection. Snapshots are instantaneous regardless of filesystem size and consume space only for changed blocks. A snapshot of a 100 TiB filesystem completes in milliseconds and immediately exposes the full point-in-time namespace through the `.snapshot` directory inside the NFS export.

For backup tools, the workflow is:

1. Backup tool (or its Pure plugin) requests a FlashBlade snapshot via the REST API
2. FlashBlade creates the snapshot instantly; the snapshot is consistent without application quiesce for NFS workloads
3. Backup tool streams data from the snapshot rather than from the live filesystem, eliminating I/O impact on production
4. After the backup stream completes, the backup tool optionally deletes the snapshot, or leaves it for additional recovery points

For object store, snapshots capture the state of a bucket at a point in time; object-level restoration is possible by listing objects within the snapshot and selectively copying them.

---

## Snapshot Management

### Create a Manual Snapshot

```bash
# Create a snapshot of a specific filesystem
purefb snapshot create --source prod-ml-training-data --name pre-maint-20260507

# Create snapshots of multiple filesystems in one command
purefb snapshot create --source prod-nfs,prod-analytics --name weekly-20260506

# Verify the snapshot was created
purefb snapshot list --source prod-ml-training-data
```

### List and Filter Snapshots

```bash
# List all snapshots
purefb snapshot list

# List snapshots for a specific filesystem
purefb snapshot list --source prod-ml-training-data

# List snapshots sorted by creation time (newest first)
purefb snapshot list --sort created-

# Show space consumed by each snapshot
purefb snapshot list --space
```

### Configure Snapshot Policies (Automated Schedules)

Snapshot policies define automatic schedules. Attach a policy to one or more filesystems to create retention-managed snapshots without manual intervention.

```bash
# List existing snapshot policies
purefb snapshot-rule list

# Create a daily snapshot policy — keep 7 days
purefb snapshot-rule create \
    --name daily-7d \
    --keep-for 7d

# Create a weekly snapshot policy — keep 4 weeks
purefb snapshot-rule create \
    --name weekly-4w \
    --keep-for 28d

# Attach a policy to a filesystem
purefb filesystem-snapshot-rule create \
    --filesystem prod-nfs \
    --rule daily-7d

# Attach the weekly policy to the same filesystem (multiple policies are supported)
purefb filesystem-snapshot-rule create \
    --filesystem prod-nfs \
    --rule weekly-4w

# Verify the attachment
purefb filesystem-snapshot-rule list --filesystem prod-nfs
```

---

## File Restore Procedures

### Self-Service File Restore via NFS `.snapshot`

The `.snapshot` directory is visible to NFS clients when the `snapshot_directory_accessible` option is enabled on the filesystem. Users can browse and restore individual files without administrator involvement.

```bash
# On the FlashBlade — enable snapshot directory access on the filesystem
purefb filesystem update --name prod-nfs --snapshot-directory-accessible true

# On the NFS client — browse available snapshots
ls /mnt/prod-nfs/.snapshot/
# Output:
# daily-7d.2026-05-06_00-00-00
# daily-7d.2026-05-07_00-00-00
# pre-maint-20260507

# Restore a single file from a snapshot
cp /mnt/prod-nfs/.snapshot/pre-maint-20260507/data/config.json \
   /mnt/prod-nfs/data/config.json

# Restore an entire directory from a snapshot
rsync -av /mnt/prod-nfs/.snapshot/daily-7d.2026-05-06_00-00-00/data/ \
          /mnt/prod-nfs/data/
```

### Restore a Filesystem to a Snapshot (Full Overwrite)

This replaces all current data in the live filesystem with the contents of the snapshot. Use only when a complete point-in-time recovery is required. All data written after the snapshot was created is lost.

```bash
# Confirm the snapshot exists
purefb snapshot list --source prod-nfs

# Overwrite the live filesystem with the snapshot — irreversible
purefb filesystem restore --name prod-nfs \
    --from-snapshot prod-nfs.pre-maint-20260507

# Verify the filesystem is accessible after restore
purefb filesystem list --name prod-nfs
```

### Clone a Snapshot to a New Filesystem

This creates an independent writable filesystem from a snapshot, leaving the original live filesystem intact. Use for parallel investigations, DR testing, or application testing against production data.

```bash
# Copy the snapshot to a new writable filesystem
purefb snapshot copy \
    --name prod-nfs.pre-maint-20260507 \
    --target prod-nfs-clone-20260507

# The new filesystem is immediately mountable
purefb filesystem list --name prod-nfs-clone-20260507

# Export via NFS (if needed)
purefb filesystem update \
    --name prod-nfs-clone-20260507 \
    --nfs-rules "10.0.1.0/24(rw,no_root_squash)"

# Mount on a client
mount -t nfs <fb-data-vip>:/prod-nfs-clone-20260507 /mnt/restore-test
```

---

## Object Store Restore Procedures

### Restore an Object from a Bucket Snapshot

Bucket snapshots are accessible via the S3 API by specifying the snapshot as an object store endpoint path.

```bash
# List snapshots for a specific bucket
purefb bucket-snapshot list --bucket prod-analytics-raw

# Create a manual bucket snapshot
purefb bucket-snapshot create \
    --bucket prod-analytics-raw \
    --name prod-analytics-raw.pre-maint-20260507

# Copy a snapshot to a new bucket for recovery
purefb bucket-snapshot copy \
    --name prod-analytics-raw.pre-maint-20260507 \
    --target prod-analytics-raw-restore

# Access the restored bucket via S3 using AWS CLI
aws s3 ls s3://prod-analytics-raw-restore \
    --endpoint-url https://<fb-s3-vip>/

# Copy an object from the restored bucket back to production
aws s3 cp s3://prod-analytics-raw-restore/data/2026/05/dataset.parquet \
          s3://prod-analytics-raw/data/2026/05/dataset.parquet \
          --endpoint-url https://<fb-s3-vip>/
```

---

## Veeam Backup & Replication Integration

Veeam integrates with FlashBlade via its NFS backup repository and, with the Pure Storage plugin, as a snapshot-integrated repository that enables instant recovery.

### Configure FlashBlade as an NFS Repository

1. On FlashBlade — create a dedicated filesystem for Veeam backups:

```bash
purefb filesystem create \
    --name prod-veeam-daily \
    --size 50T \
    --nfs \
    --nfs-rules "10.0.10.0/24(rw,no_root_squash)"
```

2. In Veeam — add the NFS share as a repository:
   - Navigate to **Backup Infrastructure > Backup Repositories > Add Repository**
   - Select **Network Attached Storage > NFS Share**
   - Hostname: FlashBlade data VIP
   - Path: `/prod-veeam-daily`
   - Set concurrent task limits to match the FlashBlade's available bandwidth

3. Verify the repository is accessible:

```bash
# From the Veeam backup server — test NFS mount
mount -t nfs <fb-data-vip>:/prod-veeam-daily /mnt/veeam-test
df -h /mnt/veeam-test
umount /mnt/veeam-test
```

### Veeam with Pure Storage Plugin (Snapshot Integration)

The Pure Storage Plugin for Veeam enables backup-from-snapshot mode: Veeam triggers a FlashBlade snapshot before reading data, then streams from the snapshot. Production filesystem performance is not impacted during backup windows.

```bash
# Confirm the Pure Storage Plugin is installed and configured in Veeam
# Plugin path on Veeam server: %ProgramFiles%\Veeam\Backup and Replication\Plugins\
# Configuration: Storage Infrastructure > Add Storage > Pure Storage FlashBlade
```

**FlashBlade REST API token for Veeam plugin:**

```bash
# On FlashBlade — create a service account and API token for Veeam
purefb user create --name svc-veeam --role storage_admin
purefb user apitoken create --name svc-veeam
# Output includes the API token — store it securely; it is shown only once
```

**Instant VM Recovery from FlashBlade snapshot:**

When Veeam has integrated FlashBlade snapshots, instant recovery starts VMs directly from the snapshot without waiting for data to be copied. Recovery time is near-zero — the VM boots from the snapshot-backed filesystem, then Veeam storage motions data back to the production datastore in the background.

---

## Commvault Integration

Commvault IntelliSnap integrates with FlashBlade to create array-level snapshots as backup sources.

```bash
# FlashBlade service account for Commvault
purefb user create --name svc-commvault --role storage_admin
purefb user apitoken create --name svc-commvault
```

In Commvault:
- Navigate to **Storage > Array Management > Add Array**
- Select **Pure Storage FlashBlade**
- Enter the FlashBlade management IP and the API token for `svc-commvault`
- Configure IntelliSnap subclient policies to trigger FlashBlade snapshots before streaming

**Best practice:** Use a dedicated FlashBlade filesystem per Commvault retention tier:

```bash
purefb filesystem create --name prod-commvault-daily --size 20T \
    --nfs --nfs-rules "10.0.10.0/24(rw,no_root_squash)"
purefb filesystem create --name prod-commvault-weekly --size 60T \
    --nfs --nfs-rules "10.0.10.0/24(rw,no_root_squash)"
```

---

## SafeMode Snapshot Protection

SafeMode prevents local admins — including `array_admin` accounts — from deleting snapshots or modifying snapshot retention until the retention window expires. Enabling SafeMode requires Pure Support involvement.

**SafeMode behaviours:**
- Snapshot schedules cannot be modified or deleted once locked
- Snapshot retention periods cannot be shortened
- Any attempt to eradicate a SafeMode-protected snapshot returns an error until the retention period expires naturally

```bash
# Verify SafeMode status after enablement
purefb array list --safemode
# Expected: 'safe_mode: enabled' in the output

# Confirm existing snapshot policies are protected
purefb snapshot-rule list
# SafeMode-protected policies display with a lock indicator in the GUI
```

**Enabling SafeMode:** Contact Pure Storage Support. SafeMode cannot be enabled from the array CLI alone — it requires a second-factor confirmation from Pure Support to activate, and Pure Support must also be involved to make any subsequent changes to protected schedules.

---

## Backup Verification Procedure

Run this verification after each backup cycle to confirm recovery points are valid before they are needed in an incident.

| Step | Command / Action | Expected Result |
|---|---|---|
| 1 | `purefb snapshot list --source <fsname>` | Recent snapshot exists with expected timestamp |
| 2 | `purefb snapshot list --space` | Snapshot consumes reasonable space relative to change rate |
| 3 | Clone the latest snapshot to a test filesystem | `purefb snapshot copy` succeeds without errors |
| 4 | Mount the clone on a test host | NFS mount succeeds and directory structure is intact |
| 5 | Verify a representative file from each application tier | File is readable and the content matches expectations |
| 6 | Confirm snapshot policy schedule is running | Policy shows expected last-run time in `purefb snapshot-rule list` |
| 7 | Eradicate the test clone after verification | `purefb filesystem destroy` and `purefb filesystem eradicate` |

Conduct full restore testing — including application startup from restored data — at least quarterly. Snapshot existence alone does not guarantee recovery; the application must be able to start and operate from the restored filesystem.

---

## Common Backup and Restore Issues

| Symptom | Likely Cause | Resolution |
|---|---|---|
| `.snapshot` directory not visible on NFS client | `snapshot-directory-accessible` not enabled on the filesystem | Run `purefb filesystem update --name <fsname> --snapshot-directory-accessible true` |
| Snapshot creation fails with capacity error | Array is at capacity; no space for new snapshot metadata | Eradicate expired snapshots; expand array or reduce snapshot retention |
| Veeam backup job fails with NFS mount error | NFS export policy blocking the Veeam backup server IP | Run `purefb filesystem list --name <fsname>` and verify the NFS rules include the backup server subnet |
| Snapshot restoration overwrote live data unintentionally | `purefb filesystem restore` was run against the wrong filesystem | Restore requires the administrator to explicitly name the target filesystem — verify the name before executing; use clone to a new filesystem for non-destructive recovery |
| Object restore bucket contains stale or partial data | Bucket snapshot was taken mid-write during an active application operation | Object snapshots are crash-consistent; coordinate with the application team to quiesce writes before taking a snapshot for backup purposes if consistency is required |
| SafeMode blocks snapshot deletion during testing | SafeMode is enabled and the retention window has not expired | Expected behaviour — SafeMode-protected snapshots cannot be deleted until retention expires; contact Pure Support for assistance if an emergency deletion is required |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
