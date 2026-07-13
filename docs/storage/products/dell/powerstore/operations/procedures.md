---
tags:
  - dell
  - operations
description: "PowerStore operational procedures — block volume and NAS file system provisioning, snapshot management, host management, replication configuration, Metro..."
---
# PowerStore — Procedures

<div class="kb-summary">
PowerStore operational procedures — block volume and NAS file system provisioning, snapshot management, host management, replication configuration, Metro volume operations, and performance monitoring.

*Applies to: PowerStore 3.x*
</div>

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Provisioning a Block Volume

### Step-by-Step: Create and Map a Volume to a Host

![Step-by-Step: Create and Map a Volume to a Host](../../../../../assets/powerstore-proc-step-by-step-create-and-map-a-volume-to-a-host.svg)

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


```text title="Expected output"
{
  "id": "vg-5f8c2a1b-9e4d-47a2-b1c3-8d7f2e9a4c6b",
  "name": "oradb-prod-vg",
  "description": "Oracle production database volume group",
  "creation_timestamp": "2024-01-15T14:32:18Z",
  "state": "healthy"
}
{
  "id": "vol-a3d7f9c2-1e5b-4a8f-9c2d-7b4e1f8a3c5d",
  "name": "oradb-prod-data-001",
  "size": 1099511627776,
  "volume_group_id": "vg-5f8c2a1b-9e4d-47a2-b1c3-8d7f2e9a4c6b",
  "description": "Oracle prod database data volume",
  "state": "healthy",
  "creation_timestamp": "2024-01-15T14:32:45Z"
}
{
  "id": "hvmap-2c8f1a9d-5e3b-4f7a-8c1d-9e2b5a7f3c6d",
  "host_id": "host-prod-db-01",
  "volume_id": "vol-a3d7f9c2-1e5b-4a8f-9c2d-7b4e1f8a3c5d",
  "logical_unit_number": 0,
  "state": "mapped",
  "creation_timestamp": "2024-01-15T14:33:12Z"
}
[
  {
    "id": "hvmap-2c8f1a9d-5e3b-4f7a-8c1d-9e2b5a7f3c6d",
    "host_id": "host-prod-db-01",
    "volume_id": "vol-a3d7f9c2-1e5b-4a8f-9c2d-7b4e1f8a3c5d",
    "logical_unit_number": 0,
    "state": "mapped"
  }
]
```

!!! warning "Common errors"
    **`"error_code": 401, "message": "Invalid or expired token"`** — Regenerate the authentication token using the PowerStore management API login endpoint and update the DELL-EMC-TOKEN header.
    **`"error_code": 400, "message": "Invalid volume_group_id"`** — Verify the volume group ID from Step 1 output and ensure it is correctly substituted in the Step 2 request body.
    **`"error_code": 409, "message": "Volume already mapped to host"`** — Check existing mappings with a GET query and either use a different LUN number or unmap the volume before remapping.
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


