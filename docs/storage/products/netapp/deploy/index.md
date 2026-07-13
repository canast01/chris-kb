---
tags:
  - deployment
  - netapp
search:
  boost: 1.5
description: "NetApp ONTAP cluster initial setup: first boot through validated host connectivity and replication — covers AFF A-series, C-series, and FAS platforms."
---
# NetApp ONTAP — Getting Started

<div class="kb-summary">
NetApp ONTAP cluster initial setup: first boot through validated host connectivity and replication — covers AFF A-series, C-series, and FAS platforms.

*Applies to: ONTAP 9.12+*
</div>

This guide covers the initial setup of a NetApp ONTAP cluster from first boot through validated host connectivity and replication. Applies to AFF A-series, C-series, and FAS platforms running ONTAP 9.12 and later.

---

```d2
direction: right

plan: "Plan" {shape: oval}
cluster_initial_setup: "Cluster Initial Setup" {shape: rectangle}
svm_creation: "SVM Creation" {shape: rectangle}
volume_provisioning: "Volume Provisioning" {shape: rectangle}
host_connectivity: "Host Connectivity" {shape: rectangle}
snapmirror: "SnapMirror" {shape: rectangle}
monitoring_setup: "Monitoring Setup" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> cluster_initial_setup
cluster_initial_setup -> svm_creation
svm_creation -> volume_provisioning
volume_provisioning -> host_connectivity
host_connectivity -> snapmirror
snapmirror -> monitoring_setup
monitoring_setup -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: NetApp ONTAP 9 Complete Training Course](https://www.youtube.com/watch?v=VE9dqRiGX2o){ .md-button }
<!-- /video-link -->


- **Access:** Storage admin credentials (cluster admin or equivalent)
- **Environment:** DNS, NTP, and network connectivity verified before starting
- **Change management:** change request approved; maintenance window scheduled
- **Rollback:** snapshot or backup taken immediately before deployment begins
- **Time estimate:** 30–90 minutes — do not start if less than 2 hours are available

---

## Cluster Initial Setup

ONTAP cluster setup is performed through the System Manager wizard (browser-based) or the ONTAP CLI setup script (`cluster setup`).

**Initial boot and console access:**

1. Power on the first node (the cluster creates when this node runs setup). Connect to the node via serial console (9600 baud, 8N1) or iDRAC/BMC serial-over-LAN.
2. Log in as `admin` with no password on first boot — ONTAP prompts you to run setup.
3. Launch the setup wizard:

```text
cluster setup
```

4. When prompted, select **Create a new cluster**.
5. Provide:
   - Cluster name (e.g., `ontap-prod-01`)
   - Cluster management IP address, subnet mask, gateway
   - DNS domain and DNS server IPs
   - NTP servers (at least two)
   - Admin password

**Add remaining nodes:**

After the first node completes setup, each additional node joins the cluster:

1. On each additional node's console, run `cluster setup`.
2. Select **Join an existing cluster**.
3. Enter the cluster management IP and admin credentials.
4. Wait for the node to join and ONTAP to begin aggregate discovery.

**Verify cluster formation:**

```bash
cluster show
# All nodes should show Health: true, Eligibility: true

node show
# Each node should show Status: online
```


```text title="Expected output"
Cluster UUID: 4a3f8c2b-9e1d-47f6-b2a9-5c7d1e9f3a2b
Health: true
Eligibility: true

