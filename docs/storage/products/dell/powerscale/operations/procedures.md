---
tags:
  - dell
  - operations
description: "PowerScale (Isilon) procedures — NFS export and SMB share management, snapshot operations, quota management, SmartConnect zone configuration, replication..."
---
# PowerScale — Procedures

<div class="kb-summary">
PowerScale (Isilon) procedures — NFS export and SMB share management, snapshot operations, quota management, SmartConnect zone configuration, replication, node maintenance, and change readiness.

*Applies to: PowerScale (Isilon) 9.x*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

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

```d2
direction: right

A: "Start Maintenance" {shape: rectangle}
B: "Notify NFS/SMB client teams" {shape: rectangle}
C: "isi status clean?" {shape: rectangle}
D: "Resolve faults first" {shape: rectangle}
E: "Pause SyncIQ policies" {shape: rectangle}
F: "Check capacity headroom\n< 80% in isi storagepool" {shape: rectangle}
G: "Node SmartFail?" {shape: rectangle}
H: "isi devices node smartfail LNN\nMonitor Restripe job" {shape: rectangle}
I: "Perform change per runbook" {shape: rectangle}
J: "isi status — all nodes ONLINE?" {shape: rectangle}
K: "K" {shape: rectangle}
L: "Re-enable SyncIQ policies\nTrigger manual run → confirm SUCCESS" {shape: rectangle}
M: "Close Window" {shape: rectangle}

A -> B
B -> C
C -> D
D -> C
C -> E
E -> F
F -> G
G -> H
G -> I
H -> I
I -> J
K -> J
J -> L
L -> M
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


```text title="Expected output"
# isi nfs exports list
Id  Path                    Description
1   /ifs/data/myshare       Application data share
2   /ifs/backup/weekly      Weekly backup export
3   /ifs/home/users         User home directories
4   /ifs/archive/2024       Archive storage
5   /ifs/shared/projects    Project collaboration

# isi nfs exports list -v
Id  Path                    Clients              Read-Write Clients   Root Clients        Description
1   /ifs/data/myshare       10.0.0.0/24          10.0.0.0/24          10.0.1.5            Application data share
2   /ifs/backup/weekly      10.0.0.0/24,10.1.0.0/24  10.0.0.0/24      10.0.1.10           Weekly backup export
3   /ifs/home/users         10.0.0.0/24          10.0.0.0/24          10.0.1.5,10.0.1.6   User home directories

# isi nfs exports view 1
Id:                    1
Path:                  /ifs/data/myshare
Description:           Application data share
Clients:               10.0.0.0/24
Read-Write Clients:    10.0.0.0/24
Root Clients:          10.0.1.5
All Dirs:              Yes
Setattr Asynchronous:  Yes

# isi nfs exports create /ifs/data/myshare --clients 10.0.0.0/24 --read-write-clients 10.0.0.0/24 --root-clients 10.0.1.5 --description "Application data share"
Export created successfully with ID: 6

# isi nfs exports modify 6 --addread-write-clients 10.0.2.0/24
Export 6 modified successfully

# isi nfs exports modify 6 --description "Updated description"
Export 6 modified successfully

# isi nfs exports check
Validating all NFS exports...
Export 1: OK
Export 2: OK
Export 3: OK
Export 4: OK
Export 5: OK
Export 6: OK
All exports validated successfully. No errors found.
```

!!! warning "Common errors"
    **`Error: Export path /ifs/data/myshare does not exist`** — Verify the path exists on the cluster with `isi fs ls /ifs/data/myshare` and create it if needed.
    **`Error: Invalid client specification '10.0.0.0/33'`** — Use a valid CIDR notation with subnet mask between /1 and /32, or specify individual IP addresses.
    **`Error: Export <export_id> is currently mounted by 5 clients`** — Unmount all active NFS clients before deleting the export, or use `--force` flag if available.
### Export Client Access Levels

![Export Client Access Levels](../../../../../assets/powerscale-proc-export-client-access-levels.svg)

| Client Type | Permission |
|---|---|
| `--clients` | Read-only access |
| `--read-write-clients` | Read/write access |
| `--root-clients` | Root access (uid 0 not squashed) |

### NFS Zones (Access Zones)

![NFS Zones (Access Zones)](../../../../../assets/powerscale-proc-nfs-zones-access-zones.svg)

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


```text title="Expected output"
Name                    Path                    AccessZone
----                    ----                    ----------
System                  /ifs                    System
Zone1                   /ifs/zone1              Zone1
Zone2                   /ifs/zone2              Zone2

