---
tags:
  - dell
  - deployment
search:
  boost: 1.5
---

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
rack_and_cable: "Rack and Cable" {shape: rectangle}
run_unisphere_initial_configuration_: "Run Unisphere Initial Configuration Wizard" {shape: rectangle}
configure_network_interfaces: "Configure Network Interfaces" {shape: rectangle}
create_storage_pools: "Create Storage Pools" {shape: rectangle}
configure_iscsi_or_fc_host_access: "Configure iSCSI or FC Host Access" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> rack_and_cable
rack_and_cable -> run_unisphere_initial_configuration_
run_unisphere_initial_configuration_ -> configure_network_interfaces
configure_network_interfaces -> create_storage_pools
create_storage_pools -> configure_iscsi_or_fc_host_access
configure_iscsi_or_fc_host_access -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: Dell Unity: Storage Provisioning and Initial Setup](https://www.youtube.com/watch?v=UeUVvuu1vfE){ .md-button }
<!-- /video-link -->


- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# Dell Unity XT — Initial Deployment

This guide covers the initial deployment of a Dell Unity XT array from physical installation through validated host access. Applies to Unity XT 380, 480, 680, and 880 models running OE 5.x.

---

## Prerequisites

**Hardware checklist:**

- Rack space confirmed (2U for base chassis; additional DAEs if capacity expansion is included)
- Dual AC power circuits available — Unity XT uses N+1 redundant PSUs
- 10GbE or 25GbE switches for iSCSI/NFS management and data paths
- FC switches (Brocade or Cisco) if FC connectivity is planned
- Management workstation on same subnet or routed access to array management IP

**Software and licensing:**

- Dell EMC Unisphere for Unity (HTML5 interface, embedded on the array)
- License key files provided by Dell — Unity uses a capacity-based license model
- NTP server details for time synchronization
- LDAP/AD server details if directory-based authentication is required

**IP address plan:**

| Component          | IP            |
|--------------------|---------------|
| SP-A management    | 192.168.1.50  |
| SP-B management    | 192.168.1.51  |
| iSCSI port 0 SP-A  | 10.0.10.10    |
| iSCSI port 0 SP-B  | 10.0.10.11    |
| NAS pool NFS VIP   | 10.0.10.20    |

Adjust for your environment before proceeding.

---

## Rack and Cable

1. Mount the Unity XT chassis into the rack using the supplied rail kit. Tighten all four rack post screws before applying weight.
2. If DAE (Disk Array Enclosure) expansion shelves are included, rack them directly below the main chassis and cable the SAS expansion ports using the factory-labeled cables (SAS-A to SP-A, SAS-B to SP-B).
3. Connect PSU cables from each PSU to separate PDU circuits.
4. Connect SP-A and SP-B management Ethernet ports to your OOB management switch.
5. Connect iSCSI or FC data ports:
   - For iSCSI: connect 10/25GbE ports to data switches
   - For FC: connect 16/32Gb FC ports to SAN switches (cable at least two ports per SP to separate fabrics)
6. Power on the array. Initial boot takes 10–15 minutes. The SP-A and SP-B fault LEDs will be amber during boot and turn off (no fault) when the array is ready.

---

## Run Unisphere Initial Configuration Wizard

Unity XT embeds Unisphere directly on the array. No external server is needed for the initial setup wizard.

1. Connect a laptop directly to the array's service port Ethernet or to the same management VLAN and browse to `https://192.168.0.1` (factory default IP for SP-A management port).
2. Log in with default credentials: `admin` / `Password123#` — these are printed on the array's service tag. Change them immediately.
3. The **Initial Configuration Wizard** launches automatically on first login. Work through each page:
   - **DNS:** Enter your DNS server IP addresses.
   - **NTP:** Enter the NTP server address. Unity XT requires accurate time for replication and LDAP.
   - **SMTP:** Enter email relay server for alert notifications.
   - **Licenses:** Upload the `.lic` file provided by Dell. Without a valid license, capacity is limited to evaluation mode.
4. Accept the EULA and click **Finish**. Unisphere will reinitialize and redirect to the dashboard.
5. Change the admin password under **Settings > Users and Groups > admin > Change Password**.

---

## Configure Network Interfaces

After the wizard completes, configure data-path network interfaces.

**iSCSI interfaces:**

1. Navigate to **Settings > Network > iSCSI Interfaces**.
2. Click **Create** and fill in:
   - SP: SP-A
   - Port: ethernet port (e.g., `eth0`)
   - IP address / subnet mask / gateway
   - VLAN tag (if applicable)
3. Repeat for SP-B on the corresponding port. Ensure SP-A and SP-B iSCSI IPs are on the same subnet but different ports for multipath.

**FC interfaces:**

1. Navigate to **Settings > FC Initiators**.
2. FC ports appear automatically after cabling. Confirm all ports show **Link Up** status.
3. Note the WWPNs for each SP — these will be used in SAN zoning.

**NFS/SMB management interface (NAS):**

1. Navigate to **Settings > Network > File Interfaces**.
2. Create a NAS server interface with the NFS/SMB VIP and associate it with the NAS pool (created in the next step).

---

## Create Storage Pools

Unity XT uses storage pools that contain tiers (SSD, SAS, NL-SAS). All LUNs and file systems are provisioned from pools.

1. Navigate to **Storage > Pools > Create**.
2. Enter a pool name (e.g., `Pool_SSD`).
3. Choose pool type:
   - **All Flash** — all drives are SSD/NVMe
   - **Hybrid** — mix of SSD and spinning disk with auto-tiering
4. Add disk groups to the pool. Select the drives detected from the chassis and expansion shelves.
5. Set RAID type per disk group:
   - RAID-5 (4+1) or RAID-6 (6+2) for flash
   - RAID-6 (6+2) recommended for NL-SAS
6. Set pool alert threshold (e.g., alert when pool reaches 80% used).
7. Click **Create**. Pool initialization runs in the background and takes a few minutes.

Verify pool status:

```bash
uemcli /stor/config/pool show -detail
```


```text title="Expected output"
Pool ID: pool_1
Pool Name: SSD_Pool_01
Pool Type: RAID 5
Total Capacity: 10.73 TB
Available Capacity: 7.42 TB
Consumed Capacity: 3.31 TB
Health Status: OK
RAID Type: RAID 5 (4+1)
Disk Count: 5
Stripe Width: 4
Block Size: 4 KB
Thin Provisioning: Enabled
Snapshots: 12
Replication: Enabled
Pool ID: pool_2
Pool Name: NL_SAS_Pool_02
Pool Type: RAID 6
Total Capacity: 45.28 TB
Available Capacity: 38.91 TB
Consumed Capacity: 6.37 TB
Health Status: OK
...
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Invalid command or syntax` | Verify the uemcli binary is installed and in your PATH, or use the full path `/opt/emc/uemcli/uemcli`. |
    | `Error: Connection refused to management interface` | Ensure the Unity array management IP is reachable and uemcli is configured with correct credentials via `-u` and `-p` flags or environment variables. |
---

## Configure iSCSI or FC Host Access

**iSCSI initiator registration:**

1. On the host, note the iSCSI initiator IQN:

```bash
cat /etc/iscsi/initiatorname.iscsi
```


```text title="Expected output"
## DO NOT EDIT OR REMOVE THIS FILE.
## If you remove this file, the iSCSI daemon will not start.
## If you change the InitiatorName, existing access control lists
## may reject this initiator.  The InitiatorName must be unique
## for each iSCSI initiator.  Do NOT duplicate iSCSI InitiatorNames.
InitiatorName=iqn.1993-08.org.debian:01:a4c2f8e9d5b2
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `cat: /etc/iscsi/initiatorname.iscsi: No such file or directory` | Install open-iscsi package with `apt-get install open-iscsi` or `yum install iscsi-initiator-utils`. |
    | `cat: /etc/iscsi/initiatorname.iscsi: Permission denied` | Run the command with `sudo` or as root user. |
2. In Unisphere, navigate to **Hosts > Create Host**.
3. Enter the host name and select **iSCSI** as the initiator type.
4. Add the host's IQN to the host object.
5. Set the host operating system type (Linux, Windows, VMware ESXi, etc.) — this sets the correct host I/O profile.

**FC initiator registration:**

1. Zone the host HBA ports to the Unity FC ports in the SAN fabric (single-initiator/single-target zones).
2. In Unisphere, navigate to **Hosts > Create Host**.
3. Select **Fibre Channel** as initiator type.
4. The host's logged-in WWPNs should appear in the discovery list — add them.

---

## Create First LUN or File System

**Block LUN:**

1. Navigate to **Storage > Block Storage > LUNs > Create**.
2. Enter a LUN name, select the pool, and set the size.
3. Set **Host access**: click **Add** and select the host created above.
4. Set the **LUN type** (thin is default). Click **Create**.
5. The LUN is immediately presented to the host. On a Linux host, rescan:

```bash
rescan-scsi-bus.sh
multipath -ll
```


```text title="Expected output"
Scanning for SCSI devices...
Host 0 Channel 00 Id 00 Lun 00: Direct-Access-RDisk DELL UNITY 450F S/N D1A2B3C4D5E6F7G8 PQ: 0 ANSI: 5
Host 1 Channel 00 Id 00 Lun 00: Direct-Access-RDisk DELL UNITY 450F S/N D1A2B3C4D5E6F7G9 PQ: 0 ANSI: 5
Host 2 Channel 00 Id 00 Lun 00: Direct-Access-RDisk DELL UNITY 450F S/N D1A2B3C4D5E6F7GA PQ: 0 ANSI: 5
Scanning for new LUNs... done

mpatha (360060e8012a0000012a0000000001a1) dm-0 DELL,UNITY 450F
size=500G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 0:0:0:0 sda 8:0 active ready running
| `- 1:0:0:0 sdb 8:16 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 2:0:0:0 sdc 8:32 active ready running
  `- 3:0:0:0 sdd 8:48 active ready running

mpathb (360060e8012a0000012a0000000001a2) dm-1 DELL,UNITY 450F
size=1T features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 4:0:0:0 sde 8:64 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 5:0:0:0 sdf 8:80 active ready running
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `bash: rescan-scsi-bus.sh: command not found` | Install sg3-utils package with `apt-get install sg3-utils` or `yum install sg3-utils`. |
    | `multipath: command not found` | Install device-mapper-multipath with `apt-get install multipath-tools` or `yum install device-mapper-multipath`. |
    | `multipathd is not running` | Start the multipath daemon with `systemctl start multipathd` and enable it with `systemctl enable multipathd`. |
**NFS File System:**

1. Navigate to **Storage > File Storage > File Systems > Create**.
2. Enter a name, select a NAS server, and set the size.
3. Create an NFS export under the file system with appropriate host access controls.
4. Mount from the host:

```bash
mount -t nfs <NAS_VIP>:/export/fs01 /mnt/unity_nfs
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `mount.nfs: access denied by server while mounting <NAS_VIP>:/export/fs01` | Verify the NAS export policy allows the client IP and check firewall rules between client and NAS. |
    | `mount.nfs: No such file or directory` | Confirm the export path `/export/fs01` exists on the NAS and the mount point `/mnt/unity_nfs` exists locally. |
    | `mount: only root can use "--options" option` | Run the command with `sudo` or as the root user. |
---

## Validate

**Check array health:**

1. Unisphere dashboard should show all components green. Navigate to **System > Hardware** and verify all SP, disk, and PSU LEDs match physical status.
2. Run the built-in health check:

```bash
uemcli /sys/time show
uemcli /sys/health show
```


```text title="Expected output"
System Time
  Timezone: UTC
  Current Time: 2024-01-15 14:32:47
  NTP Server: 10.20.50.1
  NTP Status: synchronized

System Health
  Overall Health: OK
  CPU Health: OK
  Memory Health: OK
  Disk Health: OK
  Temperature: 42°C (Normal)
  Power Supply 1: OK
  Power Supply 2: OK
  Battery Backup Unit: OK
  SSD Health: OK
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Connection refused (111)` | Verify the Unity array is reachable and uemcli service is running with `systemctl status uemcli`. |
    | `Error: Authentication failed` | Ensure you have valid credentials configured in `/etc/uemcli/credentials` or pass `-u` and `-p` flags to authenticate. |
**Verify LUN path count from host:**

```bash
multipath -ll
# Each LUN should show 4 active paths (2 per SP) for dual-fabric iSCSI or FC
```


```text title="Expected output"
mpatha (36006016054d02700ca44a9d9d4e8e111) dm-0 DELL,UNITY
size=500G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 2:0:0:1 sda 8:0   active ready running
| `- 3:0:0:1 sdb 8:16  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 4:0:0:1 sdc 8:32  active ready running
  `- 5:0:0:1 sdd 8:48  active ready running
mpathb (36006016054d02700ca44a9d9d4e8e222) dm-1 DELL,UNITY
size=250G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |- 2:0:1:1 sde 8:64  active ready running
| `- 3:0:1:1 sdf 8:80  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |- 4:0:1:1 sdg 8:96  active ready running
  `- 5:0:1:1 sdh 8:112 active ready running
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `mpatha: No such file or directory` | Ensure the `device-mapper-multipath` package is installed and the `multipathd` service is running with `systemctl start multipathd`. |
    | `the following lines in the output show failed paths: ... failed faulty offline` | Check fabric connectivity and SAN switch zoning; verify both FC/iSCSI initiators are logged in with `iscsiadm -m session` or `fcinfo fcportlogin`. |
**Confirm pool statistics:**

1. Navigate to **Performance > Storage Pools** and verify I/O latency is normal (sub-1ms for SSD pools under light load).
2. Confirm no alerts are active in **System > Alerts**.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Unity — Procedures](../operations/procedures/)
- [Unity — Common Issues](../troubleshooting/common-issues/)
- [Unity — How It Works](../architecture/how-it-works/)
