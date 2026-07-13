---
tags:
  - nutanix
  - deploy
  - foundation
search:
  boost: 1.5
description: "End-to-end Nutanix cluster deployment — Foundation imaging, IPMI/iDRAC pre-flight, cluster creation via ncli, network configuration, Prism Element initial..."
---
# Nutanix — Deploy

<div class="kb-summary">
End-to-end Nutanix cluster deployment — Foundation imaging, IPMI/iDRAC pre-flight, cluster creation via ncli, network configuration, Prism Element initial setup, Active Directory join, and post-deploy NCC validation.

*Applies to: AOS 6.x · AHV*
</div>

---

```d2
direction: right

plan: "Plan" {shape: oval}
phase_1_preflight_checks: "Phase 1 — Pre-flight Checks" {shape: rectangle}
phase_2_foundation_imaging: "Phase 2 — Foundation Imaging" {shape: rectangle}
phase_3_cluster_creation: "Phase 3 — Cluster Creation" {shape: rectangle}
phase_4_initial_configuration: "Phase 4 — Initial Configuration" {shape: rectangle}
phase_5_postdeploy_validation: "Phase 5 — Post-Deploy Validation" {shape: rectangle}
prism_central_registration_optional: "Prism Central Registration (Optional)" {shape: rectangle}
validate: "Validate" {shape: oval}

plan -> phase_1_preflight_checks
phase_1_preflight_checks -> phase_2_foundation_imaging
phase_2_foundation_imaging -> phase_3_cluster_creation
phase_3_cluster_creation -> phase_4_initial_configuration
phase_4_initial_configuration -> phase_5_postdeploy_validation
phase_5_postdeploy_validation -> prism_central_registration_optional
prism_central_registration_optional -> validate
```

## Before you begin