Export ID: 3
Path: /ifs/zone1/data
Access Zone: Zone1
Read-Write Clients: 10.1.0.0/24
Read-Only Clients: (none)

Export ID  Path              Access Zone  Read-Write Clients
-------    ----              -----------  ------------------
3          /ifs/zone1/data   Zone1        10.1.0.0/24
```

!!! warning "Common errors"
    **`Error: Invalid access zone 'Zone1'`** — Verify the zone name exists by running `isi zones list` and use the exact name shown in the output.
    **`Error: Path /ifs/zone1/data does not exist`** — Create the directory first with `mkdir -p /ifs/zone1/data` before exporting it.
### Troubleshooting NFS

![Troubleshooting NFS](../../../../../assets/powerscale-proc-troubleshooting-nfs.svg)

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


```text title="Expected output"
Export list for 192.168.1.50:
/ifs/data/share                    192.168.0.0/16
/ifs/data/archive                  192.168.0.0/16

mount.nfs: mounting 192.168.1.50:/ifs/data/share on /mnt/test
[12847.234521] NFS: nfs mount opts='vers=4.1,rsize=1048576,wsize=1048576,hard,proto=tcp'
[12847.456789] NFS: Server 192.168.1.50 replied too late with 0x0
[12847.678901] NFS: Referral server unavailable
[12848.123456] NFS: state manager: server 192.168.1.50 not responding, timed out
[12848.456789] NFS: state manager: server 192.168.1.50 still not responding, timed out

Protocol: nfs3
  Ops/sec: 1247.3
  Bytes read/sec: 52428800
  Bytes written/sec: 31457280
  Avg latency (ms): 2.14

Protocol: nfs4
  Ops/sec: 3891.2
  Bytes read/sec: 104857600
  Bytes written/sec: 67108864
  Avg latency (ms): 1.87

ID: EVT-2024-001847 | Severity: Warning | Protocol: NFS | Message: NFS client 192.168.0.42 exceeded max open files
ID: EVT-2024-001823 | Severity: Info | Protocol: NFS | Message: NFS export /ifs/data/share accessed by new client 192.168.0.105

Quota ID: 1024 | Path: /ifs/data/share | Usage: 847.3 GB | Limit: 1.0 TB | Status: OK

total 48
drwxr-xr-x  8 root  wheel   4096 Jan 15 14:32 .
drwxr-xr-x 12 root  wheel   4096 Jan 10 09:18 ..
-rw-r--r--  1 admin admin   2048 Jan 15 14:15 config.xml
drwxrwxr-x  3 admin admin   4096 Jan 15 13:47 backups
```

!!! warning "Common errors"
    **`mount.nfs: access denied by server while mounting 192.168.1.50:/ifs/data/share`** — Verify the client IP is in the NFS export allow list with `isi nfs exports list` and add it if missing.
    **`showmount: RPC: Unable to receive; errno = No route to host`** — Confirm network connectivity to the PowerScale cluster IP and that NFS service is running with `isi services nfs status`.
    **`ls: cannot open directory '/ifs/data/share': Permission denied`** — Check file permissions on the cluster with `isi nfs exports view /ifs/data/share` and verify the connecting user has appropriate access rights.
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


```text title="Expected output"
# isi smb shares list
Name                    Path                          Description
project1                /ifs/data/project1            Project 1 share
backups                 /ifs/backups                  Weekly backups
archive                 /ifs/archive                  Archive storage
shared_docs             /ifs/shared/documents         Shared documents

# isi smb shares list -v
Name: project1
Path: /ifs/data/project1
Description: Project 1 share
Browsable: yes
Allow Execute Always: yes
Created: 2024-01-15T09:23:45Z
Modified: 2024-01-20T14:12:10Z

# isi smb shares view project1
Name: project1
Path: /ifs/data/project1
Description: Project 1 share
Browsable: yes
Allow Execute Always: yes
Permissions: Everyone:allow:read, DOMAIN\project_team:allow:full

# isi smb shares create project1 /ifs/data/project1 --description "Project 1 share" --browsable yes --allow-execute-always yes
Created SMB share 'project1'

# isi smb shares modify project1 --description "Updated description"
Modified SMB share 'project1'

