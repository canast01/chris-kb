---
tags:
  - dell
  - operations
---
# Dell VPLEX — CLI Reference (vplexcli)

<div class="kb-summary">
`vplexcli` is the primary management interface for Dell VPLEX. Connect to the VPLEX Management Server (VMS) via SSH, then launch the shell with `vplexcli`. Commands follow a filesystem-like navigation model: objects are addressed as paths (e.g.

*Applies to: VPLEX*
</div>
![Dell VPLEX — CLI Reference (vplexcli)](../../../../assets/storage-dell-vplex-operations-cli-reference.svg)

 `/clusters/cluster-1/`) and `ll` (list-long) is the standard inspection command.

> **Access**: `ssh service@<VMS_IP>` → `vplexcli` — or run one-shot commands with `vplexcli -q -e "<command>"`.

```d2
direction: right

operator: "Operator /\nAutomation script" {shape: rectangle}
vms: "VMS\nvplexcli shell\nssh service@VMS_IP" {shape: rectangle}
unisphere: "Unisphere for VPLEX\nhttps://VMS_IP" {shape: rectangle}
directors: "VPLEX Directors\nData path components" {shape: rectangle}
arrays: "Back-end Arrays\nPowerMax / Unity" {shape: rectangle}
hosts: "Hosts\nESXi / Linux / Windows" {shape: rectangle}

operator -> vms
operator -> unisphere
vms -> directors
unisphere -> directors
directors -> arrays
directors -> hosts
```

---

## Before you begin

- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Quick-Reference Command Table

| Command | Purpose |
|---|---|
| `vplexcli -q -e "health-check"` | Overall cluster health summary |
| `vplexcli -q -e "ll /clusters/"` | List all clusters |
| `vplexcli -q -e "ll /engines/"` | List all engines (chassis) |
| `vplexcli -q -e "ll /clusters/*/health-indications/"` | Health indications across all clusters |
| `vplexcli -q -e "ll /virtual-volumes/"` | List all virtual volumes |
| `vplexcli -q -e "ll /distributed-storage/distributed-devices/"` | List Metro distributed devices |
| `vplexcli -q -e "ll /distributed-storage/consistency-groups/"` | List consistency groups |
| `vplexcli -q -e "ll /clusters/*/exports/storage-views/"` | List all storage views (masking) |
| `vplexcli -q -e "collect-support-log -f /var/log/support.tar.gz"` | Collect support bundle |

---

## Cluster and Director Status

```bash
# Launch vplexcli interactively
ssh service@<VMS_IP>
vplexcli

# --- One-shot equivalents (use in scripts) ---

# List all clusters
vplexcli -q -e "ls /clusters"

# Show cluster-1 health indications
vplexcli -q -e "ll /clusters/cluster-1/health-indications/"

# Full system health check
vplexcli -q -e "health-check"

# List all engines (physical chassis)
vplexcli -q -e "ls /engines"

# Show all directors across all engines
vplexcli -q -e "ll /engines/*/directors/"

# Show a specific director's hardware status
vplexcli -q -e "ll /engines/engine-1-1/directors/director-1-1-A/hardware/"

# List director front-end (FE) ports
vplexcli -q -e "ll /engines/engine-1-1/directors/director-1-1-A/hardware/ports/"

# Check inter-cluster link (ICL) status (Metro)
vplexcli -q -e "ll /clusters/cluster-1/communication/inter-cluster-links/"
```


```text title="Expected output"
service@vplex-vms-01:~$ ssh service@192.168.1.50
service@192.168.1.50's password: 
Last login: Wed Jan 15 14:32:18 2025 from 192.168.1.100
service@vplex-vms-01:~$ vplexcli

vplexcli> ls /clusters
  cluster-1
  cluster-2

vplexcli> ll /clusters/cluster-1/health-indications/
  health-state = ok
  operational-status = ok
  health-check-time = 2025-01-15 14:45:22
  redundancy-status = healthy

vplexcli> health-check
  Cluster cluster-1: HEALTHY
  Cluster cluster-2: HEALTHY
  All engines operational
  All directors operational
  All storage arrays reachable

vplexcli> ls /engines
  engine-1-1
  engine-2-1

vplexcli> ll /engines/*/directors/
  engine-1-1/directors/director-1-1-A
  engine-1-1/directors/director-1-1-B
  engine-2-1/directors/director-2-1-A
  engine-2-1/directors/director-2-1-B

vplexcli> ll /engines/engine-1-1/directors/director-1-1-A/hardware/
  state = operational
  temperature = 42C
  power-supply-1 = ok
  power-supply-2 = ok
  fan-status = ok

vplexcli> ll /engines/engine-1-1/directors/director-1-1-A/hardware/ports/
  port-0 = online, speed=8Gbps
  port-1 = online, speed=8Gbps
  port-2 = online, speed=8Gbps
  port-3 = online, speed=8Gbps

vplexcli> ll /clusters/cluster-1/communication/inter-cluster-links/
  icl-1 = operational, latency=2.3ms
  icl-2 = operational, latency=2.1ms
  icl-3 = operational, latency=2.4ms
```

