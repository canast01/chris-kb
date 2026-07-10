---
tags:
  - deployment
  - pure
search:
  boost: 1.5
---

```d2
direction: right

plan: "Plan" {shape: oval}
prerequisites: "Prerequisites" {shape: rectangle}
run_purity_initial_setup: "Run Purity Initial Setup" {shape: rectangle}
configure_management_network: "Configure Management Network" {shape: rectangle}
configure_host_connectivity_fc_or_is: "Configure Host Connectivity (FC or iSCSI)" {shape: rectangle}
create_first_volume: "Create First Volume" {shape: rectangle}
set_up_protection_group: "Set Up Protection Group" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> run_purity_initial_setup
run_purity_initial_setup -> configure_management_network
configure_management_network -> configure_host_connectivity_fc_or_is
configure_host_connectivity_fc_or_is -> create_first_volume
create_first_volume -> set_up_protection_group
set_up_protection_group -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# FlashArray — Initial Deployment

This guide covers deploying a Pure Storage FlashArray (//X, //C, or //XL series) from physical installation through validated host connectivity. All steps apply to Purity//FA 6.x.

---

## Prerequisites

**Hardware:**

- FlashArray chassis with controller modules installed (dual controllers for HA)
- DirectFlash modules (NVMe flash) populated — Pure ships arrays at the ordered capacity
- 25GbE or 100GbE switches for iSCSI or NVMe-oF connectivity (or FC switches for Fibre Channel)
- OOB management network switch with DHCP for initial discovery, or pre-configured static IP

**Network planning:**

| Component                    | IP / Port       |
|------------------------------|-----------------|
| Management VIP               | 10.0.0.50       |
| CT0 management               | 10.0.0.51       |
| CT1 management               | 10.0.0.52       |
| iSCSI data VIF (CT0)         | 10.0.10.10      |
| iSCSI data VIF (CT1)         | 10.0.10.11      |

**Software:**

- Purity//FA 6.x (pre-installed at factory — verify the version post-setup)
- Pure Storage Host Utilities installed on each host (Linux, Windows, VMware ESXi)
- Pure1 account for monitoring (register at `pure1.purestorage.com`)
- NTP server accessible from the management network

---

## Run Purity Initial Setup

**Locate the array on the network:**

1. After racking and powering on, the array management interface acquires an IP via DHCP on the management switch. Check your DHCP server for the lease, or connect directly via serial console (9600/8N1) to read the assigned IP from the console output.
2. Browse to `https://<dhcp_assigned_ip>` and log in using the credentials in the Quick Start Guide shipped with the array.

**Run the initial setup wizard:**

1. Accept the EULA.
2. The **Initial Setup Wizard** presents the following screens in order:
   - **Array name:** Set a short DNS-compatible name (e.g., `fa-prod-01`).
   - **Management network:** Enter the management VIP, CT0 management IP, CT1 management IP, subnet mask, and gateway.
   - **DNS:** Enter primary and secondary DNS server IPs.
   - **NTP:** Enter the NTP server address. Accurate time is critical for replication consistency.
   - **SMTP / Alert email:** Enter a relay server and destination email for alerts.
   - **Admin password:** Set a strong password. Pure recommends integrating with LDAP or SAML after initial setup.
3. Click **Finish**. Purity applies the configuration and reconnects at the new management VIP.

**Verify Purity version and array health:**

1. Log in at `https://<management_vip>`.
2. Navigate to **Storage > Array**. All hardware components should show green.
3. Note the Purity version from **System > Software**. If the version is not current, check Pure1 for available upgrades.

---

## Configure Management Network

After the wizard, fine-tune the management network configuration.

1. Navigate to **System > Network**.
2. Verify that CT0 and CT1 management IPs and the management VIP are correct.
3. Confirm the DNS configuration resolves correctly:

```bash
# Via Purity CLI (SSH to management VIP as pureuser)
puredns resolve --hostname your.ntp.server
```