# isi smb shares modify project1 --add-permissions 'user:jsmith:allow:full'
Modified SMB share 'project1'

# isi smb shares delete project1
Deleted SMB share 'project1'
```

!!! warning "Common errors"
    **`Error: Share 'project1' already exists`** — Use `isi smb shares modify` instead of create, or choose a different share name.
    **`Error: Path '/ifs/data/project1' does not exist`** — Create the directory first with `mkdir -p /ifs/data/project1` before creating the share.
    **`Error: Permission denied`** — Run the command with appropriate cluster admin privileges or use `sudo isi` if configured.
### SMB Permissions

![SMB Permissions](../../../../../assets/powerscale-proc-smb-permissions.svg)

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


```text title="Expected output"
Permission
    user:CORP\jsmith:allow:read
    group:CORP\fileusers:allow:change
    group:CORP\storeadmins:allow:full
    user:CORP\mchen:allow:read
    group:CORP\domain_users:allow:read

Share modified successfully.
Share modified successfully.
Share modified successfully.
Share modified successfully.
```

!!! warning "Common errors"
    **`Error: Unable to resolve user 'CORP\jsmith': User not found`** — Verify the username exists in Active Directory and use the correct domain\username format with proper escaping.
    **`Error: Permission entry already exists for user:CORP\jsmith:allow:read`** — Remove the duplicate entry first using `--remove-permissions` before re-adding with different permissions.
    **`Error: Access denied: Insufficient privileges to modify share permissions`** — Run the command as root or a user with administrative privileges on the PowerScale cluster.
### SMB Sessions and Open Files

![SMB Sessions and Open Files](../../../../../assets/powerscale-proc-smb-sessions-and-open-files.svg)

```bash
# Active SMB sessions
isi smb sessions list

# Open files per session
isi smb openfiles list

# Disconnect a specific session
isi smb sessions delete <session_id>
```


```text title="Expected output"
Session ID                           User              Client IP        Connected Time
0x00000001-0000-0000-0000-000000000001 CORP\jsmith       192.168.1.45     2024-01-15 09:23:14
0x00000002-0000-0000-0000-000000000002 CORP\mchen        192.168.1.67     2024-01-15 10:45:22
0x00000003-0000-0000-0000-000000000003 CORP\agarcia      192.168.50.12    2024-01-15 11:02:08
0x00000004-0000-0000-0000-000000000004 CORP\dwalker      192.168.1.89     2024-01-15 13:15:41

File ID    Session ID                           Path                          User
1024       0x00000001-0000-0000-0000-000000000001 /ifs/data/reports/Q4_2024.xlsx CORP\jsmith
1025       0x00000002-0000-0000-0000-000000000002 /ifs/data/projects/budget.docx CORP\mchen
1026       0x00000003-0000-0000-0000-000000000003 /ifs/archive/logs/app.log     CORP\agarcia
1027       0x00000001-0000-0000-0000-000000000001 /ifs/data/shared/config.ini   CORP\jsmith

Session 0x00000002-0000-0000-0000-000000000002 deleted successfully.
```

!!! warning "Common errors"
    **`Error: Invalid session ID format`** — Ensure the session ID is enclosed in quotes and matches the exact format shown in the sessions list output.
    **`Error: Session not found or already disconnected`** — Verify the session ID is still active by running `isi smb sessions list` again before attempting deletion.
### Troubleshooting SMB

![Troubleshooting SMB](../../../../../assets/powerscale-proc-troubleshooting-smb.svg)

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


```text title="Expected output"
Protocol: smb2
  Ops/sec: 1247.3
  Read ops/sec: 342.1
  Write ops/sec: 156.8
  Latency (ms): 4.2
Protocol: smb3
  Ops/sec: 3891.5
  Read ops/sec: 1205.3
  Write ops/sec: 892.4
  Latency (ms): 2.8

Event ID 12847 | 2024-01-15T09:23:41Z | SMB: Authentication failure for user CORP\jsmith
Event ID 12851 | 2024-01-15T09:45:12Z | SMB: Session timeout on share \\PSCALE-01\data

Active Directory: joined
  Domain: corp.example.com
  Forest: corp.example.com
  Status: Online

ADS Name: corp.example.com
  Provider: Active Directory
  Status: Connected
  Server: dc01.corp.example.com (192.168.1.50)

