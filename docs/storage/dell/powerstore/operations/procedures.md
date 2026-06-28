---
tags:
  - dell
  - operations
---
# PowerStore — Procedures


<div class="kb-summary">
PowerStore operational procedures — block volume and NAS file system provisioning, snapshot management, host management, replication configuration, Metro volume operations, and performance monitoring.

*Applies to: PowerStore 3.x*
</div>



```d2
direction: right

hub: "PowerStore\nOperations" {shape: hexagon}
provisioning_a_block_volume: "Provisioning a Block Volume" {shape: rectangle}
provisioning_a_nas_file_system_nfs: "Provisioning a NAS File System (NFS)" {shape: rectangle}
snapshot_operations: "Snapshot Operations" {shape: rectangle}
host_management: "Host Management" {shape: rectangle}
replication_management: "Replication Management" {shape: rectangle}
metro_volume_operations: "Metro Volume Operations" {shape: rectangle}

hub -> provisioning_a_block_volume
hub -> provisioning_a_nas_file_system_nfs
hub -> snapshot_operations
hub -> host_management
hub -> replication_management
hub -> metro_volume_operations
```

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Provisioning a Block Volume

### Step-by-Step: Create and Map a Volume to a Host

![Step-by-Step: Create and Map a Volume to a Host](../../../../assets/powerstore-proc-step-by-step-create-and-map-a-volume-to-a-host.svg)

This is the core provisioning workflow for presenting block storage to a host.

**Prerequisites:**
- Host object created in PowerStore with the correct initiators (FC WWNs or iSCSI IQNs)
- Host group created (if multiple hosts need access to the same volume)
- Volume group created for the application (groups volumes for consistent snapshot/replication)
- Protection policy assigned to the volume group

```bash
# Step 1: Create a volume group
curl -k -X POST "https://<mgmt-ip>/api/rest/volume_group" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "oradb-prod-vg",
    "description": "Oracle production database volume group"
  }'

# Step 2: Create the volume (size in bytes; 1 TiB = 1099511627776 bytes)
curl -k -X POST "https://<mgmt-ip>/api/rest/volume" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "oradb-prod-data-001",
    "size": 1099511627776,
    "volume_group_id": "<vg-id>",
    "description": "Oracle prod database data volume"
  }'

# Step 3: Map the volume to the host (or host group for clusters)
curl -k -X POST "https://<mgmt-ip>/api/rest/host_volume_mapping" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "host_id": "<host-id>",
    "volume_id": "<volume-id>",
    "logical_unit_number": 0
  }'

# Step 4: Confirm the mapping was created
curl -k -X GET "https://<mgmt-ip>/api/rest/host_volume_mapping?host_id=<host-id>" \
  -H "DELL-EMC-TOKEN: <token>"
```

**Post-provisioning on the host (Linux):**

```bash
# Rescan storage for new LUN
echo "- - -" > /sys/class/scsi_host/host0/scan
iscsiadm -m session --rescan   # For iSCSI hosts

# Confirm multipath device visible
multipath -ll

# Identify the new device
lsblk | grep -v loop

# Create file system (if not using as raw device)
mkfs.xfs /dev/mapper/<device>

# Mount
mkdir -p /mnt/oradb
mount /dev/mapper/<device> /mnt/oradb
```

## Provisioning a NAS File System (NFS)

```bash
# Step 1: Create a NAS server (if not already present)
curl -k -X POST "https://<mgmt-ip>/api/rest/nas_server" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "nas-prod-001",
    "description": "Production NAS server",
    "current_node_id": "<node-a-id>"
  }'

# Step 2: Create a file system
curl -k -X POST "https://<mgmt-ip>/api/rest/filesystem" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "homedirs-prod-001",
    "nas_server_id": "<nas-server-id>",
    "size_total": 5497558138880,
    "description": "Home directories production"
  }'

# Step 3: Create an NFS export
curl -k -X POST "https://<mgmt-ip>/api/rest/nfs_export" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "homedirs-prod-export",
    "filesystem_id": "<fs-id>",
    "path": "/",
    "rw_hosts": [{"ip": "192.168.10.0", "prefix_length": 24}],
    "no_access_hosts": [],
    "min_security": "sys",
    "anonymous_uid": 65534,
    "anonymous_gid": 65534,
    "no_suid": true
  }'
```

**Mount on Linux host:**