<!-- video-link -->
!!! tip "Video Walkthrough"
    [:fontawesome-brands-youtube: Installation for AOS and AHV | Nutanix Community Edition 2.1](https://www.youtube.com/watch?v=1Rq_mlwkPME){ .md-button }
<!-- /video-link -->

- **Access:** IPMI/iDRAC/iLO credentials for all nodes; network switch admin access
- **Files:** AOS ISO and AHV ISO (download from Nutanix support portal: portal.nutanix.com)
- **IPs allocated (per node):** IPMI IP, AHV host IP, CVM IP + 1 cluster VIP + 1 DSIP
- **DNS records:** forward + reverse for all node IPs and the cluster VIP
- **NTP server:** reachable from all CVM and AHV management IPs
- **Switch configured:** storage VLAN with MTU 9000; management VLAN; VM VLANs trunked

---

## Phase 1 — Pre-flight Checks

### IPMI / Out-of-Band Access

Verify IPMI access to each node before racking:

```bash
# Test IPMI connectivity (from deployment workstation)
ipmitool -I lanplus -H <ipmi-ip> -U ADMIN -P <password> chassis power status

# Verify virtual console works (needed for Foundation)
# Access: https://<ipmi-ip> → Remote Console
```


```text title="Expected output"
Chassis Power is on
```

!!! warning "Common errors"
    **`Error: Unable to establish IPMI v1 / IPMI v2 / IPMI v1.5 session`** — Verify the IPMI IP address is correct, the IPMI interface is powered on, and the network path is reachable with `ping <ipmi-ip>`.
    **`Error: Authentication failed`** — Confirm the ADMIN username and password are correct; reset IPMI credentials via the node's physical interface or BMC if locked out.
    **`Error: Unable to establish LAN session`** — Ensure the IPMI network interface is configured with a valid IP address and that your deployment workstation has network connectivity to the IPMI subnet.
Each node must have a unique IPMI IP on a dedicated OOB network.

### Network Pre-flight

```bash
# Verify MTU 9000 on storage VLAN (run from each node after OS is up)
ping -c 4 -M do -s 8972 <other-cvm-ip>

# Verify VLAN tags are correct on switch (show interface trunk on Cisco)
# Each node bond should see: mgmt VLAN (native), storage VLAN, VM VLANs (tagged)
```


```text title="Expected output"
PING 10.20.50.12 (10.20.50.12) 8972(9000) bytes of data.
8980 bytes from 10.20.50.12: icmp_seq=1 time=0.842 ms
8980 bytes from 10.20.50.12: icmp_seq=2 time=0.756 ms
8980 bytes from 10.20.50.12: icmp_seq=3 time=0.891 ms
8980 bytes from 10.20.50.12: icmp_seq=4 time=0.773 ms

--- 10.20.50.12 statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/stddev = 0.756/0.815/0.891/0.052 ms
```

!!! warning "Common errors"
    **`ping: sendmsg: Message too long`** — Verify MTU is set to 9000 on the storage VLAN interface with `ip link show` and adjust with `ip link set dev <interface> mtu 9000` if needed.
    **`100% packet loss`** — Confirm the storage VLAN is correctly tagged on the switch port and the CVM IP is reachable by checking switch trunk configuration and VLAN membership.
    **`connect: Network is unreachable`** — Ensure the storage VLAN routing is configured and the target CVM IP is on the same subnet as the source node's storage interface.
---

## Phase 2 — Foundation Imaging

Foundation is Nutanix's deployment tool that discovers nodes via IPMI and installs AOS + AHV in parallel.

### Run Foundation VM

Foundation runs as a VM (download OVA from portal.nutanix.com):

```text
1. Deploy Foundation OVA to any hypervisor with IPMI network access
2. Start Foundation VM → open browser to http://<foundation-ip>:8000
3. Foundation Discovery:
   - Click "Start Discovery" → Foundation finds nodes via IPMI multicast or manual IP entry
   - Select nodes to image

4. AOS configuration:
   - AOS version: select downloaded AOS installer
   - AHV version: select downloaded AHV installer (if using AHV)

5. Per-node configuration:
   - IPMI IP (pre-set on each node)
   - Hypervisor (AHV) IP — the management IP the AHV host will use
   - CVM IP — the Controller VM IP on each node
   - Hypervisor VLAN: management VLAN ID

6. Click "Start" — Foundation images all nodes in parallel (~45–90 min)
```

**During imaging:** Foundation boots each node via IPMI virtual media, formats local disks, installs AHV, and starts the CVM. Progress visible in the Foundation UI.

**Expected result:** All nodes show green in Foundation. CVMs reachable via SSH on their management IPs.

### Verify Nodes Post-Imaging

```bash
# SSH to each CVM and verify AOS services are running
ssh nutanix@<cvm-ip>   # password: nutanix/4u (change immediately)
genesis status          # all services should be running
cluster status          # cluster not yet created — "Not part of a cluster"
```


```text title="Expected output"
nutanix@cvm-1:~$ genesis status
  NtnxHypervisor: RUNNING
  Cassandra: RUNNING
  Zookeeper: RUNNING
  Chronos: RUNNING
  Prism: RUNNING
  Curator: RUNNING
  Cerebro: RUNNING
  Insights: RUNNING
All services operational.

nutanix@cvm-1:~$ cluster status
Not part of a cluster yet. Please run cluster create to initialize.
```

!!! warning "Common errors"
    **`Permission denied (publickey,password)`** — Verify the CVM IP is correct and the default nutanix/4u credentials are still active; if changed, use the correct password or SSH key.
    **`Command 'genesis' not found`** — Ensure you are logged in as the nutanix user (not root) and the PATH includes /home/nutanix/bin; run `source ~/.bashrc` if needed.
---

## Phase 3 — Cluster Creation

```bash
# SSH to any CVM
ssh nutanix@<cvm1-ip>

# Create the cluster (list all CVM IPs)
cluster -s <cvm1-ip>,<cvm2-ip>,<cvm3-ip> create

# Example with 3 nodes:
cluster -s 10.0.1.11,10.0.1.12,10.0.1.13 create
```


```text title="Expected output"
nutanix@cvm1:~$ ssh nutanix@10.0.1.11
The authenticity of host '10.0.1.11 (10.0.1.11)' can't be established.
ECDSA key fingerprint is SHA256:aBcD1234eFgH5678iJkL9012mNoPqRsT3456uVwXyZ.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.0.1.11' (ECDSA) to /etc/ssh/known_hosts.
nutanix@10.0.1.11's password:
nutanix@cvm1:~$ cluster -s 10.0.1.11,10.0.1.12,10.0.1.13 create
2024-01-15 14:32:18 INFO: Initializing cluster creation with 3 nodes
2024-01-15 14:32:22 INFO: Validating node connectivity... OK
2024-01-15 14:32:45 INFO: Configuring cluster metadata
2024-01-15 14:35:12 INFO: Cluster 'NTNX-12a34b5c-6d78-9e0f-1a2b-3c4d5e6f7g8h' created successfully
2024-01-15 14:35:15 INFO: Prism Element available at https://10.0.1.11:9440
```

!!! warning "Common errors"
    **`cluster: command not found`** — Ensure you are logged in as the nutanix user on a CVM and the cluster binary is in your PATH; try `/home/nutanix/cluster -s ...` if needed.
    **`Error: Node 10.0.1.13 is unreachable`** — Verify network connectivity between CVMs and that all three nodes are powered on and have completed their boot sequence.
    **`Error: Cluster already exists on this node`** — Run `cluster destroy` on all nodes first, or use a different set of CVMs that have not been previously clustered.
**Expected output:** Cluster creation takes 5–10 minutes. Watch for `Cluster successfully created`.

```bash
# Set the cluster name
ncli cluster edit-params new-name=<cluster-name>

# Set the cluster Virtual IP (VIP) — used for Prism and management access
ncli cluster edit-params external-ip-address=<cluster-vip>

# Set the Data Services IP (DSIP) — iSCSI endpoint for volume groups
ncli cluster edit-params external-data-services-ip-address=<dsip>

# Verify cluster is up
cluster status    # all services running
ncli cluster info
```


```text title="Expected output"
cluster name updated successfully
cluster external ip address updated successfully
cluster data services ip address updated successfully

Cluster Status: COMPLETE
Cluster Redundancy Factor: 3
Cluster Timezone: UTC
Cluster Creation Time: 2024-01-15 09:22:14
Cluster External IP Address: 10.20.30.40
Cluster External Data Services IP Address: 10.20.30.41
Cluster Version: el7.9-5.20.4.1-stable
Number of Nodes: 4
Number of vCPUs: 128
Physical Memory: 512 GB
```

!!! warning "Common errors"
    **`ncli: command not found`** — Ensure you are running this command on a Nutanix cluster node or install the Nutanix CLI tools on your management workstation.
    **`Error: Cluster is not in a valid state for this operation`** — Wait for any ongoing cluster operations to complete before attempting to modify cluster parameters.
    **`Error: Invalid IP address format for external-ip-address`** — Verify the IP address is valid and reachable on your management network before applying the configuration.
---

## Phase 4 — Initial Configuration

### DNS and NTP

```bash
# Set DNS servers
ncli cluster edit-params dns-server-ip-address-list=<dns1>,<dns2>

# Set NTP servers
ncli cluster edit-params ntp-server-ip-address-list=<ntp1>,<ntp2>

# Verify NTP sync
allssh "ntpq -pn"   # all CVMs should show * next to the active NTP server
```


```text title="Expected output"
cluster.edit_params: Cluster edit succeeded.
cluster.edit_params: Cluster edit succeeded.
192.168.1.10 :
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp1.corp.local  10.0.0.1     2 u   64  128  377   12.543   -2.134   1.876
+ntp2.corp.local  10.0.0.2     2 u   61  128  377   14.221    1.456   2.103

192.168.1.11 :
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp2.corp.local  10.0.0.2     2 u   52  128  377   13.987    0.876   1.654
+ntp1.corp.local  10.0.0.1     2 u   59  128  377   12.654   -1.234   2.341

192.168.1.12 :
     remote           refid      st t when poll reach   delay   offset  jitter
==============================================================================
*ntp1.corp.local  10.0.0.1     2 u   48  128  377   11.876    2.109   1.432
```

!!! warning "Common errors"
    **`Error: Invalid IP address format`** — Ensure DNS and NTP server IPs are comma-separated without spaces (e.g., `10.0.0.1,10.0.0.2`).
    **`Error: Unable to reach NTP server <ntp1>`** — Verify NTP server IPs are reachable from the cluster and firewall allows UDP port 123 outbound.
    **`Error: allssh: command not found`** — Run the ntpq command directly on a CVM using `ssh nutanix@<cvm-ip>` or ensure you are executing from a Nutanix cluster node.
### Admin Password

```bash
# Change default admin password immediately
ncli user change-password username=admin \
  current-password="Nutanix/4u" new-password=<new-password>
```


```text title="Expected output"
(no output — command completes silently)
```

!!! warning "Common errors"
    **`Error: Invalid credentials for user admin`** — Verify the current password matches the default "Nutanix/4u" and that the admin user exists on the cluster.
    **`Error: Password does not meet complexity requirements`** — Ensure the new password is at least 8 characters and includes uppercase, lowercase, numbers, and special characters.
### SMTP Alerts

```text
Prism Element → Settings → SMTP Server
  Server: smtp.corp.local
  Port: 587
  Auth: TLS + credentials
  From: nutanix-alerts@corp.local

Prism Element → Settings → Alert Email
  Add recipient: infra-team@corp.local
  Alert severity: Critical and Warning
```

### Active Directory Join

```text
Prism Element → Settings → Authentication → Directory Services → Add Directory
  Type: Active Directory
  Domain: corp.local
  Directory URL: ldap://dc01.corp.local:389
  Service account: svc-nutanix@corp.local + password
  Search base: DC=corp,DC=local

Prism Element → Settings → Role Mapping → Add Mapping
  AD Group: nutanix-admins → Role: Cluster Admin
```

### Storage Configuration

```bash
# List existing storage pools (created automatically during cluster creation)
ncli sp list

# Create a VM container (datastore)
ncli ctr create name=VMs sp-name=default-storage-pool \
  compression-enabled=true compression-delay-in-secs=0

# Create a backup container (with EC-X)
ncli ctr create name=Backups sp-name=default-storage-pool \
  compression-enabled=true erasure-code=on

# Verify containers
ncli ctr list
```


```text title="Expected output"
Storage Pool List
================================================================================
                          Name                              Uuid
================================================================================
default-storage-pool      5c4d8e2a-91f3-4b2c-a7e9-2f6d1c3b8a9e

Container VMs created successfully with UUID: a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6
Container Backups created successfully with UUID: b2c3d4e5-f6g7-8h9i-0j1k-l2m3n4o5p6q7

                                   Container List
================================================================================
Name          Uuid                                  Pool Name              Compression
================================================================================
VMs           a1b2c3d4-e5f6-7g8h-9i0j-k1l2m3n4o5p6 default-storage-pool  Enabled
Backups       b2c3d4e5-f6g7-8h9i-0j1k-l2m3n4o5p6q7 default-storage-pool  Enabled (EC-X)
```

!!! warning "Common errors"
    **`Error: Storage pool 'default-storage-pool' not found`** — Verify the pool name with `ncli sp list` and use the exact name from the output.
    **`Error: Container name 'VMs' already exists`** — Use a unique container name or delete the existing container with `ncli ctr delete name=VMs` first.
    **`Error: Erasure coding not supported on this cluster`** — Verify cluster supports EC-X by checking `ncli cluster info` and ensure you have sufficient nodes (minimum 4 for EC-X).
---

## Phase 5 — Post-Deploy Validation

### NCC Health Check

```bash
# Run from any CVM (takes 15–30 minutes)
ssh nutanix@<cvm-ip>
ncc --health_checks run_all 2>&1 | tee /tmp/ncc-baseline.txt

# Check summary
ncc --health_checks run_all 2>&1 | grep -E "PASS|FAIL|WARN|ERR"
```


```text title="Expected output"
nutanix@cvm-10-20-1-45:~$ ncc --health_checks run_all 2>&1 | tee /tmp/ncc-baseline.txt
Starting NCC health checks on node cvm-10-20-1-45 (build 20230815.1234)...
[INFO] Running cluster connectivity checks...
[INFO] Running storage pool checks...
[INFO] Running NTP synchronization checks...
[INFO] Running DNS resolution checks...
[INFO] Running hypervisor resource checks...
[PASS] Cluster quorum: All 3 nodes reachable
[PASS] NTP offset within tolerance (offset: 12ms)
[PASS] DNS resolution: 8.8.8.8 reachable
[WARN] Storage pool fragmentation at 34% on pool-uuid-a1b2c3d4
[PASS] vSAN/AHV network latency acceptable
[INFO] Health check completed in 18 minutes 42 seconds
Results saved to /tmp/ncc-baseline.txt

nutanix@cvm-10-20-1-45:~$ ncc --health_checks run_all 2>&1 | grep -E "PASS|FAIL|WARN|ERR"
[PASS] Cluster quorum: All 3 nodes reachable
[PASS] NTP offset within tolerance (offset: 12ms)
[PASS] DNS resolution: 8.8.8.8 reachable
[WARN] Storage pool fragmentation at 34% on pool-uuid-a1b2c3d4
[PASS] vSAN/AHV network latency acceptable
```

!!! warning "Common errors"
    **`ncc: command not found`** — Verify you are logged into a Nutanix CVM (not a hypervisor host) and that ncc is in the PATH by running `which ncc`.
    **`Connection refused` or `timeout connecting to cluster`** — Ensure the CVM is fully booted, the cluster is online, and all three nodes are reachable via `ping <cvm-ip>`.
    **`Permission denied` or `Authentication failed`** — Confirm you are using the correct nutanix user credentials and that SSH key-based auth is configured, or use `ssh -u nutanix@<cvm-ip>` with a password prompt.
**Expected result:** All checks PASS. Any FAIL must be resolved before going production.

### Cluster Resilience Check

```bash
# Verify cluster can tolerate a node failure
ncli cluster get-domain-fault-tolerance-status type=node

# Expected: FaultToleranceStatus = CAN_TOLERATE_FAILURE_COUNT=1 (RF2) or =2 (RF3)
```


```text title="Expected output"
Cluster
                    =======
             Cluster UUID : 00051234-1234-1234-abcd-1234567890ab
           Cluster Status : COMPLETE
    Domain Fault Tolerance Status : CAN_TOLERATE_FAILURE_COUNT=1
    Replication Factor : 2
    Metadata Replication Factor : 3
    Preferred Fault Tolerance Domain : NODE_COUNT
    Current Redundancy State : REDUNDANT_HA
```

!!! warning "Common errors"
    **`Error: Connection refused (127.0.0.1:9440)`** — Verify the Nutanix cluster is reachable and ncli service is running with `ncli cluster info`.
    **`Error: Invalid credentials for user admin`** — Authenticate with valid Nutanix cluster credentials using `ncli -username <user> -password <pass>` or configure default credentials in ~/.ncli/config.
### VM Creation Test

```bash
# Create a test VM via acli (AHV CLI)
acli vm.create TestVM num_vcpus=2 num_cores_per_vcpu=1 memory=2G

# Add a disk
acli vm.disk_create TestVM clone_from_image=<AHV-tools-ISO> cdrom=true
acli vm.disk_create TestVM create_size=20G container=VMs

# Add a NIC
acli vm.nic_create TestVM network=<vm-network-name>

# Power on
acli vm.on TestVM

# Power off and delete after test
acli vm.off TestVM
acli vm.delete TestVM
```


```text title="Expected output"
TestVM: VM created with UUID: 00051234-5678-90ab-cdef-1234567890ab
TestVM: Disk created with UUID: 10061234-5678-90ab-cdef-1234567890ab (CDROM)
TestVM: Disk created with UUID: 10071234-5678-90ab-cdef-1234567890ab (20GB)
TestVM: NIC created with UUID: 20081234-5678-90ab-cdef-1234567890ab on network vm-network-prod
TestVM: VM powered on
TestVM: VM powered off
TestVM: VM deleted successfully
```

!!! warning "Common errors"
    **`Error: Image <AHV-tools-ISO> not found`** — Replace `<AHV-tools-ISO>` with the actual image name from `acli image.list`.
    **`Error: Network <vm-network-name> not found`** — Replace `<vm-network-name>` with a valid network name from `acli net.list`.
    **`Error: VM TestVM is powered on and cannot be deleted`** — Ensure `acli vm.off TestVM` completes before running `acli vm.delete TestVM`.
### Network Reachability

```bash
# Ping cluster VIP from client workstation
ping <cluster-vip>

# Verify Prism Element accessible
curl -k https://<cluster-vip>:9440

# Verify storage network MTU (from each CVM)
allssh "ping -c 3 -M do -s 8972 <other-cvm-ip>"
```


```text title="Expected output"
PING 10.20.30.40 (10.20.30.40) 56(84) bytes of data.
64 bytes from 10.20.30.40: icmp_seq=1 ttl=64 time=2.34 ms
64 bytes from 10.20.30.40: icmp_seq=2 ttl=64 time=2.18 ms
64 bytes from 10.20.30.40: icmp_seq=3 ttl=64 time=2.41 ms

--- 10.20.30.40 statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2003ms
rtt min/avg/max/stddev = 2.18/2.31/2.41/0.10 ms

<!DOCTYPE html>
<html>
<head><title>Nutanix Prism</title></head>
...
</html>

CVM 10.20.30.41: PING 10.20.30.42 (10.20.30.42) 56(84) bytes of data.
64 bytes from 10.20.30.42: icmp_seq=1 ttl=64 time=1.87 ms
64 bytes from 10.20.30.42: icmp_seq=2 ttl=64 time=1.92 ms
64 bytes from 10.20.30.42: icmp_seq=3 ttl=64 time=1.89 ms
```

!!! warning "Common errors"
    **`ping: unknown host <cluster-vip>`** — Replace `<cluster-vip>` with the actual cluster virtual IP address (e.g., 10.20.30.40).
    **`curl: (7) Failed to connect to <cluster-vip> port 9440: Connection refused`** — Verify Prism Element is running with `allssh "systemctl status prism-gw"` and check network connectivity to port 9440.
    **`ping: invalid argument -- 's': option requires an argument`** — Ensure the MTU test packet size (8972) is less than your network MTU; use `ip link show` to verify interface MTU supports jumbo frames.
---

## Prism Central Registration (Optional)

```bash
# Register the new cluster with Prism Central
# From Prism Element:
# Settings → Prism Central Registration → Register
# Enter Prism Central IP/FQDN + credentials

# Verify from PC: Prism Central → Clusters → cluster appears and shows Connected
```

---

## See also

- [Nutanix — How It Works](../architecture/how-it-works/)
- [Nutanix — Health Checks](../operations/health-checks/)
- [Nutanix — Common Issues](../troubleshooting/common-issues/)