User: CORP\jsmith
  UID: 1005
  Primary Group: CORP\Domain Users (GID 513)
  Member of: CORP\Engineering, CORP\File-Share-Access

Group: CORP\Engineering
  GID: 1201
  Members: 47
  Type: Global

Zone Name: System
  Path: /ifs
  Auth Providers: Local, Active Directory
  SMB Enabled: Yes
  NFS Enabled: Yes
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure you are running commands on the PowerScale cluster directly or via SSH, not from a remote workstation without the OneFS CLI installed.
    **`Error: Invalid username <username>`** — Replace `<username>` with an actual AD user in the format `DOMAIN\username` (e.g., `CORP\jsmith`).
    **`Error: Active Directory is not joined`** — Run `isi auth ads create` to join the cluster to Active Directory before querying authentication status.
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


```text title="Expected output"
Created snapshot: project1-20250115
Snapshots:
  ID                                    Name                      Created                Size
  --------                              ----------------------    -------------------   ----------
  1                                     project1-20250115         2025-01-15 14:32:18   2.3 GB
  2                                     project1-20250114         2025-01-14 09:15:42   2.3 GB
  3                                     weekly-backup-20250108    2025-01-08 02:00:00   5.7 GB
  4                                     project1-20250101         2025-01-01 18:45:33   2.1 GB
  ...

Snapshot ID: 1
Name: project1-20250115
Path: /ifs/data/project1
Created: 2025-01-15 14:32:18 UTC
Size: 2.3 GB
State: active
Expires: Never

Snapshot deleted successfully: project1-20250101
```

!!! warning "Common errors"
    **`Error: Snapshot not found: <snap_id>`** — Verify the snapshot ID or name exists with `isi snapshot snapshots list` before attempting deletion.
    **`Error: Permission denied`** — Ensure your user account has snapshot management privileges; contact your OneFS administrator to grant appropriate roles.
    **`Error: Snapshot is locked and cannot be deleted`** — Wait for any active replication or backup jobs to complete, or use `isi snapshot snapshots view <snap_id>` to check the lock status.
### Snapshot Schedules

![Snapshot Schedules](../../../../../assets/powerscale-proc-snapshot-schedules.svg)

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


```text title="Expected output"
Id                          Path                    Schedule            Retention   Alias
daily-project1              /ifs/data/project1      every 1 days at 00:00  2W         latest-project1
hourly-backup               /ifs/data/backup        every 1 hours           7D         hourly-bak
weekly-archive              /ifs/data/archive       every 7 days at 02:00   4W         weekly-arch

Schedule 'daily-project1' created successfully.
Id: daily-project1
Path: /ifs/data/project1
Schedule: every 1 days at 00:00
Retention: 2W
Alias: latest-project1

Schedule '<schedule_name>' modified successfully.
Retention updated to: 1M

Schedule '<schedule_name>' deleted successfully.
Note: Existing snapshots will not be deleted.
```

!!! warning "Common errors"
    **`Error: Path does not exist: /ifs/data/project1`** — Verify the target path exists and is accessible with `isi ls /ifs/data/project1` before creating the schedule.
    **`Error: Invalid retention format '<value>'`** — Use valid retention syntax like `7D`, `2W`, `1M`, or `1Y` (days, weeks, months, or years).
    **`Error: Schedule '<schedule_name>' not found`** — Run `isi snapshot schedules list` to confirm the exact schedule name before modifying or deleting.
### Recovering Files from a Snapshot

![Recovering Files from a Snapshot](../../../../../assets/powerscale-proc-recovering-files-from-a-snapshot.svg)

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


```text title="Expected output"
'report.xlsx' -> '/ifs/data/project1/report.xlsx'

sending incremental file list
./
config.json
report.xlsx
data.csv
archive/
archive/2025_backup.tar.gz
archive/old_logs/
archive/old_logs/system.log

sent 2,847,392 bytes  received 1,024 bytes  matched 2,847,104 bytes  speedup 1.00

Snapshot ID: 12345678-90ab-cdef-1234-567890abcdef
Snapshot modified.
WARNING: Reverting snapshot 12345678-90ab-cdef-1234-567890abcdef will destroy all data written after 2026-01-01 12:00:00 UTC. Continue? (yes/no): yes
Reverting snapshot...
Revert operation completed successfully.
```

