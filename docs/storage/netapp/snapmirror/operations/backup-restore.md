---
tags:
  - netapp
  - operations
---
# SnapMirror — Backup & Restore


<div class="kb-summary">
Part of the [SnapMirror Operations](index.md) reference.
</div>
```text
┌─────────────────────────────── NetApp SnapMirror — Backup and Restore ────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     SnapMirror backup: snapshots, replication, and external backup application integration    │   │
│   │        Snapshot schedule: hourly for 24 h, daily for 7 days, weekly for 4 weeks minimum       │   │
│   │            Replication: async or sync to DR site for off-site data protection copy            │   │
│   │       Restore: volume-level or file-level restore from snapshot; test restore quarterly       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Snapshot → replicate to DR → verify → document → test restore                                      │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │            Async            │  │        Periodic sync        │  │         RPO: minutes        │   │
│   │             Sync            │  │           Zero RPO          │  │          Sub-ms lag         │   │
│   │            SM-BC            │  │        Active-active        │  │        Transparent FO       │   │
│   │            Vault            │  │        Long retention       │  │         Backup copy         │   │
│   │            Cloud            │  │         ONTAP → CVO         │  │       Cloud DR/backup       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │       Type       │     Schedule     │     Retention     │     Offsite?     │    Test cycle    │   │
│   │     Snapshot     │   Hourly/daily   │    7/30/90 days   │        No        │     Monthly      │   │
│   │   Replication    │  Policy-driven   │     Per policy    │     Yes (DR)     │    Quarterly     │   │
│   │    Backup app    │ Daily full+incr  │      90+ days     │ Yes (tape/cloud  │    Quarterly     │   │
│   │     Archive      │     Monthly      │      7+ years     │   Yes (object)   │      Annual      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Source ONTAP cluster · destination ONTAP cluster · intercluster LIFs · WAN link          │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    SnapMirror         = ONTAP replication; transfers only changed blocks after initial baseline sync  │
│    Intercluster LIF   = dedicated logical interface for SnapMirror traffic between clusters           │
│    SnapMirror policy  = defines schedule, retention, and transfer type (async/sync/vault)             │
│    Baseline transfer  = first full snapshot transfer establishing the SnapMirror relationship         │
│    Update             = incremental transfer; only sends new or changed blocks since last successfu...│
│    Snapmirror break   = breaks the DR relationship; activates destination volume for read-write       │
│    Resync             = re-establishes a broken SnapMirror relationship from the last common snapshot │
│    SM-BC              = SnapMirror Business Continuity; synchronous zero-RPO active-active SAN volumes│
│    Mediator           = ONTAP Mediator; quorum service for SM-BC running on Linux VM at third site    │
│    SnapVault          = SnapMirror variant for backup retention; destination has independent schedule │
│    MirrorAndVault     = policy combining SnapMirror DR and SnapVault backup retention copies          │
│    Fanout             = single source volume replicating to multiple destination clusters simultane...│
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## How SnapMirror Fits into Backup and Restore

SnapMirror is a replication technology, not a backup application. It maintains a continuously updated copy of source data on a destination cluster. The destination volume retains a configurable number of snapshots that represent point-in-time recovery points. For application-consistent backup orchestration — quiesce, snapshot, SnapMirror update, catalog registration — use [SnapCenter](../../snapcenter/index.md).

The following procedures cover the ONTAP-level operations for DR-oriented restore from a SnapMirror destination, snapshot-level recovery from a vault (XDP) relationship, and SVM-DR-level restore.

---

## Restore from a SnapMirror Destination (DR Failover)

In a DR scenario where the source cluster is unavailable, restore access to data by activating the destination volume.

### Planned Failover (Source Available)

If the source is still accessible, run a final update to minimise RPO before breaking the relationship.

```bash
# Step 1: Final update to reduce RPO gap
snapmirror update -destination-path svm_dr:vol_data
# Wait for the update to complete
snapmirror show -destination-path svm_dr:vol_data -fields transfer-progress,last-transfer-end-timestamp

# Step 2: Quiesce to stop further transfers
snapmirror quiesce -destination-path svm_dr:vol_data

# Step 3: Break the mirror — destination becomes read-write
snapmirror break -destination-path svm_dr:vol_data

# Step 4: Verify the destination volume is now read-write
volume show -vserver svm_dr -volume vol_data -fields state,junction-path

# Step 5: Mount the volume if not already mounted
volume mount -vserver svm_dr -volume vol_data -junction-path /vol_data

# Step 6: Update export policy or CIFS share to allow client access
# (if not pre-configured on the DR SVM)
export-policy rule show -vserver svm_dr -policyname <policy>
```

### Unplanned Failover (Source Down)

```bash
# Source is unreachable — break the relationship to activate the destination
snapmirror break -destination-path svm_dr:vol_data

# Check lag time to understand RPO impact
snapmirror show -destination-path svm_dr:vol_data -fields lag-time
# Lag time = amount of data loss since last successful transfer

# Mount and serve data from the DR volume
volume mount -vserver svm_dr -volume vol_data -junction-path /vol_data

# Update DNS to point the storage hostname to the DR SVM LIF
# (update your DNS zone for the storage hostname)
network interface show -vserver svm_dr -role data
```

---

## Restore from a Snapshot on the Destination Volume (Point-in-Time Recovery)

SnapMirror destinations retain multiple snapshots. If the required data was present at an earlier point in time, restore from a specific snapshot rather than using the most recent state.

### List Available Snapshots on the Destination

```bash
# List all snapshots on the destination volume
snapshot list -vserver svm_dr -volume vol_data