!!! warning "Common errors"
    **`Connection refused`** — Verify the VMS IP address is correct and the VPLEX management server is running with `systemctl status vplex-vms`.
    **`Authentication failed for user 'service'`** — Confirm the service account password is current and the account has not been locked; reset via VPLEX admin console if needed.
    **`No such object: /clusters/cluster-1`** — Check cluster name spelling and confirm the cluster exists by running `ls /clusters` first.
**Key health-indication values:**

| Value | Meaning |
|---|---|
| `ok` | Component is healthy |
| `major-failure` | Fault requiring immediate action |
| `minor-failure` | Degraded but operational |
| `unknown` | Communication loss to component |

---

## Virtual Volume Management

Virtual volumes are the objects presented to hosts. They are built on top of extents → local devices → virtual volumes.

```d2
direction: right

step1: "Step 1: Claim storage volume\nstorage-volume claim --storage-volume ..." {shape: rectangle}
step2: "Step 2: Create extent\nextent create --name ext_app_001 ..." {shape: rectangle}
step3: "Step 3: Create local device\nlocal-device create --geometry raid-0 ..." {shape: rectangle}
step4: "Step 4: Create distributed device\ndistributed-device create --geometry raid-1 ..." {shape: rectangle}
step5: "Step 5: Create virtual volume\nvirtual-volume create --distributed-device ..." {shape: rectangle}
step6: "Step 6: Add to storage view\nstorage-view add-virtual-volumes ..." {shape: rectangle}
step7: "Step 7: Host sees volume\nRescan HBAs on host" {shape: rectangle}

step1 -> step2
step2 -> step3
step3 -> step4
step4 -> step5
step5 -> step6
step6 -> step7
```

```bash
# --- List all virtual volumes (one-shot) ---
vplexcli -q -e "ls /virtual-volumes"

# Show detailed attributes of a specific virtual volume
vplexcli -q -e "ll /virtual-volumes/my_app_vol_1/"

# List virtual volumes with health state
vplexcli -q -e "ll /virtual-volumes/*/health-indications/"

# --- Create a new virtual volume ---
# Step 1: Claim a back-end storage volume as a VPLEX storage volume
vplexcli -q -e "storage-volume claim --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"

# Step 2: Create an extent from the storage volume
vplexcli -q -e "extent create --name ext_app_001 --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"

# Step 3: Create a local device from the extent
vplexcli -q -e "local-device create --name dev_app_001 --geometry raid-0 --extents /clusters/cluster-1/storage-elements/extents/ext_app_001"

# Step 4: Create a virtual volume from the local device
vplexcli -q -e "virtual-volume create --name my_app_vol_1 --local-device /clusters/cluster-1/devices/dev_app_001"

# --- Expand a virtual volume ---
# First expand the back-end LUN on the array, then:
vplexcli -q -e "storage-volume rediscover --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"
vplexcli -q -e "extent expand --extent /clusters/cluster-1/storage-elements/extents/ext_app_001"
vplexcli -q -e "virtual-volume expand --virtual-volume /virtual-volumes/my_app_vol_1"

# --- Delete a virtual volume ---
# Remove from storage view first, then:
vplexcli -q -e "virtual-volume destroy --virtual-volume /virtual-volumes/my_app_vol_1 --force"
vplexcli -q -e "local-device destroy --local-device /clusters/cluster-1/devices/dev_app_001"
vplexcli -q -e "extent destroy --extent /clusters/cluster-1/storage-elements/extents/ext_app_001"
vplexcli -q -e "storage-volume unclaim --storage-volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"
```