!!! warning "Common errors"
    **`cp: cannot create regular file '/ifs/data/project1/report.xlsx': Permission denied`** — Verify the user running the command has write permissions on `/ifs/data/project1/` using `isi auth access list /ifs/data/project1/`.
    **`rsync: change_dir "/ifs/data/project1/.snapshot/project1-20260101" failed: No such file or directory (2)`** — Confirm the snapshot name exists by running `isi snapshot snapshots list` and verify the exact snapshot directory path.
    **`Error: Invalid snapshot ID format`** — Use `isi snapshot snapshots list` to retrieve the correct snapshot ID and ensure it is a valid UUID.
---

### SmartConnect Zone Configuration

![SmartConnect Zone Configuration](../../../../../assets/powerscale-proc-smartconnect-zone-configuration.svg)

SmartConnect zones distribute NFS and SMB client connections across node pools using DNS-based load balancing.

```bash
# Create an IP pool with a SmartConnect DNS zone and round-robin load balancing
isi network pools create \
    --name=pool1 \
    --subnet=subnet0 \
    --ifaces=1:ext-1 \
    --sc-dns-zone=pool1.cluster.domain.com \
    --sc-load-balance-policy=round_robin

# Verify the pool configuration
isi network pools view pool1
```


```text title="Expected output"
Created pool: pool1

Name: pool1
Subnet: subnet0
Interfaces: 1:ext-1
SmartConnect DNS Zone: pool1.cluster.domain.com
SmartConnect Load Balance Policy: round_robin
Access Zone: System
Rebalance Policy: auto
Enable SmartConnect: Yes
Aggregation Mode: lacp
```

!!! warning "Common errors"
    **`Error: subnet0 does not exist`** — Verify the subnet name with `isi network subnets list` and use the correct subnet identifier.
    **`Error: Interface 1:ext-1 not found`** — Confirm the interface exists and is properly configured with `isi network interfaces list`.
    **`Error: SmartConnect is not licensed`** — Enable SmartConnect licensing on the cluster or remove the `--sc-dns-zone` parameter to create a standard pool.
Delegate the SmartConnect zone FQDN (`pool1.cluster.domain.com`) in your DNS infrastructure to the cluster's SmartConnect service IP. Test: `nslookup pool1.cluster.domain.com` — it should return multiple node IPs in rotation across successive lookups.

### SmartQuotas — Create and Monitor Quotas

![SmartQuotas — Create and Monitor Quotas](../../../../../assets/powerscale-proc-smartquotas-create-and-monitor-quotas.svg)

Set hard and soft limits on directories, users, or groups to control storage consumption.

```bash
# Create a directory quota with hard, soft, and advisory thresholds
isi quota quotas create \
    --path=/ifs/data/project1 \
    --type=directory \
    --hard-threshold=10T \
    --soft-threshold=8T \
    --soft-grace=7D \
    --advisory-threshold=9T

# List all active quotas
isi quota quotas list

# Generate a quota usage report
isi quota reports create
isi quota reports list
```


```text title="Expected output"
Created quota for /ifs/data/project1
ID: 1234567890
Path: /ifs/data/project1
Type: directory
Hard Threshold: 10.0 TB
Soft Threshold: 8.0 TB
Soft Grace Period: 7 days
Advisory Threshold: 9.0 TB

ID      Path                    Type        Hard Threshold    Soft Threshold    Advisory Threshold    Usage
1234567890  /ifs/data/project1      directory   10.0 TB           8.0 TB            9.0 TB                2.3 TB
1234567891  /ifs/data/project2      directory   5.0 TB            4.0 TB            4.5 TB                3.8 TB
1234567892  /ifs/home/users         directory   20.0 TB           18.0 TB           19.0 TB               15.2 TB

Report ID: report-20240115-001
Status: COMPLETED
Created: 2024-01-15T14:32:18Z
Path: /ifs/data

Report ID      Status      Created                 Path
report-20240115-001  COMPLETED   2024-01-15T14:32:18Z    /ifs/data
report-20240115-002  COMPLETED   2024-01-14T09:15:42Z    /ifs/home
```

!!! warning "Common errors"
    **`Error: Path /ifs/data/project1 does not exist`** — Create the directory first with `mkdir -p /ifs/data/project1` before applying the quota.
    **`Error: Invalid threshold value: hard-threshold must be greater than soft-threshold`** — Ensure hard-threshold (10T) is larger than soft-threshold (8T) and advisory-threshold (9T).
    **`Error: Permission denied: insufficient privileges to create quotas`** — Run the command as root or a user with cluster admin privileges.