```text title="Expected output"
your.ntp.server: 203.0.113.42
```

!!! warning "Common errors"
    **`Error: DNS resolution failed for your.ntp.server`** — Verify the hostname is correct and that the FlashArray's DNS servers are configured with `puredns list` and update if needed using `puredns set --servers <ip1> <ip2>`.
    **`Error: Connection refused`** — Ensure you are SSH'd into the FlashArray management VIP as the pureuser account and have network connectivity to the management interface.
4. Set the time zone:

```bash
puretime set --timezone Europe/London
puretime list
# Verify NTP sync status is "Synced"
```


```text title="Expected output"
Timezone set to Europe/London
Timezone: Europe/London
NTP Servers: 169.254.169.123, 169.254.169.124
NTP Sync Status: Synced
Last NTP Sync: 2024-01-15T14:32:18Z
Current Time: 2024-01-15 14:32:45 GMT
```

!!! warning "Common errors"
    **`puretime: command not found`** — Ensure you are logged into the Pure FlashArray management interface or SSH session with appropriate CLI access.
    **`NTP Sync Status: Unsynced`** — Verify NTP servers are reachable and correctly configured; check network connectivity to the configured NTP server IPs.
5. Configure the management interface for a dedicated management VLAN if required:

Navigate to **System > Network > Management Interfaces** and set the VLAN tag on the management ports.

---

## Configure Host Connectivity (FC or iSCSI)

**FC Connectivity:**

1. Navigate to **Storage > Ports**. FC target port WWPNs are listed per controller.
2. Record the WWPNs for CT0 and CT1 — you will use these for SAN zoning.
3. Create zones on your FC switches:
   - One zone per host HBA port, including that HBA's WWN and the FlashArray FC target ports it should reach.
   - Best practice: zone each host HBA to both CT0 and CT1 FC ports for HA.
4. After zoning, log in to the Purity UI. Navigate to **Storage > Hosts** and click **Create Host**.
5. The host's WWPNs should appear automatically after zoning is established. Select them and click **Create**.

**iSCSI Connectivity:**

1. Navigate to **System > Network > Data Interfaces (iSCSI)**.
2. Configure iSCSI VIFs on both controllers:
   - Click **Edit** on each interface and assign the IP address, subnet mask, and MTU (9000 recommended).
   - Ensure both CT0 and CT1 iSCSI interfaces are on the same iSCSI VLAN as the hosts.
3. On the host (Linux example):

```bash
# Install and enable iSCSI initiator
yum install -y iscsi-initiator-utils
systemctl enable --now iscsid

# Discover the FlashArray iSCSI targets
iscsiadm -m discovery -t st -p 10.0.10.10

# Log in to all targets
iscsiadm -m node -L all

# Install Pure Host Package for optimal multipath settings
# (Download from support.purestorage.com)
rpm -ivh pure-storage-host-utilities-<version>.x86_64.rpm
```


```text title="Expected output"
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostinfo
Resolving Dependencies
--> Running transaction check
---> Package iscsi-initiator-utils.x86_64 0:6.2.0.877-21.el7 will be installed
--> Processing Dependency: iscsi-initiator-utils-iscsiuio for package: iscsi-initiator-utils-6.2.0.877-21.el7.x86_64
--> Finished Dependency Resolution
Installed:
  iscsi-initiator-utils.x86_64 0:6.2.0.877-21.el7
Created symlink from /etc/systemd/system/multi-user.target.wants/iscsid.service to /usr/lib/systemd/system/iscsid.service.
10.0.10.10:3260,1 iqn.2010-06.com.purestorage:flasharray.1234567890abcdef.1
10.0.10.10:3260,2 iqn.2010-06.com.purestorage:flasharray.1234567890abcdef.2
Logging in to [iface: default, target: iqn.2010-06.com.purestorage:flasharray.1234567890abcdef.1, portal: 10.0.10.10,3260] (multiple)
Login to [iface: default, target: iqn.2010-06.com.purestorage:flasharray.1234567890abcdef.1, portal: 10.0.10.10,3260] successful.
Login to [iface: default, target: iqn.2010-06.com.purestorage:flasharray.1234567890abcdef.2, portal: 10.0.10.10,3260] successful.
Preparing...                          ################################# [100%]
Updating / installing...
   1:pure-storage-host-utilities-6.1.0-1 ################################# [100%]
```

