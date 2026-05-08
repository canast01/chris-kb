# PowerScale — Procedures

## Change Readiness

Verify these items before performing any change on a PowerScale cluster — node additions, OneFS upgrades, SyncIQ policy changes, or quota modifications.

- [ ] `isi status` is clean — no SMARTFAIL nodes, no DOWN nodes, no unacknowledged drive faults
- [ ] SyncIQ policies are in a successful or idle state — `isi sync policies list` shows no policies in ERROR; pause scheduled policies during the change window if needed
- [ ] Quota headroom confirmed — `isi quota quotas list` shows no directories at or above hard threshold before the change
- [ ] No active cluster jobs that would conflict: `isi job list` — Restripe, MultiScan, and FSAnalyze should not be running during major changes
- [ ] Snapshot reserve space is within limits — `isi snapshot list` confirms no unexpected snapshot accumulation consuming pool headroom
- [ ] Confirm OneFS version is within the supported upgrade path if this is a software change (Dell upgrade compatibility matrix)
- [ ] Inform NFS and SMB client teams of the change window; confirm application quiesce plan if node-level work is planned
- [ ] If removing or SmartFailing a node, confirm the cluster has sufficient capacity to absorb the restripe

| Item | Status | Notes |
|---|---|---|
| isi status clean (no SMARTFAIL / DOWN) | | |
| SyncIQ policies idle or paused | | |
| No active conflicting cluster jobs | | |
| Quota headroom confirmed | | |
| Snapshot reserve within limits | | |

## Maintenance Window

```mermaid
flowchart TD
    A([Start Maintenance]) --> B["Notify NFS/SMB client teams"]
    B --> C{"isi status clean?"}
    C -->|No| D["Resolve faults first"]
    D --> C
    C -->|Yes| E["Pause SyncIQ policies"]
    E --> F["Check capacity headroom\n< 80% in isi storagepool"]
    F --> G{"Node SmartFail?"}
    G -->|Yes| H["isi devices node smartfail LNN\nMonitor Restripe job"]
    G -->|No| I["Perform change per runbook"]
    H --> I
    I --> J["isi status — all nodes ONLINE?"]
    J -->|No| K["Investigate & resolve"]
    K --> J
    J -->|Yes| L["Re-enable SyncIQ policies\nTrigger manual run → confirm SUCCESS"]
    L --> M([Close Window])
```

Steps for planned maintenance on a PowerScale cluster — node SmartFail, OneFS upgrade, or network reconfiguration.

1. Notify NFS and SMB client teams; confirm the maintenance window and coordinate any application quiesce if node-level work is planned
2. Confirm `isi status` is clean — no SMARTFAIL, no DOWN nodes, no unresolved drive faults before starting
3. Pause all SyncIQ scheduled policies to prevent replication from running during the change: `isi sync policies modify <name> --enabled false` for each active policy
4. If adding or removing a node, confirm the cluster has sufficient capacity headroom in `isi storagepool list` to absorb the restripe without crossing 80% used
5. To SmartFail a node for planned maintenance: `isi devices node smartfail <node-lnn>` — monitor Restripe job progress in `isi job list` until complete before physically servicing the node
6. Perform the change per the approved runbook
7. After the change, run `isi status` to confirm all nodes are back ONLINE and drive health is clean
8. Re-enable SyncIQ policies: `isi sync policies modify <name> --enabled true`; trigger a manual run with `isi sync policies run <name>` and confirm SUCCESS before closing the window

## Post-Change Validation

Run these checks after any change to confirm the cluster is healthy and client services have resumed normally.

- [ ] `isi status` — all nodes ONLINE, no SMARTFAIL, no DOWN, no drive faults introduced by the change
- [ ] `isi storagepool list` — all pools and tiers below 80% used; Restripe job completed if a node was added or removed
- [ ] `isi sync policies list` — all SyncIQ policies re-enabled and showing a successful run after the change
- [ ] `isi event list --limit 20` — no new CRITICAL events introduced by the change
- [ ] NFS and SMB client connectivity verified from at least one representative client per access zone
- [ ] Snapshot schedules running as expected: `isi snapshot schedules list`
- [ ] Quota thresholds intact: `isi quota quotas list` shows no unexpected threshold exceedances introduced by the change
- [ ] CloudIQ or InsightIQ shows no new performance anomalies in the post-change window