# Show snapshot sizes and creation times
snapshot show -vserver svm_dr -volume vol_data \
    -fields snapshot,size,create-time
```

### Mount a Specific Snapshot for File-Level Recovery

```bash
# Create a FlexClone from a specific snapshot for read access
# (does not affect the destination volume or SnapMirror relationship)
volume clone create \
    -vserver svm_dr \
    -flexclone vol_data_recovery \
    -type RW \
    -parent-volume vol_data \
    -parent-snapshot <snapshot-name>

# Mount the clone
volume mount -vserver svm_dr \
    -volume vol_data_recovery \
    -junction-path /vol_data_recovery

# Copy the required files from the clone mount point to the active volume
# (done via NFS/CIFS client — mount /vol_data_recovery, copy files)

# After recovery, unmount and delete the clone
volume unmount -vserver svm_dr -volume vol_data_recovery
volume delete -vserver svm_dr -volume vol_data_recovery
```

### Revert a Destination Volume to a Specific Snapshot

This is destructive — it discards all data newer than the selected snapshot on the destination. Only use when breaking the mirror and restoring from a specific point-in-time.

```bash
# Break the mirror first
snapmirror break -destination-path svm_dr:vol_data

# Revert the volume to a specific snapshot
snapshot restore -vserver svm_dr -volume vol_data \
    -snapshot <snapshot-name>

# Confirm the volume reflects the correct restore point
snapshot show -vserver svm_dr -volume vol_data
```

---

## Restore from a SnapVault (XDP Vault) Relationship

XDP vault relationships retain long-term backup copies on the destination, with independent retention policies that allow keeping daily, weekly, and monthly snapshots separately from the source. This is the primary mechanism for restoring from a backup copy older than what SnapMirror async retention provides.

```bash
# List all retained snapshots in the vault
snapshot show -vserver svm_vault -volume vol_data_vault \
    -fields snapshot,create-time,size | sort -k2

# For file-level recovery — clone from a specific vault snapshot
volume clone create \
    -vserver svm_vault \
    -flexclone vol_data_clone \
    -type RW \
    -parent-volume vol_data_vault \
    -parent-snapshot <snapshot-name>

volume mount -vserver svm_vault \
    -volume vol_data_clone \
    -junction-path /vol_data_clone

# After copying the required files, clean up the clone
volume unmount -vserver svm_vault -volume vol_data_clone
volume delete -vserver svm_vault -volume vol_data_clone
```

### Restore from Vault to Source (Full Volume Restore)

This procedure restores a full volume from the XDP vault back to the source — for example, after an accidental deletion or corruption on the source.

```bash
# Step 1: Break the existing XDP vault relationship
snapmirror quiesce -destination-path svm_vault:vol_data_vault
snapmirror break -destination-path svm_vault:vol_data_vault

# Step 2: Reverse resync — vault becomes source, original source becomes destination
snapmirror resync \
    -source-path svm_vault:vol_data_vault \
    -destination-path svm_prod:vol_data

# Step 3: Monitor until the reverse sync completes
snapmirror show -destination-path svm_prod:vol_data -fields lag-time,mirror-state

# Step 4: Break the reverse relationship to make the source writable
snapmirror break -destination-path svm_prod:vol_data

# Step 5: Re-establish the original XDP relationship direction
snapmirror resync -destination-path svm_vault:vol_data_vault

# Step 6: Verify normal replication is restored
snapmirror show -destination-path svm_vault:vol_data_vault -fields healthy,lag-time
```

---

## SVM-DR Failover and Failback

SVM-DR replicates the entire SVM — volumes, LIF configuration, NFS exports, CIFS shares, and local users. Activating an SVM-DR relationship brings up the destination SVM as a fully functional replacement.

```bash
# Break the SVM-DR relationship to activate the destination SVM
snapmirror break -destination-path svm_dr:

# Start the destination SVM (starts all volumes and makes the SVM operational)
vserver start -vserver svm_dr

# Verify the SVM is running
vserver show -vserver svm_dr -fields state
# Expected: state: running

# Verify volumes are online and mounted
volume show -vserver svm_dr -fields state,junction-path

# Update DNS to point the SVM hostname to the DR SVM LIF
network interface show -vserver svm_dr -role data
```

### SVM-DR Failback

```bash
# After the primary SVM is recovered, reverse sync from DR back to primary
snapmirror resync \
    -source-path svm_dr: \
    -destination-path svm_prod:

# Wait for sync to complete
snapmirror show -destination-path svm_prod: -fields lag-time,healthy

# Break the reverse relationship
snapmirror break -destination-path svm_prod:

# Re-establish original direction (primary → DR)
snapmirror resync -destination-path svm_dr:

# Verify SVM-DR relationship is healthy
snapmirror show -destination-path svm_dr: -fields healthy,lag-time
```

---

## Post-Restore Validation

```bash
# Confirm the restored volume is accessible
volume show -vserver <svm> -volume <vol> -fields state,junction-path

# Verify application connectivity after restore
# (application-specific — for example, mount NFS path and check files)

# For SQL/Oracle databases — run integrity checks at the application layer
# before re-enabling production workloads

# After restore and validation, confirm SnapMirror protection is re-established
snapmirror show -fields healthy,lag-time
# All relationships should return to healthy: true with lag within RPO
```

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record
