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
rack_cable_and_power_on: "Rack, Cable, and Power On" {shape: rectangle}
run_powerstore_manager_setup_wizard: "Run PowerStore Manager Setup Wizard" {shape: rectangle}
configure_network: "Configure Network" {shape: rectangle}
create_first_volume: "Create First Volume" {shape: rectangle}
configure_host_connectivity: "Configure Host Connectivity" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> rack_cable_and_power_on
rack_cable_and_power_on -> run_powerstore_manager_setup_wizard
run_powerstore_manager_setup_wizard -> configure_network
configure_network -> create_first_volume
create_first_volume -> configure_host_connectivity
configure_host_connectivity -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: Dell PowerStore Initial Configuration](https://www.youtube.com/watch?v=_zbJH90Muc4){ .md-button }
<!-- /video-link -->


- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# Dell PowerStore — Initial Deployment

This guide covers initial deployment of a Dell PowerStore appliance from physical installation through validated connectivity. Applies to PowerStore T-series (500T, 1000T, 3000T, 5000T, 9000T) running PowerStoreOS 3.x.

---

## Prerequisites

**Hardware:**

- Rack space confirmed (2U for single-node; 4U for dual-node appliance pair)
- Dual PDU circuits — PowerStore uses N+1 redundant power supplies
- 25GbE switches for data and iSCSI/NVMe-oF connectivity
- 16Gb or 32Gb FC switches if FC connectivity is planned
- At minimum two Ethernet links from each node for LACP bonding

**Network planning:**

| Component                | IP            |
|--------------------------|---------------|
| Node A management        | 10.0.0.10     |
| Node B management        | 10.0.0.11     |
| Cluster management VIP   | 10.0.0.12     |
| iSCSI/NVMe data port A   | 10.0.10.20    |
| iSCSI/NVMe data port B   | 10.0.10.21    |

**Software and licenses:**

- Dell PowerStore Manager (embedded, browser-accessible)
- License file (`.lic`) from Dell — covers capacity and optional features (replication, analytics)
- NTP server accessible from the management network
- Syslog or SMTP server for alert forwarding

---

## Rack, Cable, and Power On

1. Mount the PowerStore appliance into the rack using the supplied rail kit. Dual-node configurations require both nodes in adjacent rack units.
2. Cable SAS expansion shelves (if ordered) from the expansion ports on Node A and Node B to the shelf using the factory-labeled SAS cables.
3. Connect management Ethernet from Node A and Node B management ports to the OOB management switch.
4. Connect data network ports (25GbE) to your data switches. Use at least two ports per node for link aggregation.
5. Connect FC ports to your SAN fabric if FC is planned — at minimum two ports per node to separate fabric A and B.
6. Connect both PSU cables per node to separate PDU circuits.
7. Press the power button on Node A first, then Node B. Allow 20 minutes for both nodes to boot and form the cluster. The status LED turns solid green when the appliance is ready.

---

## Run PowerStore Manager Setup Wizard

PowerStore Manager is embedded on the cluster and accessible via browser.

1. From a host on the management network, open a browser and navigate to `https://<Node_A_IP>`.
2. The browser redirects to the **Setup Wizard** on first access.
3. Step through the wizard pages:

   **Network configuration:**
   - Set the cluster management VIP (hosts use this for all management operations after setup).
   - Assign the node management IPs if not already set via DHCP during boot.
   - Set default gateway and DNS servers.

   **Time settings:**
   - Set NTP server address and time zone.

   **License:**
   - Upload the `.lic` file provided by Dell. Click **Validate** to confirm it activates.

   **Naming:**
   - Set the cluster name. This name appears in alerts and replication relationships.

4. Click **Apply** and wait for the cluster to reinitialize (~5 minutes). The wizard redirects to the PowerStore Manager dashboard on completion.
5. Change the default admin password immediately under **Settings > Security > Users**.

---

## Configure Network

After initial setup, configure the data-plane network interfaces used by hosts.

**Configure Ethernet data interfaces:**

1. Navigate to **Settings > Network > Network Settings**.
2. Click on the appliance and select the Ethernet ports designated for iSCSI or NVMe-oF.
3. Set IP addresses, subnet masks, and MTU (9000 for jumbo frames — recommended for iSCSI/NVMe-oF).
4. Apply link aggregation (LACP) if your switch supports it:
   - Select two ports and assign a bond interface.
   - Configure the switch-side port-channel to match.

**Configure VLAN tagging:**

1. Under each port's settings, set the VLAN ID if data traffic is isolated to a specific VLAN.

**Configure FC (if applicable):**

1. FC ports are recognized automatically. Navigate to **Settings > Hardware > Ports** and confirm all FC ports show **Operational**.
2. Note the FC port WWNs — use these for SAN zoning.

---

## Create First Volume

PowerStore uses volumes (block) and file systems (NAS) as primary storage objects, provisioned from a central storage pool per appliance.

**Create a volume:**

1. Navigate to **Storage > Volumes > Create Volume**.
2. Enter a volume name (e.g., `vol_sql01_data`).
3. Set the size (e.g., 500 GiB). PowerStore volumes are thin-provisioned by default.
4. Select the appliance to host the volume.
5. Optionally select a performance tier or policy (if differentiated performance tiers are configured).
6. Click **Create**.

**Verify via CLI (optional):**

```bash
# Using PowerStore CLI (pstcli) from a management host
pstcli --address <cluster_vip> --user admin --password <password> volume query --name vol_sql01_data
```


```text title="Expected output"
Volume ID: 8b4c2e1f-9a3d-47b2-8c5d-6f2a1e9d4c3b
Name: vol_sql01_data
Size: 1099511627776 (1 TB)
Provisioning Type: Thin
Replication State: Synchronized
Protection Policy: sql_daily_backup
Snapshots: 3
Creation Time: 2024-01-15T09:23:47Z
Modification Time: 2024-01-22T14:56:12Z
Status: OK
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Connection refused to <cluster_vip>:443` | Verify the cluster VIP is correct and reachable from the management host using `ping <cluster_vip>` or `nc -zv <cluster_vip> 443`. |
    | `Error: Authentication failed for user 'admin'` | Confirm the password is correct and the admin account is not locked; reset credentials in the PowerStore GUI if needed. |
    | `Error: Volume 'vol_sql01_data' not found` | Check the exact volume name with `pstcli --address <cluster_vip> --user admin --password <password> volume query` to list all volumes. |
---

## Configure Host Connectivity

**Register a host:**

1. Navigate to **Compute > Hosts > Add Host**.
2. Enter the host name and select the OS type (Linux, Windows, VMware ESXi).
3. Add initiators:
   - **iSCSI:** Enter the host's IQN (`cat /etc/iscsi/initiatorname.iscsi` on Linux).
   - **FC:** WWPNs appear automatically after zoning is complete.
   - **NVMe-oF:** Enter the host's NQN (`cat /etc/nvme/hostnqn` on Linux).
4. Click **Add**.

**Attach a volume to a host:**

1. Select the volume created above.
2. Click **Attach > Host** and select the host.
3. Assign a logical unit number (LUN) or leave it auto-assigned.
4. Click **Attach**.

The volume is immediately presented. On a Linux host:

```bash
rescan-scsi-bus.sh
lsblk
multipath -ll
```


```text title="Expected output"
Scanning for SCSI devices...
Scanning host 0 for SCSI target IDs 0:0:0:0, 0:0:1:0, 0:0:2:0
Scanning host 1 for SCSI target IDs 1:0:0:0, 1:0:1:0
Scanning host 2 for SCSI target IDs 2:0:0:0
3 new device(s) found.
Rescan complete.

NAME                          MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINTS
sda                             8:0    0  100G  0 disk
├─sda1                          8:1    0    1G  0 part  /boot
└─sda2                          8:2    0   99G  0 part  /
sdb                             8:16   0  500G  0 disk
sdc                             8:32   0  500G  0 disk
sdd                             8:48   0  500G  0 disk

mpatha (360060e8007042000086e042d4c5dd11) dm-0 DELL,PowerStore
size=500G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 2:0:0:0 sdb 8:16 active ready running
  `- 3:0:0:0 sdc 8:32 active ready running
mpathb (360060e8007042000086e042d4c5dd12) dm-1 DELL,PowerStore
size=500G features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  `- 4:0:0:0 sdd 8:48 active ready running
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `rescan-scsi-bus.sh: command not found` | Install sg3_utils package with `apt-get install sg3-utils` or `yum install sg3_utils`. |
    | `multipathd is not running` | Start the multipath daemon with `systemctl start multipathd` and enable it with `systemctl enable multipathd`. |
---

## Set Up Data Protection

**Snapshot policies:**

1. Navigate to **Protection > Protection Policies > Create Policy**.
2. Name the policy (e.g., `hourly_24h`).
3. Add a snapshot rule:
   - Interval: every 1 hour
   - Retention: 24 hours
4. Assign the policy to the volume or file system under **Storage > Volumes > [volume] > Protection**.

**Replication (if licensed):**

1. Navigate to **Protection > Replication Rules > Create**.
2. Set the RPO (e.g., 5 minutes for synchronous, 1 hour for asynchronous).
3. Navigate to **Protection > Remote Systems > Add Remote System** and enter the peer PowerStore cluster VIP and credentials.
4. Create a replication session linking the local volume to a remote volume.
5. Monitor replication state under **Protection > Replication Sessions**.

---

## Validate

1. From the PowerStore Manager dashboard, confirm all nodes, disks, and power supplies show green health indicators under **Infrastructure > Hardware**.
2. Verify the host can see the volume with correct path count:

```bash
multipath -ll
# Expect 2 or 4 paths depending on port and fabric count
```


```text title="Expected output"
mpatha (36006016054f03200525e9b4a2e5de11) dm-0 DELL,PowerStore
size=2.0T features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 2:0:0:0 sda 8:0  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 3:0:0:0 sdb 8:16 active ready running

mpathb (36006016054f03200525e9b4a2e5de12) dm-1 DELL,PowerStore
size=4.0T features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 4:0:0:0 sdc 8:32 active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 5:0:0:0 sdd 8:48 active ready running
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `multipath: command not found` | Install device-mapper-multipath package with `yum install device-mapper-multipath` or `apt-get install multipath-tools`. |
    | `the following paths have not been initialized: sda sdb sdc sdd` | Run `multipath -v3` to initialize paths, then verify FC fabric connectivity and zoning rules allow host-to-array communication. |
    | `mpatha: all paths are down` | Check FC switch port status, verify array LUNs are exported to the host's WWN, and confirm ALUA is enabled on the PowerStore array. |
3. Run a quick I/O test to confirm no errors:

```bash
dd if=/dev/zero of=/dev/mapper/<mpath_dev> bs=1M count=512 oflag=direct
```


```text title="Expected output"
512+0 records in
512+0 records out
536870912 bytes (537 MB, 512 MiB) copied, 2.847 s, 189 MB/s
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `dd: opening '/dev/mapper/<mpath_dev>': No such file or block device` | Verify the multipath device exists with `multipath -ll` and substitute the actual device name (e.g., `mpatha`). |
    | `dd: writing to '/dev/mapper/<mpath_dev>': Read-only file system` | Ensure the device is not write-protected; check with `blockdev --getro /dev/mapper/<mpath_dev>` and disable read-only mode if needed. |
    | `dd: opening '/dev/mapper/<mpath_dev>': Permission denied` | Run the command with `sudo` or as root user. |
4. Check PowerStore Manager **Monitoring > Performance** — latency should be sub-millisecond for NVMe-based appliances at low queue depth.
5. Confirm no active alerts under **Monitoring > Alerts**.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Powerstore — Procedures](../operations/procedures/)
- [Powerstore — Common Issues](../troubleshooting/common-issues/)
- [Powerstore — How It Works](../architecture/how-it-works/)