!!! warning "Common errors"
    **`iscsiadm: No records found`** — Verify the FlashArray iSCSI portal IP (10.0.10.10) is reachable and iSCSI service is enabled on the array using `ping 10.0.10.10` and checking array network settings.
    **`rpm: error reading package header`** — Download the correct Pure Host Package RPM file from support.purestorage.com matching your OS version and verify the file is not corrupted with `file pure-storage-host-utilities-*.x86_64.rpm`.
    **`iscsid.service is not running`** — Start the iSCSI daemon explicitly with `systemctl start iscsid` before attempting discovery or login.
4. Register the host in Purity by entering its IQN manually:

Navigate to **Storage > Hosts > Create Host**. Enter the host name and IQN.

---

## Create First Volume

1. Navigate to **Storage > Volumes > Create Volume**.
2. Enter:
   - Volume name (e.g., `vol_sql01_data`)
   - Size (e.g., `500G`) — volumes are thin-provisioned; actual capacity is consumed as data is written
   - Protection group (optional — assign to an existing protection group for automated snapshots)
3. Click **Create**.

**Connect the volume to a host:**

1. Select the volume, click **Connect**.
2. Select the host created above (e.g., `linux_host01`).
3. LUN assignment is automatic unless specified.
4. Click **Connect Volume**.

**Verify on the host:**

```bash
rescan-scsi-bus.sh
multipath -ll
# The Pure FlashArray volume should appear with model "PURE"
# Expect 4 paths for single-fabric iSCSI (2 per controller) or 4-8 for FC
```


```text title="Expected output"
Scanning for SCSI devices...
Scanning host 0 for SCSI devices
Scanning host 1 for SCSI devices
Scanning host 2 for SCSI devices
Scanning host 3 for SCSI devices
New device(s) found

mpatha (360a98000534d38754d6f6f2d4c000000) dm-0 PURE,FlashArray//m
size=1.0T features='1 queue_if_no_path' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| |-+- 2:0:0:0 sdb 65:0   active ready running
| `-+- 3:0:0:0 sdc 65:16  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  |-+- 4:0:0:0 sdd 65:32  active ready running
  `-+- 5:0:0:0 sde 65:48  active ready running
```

!!! warning "Common errors"
    **`No such file or directory`** — Ensure the `sg3_utils` package is installed with `apt-get install sg3-utils` or `yum install sg3_utils`.
    **`multipathd is not running`** — Start the multipath daemon with `systemctl start multipathd && systemctl enable multipathd`.
    **`No multipath output or device shows "faulty" status`** — Verify iSCSI/FC connectivity with `iscsiadm -m session` or `fcinfo fcportlogin`, and confirm Pure array target configuration.
---

## Set Up Protection Group

Protection groups enable consistent snapshot schedules and replication across volumes.

1. Navigate to **Storage > Protection Groups > Create Protection Group**.
2. Name the group (e.g., `pg_sql_prod`).
3. Add volumes: click **Add Volumes** and select the SQL data and log volumes.
4. Add a snapshot schedule:
   - Click **Edit Schedule**
   - Frequency: every 1 hour
   - Retention: 24 snapshots (24-hour local retention)
   - Replicate to: select the target array (if replication is configured)
   - Replication retention: keep replicated snapshots for 7 days
5. Click **Apply**.

**Test an on-demand snapshot:**

1. Select the protection group, click **Take Snapshot**.
2. Navigate to **Storage > Snapshots** and confirm the snapshot appears.