```text title="Expected output"
- - -
iscsiadm: No active sessions.
NAME                    MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINTS
sda                       8:0    0  100G  0 disk
├─sda1                    8:1    0    1G  0 part  /boot
└─sda2                    8:2    0   99G  0 part  /
sdb                       8:16   0  500G  0 disk
└─sdb1                    8:17   0  500G  0 part
sdc                       8:32   0  250G  0 disk
mpatha (36006016b8a4c2e00e8d4b5c8f9a2b1c0) dm-0 DELL,PowerStore
size=250G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  `- 4:0:0:0 sdc 8:32 active ready running
mkfs.xfs: /dev/mapper/mpatha appears to be mounted
mount: /mnt/oradb: mount point does not exist
```

!!! warning "Common errors"
    **`mkfs.xfs: /dev/mapper/mpatha appears to be mounted`** — Unmount the device first with `umount /dev/mapper/mpatha` before formatting.
    **`mount: /mnt/oradb: mount point does not exist`** — Create the mount point directory with `mkdir -p /mnt/oradb` before running the mount command.
    **`iscsiadm: No active sessions.`** — Ensure iSCSI targets are discovered and logged in with `iscsiadm -m discovery -t st -p <target_ip>` and `iscsiadm -m node --login` before rescanning.
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


```text title="Expected output"
{"id":"nas_server_6f8a2c1d-4e92-11ed-9e5f-005056a50001","name":"nas-prod-001","description":"Production NAS server","current_node_id":"node-a-id-005056a50001","filesystem_count":0,"is_replication_destination":false,"_links":{"self":{"href":"/api/rest/nas_server/nas_server_6f8a2c1d-4e92-11ed-9e5f-005056a50001"}}}
{"id":"filesystem_8b3f5e2a-7c14-11ed-a1b2-005056a50002","name":"homedirs-prod-001","nas_server_id":"nas_server_6f8a2c1d-4e92-11ed-9e5f-005056a50001","size_total":5497558138880,"size_used":0,"description":"Home directories production","state":"Ready","_links":{"self":{"href":"/api/rest/filesystem/filesystem_8b3f5e2a-7c14-11ed-a1b2-005056a50002"}}}
{"id":"nfs_export_c4d7a9f1-9b22-11ed-b3c4-005056a50003","name":"homedirs-prod-export","filesystem_id":"filesystem_8b3f5e2a-7c14-11ed-a1b2-005056a50002","path":"/","rw_hosts":[{"ip":"192.168.10.0","prefix_length":24}],"no_access_hosts":[],"min_security":"sys","anonymous_uid":65534,"anonymous_gid":65534,"no_suid":true,"_links":{"self":{"href":"/api/rest/nfs_export/nfs_export_c4d7a9f1-9b22-11ed-b3c4-005056a50003"}}}
```

!!! warning "Common errors"
    **`{"error_code":"400","message":"Invalid DELL-EMC-TOKEN or token expired"}`** — Regenerate the authentication token using the PowerStore management API login endpoint and update the DELL-EMC-TOKEN header value.
    **`{"error_code":"409","message":"NAS server with name 'nas-prod-001' already exists"}`** — Query existing NAS servers with `curl -k -X GET "https://<mgmt-ip>/api/rest/nas_server" -H "DELL-EMC-TOKEN: <token>"` and use an existing server ID or choose a unique name.
    **`{"error_code":"422","message":"Invalid filesystem size: size_total must be greater than 1GB"}`** — Increase the `size_total` parameter to at least 1073741824 bytes (1 GB) or verify the value is in bytes, not GB.
**Mount on Linux host:**

```bash
# Mount the NFS export
mount -t nfs 192.168.20.10:/homedirs-prod-001 /mnt/homedirs \
  -o rw,nfsvers=4.1,hard,intr,timeo=600,retrans=3

# Add to /etc/fstab for persistence
echo "192.168.20.10:/homedirs-prod-001 /mnt/homedirs nfs4 rw,hard,intr,timeo=600,retrans=3 0 0" \
  >> /etc/fstab
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`mount.nfs: access denied by server while mounting 192.168.20.10:/homedirs-prod-001`** — Verify the NFS export permissions on the PowerStore array and ensure the client IP is listed in the export ACL.
    **`mount.nfs: No such file or directory`** — Create the mount point directory with `mkdir -p /mnt/homedirs` before attempting to mount.
    **`mount.nfs: Protocol not supported`** — Confirm the NFS client supports NFSv4.1 by running `cat /proc/fs/nfsd/versions` and install `nfs-utils` if needed.
## Snapshot Operations

### Create a Manual Snapshot

![Create a Manual Snapshot](../../../../../assets/powerstore-proc-create-a-manual-snapshot.svg)

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


```text title="Expected output"
{
  "id": "snap-0a1b2c3d4e5f6g7h",
  "name": "oradb-prod-data-001-snap-20260507",
  "volume_id": "vol-8f9e8d7c6b5a4321",
  "description": "Pre-patch snapshot before OS upgrade",
  "creation_timestamp": "2026-05-07T14:32:18Z",
  "size": 536870912000,
  "state": "ready"
}
{
  "id": "snap-9x8y7z6w5v4u3t2s",
  "name": "homedirs-prod-001-snap-20260507",
  "filesystem_id": "fs-prod-homedir-001",
  "description": "Daily backup snapshot",
  "creation_timestamp": "2026-05-07T14:32:22Z",
  "size": 214748364800,
  "state": "ready"
}
```