```bash
# Mount the NFS export
mount -t nfs 192.168.20.10:/homedirs-prod-001 /mnt/homedirs \
  -o rw,nfsvers=4.1,hard,intr,timeo=600,retrans=3

# Add to /etc/fstab for persistence
echo "192.168.20.10:/homedirs-prod-001 /mnt/homedirs nfs4 rw,hard,intr,timeo=600,retrans=3 0 0" \
  >> /etc/fstab
```

## Snapshot Operations

### Create a Manual Snapshot

![Create a Manual Snapshot](../../../../assets/powerstore-proc-create-a-manual-snapshot.svg)

```bash
# Create a volume snapshot (manual, immediate)
curl -k -X POST "https://<mgmt-ip>/api/rest/volume_snapshot" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "volume_id": "<volume-id>",
    "name": "oradb-prod-data-001-snap-20260507",
    "description": "Pre-patch snapshot before OS upgrade"
  }'

# Create a filesystem snapshot
curl -k -X POST "https://<mgmt-ip>/api/rest/filesystem_snapshot" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "filesystem_id": "<fs-id>",
    "name": "homedirs-prod-001-snap-20260507",
    "description": "Daily backup snapshot"
  }'
```

### Restore a Volume from Snapshot

![Restore a Volume from Snapshot](../../../../assets/powerstore-proc-restore-a-volume-from-snapshot.svg)

Use this procedure to roll back a volume to a previous snapshot. The source volume must be unmounted or quiesced before restore.

```bash
# Step 1: List available snapshots for the volume
curl -k -X GET "https://<mgmt-ip>/api/rest/volume_snapshot?volume_id=<volume-id>" \
  -H "DELL-EMC-TOKEN: <token>"

# Step 2: Restore the volume from the selected snapshot
# The restore operation replaces the current volume content with the snapshot content
curl -k -X POST "https://<mgmt-ip>/api/rest/volume_snapshot/<snapshot-id>/restore" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"backup_snap_name": "pre-restore-backup-20260507"}'
  # backup_snap_name: PowerStore creates a backup snapshot of the current state before restoring
  # Remove this field if you don't want to keep the current state
```

### Clone a Volume

![Clone a Volume](../../../../assets/powerstore-proc-clone-a-volume.svg)

Cloning creates an independent, read-write copy of a volume from its current state. Useful for dev/test provisioning without impacting production.

```bash
curl -k -X POST "https://<mgmt-ip>/api/rest/volume/<source-volume-id>/clone" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "oradb-dev-clone-20260507",
    "description": "Dev clone from production volume for testing",
    "volume_group_id": "<dev-vg-id>"
  }'
```

## Host Management

### Add a New Host

![Add a New Host](../../../../assets/powerstore-proc-add-a-new-host.svg)

```bash
# Create host object
curl -k -X POST "https://<mgmt-ip>/api/rest/host" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "lon01-db-srv-001",
    "os_type": "Linux",
    "description": "Oracle database server lon01-db-srv-001"
  }'

# Add FC initiator (repeat for each HBA port)
curl -k -X POST "https://<mgmt-ip>/api/rest/host_initiator" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "host_id": "<host-id>",
    "port_name": "21:00:00:11:0d:ab:cd:01",
    "port_type": "FC"
  }'

# Add host to host group
curl -k -X POST "https://<mgmt-ip>/api/rest/host_group/<host-group-id>/add_hosts" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"host_ids": ["<host-id>"]}'
```

### Decommission a Host

![Decommission a Host](../../../../assets/powerstore-proc-decommission-a-host.svg)

Before decommissioning, confirm all volumes are unmounted on the host and all mappings are removed.

```bash
# Step 1: List all volume mappings for the host
curl -k -X GET "https://<mgmt-ip>/api/rest/host_volume_mapping?host_id=<host-id>" \
  -H "DELL-EMC-TOKEN: <token>"

# Step 2: Delete each mapping
curl -k -X DELETE "https://<mgmt-ip>/api/rest/host_volume_mapping/<mapping-id>" \
  -H "DELL-EMC-TOKEN: <token>"

# Step 3: Remove host from host group
curl -k -X POST "https://<mgmt-ip>/api/rest/host_group/<hg-id>/remove_hosts" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"host_ids": ["<host-id>"]}'

# Step 4: Delete the host object
curl -k -X DELETE "https://<mgmt-ip>/api/rest/host/<host-id>" \
  -H "DELL-EMC-TOKEN: <token>"
```

