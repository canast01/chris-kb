---
tags:
  - dell
  - deployment
search:
  boost: 1.5
---
# Dell VPLEX — Initial Deployment

<div class="kb-summary">
Dell VPLEX initial deployment: physical installation, backend array connection, virtual volume creation, and validated host access — Local and Metro configurations covered.

*Applies to: VPLEX 6.x*
</div>

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
rack_and_cable: "Rack and Cable" {shape: rectangle}
vplex_management_cli_initial_setup: "VPLEX Management CLI Initial Setup" {shape: rectangle}
connect_backend_storage_arrays: "Connect Backend Storage Arrays" {shape: rectangle}
create_storage_volumes_and_extents: "Create Storage Volumes and Extents" {shape: rectangle}
create_virtual_volumes: "Create Virtual Volumes" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> rack_and_cable
rack_and_cable -> vplex_management_cli_initial_setup
vplex_management_cli_initial_setup -> connect_backend_storage_arrays
connect_backend_storage_arrays -> create_storage_volumes_and_extents
create_storage_volumes_and_extents -> create_virtual_volumes
create_virtual_volumes -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

This guide covers the initial deployment of a Dell VPLEX (Local or Metro) from physical installation through validated host access to virtual volumes. VPLEX provides storage federation — presenting storage from backend arrays as virtual volumes to hosts, with optional Metro mirroring across two sites.

---

## Prerequisites

**Hardware and infrastructure:**

- VPLEX engine (VS2 or VS6) — each engine contains two clusters (director pairs) for Metro configurations
- Dual-controller chassis per site with redundant power
- 16Gb or 32Gb FC switches at each site — VPLEX requires dedicated FC zoning between:
  - VPLEX back-end ports to backend array ports
  - Host HBA ports to VPLEX front-end ports
- FC SAN zoning plan prepared before racking (VPLEX uses strict zone separation between front-end and back-end)
- For VPLEX Metro: WAN connectivity between sites with latency under 10ms round-trip (synchronous write requirement)

**Backend array requirements:**

- Backend arrays must be supported — Dell PowerMax, Unity, PowerStore, or legacy VNX
- Dedicated LUNs created on the backend array for VPLEX consumption (these become "extents" in VPLEX terminology)
- Backend array FC ports zoned to VPLEX back-end initiator ports (not host ports)

**Management:**

- VPLEX Management Server (VMS) — a dedicated Linux VM that hosts the VPLEX management software and communicates with the VPLEX directors via the management Ethernet
- NTP server accessible from VMS and VPLEX management interfaces
- IP addresses reserved for: VMS, each director's management interface, each cluster management VIP

---

## Rack and Cable

1. Mount the VPLEX engine into the rack. The VS2 engine is a 7U chassis; position it with sufficient airflow clearance front and rear.
2. Connect dual PDU power to each power shelf in the chassis — use separate circuit feeds for each shelf.
3. Connect management Ethernet from each director's management port to the OOB management switch. VPLEX VS2 has two directors; each has its own management IP.
4. Connect FC cabling:
   - **Back-end ports** (labeled BE) to the backend storage array FC ports via the SAN fabric.
   - **Front-end ports** (labeled FE) to the host FC zones via the SAN fabric.
   - Back-end and front-end ports must be in separate SAN zones — never mix front-end initiators into back-end zones.
5. For Metro configurations: connect the WAN inter-cluster link (ICL) — typically dedicated FC or IP links between the two VPLEX engines.
6. Power on the engine. Directors boot in sequence and take 10–15 minutes to reach a ready state.

---

## VPLEX Management CLI Initial Setup

VPLEX management is done via the VMS CLI (`management-server` commands) or the VPLEX Management Console (VPLEXMC) web interface running on the VMS.

**Install the VMS (Management Server):**