Node              Status  Health  Eligibility
netapp-node-01    online  true    true
netapp-node-02    online  true    true
netapp-node-03    online  true    true
netapp-node-04    online  true    true
```

!!! warning "Common errors"
    **`Error: command not found: cluster show`** — Ensure you are logged into the NetApp cluster management interface (SSH to the cluster management IP) rather than a node management IP.
    **`Health: false`** — Check cluster event logs with `event log show` and resolve any failed disk or network issues before proceeding.
**Create a cluster-wide service policy for management traffic (if using separated management VLANs):**

```bash
network interface create -vserver <cluster_name> -lif cluster_mgmt -role cluster-mgmt -home-node <node_name> -home-port e0M -address <ip> -netmask <mask>
network route create -vserver <cluster_name> -destination 0.0.0.0/0 -gateway <gw>
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: command failed: EINVALIDARGUMENT: Invalid value specified for "address" : <ip>`** — Verify the IP address format is valid (e.g., 192.168.1.100) and not already in use on the network.
    **`Error: command failed: EOBJECTNOTFOUND: Vserver "<cluster_name>" does not exist.`** — Ensure the vserver name matches an existing cluster and is spelled correctly.
    **`Error: command failed: EOBJECTNOTFOUND: Node "<node_name>" does not exist.`** — Confirm the node name is valid and part of the cluster using `cluster show`.
---

## SVM Creation

A Storage Virtual Machine (SVM) is the logical container for volumes, LIFs, and protocol access. Each workload (NFS, iSCSI, SMB) typically has its own SVM.

**Create an NFS SVM:**

```bash
vserver create -vserver svm_nfs01 -rootvolume root_nfs01 -rootvolume-security-style unix -language C.UTF-8 -snapshot-policy default

# Add NFS protocol
vserver nfs create -vserver svm_nfs01 -v3 enabled -v4.1 enabled

# Create a data LIF for NFS access
network interface create -vserver svm_nfs01 -lif nfs_lif01 -role data -data-protocol nfs -home-node <node_name> -home-port e0d -address 192.168.10.50 -netmask 255.255.255.0

# Create a default route for the SVM
network route create -vserver svm_nfs01 -destination 0.0.0.0/0 -gateway 192.168.10.1
```


```text title="Expected output"
vserver create: Command completed successfully.
vserver nfs create: NFS enabled on SVM "svm_nfs01".
network interface create: Logical interface "nfs_lif01" created successfully.
  Vserver Name: svm_nfs01
  Logical Interface Name: nfs_lif01
  Role: data
  Data Protocol: nfs
  Address: 192.168.10.50
  Netmask: 255.255.255.0
  Home Node: node-01
  Home Port: e0d
  Status Admin: up
  Status Oper: up
network route create: Route created successfully.
  Vserver: svm_nfs01
  Destination: 0.0.0.0/0
  Gateway: 192.168.10.1
```

!!! warning "Common errors"
    **`Error: command failed: Vserver "svm_nfs01" already exists.`** — Delete the existing SVM with `vserver delete -vserver svm_nfs01` or use a different SVM name.
    **`Error: command failed: Port "e0d" does not exist on node "<node_name>".`** — Verify the correct port name using `network port show -node <node_name>` and update the `-home-port` parameter.
    **`Error: command failed: IP address 192.168.10.50 is already in use.`** — Check for address conflicts with `network interface show -address 192.168.10.50` and assign an unused IP address.
**Create an iSCSI SVM:**

```bash
vserver create -vserver svm_iscsi01 -rootvolume root_iscsi01 -rootvolume-security-style unix

# Enable iSCSI
vserver iscsi create -vserver svm_iscsi01
vserver iscsi show -vserver svm_iscsi01
# Note the iSCSI IQN for this SVM

# Create iSCSI data LIFs (one per node, per fabric)
network interface create -vserver svm_iscsi01 -lif iscsi_lif01 -role data -data-protocol iscsi -home-node <node1> -home-port e0e -address 10.0.10.50 -netmask 255.255.255.0
network interface create -vserver svm_iscsi01 -lif iscsi_lif02 -role data -data-protocol iscsi -home-node <node2> -home-port e0e -address 10.0.10.51 -netmask 255.255.255.0
```


```text title="Expected output"
cluster1::> vserver create -vserver svm_iscsi01 -rootvolume root_iscsi01 -rootvolume-security-style unix
[Job 245] Job succeeded: Vserver creation completed.