## Replication Management

### Create an Async Replication Session

![Create an Async Replication Session](../../../../assets/powerstore-proc-create-an-async-replication-session.svg)

```bash
# Step 1: Ensure a remote system object exists for the target PowerStore
curl -k -X GET "https://<mgmt-ip>/api/rest/remote_system" \
  -H "DELL-EMC-TOKEN: <token>"

# If not present, create the remote system
curl -k -X POST "https://<mgmt-ip>/api/rest/remote_system" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "lon02-pstore-001",
    "management_address": "192.168.20.50",
    "description": "DR site PowerStore"
  }'

# Step 2: Create a replication rule (defines RPO)
curl -k -X POST "https://<mgmt-ip>/api/rest/replication_rule" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "1h-async",
    "rpo": "One_Hour",
    "remote_system_id": "<remote-system-id>"
  }'

# Step 3: Assign the replication rule to a protection policy
# Then assign the policy to a volume group — replication sessions are created automatically
```

### Failover to DR (Planned Failover)

![Failover to DR (Planned Failover)](../../../../assets/powerstore-proc-failover-to-dr-planned-failover.svg)

Planned failover for a scheduled DR test or migration:

```bash
# Step 1: Sync and pause replication to ensure data is current
curl -k -X POST "https://<mgmt-ip>/api/rest/replication_session/<session-id>/sync" \
  -H "DELL-EMC-TOKEN: <token>"

# Wait for sync to complete (check state = synchronized)
curl -k -X GET "https://<mgmt-ip>/api/rest/replication_session/<session-id>?select=state,last_sync_time" \
  -H "DELL-EMC-TOKEN: <token>"

# Step 2: Failover (planned) — swaps source and destination roles
curl -k -X POST "https://<mgmt-ip>/api/rest/replication_session/<session-id>/failover" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"is_planned": true}'

# Step 3: On the DR PowerStore — map the failed-over volumes to DR hosts
# Then bring up applications at DR site

# Step 4: When ready to fail back — perform another planned failover from DR to production
```

## Metro Volume Operations

### Promote a Metro Volume (Site Failure)

![Promote a Metro Volume (Site Failure)](../../../../assets/powerstore-proc-promote-a-metro-volume-site-failure.svg)

If the primary site fails and the mediator has granted authority to the secondary site:

```bash
# On the surviving secondary PowerStore:
# Check Metro Volume state — should show 'Primary_With_No_Secondary' or mediator has promoted
curl -k -X GET "https://<dr-mgmt-ip>/api/rest/replication_session?select=name,state" \
  -H "DELL-EMC-TOKEN: <token>"

# Promote the secondary volume to primary (makes it writable to hosts)
curl -k -X POST "https://<dr-mgmt-ip>/api/rest/replication_session/<session-id>/promote" \
  -H "DELL-EMC-TOKEN: <token>"

# Hosts at the secondary site can now mount the volumes and bring up applications
```

### Resync After Site Recovery

![Resync After Site Recovery](../../../../assets/powerstore-proc-resync-after-site-recovery.svg)

```bash
# After primary site recovery, resync Metro Volume
# This operation resyncs data from the current primary (secondary site) back to the original primary
curl -k -X POST "https://<primary-mgmt-ip>/api/rest/replication_session/<session-id>/resync" \
  -H "DELL-EMC-TOKEN: <token>"
```

## NAS Server Failover

NAS servers run on one node at a time. To manually fail over a NAS server to the peer node (e.g., before node maintenance):

```bash
# Identify the NAS server and its current node
curl -k -X GET "https://<mgmt-ip>/api/rest/nas_server?select=name,current_node,preferred_node" \
  -H "DELL-EMC-TOKEN: <token>"

# Initiate manual failover to peer node
curl -k -X POST "https://<mgmt-ip>/api/rest/nas_server/<nas-id>/failover" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"planned": true}'

# Confirm failover completed — current_node should now reflect the new node
curl -k -X GET "https://<mgmt-ip>/api/rest/nas_server/<nas-id>?select=name,current_node" \
  -H "DELL-EMC-TOKEN: <token>"
```

NFS clients experience a brief interruption (seconds) during NAS server failover. SMB clients may require re-mounting depending on the session timeout configuration.

---

### Manage Protection Policies

![Manage Protection Policies](../../../../assets/powerstore-proc-manage-protection-policies.svg)

