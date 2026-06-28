---
tags:
  - operations
  - pure
---
# FlashBlade — Procedures


<div class="kb-summary">
Procedures reference covering Change Readiness, Maintenance Window, Post-Change Validation, Snapshots.

*Applies to: FlashBlade Purity//FB 4.x*
</div>

![FlashBlade — Procedures — Diagram](../../../../assets/storage-pure-flashblade-operations-procedures-diagram.svg)

> Part of the [FlashBlade Operations](index.md) reference.

---

```d2
direction: right

hub: "FlashBlade\nOperations" {shape: hexagon}
change_readiness: "Change Readiness" {shape: rectangle}
maintenance_window: "Maintenance Window" {shape: rectangle}
postchange_validation: "Post-Change Validation" {shape: rectangle}
snapshots: "Snapshots" {shape: rectangle}
create_a_file_system: "Create a File System" {shape: rectangle}
create_an_object_store_bucket: "Create an Object Store Bucket" {shape: rectangle}

hub -> change_readiness
hub -> maintenance_window
hub -> postchange_validation
hub -> snapshots
hub -> create_a_file_system
hub -> create_an_object_store_bucket
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Change Readiness

- [ ] No active blade rebuilds or hardware failures — `purefb blade list` and `purefb hardware list` are clean
- [ ] ActiveDR replication is current — lag is within RPO; document baseline lag before the change
- [ ] NFS and SMB clients are informed of the potential brief reconnection event during Purity upgrades
- [ ] S3 clients and applications are notified if the change could cause a brief service interruption
- [ ] Filesystem capacity headroom is sufficient — no filesystems above 70% provisioned limit during the window
- [ ] Pure1 upgrade readiness report reviewed (for Purity//FB upgrades): no blockers flagged
- [ ] Snapshot schedule expiry policy is functioning — no runaway snapshot growth that could fill capacity during the window

| Item | Status | Notes |
|---|---|---|
| No active blade rebuilds | | |
| ActiveDR replication current | | |
| NFS/SMB client impact assessed | | |
| Filesystem capacity headroom sufficient | | |
| Pure1 upgrade readiness checked (if upgrading) | | |

## Maintenance Window

1. Notify NFS, SMB, and S3 clients of the maintenance window — Purity//FB upgrades are non-disruptive but protocol sessions may briefly re-establish
2. For blade maintenance: use `purefb blade maintenance` to put the blade in maintenance mode before physical intervention — data rebalances automatically
3. For Purity//FB upgrade: confirm `purefb blade list` shows all blades `healthy` and no alerts are open before starting
4. Download the Purity//FB upgrade image from the Pure Support portal and stage it on the array
5. Run the pre-upgrade validation from the GUI or CLI to confirm no blockers
6. Execute the upgrade during the window; monitor progress from the Purity//FB GUI or `purefb array list`
7. For ActiveDR: pause replication links if required during the change with `purefb replication link update --paused true`; resume with `--paused false` after the change

## Post-Change Validation

- [ ] `purefb alert list` — no unresolved alerts
- [ ] `purefb blade list` — all blades `healthy`; no blades in maintenance or failed state
- [ ] `purefb hardware list` — all hardware components healthy
- [ ] `purefb filesystem list` — all filesystems accessible and below provisioned limit
- [ ] Test NFS mount from a representative client: `mount -t nfs <fb-data-vip>:/<filesystem> /mnt/test`
- [ ] Test S3 API response: confirm bucket listing or object operation succeeds from an S3 client or `aws s3 ls`
- [ ] `purefb replication list` — all ActiveDR links are `active` and lag is recovering toward RPO
- [ ] Pure1 shows the new Purity//FB version and no new hardware alerts (if this was an upgrade)

---

## Snapshots

FlashBlade supports snapshots at the file system level. Snapshots are space-efficient and near-instantaneous.

### List Snapshots

![List Snapshots](../../../../assets/flashblade-proc-list-snapshots.svg)

```bash
purefb fs-snapshot list
purefb fs-snapshot list --filter "source='<fs_name>'"
```

### Create a Snapshot

![Create a Snapshot](../../../../assets/flashblade-proc-create-a-snapshot.svg)

```bash
purefb fs-snapshot create --source <fs_name> --suffix <snap_name>
```

Example:
```bash
purefb fs-snapshot create --source prod-nfs --suffix daily-2026-05-06
```

### Accessing Snapshot Data

![Accessing Snapshot Data](../../../../assets/flashblade-proc-accessing-snapshot-data.svg)

Snapshots are accessible via the NFS `.snapshot` directory (if enabled):

```bash
ls /mnt/<fs_mount>/.snapshot/
# Lists available snapshots by suffix
```

Users can browse and copy files directly from the `.snapshot` path without administrator involvement.

### Restore a File System from Snapshot

![Restore a File System from Snapshot](../../../../assets/flashblade-proc-restore-a-file-system-from-snapshot.svg)

```bash
# Overwrite the live file system with snapshot content
purefb fs-snapshot restore <fs_name>.<snap_name> --overwrite-fs
```

> This replaces all current data on the file system — ensure this is intentional.

### Copy a Snapshot to a New File System

![Copy a Snapshot to a New File System](../../../../assets/flashblade-proc-copy-a-snapshot-to-a-new-file-system.svg)

```bash
purefb fs-snapshot copy <fs_name>.<snap_name> --name <new_fs_name>
```

Creates a new independent file system from the snapshot without affecting the original.

### Delete a Snapshot

![Delete a Snapshot](../../../../assets/flashblade-proc-delete-a-snapshot.svg)

```bash
# Destroy (recoverable for 24 hours)
purefb fs-snapshot destroy <fs_name>.<snap_name>