1. Deploy the VMS VM on a VMware host using the OVA provided by Dell. Minimum specs: 4 vCPU, 16 GB RAM, 200 GB disk.
2. Power on the VM. During boot it prompts for the initial IP configuration:

```text
VMS IP address: 192.168.1.30
Netmask: 255.255.255.0
Gateway: 192.168.1.1
```

3. SSH to the VMS as `root` once it is reachable.
4. Configure VPLEX director connectivity — VMS must reach each director's management IP:

```bash
vplexcli -h <director1_mgmt_ip> -u admin -p <password> -q "ll /clusters/*"
```


```text title="Expected output"
Cluster: cluster-1
  Director: director-1a (10.50.12.45)
  Director: director-1b (10.50.12.46)
  Status: Online
  Version: 6.2.1.0-20231015
  Witness: witness-1 (10.50.12.50)

Cluster: cluster-2
  Director: director-2a (10.50.13.45)
  Director: director-2b (10.50.13.46)
  Status: Online
  Version: 6.2.1.0-20231015
  Witness: witness-2 (10.50.13.50)
```

!!! warning "Common errors"
    **`Connection refused: Unable to connect to 10.50.12.45:443`** — Verify the director management IP is correct and the VPLEX management interface is reachable on port 443.
    **`Authentication failed: Invalid credentials for user 'admin'`** — Confirm the admin password is correct and the user account has not been locked after failed login attempts.
    **`Command not found: vplexcli`** — Ensure the VPLEX CLI tools are installed and the installation directory is in your system PATH.
**Connect VMS to VPLEX directors:**

```bash
# From VMS CLI
management-server connect --host <director1_ip> --username admin --password <password>
management-server connect --host <director2_ip> --username admin --password <password>
```


```text title="Expected output"
Connected to director1.vplex.local (192.168.1.50) as admin
Cluster: vplex-cluster-01
Build: 6.1.2.0-20231015
Session ID: 550e8400-e29b-41d4-a716-446655440000
Connected to director2.vplex.local (192.168.1.51) as admin
Cluster: vplex-cluster-01
Build: 6.1.2.0-20231015
Session ID: 550e8400-e29b-41d4-a716-446655440001
```

!!! warning "Common errors"
    **`Connection refused: Unable to reach <director1_ip>:443`** — Verify the director IP address is correct and the management network is reachable with `ping <director1_ip>`.
    **`Authentication failed: Invalid credentials for user admin`** — Confirm the password is correct and the admin account is not locked by checking director logs or resetting credentials via the local console.
    **`Build mismatch: director1 (6.1.2.0) does not match director2 (6.1.1.0)`** — Upgrade both directors to the same firmware version before establishing the cluster connection.
Verify both directors appear:

```bash
vplexcli -h <director1_ip> -u admin -q "ll /engines/*/directors/*"
```


```text title="Expected output"
Director: director-1 (Active)
  Engine: engine-0
    director-1a: ONLINE, Build: 6.2.0.0.0-12345, Serial: VPX123456789
    director-1b: ONLINE, Build: 6.2.0.0.0-12345, Serial: VPX123456790
  Engine: engine-1
    director-1a: ONLINE, Build: 6.2.0.0.0-12345, Serial: VPX123456791
    director-1b: ONLINE, Build: 6.2.0.0.0-12345, Serial: VPX123456792

Director: director-2 (Standby)
  Engine: engine-0
    director-2a: ONLINE, Build: 6.2.0.0.0-12345, Serial: VPX123456793
    director-2b: ONLINE, Build: 6.2.0.0.0-12345, Serial: VPX123456794
```

!!! warning "Common errors"
    **`Connection refused: Unable to connect to <director1_ip>:443`** — Verify the director IP is correct and reachable, and that the VPLEX management service is running with `systemctl status vplex-mgmt`.
    **`Authentication failed: Invalid credentials for user 'admin'`** — Confirm the admin password is correct and the user account is not locked; reset credentials via the VPLEX console if needed.
    **`Command not found: vplexcli`** — Ensure vplexcli is installed and in your PATH, or use the full path `/opt/vplex/bin/vplexcli`.
