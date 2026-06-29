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
rack_nodes: "Rack Nodes" {shape: rectangle}
run_onefs_setup_wizard: "Run OneFS Setup Wizard" {shape: rectangle}
configure_network_interfaces_and_sma: "Configure Network Interfaces and SmartConnect" {shape: rectangle}
add_nodes_to_cluster: "Add Nodes to Cluster" {shape: rectangle}
configure_nfs_and_smb: "Configure NFS and SMB" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> prerequisites
prerequisites -> rack_nodes
rack_nodes -> run_onefs_setup_wizard
run_onefs_setup_wizard -> configure_network_interfaces_and_sma
configure_network_interfaces_and_sma -> add_nodes_to_cluster
add_nodes_to_cluster -> configure_nfs_and_smb
configure_nfs_and_smb -> validate
```

## Before you begin

- **Access:** admin credentials for the target system and any upstream dependencies (DNS, NTP, vCenter, directory services)
- **Timing:** safe to run during a scheduled maintenance window; allow 1-2 hours for initial deployment
- **Dependencies:** network connectivity verified; DNS resolvable; NTP configured; any licence keys available
- **Logging:** record every IP address, hostname, and credential set assigned during this deployment

---

# Dell PowerScale — Initial Deployment

This guide covers deploying a Dell PowerScale (formerly Isilon) cluster from physical node installation through validated NFS and SMB access. Applies to PowerScale F600, H700, and H7000 nodes running OneFS 9.x.

---

## Prerequisites

**Hardware:**

- At minimum three nodes (OneFS requires a quorum of three nodes for cluster formation)
- InfiniBand or 100GbE internal backend switches for intra-cluster communication (Dell provides dedicated backend switches for PowerScale configurations)
- Front-end network switches (10GbE/25GbE) for client data access
- OOB management network for node management interfaces (Eth0 on each node)
- Rack units: each 1U node occupies 1RU; chassis nodes (H7000) are 4U

**Networking plan:**

| Component                | Network          | IP range         |
|--------------------------|------------------|------------------|
| Node management (Eth0)   | OOB management   | 10.0.0.21–23     |
| External client access   | Data VLAN        | 192.168.10.0/24  |
| SmartConnect zone VIP    | Data VLAN        | 192.168.10.100   |
| Backend (internal)       | InfiniBand/100GbE| Factory default  |

**Software and licenses:**

- OneFS license file (capacity-based) from Dell
- SmartConnect Advanced license if you need zone-based DNS failover
- SyncIQ license for replication
- NTP server for cluster time sync (critical for SMB Kerberos authentication)
- AD domain details if SMB with Active Directory authentication is required

---

## Rack Nodes

1. Mount each node into the rack using the rail kit supplied per node. Maintain consistent top-to-bottom order if using Dell-supplied rear backend switches — cable lengths are factory-matched.
2. Connect the backend InfiniBand or 100GbE cables between nodes:
   - Each node has two internal network ports — connect port 1 to the internal switch fabric port A and port 2 to fabric port B.
   - Dell ships the backend switch and cables bundled — do not substitute cable lengths.
3. Connect each node's management Ethernet (Eth0) to the OOB management switch.
4. Connect each node's front-end data ports (10GbE/25GbE) to the client data network switches.
5. Connect PDU cables. Nodes use standard C13/C19 power connectors.
6. Power on all nodes simultaneously by pressing the power button on each or using the Dell IPMI/iDRAC remote power-on if configured.

---

## Run OneFS Setup Wizard

OneFS cluster formation is initiated from the first node (the "wizard node").

1. Connect a serial console cable to Node 1's serial port (or access via iDRAC/IPMI serial-over-LAN).
2. Log in as `root` using the default password printed on the node's service tag.
3. Launch the cluster creation wizard:

```bash
isi_setup
```


```text title="Expected output"
Dell EMC PowerScale OneFS Setup Utility
Version: 9.4.0.0 (Build 084)

Welcome to the Interactive Setup Wizard
=====================================

System Information:
  Hostname: isilon-node-01
  Serial Number: ACR2024001234
  Model: PowerScale F200
  Cluster UUID: 550e8400-e29b-41d4-a716-446655440000

Current Configuration Status:
  Cluster Name: Not configured
  Network: Not configured
  Licensing: Not configured