```text title="Expected output"
my_app_vol_1
my_app_vol_2
backup_vol_prod
test_vol_ephemeral

Name                          : my_app_vol_1
Size                          : 1099511627776
Health State                  : Healthy
Operational Status            : Online
Cluster                       : cluster-1
Device                        : dev_app_001

/virtual-volumes/my_app_vol_1/health-indications/ : Healthy
/virtual-volumes/my_app_vol_2/health-indications/ : Healthy
/virtual-volumes/backup_vol_prod/health-indications/ : Healthy
/virtual-volumes/test_vol_ephemeral/health-indications/ : Healthy

Storage Volume sv_001 claimed successfully. Claim ID: 8f3a2c1d-9e4b-47c2-a1f6-5d8e2b9c4a7f
Extent ext_app_001 created successfully. Extent ID: ext-7429a8c5
Local Device dev_app_001 created successfully. Device ID: dev-5c1e9f3a
Virtual Volume my_app_vol_1 created successfully. Virtual Volume ID: vv-a4d2e8f1

Storage Volume sv_001 rediscovered. New capacity: 2199023255552
Extent ext_app_001 expanded to 2199023255552 bytes
Virtual Volume my_app_vol_1 expanded to 2199023255552 bytes

Virtual Volume my_app_vol_1 destroyed successfully
Local Device dev_app_001 destroyed successfully
Extent ext_app_001 destroyed successfully
Storage Volume sv_001 unclaimed successfully
```

!!! warning "Common errors"
    **`Error: Storage volume /storage-elements/storage-arrays/array-A/storage-volumes/sv_001 is already claimed`** — Verify the storage volume is not in use by another virtual volume or extent using `vplexcli -q -e "ll /storage-elements/storage-arrays/array-A/storage-volumes/sv_001"` before claiming.
    **`Error: Virtual volume my_app_vol_1 is in use by storage view prod-sv-001, cannot destroy`** — Remove the virtual volume from all storage views using the VPLEX management console or `storage-view remove-member` before attempting destruction.
    **`Error: Extent ext_app_001 expansion failed: backend LUN size unchanged`** — Expand the LUN size on the storage array first, then run `storage-volume rediscover` before attempting extent expansion.
---

## Distributed Device Operations (VPLEX Metro)

Distributed devices span two clusters and provide Metro active-active access. Consistency groups ensure write-order fidelity.

```bash
# List all distributed devices
vplexcli -q -e "ls /distributed-storage/distributed-devices"

# Show health of all distributed devices
vplexcli -q -e "ll /distributed-storage/distributed-devices/*/health-indications/"

# Show sync state of a specific distributed device
vplexcli -q -e "ll /distributed-storage/distributed-devices/dist_app_vol_1/"

# --- Create a distributed device (Metro) ---
# Prerequisite: local devices exist on both cluster-1 and cluster-2
vplexcli -q -e "distributed-device create \
  --name dist_app_vol_1 \
  --geometry raid-1 \
  --components /clusters/cluster-1/devices/dev_app_001,/clusters/cluster-2/devices/dev_app_002"

# Create a virtual volume on top of the distributed device
vplexcli -q -e "virtual-volume create --name app_vol_metro_1 \
  --distributed-device /distributed-storage/distributed-devices/dist_app_vol_1"

# --- Consistency groups ---
# List all consistency groups
vplexcli -q -e "ls /distributed-storage/consistency-groups"

# Show consistency group details
vplexcli -q -e "ll /distributed-storage/consistency-groups/cg_app_tier/"

# Create a consistency group
vplexcli -q -e "consistency-group create --name cg_app_tier"

# Add a virtual volume to a consistency group
vplexcli -q -e "consistency-group add-virtual-volumes \
  --consistency-group /distributed-storage/consistency-groups/cg_app_tier \
  --virtual-volumes /virtual-volumes/app_vol_metro_1"

# Remove a volume from a consistency group
vplexcli -q -e "consistency-group remove-virtual-volumes \
  --consistency-group /distributed-storage/consistency-groups/cg_app_tier \
  --virtual-volumes /virtual-volumes/app_vol_metro_1"

# --- Metro node / Witness status ---
# Check Witness connectivity
vplexcli -q -e "ll /clusters/cluster-1/cluster-witness/"
vplexcli -q -e "ll /clusters/cluster-2/cluster-witness/"
```