---

## Connect Backend Storage Arrays

VPLEX discovers backend storage through FC. Confirm backend zoning is correct before registration.

1. From the VMS CLI, list discovered backend targets:

```bash
vplexcli -q "ll /clusters/cluster-1/storage-elements/storage-arrays/*"
```


```text title="Expected output"
/clusters/cluster-1/storage-elements/storage-arrays/SAN-ARRAY-01
/clusters/cluster-1/storage-elements/storage-arrays/SAN-ARRAY-02
/clusters/cluster-1/storage-elements/storage-arrays/EMC-VMAX-03
/clusters/cluster-1/storage-elements/storage-arrays/PURE-FA-04
/clusters/cluster-1/storage-elements/storage-arrays/NETAPP-AFF-05
```

!!! warning "Common errors"
    **`Error: Connection refused (111)`** — Verify the VPLEX management IP is reachable and vplexcli service is running with `systemctl status vplex-cli`.
    **`Error: Authentication failed for user 'admin'`** — Ensure your VPLEX credentials are correct and your user account has CLI access permissions in the VPLEX management console.
2. If the backend array does not appear, verify FC zoning between VPLEX BE ports and array FA/FC target ports.
3. Register the backend array:

```bash
vplexcli -q "array register --name powermax_prod --type SYMMETRIX --wwn <array_wwn>"
```


```text title="Expected output"
Array 'powermax_prod' registered successfully
Registration ID: reg-2847-5f9c-11eb
Array Type: SYMMETRIX
WWN: 500009720a1b2c3d
Status: READY
```

!!! warning "Common errors"
    **`Error: Array with name 'powermax_prod' already exists`** — Use a unique array name or unregister the existing array first with `vplexcli -q "array unregister --name powermax_prod"`.
    **`Error: Invalid WWN format or array unreachable at <array_wwn>`** — Verify the WWN syntax matches the array's actual identifier and that network connectivity exists between VPLEX and the storage array.
4. Refresh storage discovery:

```bash
vplexcli -q "storage-array rediscover-all"
```


```text title="Expected output"
Rediscovering storage arrays...
Array: EMC VMAX (SN: 000123456789)
  Status: SUCCESS
  LUNs discovered: 247
  Capacity: 50.2 TB
Array: Dell PowerVault (SN: 000987654321)
  Status: SUCCESS
  LUNs discovered: 89
  Capacity: 12.8 TB
Rediscovery completed in 34 seconds
Total arrays processed: 2
```

!!! warning "Common errors"
    **`vplexcli: command not found`** — Ensure the VPLEX CLI tools are installed and the PATH includes the VPLEX bin directory (typically `/opt/vplex/bin`).
    **`Error: Unable to connect to VPLEX cluster at localhost:443`** — Verify the VPLEX management console is running and accessible; check network connectivity and firewall rules for port 443.
    **`Error: Invalid credentials for VPLEX authentication`** — Confirm your VPLEX user credentials are correct and have sufficient permissions to execute storage array commands.
5. Verify backend LUNs are visible as storage volumes:

```bash
vplexcli -q "ll /clusters/cluster-1/storage-elements/storage-volumes/*"
```


```text title="Expected output"
/clusters/cluster-1/storage-elements/storage-volumes/sv-001
/clusters/cluster-1/storage-elements/storage-volumes/sv-002
/clusters/cluster-1/storage-elements/storage-volumes/sv-003
/clusters/cluster-1/storage-elements/storage-volumes/sv-004
/clusters/cluster-1/storage-elements/storage-volumes/sv-005
/clusters/cluster-1/storage-elements/storage-volumes/sv-006
/clusters/cluster-1/storage-elements/storage-volumes/sv-007
/clusters/cluster-1/storage-elements/storage-volumes/sv-008
...
```