# Eradicate permanently
purefb fs-snapshot eradicate <fs_name>.<snap_name>
```

### Snapshot Policy (Automated Scheduling)

![Snapshot Policy (Automated Scheduling)](../../../../assets/flashblade-proc-snapshot-policy-automated-scheduling.svg)

FlashBlade supports policy-based snapshots via the GUI:
1. Navigate to **Protection → Snapshot Policies**
2. Create a policy with frequency and retention settings
3. Assign the policy to file systems

```bash
# View policies via CLI
purefb policies list
```

### Common Issues

![Common Issues](../../../../assets/flashblade-proc-common-issues.svg)

| Issue | Check | Action |
|---|---|---|
| `.snapshot` not visible | Snapshots enabled on FS | `purefb fs update <name> --snapshot-enabled true` |
| Snapshot create fails | Capacity | Check array free space |
| Restore failed | File system in use | Unmount/quiesce clients first |
| Snapshots not auto-created | Policy attached? | Verify snapshot policy assignment |

## Create a File System

FlashBlade file systems are the primary NFS and SMB storage containers. Create the file system, configure an export policy, and mount it from clients.

```bash
# Step 1 — Create the file system
pureds create --name <name> --size <size>T

# Step 2 — Create an export policy for NFS access
pureexportpolicy create --name <policy-name>

# Step 3 — Add an NFS rule to the export policy
# Allow a specific subnet with read/write access
pureexportpolicy rule add --policy <policy-name> \
    --client <client-cidr> \
    --access rw \
    --root-squash false

# Step 4 — Apply the export policy to the file system
pureds update --name <name> --nfs-export-policy <policy-name>

# Step 5 — Mount from client
mount -t nfs <fb-data-vip>:/<name> /mnt/<name>
```

Verify the mount is accessible and confirm read/write permissions from the client before closing the change.

## Create an Object Store Bucket

FlashBlade S3 buckets provide object storage accessible via the S3 API. Buckets are scoped to an account and require an access policy for external clients.

```bash
# Step 1 — Create the S3 bucket under an existing account
purebucket create \
    --name <bucket-name> \
    --account <account-name>

# Step 2 — Configure an access policy (via GUI or API)
# Unisphere/Purity//FB GUI: Object Store → Buckets → select bucket → Access Policies
# Add bucket policy granting s3:GetObject, s3:PutObject, s3:ListBucket as needed

# Step 3 — Test bucket access from an S3 client
aws s3 ls s3://<bucket-name> \
    --endpoint-url https://<fb-s3-vip>
```

Confirm the bucket listing returns without error. For application integration, create an object store user and generate access keys: **Object Store → Users → Create User → Generate Access Key**.

## Create a Snapshot Schedule

Automated snapshot schedules protect file systems on a recurring basis. Create the schedule, then attach it to the target file system as a protection policy.

```bash
# Step 1 — Create the snapshot schedule
puresnapshot schedule create \
    --name <sched> \
    --every 1h \
    --keep-for 24h

# Step 2 — Attach the schedule to a file system as a protection policy
pureds create-protection \
    --name <name> \
    --schedule <sched>

# Verify snapshots are being created after the first interval
purefb fs-snapshot list --filter "source='<name>'"
```

Adjust `--every` and `--keep-for` values to match the RPO requirement. Longer retention periods consume more capacity — monitor array free space after enabling the schedule.

## Configure Replication to a Remote FlashBlade

FlashBlade-to-FlashBlade replication (ActiveDR) protects NFS file systems by continuously replicating to a remote FlashBlade. Configure the remote target first, then create the file copy job.

```bash
# Step 1 — Add the remote FlashBlade as a replication target
pureremote create \
    --name <target-fb> \
    --address <ip>

# Step 2 — Create the file copy replication job
purefilecopy create \
    --source <fs> \
    --target <target-fb>:<fs>

# Step 3 — Monitor replication progress
purefilecopy list
# Check: status, lag, bytes-transferred
```

Confirm the replication lag is within the RPO requirement. For Active-Active configurations where both sites serve I/O, use ActiveDR failover procedures rather than a simple file copy.

## Expand a File System

File system expansion on FlashBlade is non-disruptive and online. NFS and SMB clients see the new capacity immediately without remounting.

```bash
# Expand the file system to a larger size
pureds modify --name <name> --size <new-size>T