```text title="Expected output"
/distributed-storage/distributed-devices/dist_app_vol_1
/distributed-storage/distributed-devices/dist_app_vol_2
/distributed-storage/distributed-devices/dist_app_vol_3

/distributed-storage/distributed-devices/dist_app_vol_1/health-indications/
    health-state: OK
/distributed-storage/distributed-devices/dist_app_vol_2/health-indications/
    health-state: OK
/distributed-storage/distributed-devices/dist_app_vol_3/health-indications/
    health-state: DEGRADED

    name: dist_app_vol_1
    geometry: raid-1
    sync-state: SYNCED
    operational-status: OK
    cluster-1-device: /clusters/cluster-1/devices/dev_app_001
    cluster-2-device: /clusters/cluster-2/devices/dev_app_002

Task: distributed-device create
Status: SUCCESS
Created: dist_app_vol_1

Task: virtual-volume create
Status: SUCCESS
Created: app_vol_metro_1

/distributed-storage/consistency-groups/cg_app_tier
/distributed-storage/consistency-groups/cg_db_tier
/distributed-storage/consistency-groups/cg_backup

    name: cg_app_tier
    virtual-volumes: 2
    consistency-group-state: CONSISTENT

Task: consistency-group create
Status: SUCCESS
Created: cg_app_tier

Task: consistency-group add-virtual-volumes
Status: SUCCESS

Task: consistency-group remove-virtual-volumes
Status: SUCCESS

    cluster-witness-state: CONNECTED
    witness-ip: 192.168.50.100
    witness-port: 8443
    last-heartbeat: 2024-01-15T14:32:18Z

    cluster-witness-state: CONNECTED
    witness-ip: 192.168.50.100
    witness-port: 8443
    last-heartbeat: 2024-01-15T14:32:19Z
```

!!! warning "Common errors"
    **`Error: Device /clusters/cluster-1/devices/dev_app_001 not found`** — Verify the local device exists on cluster-1 by running `vplexcli -q -e "ls /clusters/cluster-1/devices"` before creating the distributed device.
    **`Error: Consistency group /distributed-storage/consistency-groups/cg_app_tier already exists`** — Use a unique consistency group name or delete the existing group first with `vplexcli -q -e "consistency-group delete --consistency-group /distributed-storage/consistency-groups/cg_app_tier"`.
    **`Error: Witness connectivity lost on cluster-2`** — Check network connectivity between the cluster and witness node, and verify witness service is running with `systemctl status witness-service` on the witness appliance.
**Distributed device health states:**

| State | Meaning |
|---|---|
| `in-sync` | Both legs healthy; Metro active-active |
| `rebuilding` | Resync in progress after ICL interruption |
| `degraded` | One leg is unreachable; single-site I/O only |
| `detached` | Both legs disconnected; I/O suspended |

---

## Storage Views (Host Masking)

Storage views map virtual volumes to host initiator ports via VPLEX front-end ports.

```bash
# List all storage views on cluster-1
vplexcli -q -e "ls /clusters/cluster-1/exports/storage-views"

# Show full details of a storage view
vplexcli -q -e "ll /clusters/cluster-1/exports/storage-views/sv_esxi_host_01/"

# List registered initiator ports on cluster-1
vplexcli -q -e "ls /clusters/cluster-1/exports/ports"

# List all initiator ports (host HBAs)
vplexcli -q -e "ls /clusters/cluster-1/exports/initiator-ports"

# --- Create a new storage view ---
# Step 1: Register host initiator port (WWN)
vplexcli -q -e "initiator-port register \
  --cluster /clusters/cluster-1 \
  --port-wwn 10:00:00:00:c9:ab:cd:ef \
  --name esxi_host_01_hba0"

# Step 2: Create the storage view
vplexcli -q -e "storage-view create \
  --name sv_esxi_host_01 \
  --cluster /clusters/cluster-1"

# Step 3: Add VPLEX front-end ports to the storage view
vplexcli -q -e "storage-view add-ports \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 \
  --ports /clusters/cluster-1/exports/ports/A0-FC00,/clusters/cluster-1/exports/ports/B0-FC00"

# Step 4: Add initiator ports (host HBAs) to the storage view
vplexcli -q -e "storage-view add-initiator-ports \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 \
  --initiator-ports /clusters/cluster-1/exports/initiator-ports/esxi_host_01_hba0"

# Step 5: Add virtual volumes to the storage view
vplexcli -q -e "storage-view add-virtual-volumes \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 \
  --virtual-volumes /virtual-volumes/app_vol_metro_1"

# --- Modify an existing storage view ---
# Add a second initiator (e.g. after HBA replacement)
vplexcli -q -e "storage-view add-initiator-ports \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 \
  --initiator-ports /clusters/cluster-1/exports/initiator-ports/esxi_host_01_hba1"

# Remove a virtual volume from a storage view (before deleting the volume)
vplexcli -q -e "storage-view remove-virtual-volumes \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 \
  --virtual-volumes /virtual-volumes/app_vol_metro_1"

# Delete a storage view
vplexcli -q -e "storage-view destroy \
  --storage-view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 --force"
```