!!! warning "Common errors"
    **`Error: cluster-1 not found`** — Verify the cluster name exists with `vplexcli -q "ll /clusters"` and correct the cluster identifier.
    **`Error: Invalid path /clusters/cluster-1/storage-elements/storage-volumes`** — Ensure VPLEX management console is accessible and the cluster is online; check connectivity with `vplexcli -q "ping"`.
    **`vplexcli: command not found`** — Add the VPLEX CLI installation directory to your PATH or use the full path to the vplexcli binary.
Each LUN on the backend array appears as a storage volume with its size and backend array identifier.

---

## Create Storage Volumes and Extents

VPLEX uses a layered model: storage volumes (from backend) → extents (claimed slices) → local devices → virtual volumes.

**Claim a storage volume as an extent:**

```bash
vplexcli -q "extent create --name ext_powermax_01 --storage-volume /clusters/cluster-1/storage-elements/storage-volumes/<vol_name>"
```


```text title="Expected output"
Created extent 'ext_powermax_01'
Extent URI: /clusters/cluster-1/extents/ext_powermax_01
Storage Volume: /clusters/cluster-1/storage-elements/storage-volumes/pmax_vol_001
Capacity: 1.0 TB
Status: Available
```

!!! warning "Common errors"
    **`Error: Storage volume not found: /clusters/cluster-1/storage-elements/storage-volumes/<vol_name>`** — Replace `<vol_name>` with the actual storage volume name (e.g., `pmax_vol_001`) and verify it exists with `vplexcli -q "storage-volume list"`.
    **`Error: Extent 'ext_powermax_01' already exists`** — Use a unique extent name or delete the existing extent with `vplexcli -q "extent delete --name ext_powermax_01"` before recreating it.
**Create a local device from the extent:**

```bash
vplexcli -q "local-device create --name ldev_prod_01 --geometry raid-0 --extents /clusters/cluster-1/storage-elements/extents/ext_powermax_01"
```


```text title="Expected output"
Created local-device: ldev_prod_01
  Device Name: ldev_prod_01
  Geometry: raid-0
  Extents: /clusters/cluster-1/storage-elements/extents/ext_powermax_01
  Status: operational
  Capacity: 2.0 TB
  Created: 2024-01-15T09:42:17Z
```

!!! warning "Common errors"
    **`Error: extent /clusters/cluster-1/storage-elements/extents/ext_powermax_01 not found`** — Verify the extent exists and the path is correct using `vplexcli -q "extent list"`.
    **`Error: local-device ldev_prod_01 already exists`** — Choose a unique device name or delete the existing device with `vplexcli -q "local-device delete --name ldev_prod_01"` first.
    **`Error: cluster-1 is not accessible`** — Ensure the cluster is online and reachable by running `vplexcli -q "cluster list"` to verify cluster status.
For RAID-1 (mirrored local device from two extents):

```bash
vplexcli -q "local-device create --name ldev_prod_01 --geometry raid-1 --extents /clusters/cluster-1/storage-elements/extents/ext_a,/clusters/cluster-1/storage-elements/extents/ext_b"
```


```text title="Expected output"
Created local device: ldev_prod_01
  Device ID: 6a8f2c1e-4d92-11ed-b878-001a6b88c0a1
  Geometry: raid-1
  Extents: 2
  Status: Online
  Capacity: 2.0 TB
  Thin Enabled: false
```

!!! warning "Common errors"
    **`Error: Extent /clusters/cluster-1/storage-elements/extents/ext_a not found`** — Verify extent names exist using `vplexcli -q "extent list"` and correct the path syntax.
    **`Error: Device ldev_prod_01 already exists`** — Use a unique device name or delete the existing device with `vplexcli -q "local-device delete --name ldev_prod_01"` first.
    **`Error: Extents must be from the same storage element`** — Ensure both extents are provisioned from the same storage array and cluster path.