Quota events appear in `isi event events list` when thresholds are crossed. Review reports regularly and adjust thresholds before directories approach the hard limit.

### SyncIQ — Configure Replication Policy

![SyncIQ — Configure Replication Policy](../../../../../assets/powerscale-proc-synciq-configure-replication-policy.svg)

Set up asynchronous replication from this cluster to a remote PowerScale cluster for DR.

```bash
# Create a SyncIQ replication policy
isi sync policies create \
    --name=DR-Policy \
    --action=sync \
    --source-root=/ifs/data \
    --target-host=<remote-cluster-ip> \
    --target-path=/ifs/data-replica \
    --schedule="every 1 hours"

# Trigger an immediate manual run
isi sync policies run DR-Policy

# Monitor replication job progress
isi sync jobs list
```


```text title="Expected output"
Successfully created sync policy 'DR-Policy'
Policy ID: 12a4b5c6-7d8e-9f0a-1b2c-3d4e5f6a7b8c
Source: /ifs/data
Target: 192.168.100.45:/ifs/data-replica
Schedule: every 1 hours
Action: sync

Job started for policy 'DR-Policy'
Job ID: job-2024-01-15-094532

ID                                    Policy      State      Progress  Bytes Transferred
job-2024-01-15-094532                 DR-Policy   running    45%       2.3 TB / 5.1 TB
job-2024-01-14-214015                 DR-Policy   completed  100%      5.1 TB / 5.1 TB
job-2024-01-14-134502                 DR-Policy   completed  100%      5.1 TB / 5.1 TB
job-2024-01-13-054018                 DR-Policy   failed     87%       4.4 TB / 5.1 TB
```

!!! warning "Common errors"
    **`Error: Invalid target host '192.168.100.45' - host unreachable`** — Verify network connectivity to the remote cluster IP and ensure the firewall rules permit SyncIQ traffic on port 8080.
    **`Error: Source path '/ifs/data' does not exist`** — Confirm the source path exists on the local cluster using `isi ls /ifs/data` before creating the policy.
    **`Error: Policy 'DR-Policy' already exists`** — Use a unique policy name or delete the existing policy with `isi sync policies delete DR-Policy` before recreating it.
Confirm the job completes with status SUCCESS. Check `isi sync reports list --policy=DR-Policy` for transfer statistics and any errors from previous runs.

### SyncIQ — Failover and Failback

![SyncIQ — Failover and Failback](../../../../../assets/powerscale-proc-synciq-failover-and-failback.svg)

Promote the replica to writable on a DR event, then re-establish replication when the primary recovers.

```bash
# --- FAILOVER (run on the TARGET / DR cluster) ---
# Allow writes to the replica — breaks the replication relationship
isi sync recovery allow-write --policy=DR-Policy

# Update client mount points and DNS to point to the target cluster

# --- FAILBACK (run when primary cluster is recovered) ---
# On the TARGET cluster: prepare the replica for resync back to the primary
isi sync recovery resync-prep --policy=DR-Policy

# On the TARGET cluster: commit the resync and re-establish original direction
isi sync recovery commit --policy=DR-Policy

# Verify replication is active again
isi sync policies list
```


```text title="Expected output"
Allow-write operation initiated for policy 'DR-Policy'
Replica is now writable and replication is broken.
WARNING: Original replication direction will need to be re-established.

Resync preparation started for policy 'DR-Policy'
Preparing target cluster to resync with primary...
Resync prep completed successfully.

Committing resync for policy 'DR-Policy'
Replication direction restored: primary -> target
Sync relationship re-established.

ID                  Name        Source Cluster      Target Cluster      State
1                   DR-Policy   10.20.1.50          10.20.2.50          active
2                   Local-Sync  10.20.1.50          10.20.1.100         active
```

!!! warning "Common errors"
    **`Error: Policy 'DR-Policy' not found or is not in a failed state`** — Verify the policy name matches exactly and that the primary cluster has actually failed before running allow-write.
    **`Error: Resync-prep failed: replication is still active`** — Run `isi sync recovery allow-write --policy=DR-Policy` first to break the replication relationship before attempting resync-prep.
    **`Error: Commit failed: target cluster is not in resync-prep state`** — Ensure resync-prep completed successfully on the target cluster and no other sync operations are in progress.
