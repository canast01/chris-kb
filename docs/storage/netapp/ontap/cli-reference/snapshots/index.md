# Snapshots

> Part of the [NetApp ONTAP CLI Reference](../).

ONTAP snapshots are read-only point-in-time copies of a volume stored within the same volume's snapshot reserve.
## List Snapshots

```bash
# All snapshots across all volumes
volume snapshot show

# Snapshots for a specific volume
volume snapshot show -vserver <svm> -volume <vol>

# Snapshot detail — size, creation time, busy state
volume snapshot show -vserver <svm> -volume <vol> -fields size, create-time, busy
```

## Create a Snapshot

```bash
# Manual snapshot
volume snapshot create -vserver <svm> -volume <vol> -snapshot <snap_name>

# Example: pre-patch snapshot
volume snapshot create -vserver prod-svm -volume db01_vol -snapshot pre-patch-20260506
```

## Delete Snapshots

```bash
# Delete a specific snapshot
volume snapshot delete -vserver <svm> -volume <vol> -snapshot <snap_name>

# Delete all snapshots on a volume (use with care)
volume snapshot delete -vserver <svm> -volume <vol> -snapshot * -force true
```

## Rename a Snapshot

```bash
volume snapshot rename -vserver <svm> -volume <vol> -snapshot <old_name> -new-name <new_name>
```

## Restore from Snapshot

```bash
# Revert a volume to a snapshot (disruptive — volume must be offline or quiesced)
volume snapshot restore -vserver <svm> -volume <vol> -snapshot <snap_name>

# For SnapRestore license — online restore (non-disruptive for non-DR scenarios)
volume snapshot restore -vserver <svm> -volume <vol> -snapshot <snap_name> -online true
```

## Snapshot Policies

Policies automate snapshot creation on a schedule:

```bash
# List snapshot policies
volume snapshot policy show

# Create a policy
volume snapshot policy create -policy <policy_name> -enabled true

# Add a schedule (hourly, daily, weekly)
volume snapshot policy add-schedule \
    -policy <policy_name> \
    -schedule hourly \
    -count 24

# Assign policy to a volume
volume modify -vserver <svm> -volume <vol> -snapshot-policy <policy_name>
```

## Snapshot Reserve

Snapshots consume space from the snapshot reserve. When the reserve is full, snapshots consume user data space:

```bash
# View snapshot reserve for a volume
volume show -vserver <svm> -volume <vol> -fields snapshot-percent

# Set snapshot reserve to 15%
volume modify -vserver <svm> -volume <vol> -percent-snapshot-space 15
```

## Accessing Snapshots from the Client

ONTAP exposes snapshots via the `.snapshot` directory (NFS) or `~snapshot` share (CIFS):

```bash
# From NFS client
ls /mnt/data/.snapshot/

# From Windows client (if enabled)
# \\server\share\~snapshot\
```