Starting configuration wizard...
Press Enter to continue or 'q' to quit:
```

!!! warning "Common errors"
    **`isi_setup: command not found`** — Ensure you are logged in as root or a user with administrative privileges, or run the command from the correct OneFS node.
    **`Error: Cluster already initialized`** — Run `isi_setup --reset` to reconfigure an existing cluster, or use `isi config` for modifications instead.
4. When prompted:
   - **Cluster name:** Enter the cluster name (e.g., `pscale-prod`).
   - **Internal network:** Select the InfiniBand or backend interface. Accept the factory defaults for internal IP range.
   - **External IP:** Assign the node's external management IP.
   - **Default gateway:** Enter the gateway for the external network.
   - **DNS:** Enter DNS server IPs.
   - **Join or create cluster:** Select **Create new cluster**.
5. The wizard finalizes cluster formation. The WebUI becomes accessible at `https://<node1_external_IP>:8080`.

---

## Configure Network Interfaces and SmartConnect

OneFS uses IP pools (sets of external IPs) and SmartConnect zones for client access. SmartConnect balances NFS/SMB connections across nodes.

**Create an IP pool for client access:**

1. In the OneFS WebUI, navigate to **Cluster Management > Network Configuration > External Network > Subnets**.
2. Select the external subnet (or create one for the client VLAN).
3. Under the subnet, click **Add Pool**.
4. Set:
   - Pool name: `client_pool`
   - Address range: assign a block of IPs (one per node)
   - Allocation method: **Dynamic** (SmartConnect assigns client connections)
   - SmartConnect zone name: `pscale.example.com`
   - SmartConnect service IP (VIP): `192.168.10.100` — this is the single DNS name clients resolve

**Configure SmartConnect DNS delegation:**

1. In your corporate DNS server, create a delegation for `pscale.example.com` pointing to the SmartConnect service IP (`192.168.10.100`).
2. Clients resolve `pscale.example.com` and SmartConnect returns the IP of the least-loaded node.

**Verify interface status via CLI:**

```bash
isi network interfaces list
isi network pools list
```


```text title="Expected output"
Name                          IP Address      Netmask             Broadcast           MAC Address
eth0                          192.168.1.45    255.255.255.0       192.168.1.255       00:0a:95:9d:68:16
eth1                          192.168.1.46    255.255.255.0       192.168.1.255       00:0a:95:9d:68:17
eth2                          10.20.30.100    255.255.255.0       10.20.30.255        00:0a:95:9d:68:18
mgmt0                         172.16.0.50     255.255.255.0       172.16.0.255        00:0a:95:9d:68:19

Name                          Subnet          Ranges
pool-data-01                  192.168.1.0/24  192.168.1.100-192.168.1.200
pool-data-02                  10.20.30.0/24   10.20.30.50-10.20.30.150
pool-mgmt                     172.16.0.0/24   172.16.0.10-172.16.0.100
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure you are logged into the PowerScale cluster via SSH or the OneFS CLI is installed on your local system.
    **`Error: Permission denied`** — Verify your user account has sufficient privileges; use an account with cluster administrator or network administrator role.
---

## Add Nodes to Cluster

Additional nodes join the cluster after the first node is set up.

1. Power on the new node.
2. Connect to its serial console and log in as `root`.
3. Run the setup wizard on the new node:

```bash
isi_setup
```


```text title="Expected output"
OneFS Setup Wizard v9.4.0.0 (Build 9.4.0.0_1)
Copyright (c) 2024 Dell Inc. All rights reserved.

Welcome to the OneFS Setup Wizard
==================================

This wizard will guide you through the initial configuration of your PowerScale cluster.

Press Enter to continue or Ctrl+C to exit...

Step 1: Network Configuration
-----------------------------
Enter the cluster name [powerscale-cluster]: 
Enter the primary IP address [192.168.1.10]: 
Enter the netmask [255.255.255.0]: 
Enter the default gateway [192.168.1.1]: 
Enter DNS servers (comma-separated) [8.8.8.8]: 

Configuration Summary
---------------------
Cluster Name: powerscale-cluster
Primary IP: 192.168.1.10
Netmask: 255.255.255.0
Gateway: 192.168.1.1
DNS: 8.8.8.8