cluster1::> vserver iscsi create -vserver svm_iscsi01
(no output — command completes silently)

cluster1::> vserver iscsi show -vserver svm_iscsi01
Vserver    Status
--------   ------
svm_iscsi01 up
Alias: svm_iscsi01
IQN: iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6:vs.1

cluster1::> network interface create -vserver svm_iscsi01 -lif iscsi_lif01 -role data -data-protocol iscsi -home-node node1 -home-port e0e -address 10.0.10.50 -netmask 255.255.255.0
(no output — command completes silently)

cluster1::> network interface create -vserver svm_iscsi01 -lif iscsi_lif02 -role data -data-protocol iscsi -home-node node2 -home-port e0e -address 10.0.10.51 -netmask 255.255.255.0
(no output — command completes silently)

cluster1::> network interface show -vserver svm_iscsi01
            Logical    Status     Network            Current       Current Is
Vserver     Interface  Admin/Oper Address/Mask       Node          Port    Home
----------- ---------- ---------- ------------------ ------------- ------- ----
svm_iscsi01 iscsi_lif01 up/up    10.0.10.50/24      node1         e0e     true
svm_iscsi01 iscsi_lif02 up/up    10.0.10.51/24      node2         e0e     true
```

!!! warning "Common errors"
    **`Error: command failed: Vserver "svm_iscsi01" already exists.`** — Verify the SVM name is unique or delete the existing SVM with `vserver delete -vserver svm_iscsi01` before retrying.
    **`Error: command failed: Port "e0e" does not exist on node "node1".`** — Confirm the correct iSCSI port names with `network port show -node <node>` and update the `-home-port` parameter accordingly.
    **`Error: command failed: Address 10.0.10.50 is already in use.`** — Verify the IP address is not assigned to another interface using `network interface show -address 10.0.10.50` and choose an unused address.
---

## Volume Provisioning

ONTAP volumes are thin-provisioned by default and reside inside aggregates (physical disk groups managed by ONTAP).

**Verify aggregate availability:**

```bash
aggr show
# Aggrs on each node should show Available space > 0
```


```text title="Expected output"
Aggregate                Size Available Used% State   #Vols  Nodes            RAID Status
--------- ----------- --------- --------- ----- ------- ------ --------------- -----------
aggr0_node1
                      744.6GB   156.2GB   79%  online       3 node1            raid_dp, normal
aggr1_node1
                      2.0TB     487.3GB   76%  online      12 node1            raid_dp, normal
aggr0_node2
                      744.6GB   201.5GB   73%  online       2 node2            raid_dp, normal
aggr2_node2
                      3.0TB     892.1GB   70%  online      18 node2            raid_dp, normal
aggr3_node2
                      1.5TB     45.8GB    97%  online       8 node2            raid_dp, degraded
```

!!! warning "Common errors"
    **`Error: command not found: aggr`** — Ensure you are connected to the NetApp cluster via SSH or the ONTAP CLI, not a Linux shell.
    **`Error: This operation is not permitted: insufficient privileges`** — Log in with an admin-level account or request cluster administrator credentials.
**Create an NFS volume:**

```bash
volume create -vserver svm_nfs01 -volume vol_nfs_data01 -aggregate aggr1_node1 -size 1TB -junction-path /nfs_data01 -security-style unix -snapshot-policy default

# Export the volume via NFS policy
export-policy rule create -vserver svm_nfs01 -policyname default -clientmatch 192.168.10.0/24 -rorule sys -rwrule sys -superuser sys
```


```text title="Expected output"
Volume created successfully
Volume "vol_nfs_data01" has been created.