---

## Create Virtual Volumes

A virtual volume is the storage object presented to hosts. It is built on top of a local device.

```bash
vplexcli -q "virtual-volume create --name vvol_sql01_data --local-device /clusters/cluster-1/local-devices/ldev_prod_01"
```


```text title="Expected output"
Virtual Volume vvol_sql01_data created successfully
  Name: vvol_sql01_data
  Cluster: cluster-1
  Local Device: ldev_prod_01
  Size: 500GB
  Status: Available
  Visibility: Local
```

!!! warning "Common errors"
    **`Error: Local device /clusters/cluster-1/local-devices/ldev_prod_01 not found`** — Verify the local device exists and the path is correct using `vplexcli -q "local-device list"`.
    **`Error: Virtual volume name vvol_sql01_data already exists`** — Choose a unique virtual volume name or delete the existing volume before recreating it.
For Metro configurations, promote the virtual volume to a distributed device (mirrors the local device to the remote cluster):

```bash
vplexcli -q "distributed-device create --name dd_sql01 --local-device-1 /clusters/cluster-1/local-devices/ldev_prod_01 --local-device-2 /clusters/cluster-2/local-devices/ldev_remote_01 --virtual-volume vvol_sql01_data"
```


```text title="Expected output"
Command: distributed-device create
Status: SUCCESS
Distributed Device Name: dd_sql01
Local Device 1: /clusters/cluster-1/local-devices/ldev_prod_01
Local Device 2: /clusters/cluster-2/local-devices/ldev_remote_01
Virtual Volume: vvol_sql01_data
Device ID: 5a3f8c2e-91b4-4d7a-b2c1-7e9f3a6d4b1c
Creation Time: 2024-01-15T14:32:47Z
Synchronization Status: IN_PROGRESS
```

!!! warning "Common errors"
    **`Error: Local device /clusters/cluster-1/local-devices/ldev_prod_01 not found`** — Verify the local device path exists using `vplexcli -q "local-device list"` and correct the path syntax.
    **`Error: Virtual volume vvol_sql01_data is already in use`** — Choose a different virtual volume name or remove the existing mapping with `vplexcli -q "virtual-volume delete --name vvol_sql01_data"`.
    **`Error: Cluster-2 is unreachable or not synchronized`** — Check cluster connectivity and witness status with `vplexcli -q "cluster status"` before retrying the command.
Verify virtual volume:

```bash
vplexcli -q "ll /clusters/cluster-1/virtual-volumes/vvol_sql01_data"
```


```text title="Expected output"
Name                           Size      Visibility  Cluster      Storage-Container
vvol_sql01_data                2.0TB     cluster-1   cluster-1    storage-container-01
  Extents:
    extent-001                 1.0TB     local       cluster-1    storage-container-01
    extent-002                 1.0TB     local       cluster-1    storage-container-01
  Attributes:
    thin_enabled               false
    replication_enabled        true
    consistency_group_id       cg-sql-prod-001
```

!!! warning "Common errors"
    **`Error: Virtual volume 'vvol_sql01_data' not found`** — Verify the virtual volume name is correct and exists in the cluster using `vplexcli -q "ll /clusters/cluster-1/virtual-volumes"`.
    **`Error: Connection refused to management server`** — Ensure the VPLEX management console is running and accessible; check network connectivity and VPLEX service status with `systemctl status vplex-mgmt`.
    **`Error: Authentication failed for user`** — Verify your VPLEX credentials are valid and your user account has sufficient permissions to query virtual volumes.
---

## Expose to Host Clusters

VPLEX uses storage views (analogous to masking views) to present virtual volumes to host initiators.

**Register host initiators:**

```bash
vplexcli -q "initiator-port register --name host_esxi01_a --wwn 10:00:00:90:fa:12:34:56"
vplexcli -q "initiator-port register --name host_esxi01_b --wwn 10:00:00:90:fa:12:34:57"
```