Apply configuration? (yes/no):
```

!!! warning "Common errors"
    **`isi_setup: command not found`** — Ensure you are logged into the PowerScale cluster console or SSH session with appropriate permissions.
    **`ERROR: Failed to apply network configuration - Address already in use`** — Verify the IP address is not already assigned to another device on the network before proceeding.
    **`ERROR: Setup wizard interrupted - incomplete configuration detected`** — Run `isi_setup` again and complete all required steps without interruption.
4. At the join prompt, select **Join existing cluster**.
5. Enter the existing cluster's internal IP (the first node's internal backend IP).
6. Enter the cluster's join password (set during cluster creation).
7. The new node joins and the cluster redistributes data automatically across all nodes.
8. Monitor join progress from the WebUI under **Cluster Management > Cluster Overview**. The new node appears with status **Joining** and transitions to **Healthy**.

Verify node count:

```bash
isi status -q
# Should show all nodes as healthy
```


```text title="Expected output"
Cluster Name: prod-cluster-01
Cluster Health: HEALTHY
Node Status:
  Node 1 (192.168.1.10): HEALTHY - CPU: 45%, Memory: 62%, Disk: 78%
  Node 2 (192.168.1.11): HEALTHY - CPU: 38%, Memory: 58%, Disk: 75%
  Node 3 (192.168.1.12): HEALTHY - CPU: 52%, Memory: 71%, Disk: 82%
  Node 4 (192.168.1.13): HEALTHY - CPU: 41%, Memory: 65%, Disk: 79%
Replication Status: IN_SYNC
Last Updated: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the OneFS CLI tools are installed and the `isi` binary is in your PATH, or run the command from a system with OneFS SDK installed.
    **`Error: Unable to connect to cluster at <IP>`** — Verify network connectivity to the cluster management IP and confirm the cluster is powered on and fully booted.
    **`Error: Authentication failed`** — Confirm you have valid OneFS credentials configured and the user account has sufficient privileges to query cluster status.
---

## Configure NFS and SMB

**NFS export:**

1. Navigate to **Protocols > Unix Sharing (NFS) > NFS Exports > Create Export**.
2. Set:
   - Directory path: `/ifs/data/nfs_share01`
   - Clients: IP range or subnet allowed to mount (e.g., `192.168.10.0/24`)
   - Access permissions: `Read/Write`
   - Root squash: enabled (recommended for security)
3. Click **Add Export**.
4. From a Linux client:

```bash
mount -t nfs pscale.example.com:/ifs/data/nfs_share01 /mnt/pscale_nfs
df -h /mnt/pscale_nfs
```


```text title="Expected output"
Filesystem      Size  Used Avail Use% Mounted on
pscale.example.com:/ifs/data/nfs_share01  50T   12T   38T  24% /mnt/pscale_nfs
```

!!! warning "Common errors"
    **`mount.nfs: access denied by server while mounting pscale.example.com:/ifs/data/nfs_share01`** — Verify the PowerScale export policy allows the client IP and check firewall rules between client and PowerScale cluster.
    **`mount.nfs: No such file or directory`** — Ensure the mount point `/mnt/pscale_nfs` exists; create it with `mkdir -p /mnt/pscale_nfs` if needed.
    **`mount.nfs: Connection timed out`** — Confirm DNS resolves `pscale.example.com` correctly and that network connectivity exists to the PowerScale cluster on port 2049.
**SMB share (Active Directory integration):**

1. Join the cluster to Active Directory:

```bash
isi auth ads create --name CORP.EXAMPLE.COM --user Administrator --password <password>
```


```text title="Expected output"
Creating Active Directory provider...
Active Directory provider 'CORP.EXAMPLE.COM' created successfully.
Provider ID: 12345678-90ab-cdef-1234-567890abcdef
Status: online
Domain: corp.example.com
Joined: true
```

!!! warning "Common errors"
    **`Error: Authentication failed for user 'Administrator'`** — Verify the password is correct and the user account has sufficient privileges to join the domain.
    **`Error: Cannot resolve domain 'CORP.EXAMPLE.COM'`** — Ensure DNS is configured correctly on the PowerScale cluster and can resolve the Active Directory domain name.
    **`Error: Active Directory provider 'CORP.EXAMPLE.COM' already exists`** — Remove the existing provider with `isi auth ads delete --name CORP.EXAMPLE.COM` before creating a new one.