```text title="Expected output"
sv_esxi_host_01
sv_esxi_host_02
sv_sql_cluster_01
sv_kubernetes_01

Name:                          sv_esxi_host_01
Cluster:                       /clusters/cluster-1
Storage View ID:               sv-esxi-host-01-a1b2c3d4
Initiator Ports:               esxi_host_01_hba0, esxi_host_01_hba1
Front-end Ports:               A0-FC00, B0-FC00
Virtual Volumes:               app_vol_metro_1, app_vol_metro_2
LUN Assignments:               LUN 0, LUN 1

A0-FC00
A1-FC00
B0-FC00
B1-FC00

esxi_host_01_hba0
esxi_host_01_hba1
sql_cluster_hba0
kubernetes_node_hba0

Initiator port registered: 10:00:00:00:c9:ab:cd:ef (esxi_host_01_hba0)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
(no output — command completes silently)
Storage view sv_esxi_host_01 destroyed successfully
```

!!! warning "Common errors"
    **`Error: Storage view /clusters/cluster-1/exports/storage-views/sv_esxi_host_01 not found`** — Verify the storage view name and cluster path are correct using `ls /clusters/cluster-1/exports/storage-views`.
    **`Error: Initiator port 10:00:00:00:c9:ab:cd:ef already registered`** — Use a different WWN or query existing initiator ports with `ls /clusters/cluster-1/exports/initiator-ports` to avoid duplicates.
    **`Error: Cannot destroy storage view with virtual volumes still assigned`** — Remove all virtual volumes from the storage view before deletion using the `remove-virtual-volumes` command.
---

## Data Migration

VPLEX can migrate data non-disruptively between back-end arrays using the data-migration feature.

```bash
# List active migrations
vplexcli -q -e "ls /data-migrations"

# Show status of all migrations
vplexcli -q -e "ll /data-migrations/*/status/"

# --- Start a non-disruptive migration ---
# Step 1: Claim the target (destination) storage volume
vplexcli -q -e "storage-volume claim \
  --storage-volume /storage-elements/storage-arrays/array-B/storage-volumes/sv_target_001"

# Step 2: Create the migration job (source → target)
vplexcli -q -e "data-migration create \
  --name mig_app_vol_1 \
  --virtual-volume /virtual-volumes/my_app_vol_1 \
  --target-storage-volume /storage-elements/storage-arrays/array-B/storage-volumes/sv_target_001"

# Step 3: Start the migration
vplexcli -q -e "data-migration start \
  --migration /data-migrations/mig_app_vol_1"

# --- Monitor migration progress ---
vplexcli -q -e "ll /data-migrations/mig_app_vol_1/"

# Step 4: Commit migration (cut over to target; source released)
vplexcli -q -e "data-migration commit \
  --migration /data-migrations/mig_app_vol_1"

# Step 5: Clean up the migration object
vplexcli -q -e "data-migration destroy \
  --migration /data-migrations/mig_app_vol_1"
```


```text title="Expected output"
/data-migrations/mig_app_vol_1
/data-migrations/mig_app_vol_2
/data-migrations/mig_legacy_db

/data-migrations/mig_app_vol_1/status/                    COMMITTED
/data-migrations/mig_app_vol_2/status/                    IN_PROGRESS
/data-migrations/mig_legacy_db/status/                    IDLE

Storage volume /storage-elements/storage-arrays/array-B/storage-volumes/sv_target_001 claimed successfully.

Migration mig_app_vol_1 created.
  Source: /virtual-volumes/my_app_vol_1
  Target: /storage-elements/storage-arrays/array-B/storage-volumes/sv_target_001
  Status: CREATED

Migration mig_app_vol_1 started.

/data-migrations/mig_app_vol_1/
  name                                    mig_app_vol_1
  status                                  IN_PROGRESS
  progress_percent                        67
  bytes_migrated                          4294967296
  bytes_total                             6442450944
  estimated_time_remaining_seconds        180

Migration mig_app_vol_1 committed successfully. Cutover complete.

Migration mig_app_vol_1 destroyed.
```