```text title="Expected output"
Initiator port 'host_esxi01_a' registered successfully with WWN 10:00:00:90:fa:12:34:56
Initiator port 'host_esxi01_b' registered successfully with WWN 10:00:00:90:fa:12:34:57
```

!!! warning "Common errors"
    **`Error: Initiator port 'host_esxi01_a' already exists`** — Use `initiator-port unregister --name host_esxi01_a` first, or choose a unique initiator port name.
    **`Error: Invalid WWN format '10:00:00:90:fa:12:34:56'`** — Ensure WWN uses colons as separators and contains exactly 16 hexadecimal characters (8 pairs).
    **`Error: VPLEX cluster unreachable or vplexcli not authenticated`** — Verify VPLEX management IP is reachable and run `vplexcli --login` to authenticate before executing commands.
**Create an initiator group:**

```bash
vplexcli -q "initiator-port create-tag --tag IG_ESX01 --initiators /clusters/cluster-1/exports/initiator-ports/host_esxi01_a,/clusters/cluster-1/exports/initiator-ports/host_esxi01_b"
```


```text title="Expected output"
Created initiator tag: IG_ESX01
  Initiators:
    - /clusters/cluster-1/exports/initiator-ports/host_esxi01_a
    - /clusters/cluster-1/exports/initiator-ports/host_esxi01_b
  Created: 2024-01-15T09:42:33Z
  Status: active
```

!!! warning "Common errors"
    **`Error: Initiator port not found: /clusters/cluster-1/exports/initiator-ports/host_esxi01_a`** — Verify the initiator port paths exist by running `vplexcli -q "initiator-port list"` and use the correct URIs.
    **`Error: Tag 'IG_ESX01' already exists`** — Either delete the existing tag with `vplexcli -q "initiator-port delete-tag --tag IG_ESX01"` or use a unique tag name.
    **`Error: Invalid cluster reference: /clusters/cluster-1`** — Confirm the cluster name with `vplexcli -q "cluster list"` and update the path accordingly.
**Create a storage view:**

```bash
vplexcli -q "storage-view create --name SV_ESX01 --ports /clusters/cluster-1/exports/ports/<FE_port_name> --virtual-volumes /clusters/cluster-1/virtual-volumes/vvol_sql01_data --initiators /clusters/cluster-1/exports/initiator-ports/host_esxi01_a,/clusters/cluster-1/exports/initiator-ports/host_esxi01_b"
```


```text title="Expected output"
Created storage view: SV_ESX01
  Name: SV_ESX01
  Ports: /clusters/cluster-1/exports/ports/FE_port_0
  Virtual Volumes: /clusters/cluster-1/virtual-volumes/vvol_sql01_data
  Initiators: /clusters/cluster-1/exports/initiator-ports/host_esxi01_a
             /clusters/cluster-1/exports/initiator-ports/host_esxi01_b
  LUN: 0
  Status: online
```

!!! warning "Common errors"
    **`Error: Invalid virtual volume path '/clusters/cluster-1/virtual-volumes/vvol_sql01_data'`** — Verify the virtual volume exists by running `vplexcli -q "virtual-volumes list"` and use the correct path.
    **`Error: Initiator port not found: /clusters/cluster-1/exports/initiator-ports/host_esxi01_a`** — Confirm initiator ports are registered in VPLEX by running `vplexcli -q "initiator-ports list"` and correct the paths.
    **`Error: Storage view 'SV_ESX01' already exists`** — Use a unique storage view name or delete the existing view with `vplexcli -q "storage-view delete --name SV_ESX01"` first.
The virtual volume is now presented to the host. Rescan from the host:

```bash
rescan-scsi-bus.sh
multipath -ll
# Should show the VPLEX virtual volume (device model: "VPLEX")
```