2. Verify AD join:

```bash
isi auth ads list
```


```text title="Expected output"
Name                    Status          Domain
----                    ------          ------
CORP.EXAMPLE.COM        connected       corp.example.com
LAB.INTERNAL            connected       lab.internal
LEGACY.DOMAIN           disconnected    legacy.domain
----
3 ADS configurations found
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure you are running this command on a PowerScale cluster node with the OneFS CLI installed, or SSH to the cluster management IP first.
    **`Error: Permission denied`** — Run the command with appropriate privileges; use `sudo isi auth ads list` or ensure your user account has cluster administrator role.
3. Navigate to **Protocols > Windows Sharing (SMB) > SMB Shares > Create Share**.
4. Set:
   - Share name: `data01`
   - Directory: `/ifs/data/smb_share01`
   - Permissions: add AD groups with appropriate read/write access
5. From a Windows client:

```cmd
net use Z: \\pscale.example.com\data01 /persistent:yes
```

---

## Configure SyncIQ for Replication

SyncIQ replicates OneFS directories to a target cluster for DR or data distribution.

**On the source cluster:**

1. Navigate to **Data Protection > SyncIQ > Policies > Create Policy**.
2. Set:
   - Policy name: `replicate_data01`
   - Action: **Synchronize**
   - Source directory: `/ifs/data`
   - Target cluster: enter the target cluster's SmartConnect hostname or IP
   - Target directory: `/ifs/replica/data`
   - Schedule: every 1 hour or as required by RPO
3. Click **Create Policy**.

**Run the first sync manually:**

```bash
isi sync policies run replicate_data01
```


```text title="Expected output"
Job ID: 1234567890
Policy: replicate_data01
State: RUNNING
Progress: 0%
Started: 2024-01-15T09:23:47Z
Source Path: /ifs/data/prod
Target Path: 192.168.1.50:/ifs/backup
Estimated Time Remaining: 2h 15m
Bytes Processed: 0 B
Bytes Remaining: 847.3 GB
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the OneFS CLI tools are installed and the `isi` binary is in your PATH, or run the command from the cluster management node.
    **`Error: Policy 'replicate_data01' not found`** — Verify the policy name exists by running `isi sync policies list` and confirm the exact spelling and case.
    **`Error: Access denied`** — Confirm your user account has administrative privileges on the PowerScale cluster or request elevated permissions from your storage administrator.
**Monitor sync progress:**

```bash
isi sync jobs list
# Shows the running job, bytes transferred, ETA
```