After failback, trigger a manual run with `isi sync policies run DR-Policy` and confirm SUCCESS before updating client mount points back to the primary cluster.

### Access Zone Management

![Access Zone Management](../../../../../assets/powerscale-proc-access-zone-management.svg)

Access zones isolate client namespaces and authentication providers, enabling multi-tenancy on a single cluster.

```bash
# Create a new access zone with a dedicated root path
isi zone zones create --name=Zone-DMZ --path=/ifs/dmz --create-path

# Add an authentication provider to the zone
isi zone zones modify Zone-DMZ --add-auth-providers=lsa-local-provider:System

# View the zone configuration
isi zone zones view Zone-DMZ
```


```text title="Expected output"
Created zone 'Zone-DMZ'
Modified zone 'Zone-DMZ'
Zone: Zone-DMZ
  Path: /ifs/dmz
  Auth Providers: lsa-local-provider:System
  Protocols: nfs, smb, ftp, hdfs
  Groupnet: groupnet0
  Created: 2024-01-15T09:42:18Z
  Modified: 2024-01-15T09:42:22Z
  SMB Shares: 0
  NFS Exports: 0
```

!!! warning "Common errors"
    **`Error: zone 'Zone-DMZ' already exists`** — Use `isi zone zones view Zone-DMZ` to verify the zone exists, then skip creation or use a different zone name.
    **`Error: path '/ifs/dmz' does not exist and --create-path not specified`** — Add the `--create-path` flag to the create command to automatically create the directory structure.
    **`Error: authentication provider 'lsa-local-provider:System' not found`** — Verify the provider name with `isi auth providers list` and use the exact provider name from the output.
After creating the zone, create a dedicated IP pool and SmartConnect zone scoped to `Zone-DMZ` so that clients connecting to the zone's IP are isolated from other zones. Verify NFS exports and SMB shares in the zone are reachable from the correct client subnet.

### Node Pool and Tier Management

![Node Pool and Tier Management](../../../../../assets/powerscale-proc-node-pool-and-tier-management.svg)

Assign nodes to pools and configure file pool policies to place data on appropriate performance tiers.

```bash
# List existing node pools and their assigned nodes
isi storagepool nodepools list

# Assign specific nodes (by logical node number) to a pool
isi storagepool nodepools modify <pool-name> --lnns=1,2,3

# Create a file pool policy to direct archive data to a capacity tier
isi filepool policies create \
    --name=Archive \
    --apply-data-storage-target=capacity-pool1 \
    --file-matching-criteria="accessed > 90 days"

# Verify overall storage pool health and tier usage
isi storagepool health
```


```text title="Expected output"
Name                    Description                 Nodes
default                 Default node pool           1,2,3,4,5,6,7,8
capacity-pool1          Capacity tier nodes         9,10,11,12
performance-pool        High-speed tier             13,14,15
(no output — command completes silently)
Created file pool policy 'Archive'
Policy ID: 12a4f8c9-3e2b-11ed-a261-0050569b4d1a
Matching criteria: accessed > 90 days
Data storage target: capacity-pool1
Status: Active

Cluster Health: BALANCED
Tier: performance-pool | Used: 2.3 TB | Free: 7.7 TB | Health: HEALTHY
Tier: capacity-pool1 | Used: 18.5 TB | Free: 31.2 TB | Health: HEALTHY
Tier: default | Used: 5.1 TB | Free: 14.9 TB | Health: HEALTHY
```

!!! warning "Common errors"
    **`Error: Invalid node pool name '<pool-name>'`** — Replace `<pool-name>` with an actual pool name from the `isi storagepool nodepools list` output.
    **`Error: One or more nodes in the list are invalid or offline`** — Verify node numbers exist and are online using `isi nodes list` before assigning them to a pool.
    **`Error: File pool policy 'Archive' already exists`** — Use `isi filepool policies modify Archive` to update an existing policy instead of creating a duplicate.
Run `isi job list` after modifying pool assignments — a Restripe job will start automatically to redistribute data. Monitor it to completion before making further pool changes.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powerscale — Health Checks](../health-checks/)
- [Powerscale — CLI Reference](../cli-reference/)
- [Powerscale — Common Issues](../../troubleshooting/common-issues/)