Protection policies bundle snapshot rules and replication rules and are assigned to volumes or volume groups.

```bash
# List all protection policies
pstcli -server <ip> -user admin protection_policy list

# List snapshot rules
curl -k -X GET "https://<mgmt-ip>/api/rest/snapshot_rule" \
  -H "DELL-EMC-TOKEN: <token>"

# Assign a protection policy to a volume
curl -k -X PATCH "https://<mgmt-ip>/api/rest/volume/<volume-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"protection_policy_id": "<policy-id>"}'
```

GUI path: Protection → Protection Policies → Create. Assign snapshot rule (name, interval, retained copies) and optional replication rule. Assign policy to volumes via Volumes → select volume → Protection → Assign Policy. Snapshots begin on the defined schedule immediately after assignment.

### Volume Migration (Import / Mobility)

![Volume Migration (Import / Mobility)](../../../../assets/powerstore-proc-volume-migration-import-mobility.svg)

Move a volume between storage tiers within the same cluster, or import volumes from an external array.

```bash
# Modify a volume's storage tier (Performance, Capacity, Extreme)
curl -k -X PATCH "https://<mgmt-ip>/api/rest/volume/<volume-id>" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{"appliance_id": "<target-appliance-id>"}'

# List active import sessions
curl -k -X GET "https://<mgmt-ip>/api/rest/import_session" \
  -H "DELL-EMC-TOKEN: <token>"
```

GUI path for tier change: Storage → Volumes → select volume → Modify → Storage Tier. For import from external array (VPLEX, Unity, VNX): Storage → Import → Create Import Session; select source array and volume; initiate cutover when ready. Monitor progress under Storage → Import → Active Sessions.

### NAS File System Creation and Share

![NAS File System Creation and Share](../../../../assets/powerstore-proc-nas-file-system-creation-and-share.svg)

PowerStore supports NFS and SMB shares from the same NAS server. Create the NAS server first before creating file systems.

```bash
# Step 1: Create a NAS server
curl -k -X POST "https://<mgmt-ip>/api/rest/nas_server" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "nas-prod-002",
    "current_node_id": "<node-id>"
  }'

# Step 2: Create a file system on the NAS server
curl -k -X POST "https://<mgmt-ip>/api/rest/filesystem" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "dept-shares-001",
    "nas_server_id": "<nas-server-id>",
    "size_total": 2199023255552
  }'

# Step 3: Create an NFS export
curl -k -X POST "https://<mgmt-ip>/api/rest/nfs_export" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "dept-shares-export",
    "filesystem_id": "<fs-id>",
    "path": "/",
    "rw_hosts": [{"ip": "192.168.10.0", "prefix_length": 24}]
  }'

# Step 4: Create an SMB share
curl -k -X POST "https://<mgmt-ip>/api/rest/smb_share" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "dept-shares",
    "filesystem_id": "<fs-id>",
    "path": "/"
  }'
```

Verify NFS from Linux: `mount <ip>:/dept-shares-001 /mnt/test`. Verify SMB from Windows: map `\\<ip>\dept-shares`. GUI path: Storage → NAS Servers → Create; then Storage → File Systems → Create.

### Performance Policy Management

![Performance Policy Management](../../../../assets/powerstore-proc-performance-policy-management.svg)

Performance policies enforce IOPS and bandwidth limits per volume for QoS across workloads.

```bash
# List existing performance policies
curl -k -X GET "https://<mgmt-ip>/api/rest/performance_policy" \
  -H "DELL-EMC-TOKEN: <token>"

# Create a performance policy with IOPS and bandwidth limits
curl -k -X POST "https://<mgmt-ip>/api/rest/performance_policy" \
  -H "DELL-EMC-TOKEN: <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "dev-limited",
    "max_iops": 1000,
    "max_bandwidth": 104857600
  }'

# Assign a performance policy to a volume
pstcli -server <ip> -user admin volume modify --name <vol> --performance_policy_id <id>
```

GUI path: Storage → Storage Policies → Performance Policies → Create (set IOPS limit and/or bandwidth limit in MB/s). Assign to a volume via Volumes → Modify → Storage Policy → select performance policy. View utilisation against limits under Dashboard → Performance. A value of `0` for `max_iops` or `max_bandwidth` means unlimited.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powerstore — Health Checks](health-checks/)
- [Powerstore — CLI Reference](cli-reference/)
- [Powerstore — Common Issues](../troubleshooting/common-issues/)