!!! warning "Common errors"
    **`"error_code": 401, "message": "Invalid or expired token"`** — Regenerate the authentication token using the PowerStore management API login endpoint and update the DELL-EMC-TOKEN header.
    **`"error_code": 404, "message": "Resource not found"`** — Verify the volume_id and filesystem_id exist by querying `/api/rest/volumes` and `/api/rest/filesystems` endpoints respectively.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to bypass SSL verification or import the PowerStore management certificate into your system's certificate store.
### Restore a Volume from Snapshot

![Restore a Volume from Snapshot](../../../../../assets/powerstore-proc-restore-a-volume-from-snapshot.svg)

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


```text title="Expected output"
{
  "snapshots": [
    {
      "id": "snapshot_1a2b3c4d-5e6f-7g8h-9i0j-1k2l3m4n5o6p",
      "name": "daily-backup-20260506",
      "volume_id": "vol_9x8y7w6v-5u4t-3s2r-1q0p-9o8n7m6l5k4j",
      "creation_timestamp": "2026-05-06T02:30:00Z",
      "size_bytes": 1099511627776,
      "state": "ready"
    },
    {
      "id": "snapshot_2b3c4d5e-6f7g-8h9i-0j1k-2l3m4n5o6p7q",
      "name": "hourly-backup-20260506-2200",
      "volume_id": "vol_9x8y7w6v-5u4t-3s2r-1q0p-9o8n7m6l5k4j",
      "creation_timestamp": "2026-05-06T22:00:15Z",
      "size_bytes": 1099511627776,
      "state": "ready"
    }
  ]
}
{
  "id": "restore_job_7f8g9h0i-1j2k-3l4m-5n6o-7p8q9r0s1t2u",
  "state": "running",
  "progress_percentage": 0,
  "estimated_completion_time": "2026-05-07T00:45:30Z",
  "backup_snapshot_id": "snapshot_3c4d5e6f-7g8h-9i0j-1k2l-3m4n5o6p7q8r"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or install the PowerStore management certificate in your system's certificate store.
    **`{"error": "Unauthorized", "error_code": 401}`** — Verify the DELL-EMC-TOKEN is valid and not expired by re-authenticating with the PowerStore management API.
    **`{"error": "Not Found", "error_code": 404}`** — Confirm the snapshot_id and volume_id exist by running the GET list command first and copying the exact IDs from the response.
### Clone a Volume

![Clone a Volume](../../../../../assets/powerstore-proc-clone-a-volume.svg)

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


```text title="Expected output"
{
  "id": "0bcc404d-8f2a-4a2e-9c3e-2a1f5e8d9b4c",
  "name": "oradb-dev-clone-20260507",
  "size": 1099511627776,
  "state": "Ready",
  "protection_policy_id": "default_protection",
  "volume_group_id": "vg-prod-oracle-001",
  "description": "Dev clone from production volume for testing",
  "creation_timestamp": "2026-05-07T14:32:18Z",
  "logical_used": 847288369152,
  "performance_policy_id": "default_performance",
  "is_thin_clone": true,
  "source_volume_id": "vol-src-8a2f4c91"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification, or import the management array's certificate into your system trust store.
    **`{"error":"Invalid token or token expired","error_code":"UNAUTHENTICATED"}`** — Regenerate the authentication token using the PowerStore login API and ensure it has not exceeded its 24-hour expiration window.
    **`{"error":"Volume not found","error_code":"NOT_FOUND"}`** — Verify the source volume ID exists by running `curl -k -H "DELL-EMC-TOKEN: <token>" https://<mgmt-ip>/api/rest/volume/<source-volume-id>` to confirm the UUID is correct.
## Host Management

### Add a New Host

![Add a New Host](../../../../../assets/powerstore-proc-add-a-new-host.svg)

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


```text title="Expected output"
{
  "id": "host_5f8c2a1b-4e9d-11ec-81d3-005056b3d764",
  "name": "lon01-db-srv-001",
  "os_type": "Linux",
  "description": "Oracle database server lon01-db-srv-001",
  "initiator_count": 0,
  "initiator_protocol_mix": "Fibre",
  "mapped_volumes": 0
}
{
  "id": "initiator_7a3f5c2d-4e9e-11ec-81d3-005056b3d764",
  "host_id": "host_5f8c2a1b-4e9d-11ec-81d3-005056b3d764",
  "port_name": "21:00:00:11:0d:ab:cd:01",
  "port_type": "FC",
  "is_logged_in": false
}
{
  "host_group_id": "hg_8b2e4f9c-4e9e-11ec-81d3-005056b3d764",
  "host_ids": [
    "host_5f8c2a1b-4e9d-11ec-81d3-005056b3d764"
  ]
}
```

!!! warning "Common errors"
    **`{"error_code":"INVALID_TOKEN","message":"The supplied token is invalid or expired"}`** — Regenerate the authentication token using the PowerStore login API and update the DELL-EMC-TOKEN header.
    **`{"error_code":"DUPLICATE_NAME","message":"A host with name 'lon01-db-srv-001' already exists"}`** — Verify the host does not already exist on the array using a GET request, or use a unique hostname.
    **`{"error_code":"INVALID_HOST_ID","message":"Host ID '<host-id>' does not exist"}`** — Confirm the host_id from the first POST response was correctly captured and used in subsequent API calls.
### Decommission a Host

![Decommission a Host](../../../../../assets/powerstore-proc-decommission-a-host.svg)

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


```text title="Expected output"
{
  "entries": [
    {
      "id": "mapping_1a2b3c4d",
      "host_id": "host_5e6f7g8h",
      "volume_id": "vol_9i0j1k2l",
      "lun": 0
    },
    {
      "id": "mapping_2b3c4d5e",
      "host_id": "host_5e6f7g8h",
      "volume_id": "vol_3m4n5o6p",
      "lun": 1
    }
  ]
}
{
  "id": "mapping_1a2b3c4d",
  "state": "Deleting"
}
{
  "id": "mapping_2b3c4d5e",
  "state": "Deleting"
}
{
  "host_group_id": "hg_7q8r9s0t",
  "state": "Updated"
}
{
  "id": "host_5e6f7g8h",
  "state": "Deleting"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present in example, but verify it's not being stripped by proxies).
    **`{"error": "Unauthorized", "error_code": 401}`** — Verify the DELL-EMC-TOKEN is valid and not expired by re-authenticating and obtaining a fresh token.
    **`{"error": "Resource in use", "error_code": 409}`** — Ensure all volume mappings are deleted before attempting to remove the host from the host group or delete the host object.
## Replication Management

### Create an Async Replication Session

![Create an Async Replication Session](../../../../../assets/powerstore-proc-create-an-async-replication-session.svg)

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


```text title="Expected output"
{
  "entries": [
    {
      "id": "61e4e8d4-5a2c-4f3b-8e1a-9c2b3d4e5f6a",
      "name": "lon02-pstore-001",
      "management_address": "192.168.20.50",
      "description": "DR site PowerStore",
      "remote_id": "A220d1e5e5e5e5e5",
      "state": "Connected"
    }
  ]
}
{
  "id": "61e4e8d4-5a2c-4f3b-8e1a-9c2b3d4e5f6b",
  "name": "lon02-pstore-001",
  "management_address": "192.168.20.50",
  "description": "DR site PowerStore",
  "remote_id": "A220d1e5e5e5e5e5"
}
{
  "id": "7f2a1b3c-9e4d-4c5a-b8f1-2e3d4a5b6c7d",
  "name": "1h-async",
  "rpo": "One_Hour",
  "remote_system_id": "61e4e8d4-5a2c-4f3b-8e1a-9c2b3d4e5f6b",
  "alert_threshold": 3600
}
```

!!! warning "Common errors"
    **`"error_code": 401, "message": "Invalid or expired token"`** — Regenerate the DELL-EMC-TOKEN using the authentication endpoint and ensure it has not exceeded its 24-hour expiration window.
    **`"error_code": 400, "message": "Invalid rpo value. Allowed values: [Five_Minutes, Fifteen_Minutes, One_Hour, Four_Hours, Daily]"`** — Correct the rpo field to one of the supported values; "One_Hour" is valid but check for typos or unsupported custom values.
    **`"error_code": 409, "message": "Remote system with name 'lon02-pstore-001' already exists"`** — Query the existing remote system by name and reuse its ID instead of attempting to create a duplicate.
### Failover to DR (Planned Failover)

![Failover to DR (Planned Failover)](../../../../../assets/powerstore-proc-failover-to-dr-planned-failover.svg)

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


```text title="Expected output"
{"id":"replication_session_123abc","state":"synchronized","last_sync_time":"2024-01-15T14:32:18Z"}
{"id":"replication_session_123abc","state":"synchronized","last_sync_time":"2024-01-15T14:32:18Z"}
{"id":"replication_session_123abc","state":"failed_over","role":"destination","last_sync_time":"2024-01-15T14:32:18Z"}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification (already present in example, but ensure it's not removed).
    **`{"error":"401 Unauthorized","message":"Invalid or expired token"}`** — Regenerate the DELL-EMC-TOKEN via the PowerStore management UI or API authentication endpoint and update the header.
    **`{"error":"409 Conflict","message":"Replication session is not in synchronized state"}`** — Wait for the sync operation to complete and verify `state=synchronized` before attempting failover.
## Metro Volume Operations

### Promote a Metro Volume (Site Failure)

![Promote a Metro Volume (Site Failure)](../../../../../assets/powerstore-proc-promote-a-metro-volume-site-failure.svg)

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


```text title="Expected output"
{
  "entries": [
    {
      "id": "repl_sess_00000000000000001",
      "name": "metro-prod-db-01",
      "state": "Primary_With_No_Secondary"
    },
    {
      "id": "repl_sess_00000000000000002",
      "name": "metro-prod-db-02",
      "state": "Primary_With_No_Secondary"
    },
    {
      "id": "repl_sess_00000000000000003",
      "name": "metro-prod-app-01",
      "state": "Primary_With_No_Secondary"
    }
  ]
}

{
  "id": "repl_sess_00000000000000001",
  "name": "metro-prod-db-01",
  "state": "Primary",
  "role": "Primary",
  "remote_system_id": "PS-2a3b4c5d6e7f8g9h",
  "last_sync_time": "2024-01-15T14:32:18Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the PowerStore management certificate into your CA bundle.
    **`{"error_code":401,"message":"Invalid or expired token"}`** — Regenerate the API token via PowerStore management console and ensure it has not exceeded its 24-hour expiration window.
    **`{"error_code":404,"message":"Replication session not found"}`** — Verify the session ID is correct by running the GET query first to list all active replication sessions and their IDs.
### Resync After Site Recovery

![Resync After Site Recovery](../../../../../assets/powerstore-proc-resync-after-site-recovery.svg)

```bash
# After primary site recovery, resync Metro Volume
# This operation resyncs data from the current primary (secondary site) back to the original primary
curl -k -X POST "https://<primary-mgmt-ip>/api/rest/replication_session/<session-id>/resync" \
  -H "DELL-EMC-TOKEN: <token>"
```


```text title="Expected output"
HTTP/1.1 202 Accepted
Content-Type: application/json
Content-Length: 342
Connection: keep-alive
Date: Thu, 15 Feb 2024 14:32:18 GMT

{
  "id": "repl_sess_12345abcde",
  "name": "metro-vol-prod-01",
  "state": "resynchronizing",
  "progress_percentage": 0,
  "estimated_completion_time": "2024-02-15T15:47:22Z",
  "source_appliance_id": "A1-node-02",
  "destination_appliance_id": "A1-node-01",
  "last_sync_timestamp": "2024-02-15T14:32:18Z"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to skip certificate verification (already present in the example, but ensure it's not removed in production variants).
    **`{"error": "401 Unauthorized", "message": "Invalid or expired DELL-EMC-TOKEN"}`** — Regenerate the authentication token via the PowerStore management interface and update the header value.
    **`{"error": "404 Not Found", "message": "Replication session <session-id> not found"}`** — Verify the session ID matches an active Metro Volume replication session using `GET /api/rest/replication_session` to list all sessions.
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


```text title="Expected output"
{
  "entries": [
    {
      "id": "nas_1",
      "name": "nas-prod-01",
      "current_node": "spa",
      "preferred_node": "spa"
    }
  ]
}
{
  "id": "nas_1",
  "name": "nas-prod-01",
  "current_node": "spa",
  "state": "Failover_In_Progress"
}
{
  "id": "nas_1",
  "name": "nas-prod-01",
  "current_node": "spb",
  "preferred_node": "spa"
}
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to bypass certificate validation, or import the management certificate into your CA bundle.
    **`{"statusCode":401,"messages":["Authentication failed"]}`** — Verify the DELL-EMC-TOKEN is valid and not expired; regenerate it from the management UI if necessary.
    **`{"statusCode":409,"messages":["NAS server is already in failover state"]}`** — Wait for the previous failover operation to complete before initiating another one; check current state with the GET query.
NFS clients experience a brief interruption (seconds) during NAS server failover. SMB clients may require re-mounting depending on the session timeout configuration.

---

### Manage Protection Policies

![Manage Protection Policies](../../../../../assets/powerstore-proc-manage-protection-policies.svg)

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


```text title="Expected output"
Protection Policy List:
ID                                   Name                 Type           Replication  Snapshot
550e8400-e29b-41d4-a716-446655440000 daily-backup         Snapshot       Disabled     Enabled
550e8400-e29b-41d4-a716-446655440001 hourly-repl          Replication    Enabled      Enabled
550e8400-e29b-41d4-a716-446655440002 archive-policy       Snapshot       Disabled     Enabled

Snapshot Rules:
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440010",
    "name": "hourly-snapshots",
    "interval": 3600,
    "retention_days": 7
  },
  {
    "id": "550e8400-e29b-41d4-a716-446655440011",
    "name": "daily-snapshots",
    "interval": 86400,
    "retention_days": 30
  }
]

Volume Protection Policy Assignment:
{
  "id": "550e8400-e29b-41d4-a716-446655440100",
  "name": "prod-volume-01",
  "protection_policy_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "OK"
}
```

!!! warning "Common errors"
    **`pstcli: command not found`** — Install the PowerStore CLI package or add it to your PATH environment variable.
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add the `-k` flag to bypass SSL verification or import the management server's certificate into your trust store.
    **`{"error": "Invalid token or token expired"}`** — Regenerate the DELL-EMC-TOKEN using the authentication endpoint and ensure it hasn't exceeded its expiration time.
GUI path: Protection → Protection Policies → Create. Assign snapshot rule (name, interval, retained copies) and optional replication rule. Assign policy to volumes via Volumes → select volume → Protection → Assign Policy. Snapshots begin on the defined schedule immediately after assignment.

### Volume Migration (Import / Mobility)

![Volume Migration (Import / Mobility)](../../../../../assets/powerstore-proc-volume-migration-import-mobility.svg)

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


```text title="Expected output"
{
  "id": "volume_1a2b3c4d",
  "name": "prod-db-vol-01",
  "size": 1099511627776,
  "appliance_id": "A1-DAE-PS01",
  "storage_tier": "Performance",
  "state": "ready",
  "creation_timestamp": "2024-01-15T09:23:47Z"
}
{
  "import_sessions": [
    {
      "id": "import_sess_789xyz",
      "source_id": "array_legacy_01",
      "state": "running",
      "progress_percentage": 67,
      "estimated_completion": "2024-01-15T14:30:00Z"
    },
    {
      "id": "import_sess_456abc",
      "source_id": "array_legacy_02",
      "state": "completed",
      "progress_percentage": 100,
      "completion_timestamp": "2024-01-14T22:15:33Z"
    }
  ]
}
```

!!! warning "Common errors"
    **`{"error": "Unauthorized", "code": 401, "message": "Invalid or expired token"}`** — Regenerate the DELL-EMC-TOKEN using the authentication endpoint and ensure it hasn't exceeded its TTL.
    **`{"error": "Not Found", "code": 404, "message": "Volume <volume-id> not found"}`** — Verify the volume ID exists on the target appliance using `curl -k -X GET "https://<mgmt-ip>/api/rest/volume" -H "DELL-EMC-TOKEN: <token>"`.
GUI path for tier change: Storage → Volumes → select volume → Modify → Storage Tier. For import from external array (VPLEX, Unity, VNX): Storage → Import → Create Import Session; select source array and volume; initiate cutover when ready. Monitor progress under Storage → Import → Active Sessions.

### NAS File System Creation and Share

![NAS File System Creation and Share](../../../../../assets/powerstore-proc-nas-file-system-creation-and-share.svg)

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


```text title="Expected output"
{"id":"nas_server_6f4a2c91-8e3f-4d7b-9c2a-1b5e8d3f7a4c","name":"nas-prod-002","current_node_id":"node-A","health":{"health_indicator":"OK"},"operational_status":"Started"}
{"id":"filesystem_8b2d5e9f-1a4c-4e7b-9d3f-2c6a8e1b5f9d","name":"dept-shares-001","nas_server_id":"nas_server_6f4a2c91-8e3f-4d7b-9c2a-1b5e8d3f7a4c","size_total":2199023255552,"size_used":0,"filesystem_type":"Primary"}
{"id":"nfs_export_3c7f1a9e-5d2b-4e8c-9a1f-6b3d8e2c5f7a","name":"dept-shares-export","filesystem_id":"filesystem_8b2d5e9f-1a4c-4e7b-9d3f-2c6a8e1b5f9d","path":"/","rw_hosts":[{"ip":"192.168.10.0","prefix_length":24}],"export_paths":["/dept-shares-export"]}
{"id":"smb_share_9e4b2f7c-1d5a-4c8e-9b2f-3a6d8c1e5f7b","name":"dept-shares","filesystem_id":"filesystem_8b2d5e9f-1a4c-4e7b-9d3f-2c6a8e1b5f9d","path":"/","unc":"\\\\nas-prod-002\\dept-shares"}
```

!!! warning "Common errors"
    **`"error_code":"INVALID_FIELD","message":"Invalid value for current_node_id"`** — Verify the node ID exists by running `curl -k -H "DELL-EMC-TOKEN: <token>" https://<mgmt-ip>/api/rest/node` and use a valid node ID from the response.
    **`"error_code":"RESOURCE_NOT_FOUND","message":"nas_server_id does not exist"`** — Replace `<nas-server-id>` with the actual ID returned from Step 1 (the "id" field in the NAS server creation response).
    **`"error_code":"INVALID_FIELD","message":"Token is invalid or expired"`** — Regenerate the DELL-EMC-TOKEN using your management console authentication endpoint and ensure it hasn't exceeded its TTL.
Verify NFS from Linux: `mount <ip>:/dept-shares-001 /mnt/test`. Verify SMB from Windows: map `\\<ip>\dept-shares`. GUI path: Storage → NAS Servers → Create; then Storage → File Systems → Create.

### Performance Policy Management

![Performance Policy Management](../../../../../assets/powerstore-proc-performance-policy-management.svg)

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


```text title="Expected output"
{
  "entries": [
    {
      "id": "policy-001a2b3c",
      "name": "default",
      "max_iops": null,
      "max_bandwidth": null,
      "created_at": "2024-01-15T08:22:11Z"
    },
    {
      "id": "policy-004d5e6f",
      "name": "prod-high-perf",
      "max_iops": 5000,
      "max_bandwidth": 524288000,
      "created_at": "2024-02-10T14:45:33Z"
    }
  ]
}
{
  "id": "policy-789ghi01",
  "name": "dev-limited",
  "max_iops": 1000,
  "max_bandwidth": 104857600,
  "created_at": "2024-03-20T09:17:42Z"
}
Volume dev-vol-01 modified successfully.
```

!!! warning "Common errors"
    **`curl: (60) SSL certificate problem: self signed certificate`** — Add `-k` flag to curl command to skip SSL verification, or import the management node's certificate into your CA bundle.
    **`{"error": "Unauthorized", "code": 401}`** — Verify the DELL-EMC-TOKEN is valid and not expired by re-authenticating with the management IP.
    **`Error: Volume <vol> not found`** — Confirm the volume name matches exactly (case-sensitive) and exists on the array using `pstcli -server <ip> -user admin volume list`.
GUI path: Storage → Storage Policies → Performance Policies → Create (set IOPS limit and/or bandwidth limit in MB/s). Assign to a volume via Volumes → Modify → Storage Policy → select performance policy. View utilisation against limits under Dashboard → Performance. A value of `0` for `max_iops` or `max_bandwidth` means unlimited.

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Powerstore — Health Checks](../health-checks/)
- [Powerstore — CLI Reference](../cli-reference/)
- [Powerstore — Common Issues](../../troubleshooting/common-issues/)