```text title="Expected output"
ID    State      Policy Name              Progress  Bytes Transferred  ETA
1     running    daily-backup-prod        45%       2.3 TB             2h 15m
2     running    archive-tier2            12%       847 GB             5h 42m
3     completed  weekly-full-sync         100%      5.6 TB             —
4     paused     disaster-recovery        78%       4.1 TB             paused
5     failed     incremental-sync-dr      0%        0 B                failed
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure the OneFS CLI tools are installed and the `isi` binary is in your PATH, or run from the PowerScale management node.
    **`Error: Authentication failed`** — Verify your credentials are valid and you have sufficient permissions; use `isi auth status` to check your current session.
    **`Error: Connection refused on 192.168.1.100:8080`** — Confirm the PowerScale cluster is reachable and the management interface is running; check network connectivity and firewall rules.
**On the target cluster**, verify the directory is populated:

```bash
ls /ifs/replica/data
```


```text title="Expected output"
drwxr-xr-x  4 root  wheel   4096 Nov 15 10:23 backup_001
drwxr-xr-x  3 root  wheel   4096 Nov 14 08:45 backup_002
drwxr-xr-x  5 root  wheel   4096 Nov 13 16:12 archive
drwxr-xr-x  2 root  wheel   4096 Nov 12 22:33 temp_sync
-rw-r--r--  1 root  wheel 2147483648 Nov 15 09:18 dataset.tar.gz
```

!!! warning "Common errors"
    **`ls: cannot access '/ifs/replica/data': No such file or directory`** — Verify the /ifs mount point is accessible and the replica dataset exists using `isi filesystem list`.
    **`ls: cannot open directory '/ifs/replica/data': Permission denied`** — Check that your user has read permissions on the directory with `isi auth access /ifs/replica/data`.
---

## Validate

1. Confirm all nodes are healthy:

```bash
isi status
# All nodes should show "Healthy" — no errors or warnings
```


```text title="Expected output"
Cluster Name: isilon-prod-01
Cluster Health: Healthy
Node 1 (192.168.1.101): Healthy
Node 2 (192.168.1.102): Healthy
Node 3 (192.168.1.103): Healthy
Node 4 (192.168.1.104): Healthy
Node 5 (192.168.1.105): Healthy
Cluster Status: All nodes operational
Last Updated: 2024-01-15 14:32:18 UTC
```

!!! warning "Common errors"
    **`isi: command not found`** — Ensure you are connected to the PowerScale cluster via SSH or have the OneFS CLI tools installed in your PATH.
    **`Connection refused on 192.168.1.100:8080`** — Verify network connectivity to the cluster management IP and confirm the OneFS API service is running with `systemctl status isi-api`.
    **`Authentication failed: Invalid credentials`** — Confirm your user account has appropriate permissions and re-authenticate using `isi auth login` or check your SSH key configuration.
2. Check the cluster's drive health:

```bash
isi devices drive list
# All drives should show status "HEALTHY"
```


```text title="Expected output"
Drive ID          Slot  Status    Capacity  Model                Serial Number
1.1               1     HEALTHY   10.9 TB   SEAGATE ST12000NM0007  Z4G1ABCD
1.2               2     HEALTHY   10.9 TB   SEAGATE ST12000NM0007  Z4G1ABCE
1.3               3     HEALTHY   10.9 TB   SEAGATE ST12000NM0007  Z4G1ABCF
1.4               4     HEALTHY   10.9 TB   SEAGATE ST12000NM0007  Z4G1ABCG
1.5               5     HEALTHY   10.9 TB   SEAGATE ST12000NM0007  Z4G1ABCH
1.6               6     HEALTHY   10.9 TB   SEAGATE ST12000NM0007  Z4G1ABCI
1.7               7     HEALTHY   10.9 TB   SEAGATE ST12000NM0007  Z4G1ABCJ
1.8               8     HEALTHY   10.9 TB   SEAGATE ST12000NM0007  Z4G1ABCK
```

!!! warning "Common errors"
    **`Error: Invalid credentials or insufficient permissions`** — Ensure your OneFS admin account has cluster administration privileges or run the command with appropriate sudo access.
    **`Error: Connection refused to cluster management interface`** — Verify the cluster is online and accessible by running `ping <cluster-ip>` and checking network connectivity to port 8080.
3. Verify NFS mounts from multiple clients to confirm SmartConnect is distributing connections across nodes.
4. Run a write test to confirm throughput meets expectations:

```bash
dd if=/dev/zero of=/mnt/pscale_nfs/test.bin bs=1M count=10240 oflag=direct
```


```text title="Expected output"
10240+0 records in
10240+0 records out
10737418240 bytes (10 GB, 10 GiB) copied, 45.2341 s, 237 MB/s
```

!!! warning "Common errors"
    **`dd: failed to open '/mnt/pscale_nfs/test.bin' for writing: Permission denied`** — Verify the NFS mount is writable and the user has sufficient permissions on the PowerScale export.
    **`dd: failed to open '/mnt/pscale_nfs/test.bin' for writing: No space left on device`** — Check available capacity on the PowerScale cluster with `df -h /mnt/pscale_nfs` and ensure sufficient free space exists.
    **`dd: opening '/mnt/pscale_nfs/test.bin': Stale file handle`** — Remount the NFS export with `umount /mnt/pscale_nfs && mount -t nfs <powerscale-ip>:/export /mnt/pscale_nfs` to refresh the connection.
5. Confirm SyncIQ policy ran successfully and shows **Finished** status under **Data Protection > SyncIQ > Reports**.
6. Check no active alerts under **Cluster Management > Events**.

---

## Verify

- **Cluster health:** all nodes show online in the management UI
- **Volume access:** mount a test LUN/NFS export from a host and confirm read/write
- **Replication:** confirm replication partner shows last-sync within RPO window

---

## See also

- [Powerscale — Procedures](../operations/procedures/)
- [Powerscale — Common Issues](../troubleshooting/common-issues/)
- [Powerscale — How It Works](../architecture/how-it-works/)