# Verify the new provisioned size
pureds list --name <name>
```

No downtime is required. NFS clients see the new capacity immediately. Confirm the updated size is reflected in the `df -h` output from a mounted client. If the file system has a snapshot policy, verify that snapshot creation continues normally after the expansion.

---

### Create a File System

![Create a File System](../../../../assets/flashblade-proc-create-a-file-system.svg)

Create a new NFS or SMB file system on FlashBlade with a provisioned size limit.

```bash
# Create a file system with NFS enabled and SMB disabled
purefb fs create <name> --size 10T --nfs-enabled true --smb-enabled false

# Verify the file system was created
purefb fs list <name>
```

GUI path: **Storage → File Systems → Create**. Set a hard limit (enforced) or soft limit (advisory with grace period) at creation time.

### Configure an NFS Export

![Configure an NFS Export](../../../../assets/flashblade-proc-configure-an-nfs-export.svg)

Add export rules to an existing file system so NFS clients can mount it.

```bash
# Apply an export policy to the file system
purefb fs update <name> --nfs-export-policy <policy-name>

# Add a rule to the export policy granting read-write access to a subnet
purefb nfs-export-policy rule create <policy-name> \
    --client 10.0.0.0/24 \
    --access read-write \
    --security sys

# Verify the policy and rules
purefb nfs-export-policy list
purefb nfs-export-policy rule list <policy-name>
```

Test from a client: `mount -t nfs <fb-data-vip>:/<name> /mnt/test` and confirm read-write access.

### Configure an SMB Share

![Configure an SMB Share](../../../../assets/flashblade-proc-configure-an-smb-share.svg)

Enable SMB on a file system and create a named share for Windows clients.

```bash
# Enable SMB on the file system
purefb fs update <name> --smb-enabled true

# Create an SMB share backed by the file system
purefb smb-share create <share-name> --file-system <fs-name>

# Update share-level ACLs (alternative: use Windows MMC)
purefb smb-share acl-update <share-name> --permission full-control --user DOMAIN\\AdminGroup
```

Verify from a Windows client: `net use \\<fb-mgmt>\<share>` — confirm the share maps successfully and files are accessible.

### Create an Object Store Bucket

![Create an Object Store Bucket](../../../../assets/flashblade-proc-create-an-object-store-bucket.svg)

Create an S3 bucket scoped to an object store account and verify access with the S3 API.

```bash
# Create the bucket under an existing object store account
purefb bucket create <bucket-name> --account <account-name>

# Create an access key for the account (GUI: Object Store → Users → Generate Access Key)
# Then test bucket access using the generated credentials
aws s3 ls s3://<bucket-name> \
    --endpoint-url https://<fb-s3-vip>
```

Confirm the listing returns without error. For application integration, generate access keys via **Object Store → Users → Create User → Generate Access Key** in the GUI.

### Configure Array-to-Array Replication

![Configure Array-to-Array Replication](../../../../assets/flashblade-proc-configure-array-to-array-replication.svg)

Set up asynchronous file system replication between two FlashBlade arrays for DR.

```bash
# Step 1 — Connect the remote FlashBlade array
purefb array-connection create \
    --management-address <remote-fb-mgmt-ip> \
    --replication-addresses <remote-repl-ip>

# Step 2 — Create an outbound replica link for the file system
purefb fs-replica-link create \
    --local-fs <fs-name> \
    --remote-fs <remote-fs-name> \
    --remote-array <remote-array-name> \
    --direction outbound

# Monitor replication status and lag
purefb fs-replica-link list
```

Confirm the replica link shows as active and lag is within the RPO target. For failover, use ActiveDR procedures to promote the remote file system.

### Expand a File System

![Expand a File System](../../../../assets/flashblade-proc-expand-a-file-system.svg)

Increase the provisioned size limit of an existing file system. Expansion is non-disruptive.

```bash
# Expand the file system to the new size
purefb fs update <name> --size 20T

# Verify the updated provisioned size
purefb fs list <name>
```

NFS and SMB clients see the new capacity immediately without remounting. Confirm with `df -h` from a mounted client. Shrinking a file system is not supported — plan capacity requirements carefully before provisioning.

### Manage Quotas (User and Group)

![Manage Quotas (User and Group)](../../../../assets/flashblade-proc-manage-quotas-user-and-group.svg)

Set per-user or per-group usage limits within a file system to prevent runaway consumption.

```bash
# Set a per-user quota limit (by UID)
purefb quota-user set \
    --file-system <name> \
    --uid 1001 \
    --quota-limit 500G

# Set a per-group quota limit (by GID)
purefb quota-group set \
    --file-system <name> \
    --gid 2000 \
    --quota-limit 2T

# List current user quotas for a file system
purefb quota-user list --file-system <name>

# List current group quotas
purefb quota-group list --file-system <name>
```

Quota limits are enforced as hard limits. Users or groups that reach their limit receive a write error. Monitor quota usage regularly to identify accounts approaching their limit before they are blocked.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [FlashBlade — Health Checks](health-checks/)
- [FlashBlade — CLI Reference](cli-reference/)
- [FlashBlade — Common Issues](../troubleshooting/common-issues/)