## NFS Export Management

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

### Export Client Access Levels

| Client Type | Permission |
|---|---|
| `--clients` | Read-only access |
| `--read-write-clients` | Read/write access |
| `--root-clients` | Root access (uid 0 not squashed) |

### NFS Zones (Access Zones)

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

### Troubleshooting NFS

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

## SMB Share Management

```bash
# List all SMB shares
isi smb shares list
isi smb shares list -v

# View a specific share
isi smb shares view <share_name>

# Create a share
isi smb shares create <share_name> /ifs/data/project1 \
    --description "Project 1 share" \
    --browsable yes \
    --allow-execute-always yes

# Modify a share
isi smb shares modify <share_name> --description "Updated description"
isi smb shares modify <share_name> --add-permissions 'user:<username>:allow:full'

# Delete a share
isi smb shares delete <share_name>
```

### SMB Permissions

```bash
# View share permissions (ACL)
isi smb shares view <share_name> | grep -A 20 "Permission"

# Add a user with read permission
isi smb shares modify <share_name> \
    --add-permissions 'user:CORP\jsmith:allow:read'

# Add a group with change permission
isi smb shares modify <share_name> \
    --add-permissions 'group:CORP\fileusers:allow:change'

# Set full control for an admin group
isi smb shares modify <share_name> \
    --add-permissions 'group:CORP\storeadmins:allow:full'

# Remove a permission entry
isi smb shares modify <share_name> \
    --remove-permissions 'user:CORP\jsmith:allow:read'
```

### SMB Sessions and Open Files

```bash
# Active SMB sessions
isi smb sessions list

# Open files per session
isi smb openfiles list

# Disconnect a specific session
isi smb sessions delete <session_id>
```

### Troubleshooting SMB

```bash
# Check SMB protocol stats
isi statistics protocol list --protocol smb2
isi statistics protocol list --protocol smb3

# Check for SMB errors in events
isi event events list | grep -i smb

# Verify AD authentication is working
isi auth status | grep -i "Active Directory\|joined"
isi auth ads list

# Check group memberships resolve correctly
isi auth users view <username>
isi auth groups view <groupname>

# Test access zone authentication
isi zone zones view <zone_name>
```

## Snapshot Management

```bash
# Create a snapshot of a directory
isi snapshot snapshots create /ifs/data/project1 --name project1-$(date +%Y%m%d)

# List all snapshots
isi snapshot snapshots list
isi snapshot snapshots list -v

# View details of a snapshot
isi snapshot snapshots view <snap_id>

# Delete a snapshot
isi snapshot snapshots delete <snap_id>

# Delete by name
isi snapshot snapshots delete --name project1-20260101
```

### Snapshot Schedules

```bash
# List all schedules
isi snapshot schedules list

# Create a daily schedule retaining 14 snapshots
isi snapshot schedules create daily-project1 \
    /ifs/data/project1 \
    --schedule "every 1 days at 00:00" \
    --retention 2W \
    --alias latest-project1

# Modify a schedule
isi snapshot schedules modify <schedule_name> --retention 1M

# Delete a schedule (does not delete existing snapshots)
isi snapshot schedules delete <schedule_name>
```

### Recovering Files from a Snapshot

```bash
# Copy a specific file from snapshot back to live filesystem
cp -p /ifs/data/project1/.snapshot/project1-20260101/report.xlsx \
      /ifs/data/project1/report.xlsx

# Restore an entire directory
rsync -av /ifs/data/project1/.snapshot/project1-20260101/ \
          /ifs/data/project1/

# Restore via SnapshotIQ revert (rolls back entire path to snapshot state)
isi snapshot snapshots modify <snap_id> --set-expiration never   # Protect before reverting
isi snapshot snapshots revert <snap_id>
# WARNING: revert is destructive — all data written after the snapshot is lost
```