```text title="Expected output"
Scanning for new SCSI devices...
Scanning host 0...
Scanning host 1...
Scanning host 2...
Scanning host 3...
Done.

size=100G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 2:0:0:0 sdb 65:0  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 3:0:0:0 sdc 65:32 active ready running

size=500G features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 4:0:0:0 sdd 65:48 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 5:0:0:0 sde 65:80 active ready running
```

!!! warning "Common errors"
    **`rescan-scsi-bus.sh: command not found`** — Install sg3-utils package with `apt-get install sg3-utils` or `yum install sg3-utils`.
    **`multipath: command not found`** — Install device-mapper-multipath with `apt-get install multipath-tools` or `yum install device-mapper-multipath`.
---

## Validate Metro/Local Configuration

**Local configuration validation:**

```bash
vplexcli -q "virtual-volume health --name vvol_sql01_data"
# Operational state should show "ok"
vplexcli -q "local-device health --name ldev_prod_01"
```


```text title="Expected output"
Virtual Volume: vvol_sql_data
  Operational State: ok
  Health State: ok
  Capacity: 2.0 TB
  Used Capacity: 1.8 TB
  Thin Provisioning: disabled

Local Device: ldev_prod_01
  Operational State: ok
  Health State: ok
  Device Type: VMAX
  Capacity: 1.0 TB
  Visibility: local
```

!!! warning "Common errors"
    **`Error: Virtual volume 'vvol_sql01_data' not found`** — Verify the virtual volume name with `vplexcli -q "virtual-volumes"` and correct any typos in the name parameter.
    **`Error: Connection refused to VPLEX management server`** — Ensure the VPLEX cluster is reachable and vplexcli is configured with the correct management IP address in `/etc/vplexcli.conf`.
**Metro configuration validation:**

1. Verify the distributed device is synchronized between both clusters:

```bash
vplexcli -q "ll /distributed-storage/distributed-devices/dd_sql01"
# Operational state: "online", Rebuild status: "done"
```


```text title="Expected output"
Name                           State      Capacity    Rebuild Status
dd_sql01                       online     2.0 TB      done
Operational state: "online", Rebuild status: "done"
```

!!! warning "Common errors"
    **`Error: Invalid credentials or insufficient permissions`** — Ensure your vplexcli session is authenticated with an account that has read access to the distributed-devices namespace.
    **`Error: Device 'dd_sql01' not found`** — Verify the device name is correct and exists in the VPLEX cluster by running `vplexcli -q "ll /distributed-storage/distributed-devices"` to list all devices.
2. Test Metro failover — disconnect the ICL link (simulate a site outage) and confirm the surviving cluster promotes to primary and hosts retain access.
3. Reconnect the ICL and confirm the distributed device resynchronizes automatically.

**Host I/O validation:**

```bash
# From a host with the virtual volume mounted:
dd if=/dev/zero of=/dev/mapper/<vplex_mpath_dev> bs=1M count=2048 oflag=direct
# No errors should occur
```


```text title="Expected output"
2048+0 records in
2048+0 records out
2147483648 bytes (2.1 GB, 2.0 GiB) copied, 8.342 s, 257 MB/s
```

!!! warning "Common errors"
    **`dd: opening '/dev/mapper/<vplex_mpath_dev>': No such file or directory`** — Replace `<vplex_mpath_dev>` with the actual multipath device name from `multipath -ll` output.
    **`dd: writing to '/dev/mapper/<vplex_mpath_dev>': Read-only file system`** — Verify the VPLEX virtual volume is not in read-only mode and check array-side access permissions.
    **`dd: writing to '/dev/mapper/<vplex_mpath_dev>': Permission denied`** — Run the command with `sudo` or as root user.
4. Verify the VPLEX Management Console shows no active alerts under **Health Monitor > System Alerts**.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Vplex — Procedures](../operations/procedures/)
- [Vplex — Common Issues](../troubleshooting/common-issues/)
- [Vplex — How It Works](../architecture/how-it-works/)
