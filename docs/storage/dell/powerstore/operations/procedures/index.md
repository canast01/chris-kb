# PowerStore — Procedures


<div class="kb-summary">
PowerStore operational procedures — block volume and NAS file system provisioning, snapshot management, host management, replication configuration, Metro volume operations, and performance monitoring.
</div>
```text
┌────────────────────────────── Dell PowerStore — Operational Procedures ───────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │           PowerStore operational procedures: standard tasks for day-2 administration          │   │
│   │           Covers: provisioning, expansion, maintenance, DR testing, and decommission          │   │
│   │           Pre/post checks required for all maintenance activities affecting storage           │   │
│   │            All procedures require approved change management tickets in production            │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Open change → pre-check → execute → verify → post-check → close                                    │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │           T-model           │  │          Block only         │  │        iSCSI/FC/NVMe        │   │
│   │           X-model           │  │         Block + File        │  │       Unified protocol      │   │
│   │            Metro            │  │       Sync replication      │  │       Zero-RPO stretch      │   │
│   │          Protection         │  │        Snapshot/Clone       │  │       Immutable snaps       │   │
│   │             Mgmt            │  │          PSM / REST         │  │         Unified pane        │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │    Procedure     │    Pre-check     │       Steps       │      Verify      │    Post-check    │   │
│   │    Provision     │  Capacity free?  │   Create volume   │   Host access    │   Monitor I/O    │   │
│   │      Expand      │   Pool space?    │    Grow volume    │    FS resize     │   Verify size    │   │
│   │     Snapshot     │   Policy set?    │   Take snapshot   │   Snap listed    │   Consistency    │   │
│   │     Failover     │  Repl. in sync?  │    Break repl.    │    App online    │    Verify RTO    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: PowerStore T/X appliance · NVMe drives · SAS expansion shelves · 10/25 GbE               │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    PowerStore         = Dell mid-range NVMe storage; T-model block-only, X-model unified block+file   │
│    PowerStore Manager = browser GUI and REST API endpoint for all PowerStore operations               │
│    Volume group       = logical collection of volumes sharing snapshot and replication policies       │
│    Protection policy  = assigned to volumes; defines snapshot schedule, retention, and replication    │
│    Metro volume       = synchronously replicated volume across two sites; zero RPO active-active      │
│    Snapshot           = space-efficient point-in-time copy; crash-consistent or app-consistent        │
│    Clone              = full writable copy of a volume or file system; independent lifecycle          │
│    Applied-to         = PowerStore host mapping; volumes are applied-to a host or host group object   │
│    Capacity license   = PowerStore uses usable-capacity licensing; licensed in TiB increments         │
│    Storage container  = PowerStore X-model; unified block and file from the same storage pool         │
│    Appliance          = single PowerStore node pair (dual controllers); scalable to 4 appliances      │
│    NVMe-oF            = NVMe over Fabrics; FC-NVMe or NVMe/TCP host connectivity on PowerStore        │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## Provisioning a Block Volume

### Step-by-Step: Create and Map a Volume to a Host

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