---

## Register with Pure1

1. Navigate to **System > Support** and enable **Phone Home**.
2. Confirm outbound HTTPS access from the management network to `support.purestorage.com` on TCP 443.
3. Log in to `https://pure1.purestorage.com` with your Pure Storage portal account.
4. The array appears automatically after Phone Home is enabled (within 30 minutes).
5. In Pure1:
   - Navigate to **Alerts** and configure email notification recipients.
   - Review the **Capacity** forecast graph to confirm usable space projections.
   - Register any open support cases for tracked issues.

---

## Validate

1. From the Purity UI, navigate to **Storage > Array** and confirm all controllers, shelves, and drives show green.
2. Confirm the volume has correct path count from the host:

```bash
multipath -ll
# Each path should show status "active ready"
```


```text title="Expected output"
mpatha (36001405abcd1234ef567890abcd1234) dm-0 PURE,FlashArray
size=1.0T features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active ready
| `- 2:0:0:0 sda 8:0  active ready
`-+- policy='service-time 0' prio=10 status=enabled ready
  `- 3:0:0:0 sdb 8:16 active ready
mpathb (36001405zyxw9876qr543210zyxw9876) dm-1 PURE,FlashArray
size=2.0T features='0' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active ready
| `- 4:0:0:0 sdc 8:32 active ready
`-+- policy='service-time 0' prio=10 status=enabled ready
  `- 5:0:0:0 sdd 8:48 active ready
```

!!! warning "Common errors"
    **`mpatha: sda: checker msg is "open error"`** — Verify iSCSI/FC connectivity to the array and ensure the initiator can reach the target portal or fabric.
    **`mpatha: sda: path checker timed out`** — Check network latency and array responsiveness; restart multipathd with `systemctl restart multipathd` if paths remain stuck.
    **`mpatha (dm-0) status: faulty`** — Run `multipath -f mpatha` to remove the failed device, then rescan with `echo 1 > /sys/block/sda/device/rescan` and rebuild the multipath map.
3. Run a write/read I/O test:

```bash
dd if=/dev/zero of=/dev/mapper/<pure_mpath_dev> bs=1M count=2048 oflag=direct
dd if=/dev/mapper/<pure_mpath_dev> of=/dev/null bs=1M count=2048 iflag=direct
```


```text title="Expected output"
2048+0 records in
2048+0 records out
2147483648 bytes (2.1 GB, 2.0 GiB) copied, 8.342 s, 257 MB/s
2048+0 records in
2048+0 records out
2147483648 bytes (2.1 GB, 2.0 GiB) copied, 7.156 s, 300 MB/s
```

!!! warning "Common errors"
    **`dd: opening '/dev/mapper/<pure_mpath_dev>': No such file or directory`** — Verify the multipath device exists with `multipath -ll` and confirm the Pure FlashArray LUN is properly mapped and the multipathd daemon is running.
    **`dd: writing to '/dev/mapper/<pure_mpath_dev>': Read-only file system`** — Check device permissions with `ls -l /dev/mapper/<pure_mpath_dev>` and ensure the device is not write-protected; run `blockdev --setrw /dev/mapper/<pure_mpath_dev>` if needed.
    **`dd: error writing '/dev/mapper/<pure_mpath_dev>': No space left on device`** — Reduce the count parameter (e.g., `count=1024`) or verify the LUN size matches expectations with `lsblk` or `fdisk -l`.
4. Check no errors in `/var/log/messages` or the multipath log.
5. Verify the protection group snapshot schedule is running: navigate to **Storage > Snapshots** and confirm hourly snapshots are being created.
6. In Pure1, confirm the array shows as **Connected** and no critical alerts are active.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Flasharray — Procedures](../operations/procedures/)
- [Flasharray — Common Issues](../troubleshooting/common-issues/)
- [Flasharray — How It Works](../architecture/how-it-works/)