(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: command failed: No matching aggregates found for given criteria`** — Verify the aggregate name exists with `storage aggregate show` and ensure it belongs to the correct node.
    **`Error: command failed: Vserver "svm_nfs01" does not exist`** — Create the SVM first using `vserver create -vserver svm_nfs01` or confirm the SVM name matches your environment.
    **`Error: command failed: Export policy "default" does not exist`** — Create the export policy with `export-policy create -vserver svm_nfs01 -policyname default` before adding rules.
**Create an iSCSI LUN:**

```bash
# Create the containing volume
volume create -vserver svm_iscsi01 -volume vol_lun_sql01 -aggregate aggr1_node1 -size 500GB

# Create the LUN within the volume
lun create -vserver svm_iscsi01 -path /vol/vol_lun_sql01/lun_sql01_data -size 400GB -ostype linux
```


```text title="Expected output"
Volume created successfully.
Created a LUN of size 400GB (429496729600B): path /vol/vol_lun_sql01/lun_sql01_data,
 lunid 0, type linux, size 400GB
```

!!! warning "Common errors"
    **`Error: command failed: No space left on device`** — Verify aggregate aggr1_node1 has sufficient free space with `storage aggregate show -aggregate aggr1_node1`.
    **`Error: command failed: Vserver "svm_iscsi01" does not exist`** — Create the SVM first using `vserver create -vserver svm_iscsi01 -rootvolume root_svm_iscsi01 -aggregate aggr1_node1`.
    **`Error: command failed: LUN path /vol/vol_lun_sql01/lun_sql01_data already exists`** — Use a unique LUN name or delete the existing LUN with `lun delete -vserver svm_iscsi01 -path /vol/vol_lun_sql01/lun_sql01_data`.
**Verify volumes:**

```bash
volume show -vserver svm_nfs01
volume show -vserver svm_iscsi01
```


```text title="Expected output"
Vserver          Volume       Aggregate    State      Type       Size  Available Used%
--------         ------       ---------    -----      ----       ----  --------- -----
svm_nfs01        vol_nfs_data aggr_01      online     RW       500GB    425.2GB   15%
svm_nfs01        vol_nfs_logs aggr_01      online     RW       100GB     89.5GB   10%
svm_nfs01        vol_nfs_snap aggr_02      online     RW       250GB    198.3GB   20%

Vserver          Volume       Aggregate    State      Type       Size  Available Used%
--------         ------       ---------    -----      ----       ----  --------- -----
svm_iscsi01      vol_iscsi_01 aggr_03      online     RW         1TB    856.4GB   14%
svm_iscsi01      vol_iscsi_02 aggr_03      online     RW       500GB    425.1GB   15%
```

!!! warning "Common errors"
    **`Error: command not found: volume`** — Ensure you are connected to the NetApp cluster CLI (use `ssh admin@<cluster-ip>`) and not a local shell.
    **`Error: "svm_nfs01" does not exist`** — Verify the SVM name is correct by running `vserver show` to list all available SVMs.
---

## Host Connectivity

**NFS mount from Linux host:**

```bash
mount -t nfs -o vers=3,rw 192.168.10.50:/nfs_data01 /mnt/ontap_nfs
df -h /mnt/ontap_nfs
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
192.168.10.50:/nfs_data01  2.0T  1.2T  800G  60% /mnt/ontap_nfs
```

!!! warning "Common errors"
    **`mount.nfs: access denied by server while mounting 192.168.10.50:/nfs_data01`** — Verify the NFS export policy on the NetApp filer permits the client IP and check firewall rules allow port 2049/111.
    **`mount.nfs: No such file or directory`** — Confirm the export path `/nfs_data01` exists on the NetApp filer and the mount point `/mnt/ontap_nfs` exists locally (create with `mkdir -p /mnt/ontap_nfs` if needed).
    **`mount: wrong fs type, bad option, bad superblock on 192.168.10.50:/nfs_data01`** — Verify NFSv3 is enabled on the NetApp filer and the client has nfs-utils installed (`yum install nfs-utils` on RHEL/CentOS).
**iSCSI initiator setup (Linux):**

1. Install and start the iSCSI initiator:

```bash
yum install -y iscsi-initiator-utils
systemctl enable --now iscsid
```


```text title="Expected output"
Loaded plugins: fastestmirror
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package iscsi-initiator-utils.x86_64 0:6.2.0.874-17.el7 will be installed
--> Processing Dependency: iscsi-initiator-utils-iscsiuio = 0:6.2.0.874-17.el7 for package: iscsi-initiator-utils-6.2.0.874-17.el7.x86_64
--> Running transaction check
---> Package iscsi-initiator-utils-iscsiuio.x86_64 0:6.2.0.874-17.el7 will be installed
--> Finished Dependency Resolution

Installed:
  iscsi-initiator-utils.x86_64 0:6.2.0.874-17.el7

Dependency Installed:
  iscsi-initiator-utils-iscsiuio.x86_64 0:6.2.0.874-17.el7

Complete!
Created symlink from /etc/systemd/system/multi-user.target.wants/iscsid.service to /usr/lib/systemd/system/iscsid.service.
```

!!! warning "Common errors"
    **`No package iscsi-initiator-utils available.`** — Ensure the RHEL/CentOS base repository is enabled with `yum repolist` and update the package cache with `yum clean all && yum makecache`.
    **`Failed to enable unit: Unit file /usr/lib/systemd/system/iscsid.service not found.`** — Verify the iscsi-initiator-utils package installed successfully and check `/usr/lib/systemd/system/` for the iscsid.service file.
2. Discover ONTAP iSCSI targets:

```bash
iscsiadm -m discovery -t st -p 10.0.10.50
```


```text title="Expected output"
10.0.10.50:3260,1 iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6g7h8:discovery:7mode.filer01
10.0.10.50:3260,2 iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6g7h8:discovery:7mode.filer02
```

!!! warning "Common errors"
    **`iscsiadm: No records found`** — Verify the iSCSI target IP address is correct and reachable with `ping 10.0.10.50`.
    **`iscsiadm: cannot connect to discovery address 10.0.10.50 port 3260`** — Ensure the iSCSI target service is running on the NetApp array and firewall rules allow port 3260 from the initiator host.
3. Log in to all discovered targets:

```bash
iscsiadm -m node -L all
```


```text title="Expected output"
Logging in to [iface: default, target: iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6, portal: 192.168.1.50,3260] (multiple)
Logging in to [iface: default, target: iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6, portal: 192.168.1.51,3260] (multiple)
Logging in to [iface: default, target: iqn.1992-08.com.netapp:sn.x9y8z7w6v5u4, portal: 192.168.1.52,3260] (multiple)
Login to [iface: default, target: iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6, portal: 192.168.1.50,3260] successful.
Login to [iface: default, target: iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6, portal: 192.168.1.51,3260] successful.
Login to [iface: default, target: iqn.1992-08.com.netapp:sn.x9y8z7w6v5u4, portal: 192.168.1.52,3260] successful.
```

!!! warning "Common errors"
    **`iscsiadm: No records found`** — Ensure iSCSI discovery has been performed first with `iscsiadm -m discovery -t sendtargets -p <portal_ip>`.
    **`iscsiadm: Could not login to [iface: default, target: iqn.1992-08.com.netapp:sn.a1b2c3d4e5f6, portal: 192.168.1.50,3260]`** — Verify network connectivity to the iSCSI portal and check that the target is accessible with `ping 192.168.1.50`.
4. Install and configure multipath:

```bash
yum install -y device-mapper-multipath
mpathconf --enable --with_multipathd y
multipath -ll
```


```text title="Expected output"
Loaded plugins: fastestmirror, security
Loading mirror speeds from cached hostfile
Resolving Dependencies
--> Running transaction check
---> Package device-mapper-multipath.x86_64 0:0.4.9-127.el6 will be installed
--> Processing Dependency: device-mapper = 0.4.9-127.el6 for package: device-mapper-multipath-0.4.9-127.el6.x86_64
--> Finished Dependency Resolution
Installing : device-mapper-multipath-0.4.9-127.el6.x86_64                 1/1
Verifying  : device-mapper-multipath-0.4.9-127.el6.x86_64                 1/1
Installed:
  device-mapper-multipath.x86_64 0:0.4.9-127.el6

(no output — command completes silently)

mpatha (360a98000534e45623334486b324d7a41) dm-2 NETAPP,LUN
size=500G features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
|-+- policy='service-time 0' prio=50 status=active
| `- 2:0:0:0 sda 8:0  active ready running
`-+- policy='service-time 0' prio=10 status=enabled
  `- 3:0:0:0 sdb 8:16 active ready running
mpathb (360a98000534e45623334486b324d7a42) dm-3 NETAPP,LUN
size=1T features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  `- 4:0:0:0 sdc 8:32 active ready running
```

!!! warning "Common errors"
    **`mpathconf: command not found`** — Install device-mapper-multipath first or ensure the package installation completed successfully.
    **`multipath: command not found`** — Verify device-mapper-multipath is installed with `rpm -q device-mapper-multipath` and check your PATH environment variable.
**Map the LUN to the host:**

```bash
# Create an igroup (initiator group) with the host's IQN
igroup create -vserver svm_iscsi01 -igroup igrp_linux01 -protocol iscsi -ostype linux -initiator iqn.1994-05.com.redhat:host01

# Map the LUN to the igroup
lun map -vserver svm_iscsi01 -path /vol/vol_lun_sql01/lun_sql01_data -igroup igrp_linux01 -lun-id 0

# Rescan on the host
rescan-scsi-bus.sh
multipath -ll
```


```text title="Expected output"
Created igroup "igrp_linux01" of protocol type "iscsi" for Vserver "svm_iscsi01".
LUN /vol/vol_lun_sql01/lun_sql01_data mapped to igroup igrp_linux01 with LUN ID 0.
Scanning for device changes...
Scanning host 0...
Scanning host 1...
Scanning host 2...
mpatha (360a98000534d49386b6d41496b4f6f44) dm-0 NETAPP,LUN C-Mode
size=500G features='3 queue_if_no_path pg_init_retries 50' hwhandler='1 alua' wp=rw
`-+- policy='service-time 0' prio=50 status=active
  |- 2:0:0:0 sdb 8:16 active ready running
  `- 3:0:0:0 sdc 8:32 active ready running
```

!!! warning "Common errors"
    **`igroup create: entry already exists`** — Use a unique igroup name or verify the igroup doesn't already exist with `igroup show -vserver svm_iscsi01`.
    **`lun map: LUN is already mapped to igroup`** — Check existing mappings with `lun mapping show -vserver svm_iscsi01 -path /vol/vol_lun_sql01/lun_sql01_data` and use a different LUN ID or igroup.
    **`rescan-scsi-bus.sh: command not found`** — Install the sg3-utils package with `apt-get install sg3-utils` (Debian/Ubuntu) or `yum install sg3-utils` (RHEL/CentOS).
---

## SnapMirror

SnapMirror replicates volumes to a remote ONTAP cluster for DR or backup. This section covers the initial configuration; for a full setup guide see the SnapMirror deployment page.

**Prerequisites for SnapMirror:**

- Intercluster LIFs configured on both source and destination clusters
- Cluster peering established
- SVM peering established

**Configure intercluster LIFs:**

```bash
network interface create -vserver <cluster_name> -lif ic_lif01 -role intercluster -home-node <node1> -home-port e0f -address 10.0.20.50 -netmask 255.255.255.0
network interface create -vserver <cluster_name> -lif ic_lif02 -role intercluster -home-node <node2> -home-port e0f -address 10.0.20.51 -netmask 255.255.255.0
```


```text title="Expected output"
(no output — command completes silently)
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: command failed: EINVALIDARGUMENT: Invalid home port e0f on node <node1>`** — Verify the physical port name exists on the node using `network port show -node <node1>` and correct the home-port parameter.
    **`Error: command failed: EOBJECTNOTFOUND: Vserver <cluster_name> does not exist`** — Replace `<cluster_name>` with the actual cluster name obtained from `cluster show` or use the correct vserver name from `vserver show`.
    **`Error: command failed: EADDRINUSE: IP address 10.0.20.50 is already in use`** — Verify the IP addresses are not already assigned to another interface using `network interface show -address 10.0.20.50` and select unused addresses.
**Peer the clusters (run from source):**

```bash
cluster peer create -peer-addrs 10.0.20.60,10.0.20.61
# Enter the passphrase set on the destination cluster
```


```text title="Expected output"
Cluster Peering Initiated
Passphrase (minimum 8 characters):
Passphrase (minimum 8 characters):
Info: Command is running in the background. Use the "cluster peer show" command to view the status of cluster peering.
```

!!! warning "Common errors"
    **`Error: cluster peer create: command not found`** — Ensure you are connected to the NetApp cluster CLI (ssh to cluster management IP) rather than running from a local shell.
    **`Error: Failed to authenticate with peer cluster at 10.0.20.60`** — Verify the peer cluster IP addresses are reachable and the passphrase matches exactly what was configured on the destination cluster.
    **`Error: Cluster peering already exists with peer address 10.0.20.60`** — Check existing peer relationships with `cluster peer show` and remove the duplicate before retrying.
**Create a SnapMirror relationship:**

```bash
snapmirror create -source-path svm_nfs01:vol_nfs_data01 -destination-path svm_dr01:vol_nfs_dr01 -type DP -schedule hourly
snapmirror initialize -destination-path svm_dr01:vol_nfs_dr01
```


```text title="Expected output"
Operation succeeded: SnapMirror relationship created.
Source: svm_nfs01:vol_nfs_data01
Destination: svm_dr01:vol_nfs_dr01
Type: DP
Schedule: hourly
Transfer started.
Transferring data...
Transfer completed successfully.
Total transferred: 847.3 GB
Elapsed time: 12m 34s
Status: Snapmirrored
```

!!! warning "Common errors"
    **`Error: command failed: Relationship already exists.`** — Verify the destination volume doesn't already have an existing SnapMirror relationship using `snapmirror show -destination-path svm_dr01:vol_nfs_dr01`.
    **`Error: command failed: Destination volume is not empty.`** — Ensure the destination volume is initialized as an empty DP volume; if needed, destroy and recreate it with `volume destroy -vserver svm_dr01 -volume vol_nfs_dr01` then `volume create -vserver svm_dr01 -volume vol_nfs_dr01 -aggregate aggr_dr01 -size 1TB -type DP`.
    **`Error: command failed: Source path does not exist.`** — Confirm the source volume exists and the SVM name is correct by running `volume show -vserver svm_nfs01`.
Monitor the initial baseline transfer:

```bash
snapmirror show -destination-path svm_dr01:vol_nfs_dr01
```


```text title="Expected output"
Source Destination Mirror State Relationship Status Last Transfer
svm_prod:vol_nfs_prod svm_dr01:vol_nfs_dr01 SnapMirror Snapmirrored Idle Success 09/15/2024 14:32:18
```

!!! warning "Common errors"
    **`Error: command not found: snapmirror`** — Ensure you are logged into the NetApp cluster CLI (via SSH or console) and not a local shell; snapmirror commands are only available in ONTAP.
    **`Error: Invalid destination path format`** — Use the correct SVM and volume name format (svm_name:volume_name) and verify both exist with `volume show` and `svm show`.
    **`Error: Access denied for snapmirror command`** — Confirm your user role has SnapMirror permissions; contact your cluster administrator to grant the appropriate RBAC role.
---

## Monitoring Setup

**Configure SNMP for monitoring integration:**

```bash
snmp init 1
system snmp community add -community-name public -type ro
system snmp traphost add -peer-address <snmp_manager_ip>
```


```text title="Expected output"
SNMP initialized successfully.
Community 'public' added with read-only access.
Trap host 192.168.1.50 added successfully.
```

!!! warning "Common errors"
    **`Error: SNMP is already initialized`** — Run `snmp status` to verify current state; if already initialized, skip the `snmp init 1` command.
    **`Error: Community 'public' already exists`** — Use `system snmp community modify` instead, or choose a different community name.
    **`Error: Invalid peer address <snmp_manager_ip>`** — Replace `<snmp_manager_ip>` with a valid IPv4 address (e.g., 192.168.1.50) and verify network connectivity to that host.
**Configure SMTP alerts:**

1. In System Manager, navigate to **Cluster > Settings > Notifications**.
2. Set the SMTP server address and destination email.
3. Test the email notification by triggering a test event:

```bash
event notification create -filter-name important-events -destinations snmp-traphost
system health alert show
```


```text title="Expected output"
Event notification rule created successfully.
Rule name: important-events
Destinations: snmp-traphost
Status: enabled

                                    Node: cluster1-01
                                Alertname: DiskShelfPowerSupplyFailed
                             Alertstate: active
                            Severity: critical
                          Description: Disk shelf power supply unit 1 in slot 3 failed
                         Corrective Action: Replace the failed power supply unit
                              Occurred: 2024-01-15 14:32:18 +00:00

                                    Node: cluster1-02
                                Alertname: HighCPUUtilization
                             Alertstate: active
                            Severity: warning
                          Description: CPU utilization on node cluster1-02 is above 85%
                         Corrective Action: Review running processes and redistribute workloads
                              Occurred: 2024-01-15 13:45:02 +00:00
```

!!! warning "Common errors"
    **`Error: destination snmp-traphost does not exist`** — Create the SNMP trap destination first using `event notification destination create -name snmp-traphost -type snmp`.
    **`Error: filter-name important-events already exists`** — Use a unique filter name or delete the existing rule with `event notification delete -filter-name important-events` before recreating it.
**Enable Active IQ integration (Call Home):**

```bash
system node autosupport modify -node * -state enable -transport https -support enable -to admin@example.com
autosupport invoke -node * -type test
```


```text title="Expected output"
node-01: AutoSupport modify successful
node-02: AutoSupport modify successful
node-03: AutoSupport modify successful
node-04: AutoSupport modify successful

node-01: AutoSupport invocation sent successfully (ID: 12345678-1234-1234-1234-123456789abc)
node-02: AutoSupport invocation sent successfully (ID: 87654321-4321-4321-4321-abcdef123456)
node-03: AutoSupport invocation sent successfully (ID: 11111111-2222-3333-4444-555555555555)
node-04: AutoSupport invocation sent successfully (ID: 99999999-8888-7777-6666-444444444444)
```

!!! warning "Common errors"
    **`Error: Invalid email address "admin@example.com"`** — Verify the email address format and ensure it is a valid recipient configured in your support contract.
    **`Error: AutoSupport transport https is not supported on this cluster`** — Check cluster ONTAP version compatibility; use `system node autosupport show` to verify current transport settings and upgrade if necessary.
Verify the test AutoSupport was received by NetApp Active IQ (check the Active IQ portal for the array).

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

## See also

- [Insightiq](../insightiq/)
- [Keystone](../keystone/)
- [Ontap](../ontap/)
- [Operations](../operations/)
- [Snapcenter](../snapcenter/)
- [Snapmirror](../snapmirror/)
- [Superna Eyeglass](../superna-eyeglass/)
- [NetApp — Overview](../)