!!! warning "Common errors"
    **`Error: Storage volume /storage-elements/storage-arrays/array-B/storage-volumes/sv_target_001 is already claimed`** — Release the volume first with `vplexcli -q -e "storage-volume unclaim --storage-volume <path>"` or choose an unclaimed target volume.
    **`Error: Virtual volume /virtual-volumes/my_app_vol_1 is already involved in an active migration`** — Wait for the existing migration to complete or destroy it with `data-migration destroy` before creating a new one.
    **`Error: Cannot commit migration mig_app_vol_1: migration is not in IN_PROGRESS state`** — Verify the migration has started and reached sufficient progress with `ll /data-migrations/mig_app_vol_1/` before attempting commit.
---

## Logs and Diagnostics

```bash
# Show all system alerts
vplexcli -q -e "ll /clusters/*/system-volumes/alerts/"

# View VPLEX management server logs (from VMS OS shell)
ssh service@<VMS_IP>
tail -f /var/log/VPlex/cli/vplexcli.log
tail -f /var/log/VPlex/vplexmanagement.log

# --- Collect support log bundle ---
# From within vplexcli:
collect-support-log -f /var/log/support_bundle.tar.gz

# From VMS OS shell (copy to a remote host):
scp service@<VMS_IP>:/var/log/support_bundle.tar.gz admin@<jump_host>:/tmp/

# --- Show GeoSynchrony (firmware) version ---
vplexcli -q -e "ll /clusters/cluster-1/system-volumes/version/"

# Show back-end storage array inventory
vplexcli -q -e "ls /storage-elements/storage-arrays"
vplexcli -q -e "ll /storage-elements/storage-arrays/array-A/"

# Check unclaimed storage volumes on a back-end array
vplexcli -q -e "ls /storage-elements/storage-arrays/array-A/storage-volumes"
```


```text title="Expected output"
# Show all system alerts
/clusters/cluster-1/system-volumes/alerts/
  alert-001 (severity: warning, timestamp: 2024-01-15T09:23:47Z)
  alert-002 (severity: info, timestamp: 2024-01-15T08:15:22Z)

# View VPLEX management server logs
service@vplex-vms-01's password: 
==> /var/log/VPlex/cli/vplexcli.log <==
2024-01-15 09:45:12 [INFO] vplexcli session started from 10.50.20.15
2024-01-15 09:45:18 [DEBUG] Command: ll /clusters/cluster-1/system-volumes/alerts/
2024-01-15 09:45:19 [INFO] Query completed successfully

==> /var/log/VPlex/vplexmanagement.log <==
2024-01-15 09:44:55 [INFO] VPLEX Management Server v7.3.1.0 running
2024-01-15 09:45:01 [INFO] Cluster cluster-1 status: HEALTHY
2024-01-15 09:45:10 [INFO] Storage array array-A connectivity: OPTIMAL

# Collect support log bundle
Collecting support logs... [████████████████████] 100%
Support bundle created: /var/log/support_bundle.tar.gz (287 MB)

# Copy to jump host
support_bundle.tar.gz                    100%  287MB   45.2MB/s   00:06

# Show GeoSynchrony version
/clusters/cluster-1/system-volumes/version/
  firmware-version: 8.4.2.1
  build-number: 20240110-1847
  release-date: 2024-01-10

# Show back-end storage array inventory
/storage-elements/storage-arrays/
  array-A
  array-B
  array-C

/storage-elements/storage-arrays/array-A/
  vendor: EMC
  model: VMAX-250F
  serial-number: 000298701234
  total-capacity: 50 TB
  status: ONLINE

# Check unclaimed storage volumes
/storage-elements/storage-arrays/array-A/storage-volumes/
  vol-001 (size: 500GB, status: unclaimed)
  vol-002 (size: 500GB, status: unclaimed)
  vol-003 (size: 1TB, status: claimed)
  vol-004 (size: 500GB, status: unclaimed)
```

!!! warning "Common errors"
    **`Connection refused`** — Verify the VMS IP address is correct and SSH service is running on port 22 with `ssh -v service@<VMS_IP>`.
    **`Permission denied (publickey,password)`** — Ensure the service account password is correct or add your SSH public key to `/home/service/.ssh/authorized_keys` on the VMS.
    **`vplexcli: command not found`** — Source the VPLEX CLI environment or add `/opt/VPlex/bin` to your PATH with `export PATH=$PATH:/opt/VPlex/bin`.
---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

---

## See also

- [Vplex — Procedures](../procedures/)
- [Vplex — Scripts](../scripts/)
- [Vplex — Health Checks](../health-checks/)
