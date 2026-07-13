---
tags:
  - nutanix
  - operations
  - procedures
description: "Common Nutanix operational procedures — adding and removing nodes, entering maintenance mode, expanding storage, upgrading AOS/AHV via LCM, cloning VMs..."
---
# Nutanix — Procedures

<div class="kb-summary">
Common Nutanix operational procedures — adding and removing nodes, entering maintenance mode, expanding storage, upgrading AOS/AHV via LCM, cloning VMs, and managing protection domains.

*Applies to: AOS 6.x · AHV*
</div>

---

```d2
direction: right

enter_host_maintenance_mode: "Enter Host Maintenance Mode" {shape: rectangle}
aos_ahv_upgrade_via_lcm: "AOS / AHV Upgrade via LCM" {shape: rectangle}
add_a_node_to_an_existing_cluster: "Add a Node to an Existing Cluster" {shape: rectangle}
remove_a_node_from_cluster: "Remove a Node from Cluster" {shape: rectangle}
expand_storage_add_disks: "Expand Storage (Add Disks)" {shape: rectangle}
clone_a_vm: "Clone a VM" {shape: rectangle}

enter_host_maintenance_mode -> aos_ahv_upgrade_via_lcm
aos_ahv_upgrade_via_lcm -> add_a_node_to_an_existing_cluster
add_a_node_to_an_existing_cluster -> remove_a_node_from_cluster
remove_a_node_from_cluster -> expand_storage_add_disks
expand_storage_add_disks -> clone_a_vm
```

## Before you begin

- **Access:** CVM SSH (nutanix) and Prism Element admin
- **NCC baseline:** run `ncc --health_checks run_all` and confirm all green before any procedure
- **Resilience:** verify `ncli cluster get-domain-fault-tolerance-status type=node` shows CAN_TOLERATE ≥ 1

---

## Enter Host Maintenance Mode

Maintenance mode live-migrates all VMs off the host before you perform hardware or OS work.

```bash
# From Prism Element: right-click host → Enter Maintenance Mode
# OR via CLI:
acli host.enter_maintenance_mode <host-name>

# Monitor migration progress
acli vm.list | grep -v "on$\|off$"
# All VMs should show "on" on other hosts

# Verify host is in maintenance mode
acli host.list | grep -i <host-name>
```


```text title="Expected output"
acli host.enter_maintenance_mode host-05
Host host-05 entering maintenance mode...
Migration of 12 VMs initiated.

acli vm.list | grep -v "on$\|off$"
VM-APP-01                          host-03              on
VM-APP-02                          host-04              on
VM-DB-PROD-01                       host-02              on
VM-BACKUP-SYNC                      host-03              on
VM-WEB-LB-01                        host-02              on
VM-WEB-LB-02                        host-04              on
...
(12 VMs migrated successfully)

acli host.list | grep -i host-05
host-05                  ACPI       4.8.1.1              MAINTENANCE_MODE       192.168.1.145
```

!!! warning "Common errors"
    **`Error: Host host-05 has running VMs that cannot be migrated`** — Verify HA policy allows migration and check for pinned VMs with `acli vm.get <vm-name> | grep pin`.
    **`Error: Connection refused to host host-05`** — Ensure the host is reachable and Prism Element cluster is healthy with `acli cluster.status`.
    **`Error: host-05 is already in MAINTENANCE_MODE`** — The host is already in maintenance mode; proceed with updates or use `acli host.exit_maintenance_mode <host-name>` to exit first.
**Expected:** Host shows `MAINTENANCE_MODE` state. No VMs running on it.

```bash
# After work is complete, exit maintenance mode
acli host.exit_maintenance_mode <host-name>

# Verify VMs rebalance back (DRS equivalent — Nutanix doesn't auto-rebalance;
# VMs remain on other hosts until manually migrated or until next power cycle)
```


```text title="Expected output"
Host exited maintenance mode successfully.
Host UUID: 00051234-1234-1234-1234-123456789abc
Host Name: ntnx-host-03.prod.local
Cluster: prod-cluster-01
Host Status: NORMAL
vCPU Available: 128
Memory Available: 512 GB
```

!!! warning "Common errors"
    **`Error: Host <host-name> not found in cluster`** — Verify the exact hostname matches the output from `acli host.list` and check cluster connectivity.
    **`Error: Host is not in maintenance mode`** — Confirm the host is currently in maintenance mode using `acli host.get <host-name> | grep maintenance_mode` before attempting to exit.
---

## AOS / AHV Upgrade via LCM

Life Cycle Manager (LCM) upgrades are non-disruptive rolling upgrades.

```text
1. Prism Central → LCM → Inventory → Run Inventory (discovers available updates)
2. Review available updates: AOS, AHV, firmware
3. Select updates to apply
4. LCM performs rolling upgrade:
   - One CVM at a time for AOS
   - One host at a time for AHV (VMs live-migrate off before AHV upgrade)
   - Firmware: node enters maintenance mode, firmware applied, node reboots
5. Monitor progress in LCM → Tasks
```

**Pre-upgrade NCC run:**
```bash
ncc --health_checks run_all 2>&1 | grep -E "FAIL|WARN"
# Must be clean before starting upgrade
```


```text title="Expected output"
WARN: Cluster clock skew detected on node-03 (offset: 127ms)
WARN: vSAN object resync in progress (3 objects pending)
FAIL: NTP service not running on node-02
WARN: One disk showing predictive failure on node-01 (S/N: SSD-2847-XYZ)
FAIL: Certificate expiration within 30 days on prism-master-01
```

!!! warning "Common errors"
    **`ncc: command not found`** — Ensure you are running this command on a Nutanix cluster node with ncc installed, or source the appropriate environment.
    **`FAIL: Cluster not in healthy state`** — Resolve all FAIL conditions (especially NTP and certificates) before proceeding with upgrade; WARN conditions can typically proceed but should be documented.
    **`Permission denied`** — Run the command with appropriate sudo privileges or as the admin user with ncc access rights.
**Estimated time:**
- AOS upgrade: ~20–30 minutes per node
- AHV upgrade: ~30–45 minutes per node (includes VM migration time)
- Firmware: ~60–90 minutes per node

---

## Add a Node to an Existing Cluster

```bash
# Prerequisites:
# - New node imaged with same AOS/AHV version as cluster (use Foundation)
# - New CVM IP on management network, reachable from existing CVMs

# SSH to any existing CVM
ssh nutanix@<existing-cvm-ip>

# Expand cluster (add new CVM to cluster)
cluster -s <existing-cvm1>,<existing-cvm2>,<existing-cvm3>,<new-cvm-ip> expand

# Monitor expansion
ncli cluster get-domain-fault-tolerance-status type=node
# Wait until new node appears in: ncli host list
```


```text title="Expected output"
nutanix@cvm-01:~$ ssh nutanix@10.20.30.41
nutanix@10.20.30.41's password: 
Last login: Wed Mar 13 14:22:18 2024 from 10.20.30.15
nutanix@cvm-01:~$ cluster -s 10.20.30.41,10.20.30.42,10.20.30.43,10.20.30.44 expand
Expanding cluster...
Adding node with CVM IP: 10.20.30.44
Cluster expansion initiated. This may take 10-15 minutes.
nutanix@cvm-01:~$ ncli cluster get-domain-fault-tolerance-status type=node
Node Fault Tolerance Status:
  Metadata Fault Tolerance: 3
  Data Fault Tolerance: 3
  Desired Metadata Fault Tolerance: 3
  Desired Data Fault Tolerance: 3
nutanix@cvm-01:~$ ncli host list
  UUID                                  Hostname       Hypervisor  State
  ----                                  --------       ----------  -----
  a1b2c3d4-e5f6-7890-abcd-ef1234567890  host-01.local  AHV         UP
  b2c3d4e5-f6a7-8901-bcde-f12345678901  host-02.local  AHV         UP
  c3d4e5f6-a7b8-9012-cdef-123456789012  host-03.local  AHV         UP
  d4e5f6a7-b8c9-0123-def0-234567890123  host-04.local  AHV         UP
```

!!! warning "Common errors"
    **`cluster: command not found`** — Ensure you are logged into a CVM as the nutanix user and the cluster services are running (check with `service cluster-agent status`).
    **`Connection refused`** — Verify the new CVM IP is reachable from the existing CVM and that the new node has completed imaging with the same AOS/AHV version using Foundation.
    **`Cluster expansion failed: Node already exists`** — Confirm the new node's CVM has a unique IP address and has not been previously added to a different cluster.
**After node is added:**
```bash
# Verify new disks are claimed
ncli disk list | grep <new-host-serial>

# Check data is rebalancing to new node (Curator will trigger automatically)
curator_cli display_curator_tasks | grep rebalance
```


```text title="Expected output"
DISK-ID                           SERIAL                    SLOT  NODE-UUID                            STATUS
disk.0a1b2c3d-4e5f-6g7h-8i9j     SN-NX-5060-123456         0     00051a3b-8c2d-4e5f-a1b2-c3d4e5f6a7b8 CLAIMED
disk.1f2e3d4c-5b6a-7g8h-9i0j     SN-NX-5060-123457         1     00051a3b-8c2d-4e5f-a1b2-c3d4e5f6a7b8 CLAIMED

Task ID                           Task Type              Status      Progress
task-curator-001                  Rebalance              RUNNING     45%
task-curator-002                  Rebalance              QUEUED      0%
```

!!! warning "Common errors"
    **`ncli: command not found`** — Ensure you are running this command on a Nutanix cluster node with ncli in the PATH, or source the Nutanix environment setup script.
    **`No such file or directory`** — Verify the serial number variable `<new-host-serial>` is correctly substituted with the actual host serial (e.g., `SN-NX-5060-123456`) before running the grep command.
---

## Remove a Node from Cluster

!!! warning "Node removal causes vSAN data rebalancing"
    All data on the leaving node's disks must evacuate to remaining nodes before removal. Ensure remaining nodes have sufficient capacity before starting.

```bash
# Step 1: Check cluster can tolerate removal
ncli cluster get-domain-fault-tolerance-status type=node
# Must show CAN_TOLERATE_FAILURE_COUNT ≥ 1

# Step 2: Mark node for removal (triggers data evacuation)
# Prism Element → Hardware → select host → Remove Host
# OR via ncli:
ncli host remove-start id=<host-id>

# Step 3: Monitor data evacuation
ncli host get id=<host-id>   # watch "removal_status" field
# Also check: acli vm.list — all VMs should migrate off

# Step 4: Confirm removal is complete
ncli host list   # host should no longer appear
```


```text title="Expected output"
Cluster Fault Tolerance Status:
  CAN_TOLERATE_FAILURE_COUNT: 2
  CURRENT_REDUNDANCY_FACTOR: 3
  METADATA_REDUNDANCY_FACTOR: 3

Host 00061234-5678-90ab-cdef-1234567890ab removal started.
Evacuation in progress...

Host Details:
  UUID: 00061234-5678-90ab-cdef-1234567890ab
  Hostname: host-05.nutanix.local
  removal_status: IN_PROGRESS
  data_evacuation_percent: 67

VM Migration Status:
  vm-prod-db-01: MIGRATED (host-03)
  vm-prod-web-02: MIGRATED (host-02)
  vm-dev-app-03: IN_PROGRESS → host-04
  vm-backup-srv: MIGRATED (host-01)

Cluster Hosts:
  host-01.nutanix.local (00061111-1111-1111-1111-111111111111)
  host-02.nutanix.local (00062222-2222-2222-2222-222222222222)
  host-03.nutanix.local (00063333-3333-3333-3333-333333333333)
  host-04.nutanix.local (00064444-4444-4444-4444-444444444444)
```

!!! warning "Common errors"
    **`Error: Cluster cannot tolerate node failure. CAN_TOLERATE_FAILURE_COUNT: 0`** — Add another node or reduce RF before removal, or wait for rebalancing to complete.
    **`Error: Host removal already in progress for id=<host-id>`** — Wait for the current removal to complete or use `ncli host remove-abort id=<host-id>` to cancel.
    **`Error: Cannot remove host with running VMs. Migrate or power off all VMs first.`** — Manually migrate remaining VMs using `acli vm.migrate` or wait for automatic evacuation to finish.
---

## Expand Storage (Add Disks)

```bash
# New disks are typically auto-discovered and claimed by AOS within 5 minutes
# Verify discovery:
ncli disk list | grep <host-name>

# If disk not auto-claimed:
# Prism Element → Hardware → select host → claim disk manually
ncli disk create host-id=<host-id> device-bus=<bus> device-id=<id>

# Monitor Curator rebalancing to new disk
curator_cli display_curator_tasks
```


```text title="Expected output"
host-name: host-prd-01
  Disk ID: 500a0b1c2d3e4f5g
  Device Bus: SATA
  Device ID: sda
  Disk Size: 1.09 TB
  Disk Status: CLAIMED
  Pinned: False

host-name: host-prd-02
  Disk ID: 500a0b1c2d3e4f6h
  Device Bus: SAS
  Device ID: sdb
  Disk Status: CLAIMED
  Pinned: False

Task ID: curator-task-20240115-001
  Task Type: Rebalance
  Status: Running
  Progress: 45%
  Estimated Time Remaining: 2h 15m
  Affected Disks: 1
  Data Moved: 450 GB / 1000 GB
```

!!! warning "Common errors"
    **`Error: Invalid host-id '<host-id>'`** — Replace `<host-id>` with the actual numeric host ID from `ncli host list` output.
    **`Error: Disk already claimed or in use`** — Verify the disk is not already assigned to another host or in a failed state using `ncli disk list --detailed`.
    **`Error: curator_cli: command not found`** — Run the command from a Nutanix node with SSH access or use `acli vm.list` to verify cluster connectivity first.
---

## Clone a VM

```bash
# Via acli
acli vm.clone <source-vm-name> clone_vm_name=<new-vm-name>

# Clone from snapshot
acli vm.clone <source-vm-name> \
  clone_vm_name=<new-vm-name> \
  snapshot_name=<snap-name>
```


```text title="Expected output"
Cloning VM 'prod-web-01' to 'prod-web-01-clone'...
VM clone task submitted successfully.
Task ID: 00058e4f-1234-5678-abcd-ef1234567890
Waiting for clone operation to complete...
Clone operation completed successfully.
New VM 'prod-web-01-clone' created with UUID: 12345678-abcd-ef01-2345-6789abcdef01
```

!!! warning "Common errors"
    **`Error: VM 'prod-web-01' not found`** — Verify the source VM name exists by running `acli vm.list` and use the exact VM name from the output.
    **`Error: Snapshot 'snap-name' not found on VM`** — Confirm the snapshot exists on the source VM using `acli vm.snapshot_list <source-vm-name>` before cloning.
    **`Error: Insufficient cluster resources to complete clone operation`** — Check available cluster capacity with `acli cluster.status` and free up storage or compute resources as needed.
From Prism: right-click VM → Clone → specify name and count.

---

## Take and Manage VM Snapshots

```bash
# Create crash-consistent snapshot
acli vm.snapshot_create <vm-name> snapshot_name=<snap-name>

# Create app-consistent snapshot (requires NGT installed in VM)
acli vm.snapshot_create <vm-name> \
  snapshot_name=<snap-name> \
  vm_consistency_type=APPLICATION_CONSISTENT

# List snapshots
acli vm.snapshot_list <vm-name>

# Revert to snapshot (VM must be powered off)
acli vm.off <vm-name>
acli vm.snapshot_revert <vm-name> snapshot_name=<snap-name>
acli vm.on <vm-name>

# Delete old snapshots (free storage)
acli vm.snapshot_delete <vm-name> snapshot_name=<snap-name>
```


```text title="Expected output"
Creating snapshot for VM prod-web-01...
Task UUID: 12a4f8c9-3e2b-47d1-9f6c-8b2e1d5a7c3f
Snapshot 'daily-backup-2024-01-15' created successfully

Creating application-consistent snapshot for VM prod-web-01...
Task UUID: 5f9e2c1b-8d4a-42c6-b1a3-7e3d9f2c1a5b
Snapshot 'app-snap-prod-web-01' created successfully

VM: prod-web-01
  Snapshot Name                    Created                Size (GB)  Type
  daily-backup-2024-01-15          2024-01-15 14:32:10    2.3        CRASH_CONSISTENT
  app-snap-prod-web-01             2024-01-15 14:35:22    3.1        APPLICATION_CONSISTENT
  weekly-backup-2024-01-08         2024-01-08 09:15:45    2.1        CRASH_CONSISTENT

Powering off VM prod-web-01...
VM prod-web-01 powered off
Reverting to snapshot 'daily-backup-2024-01-15'...
Snapshot revert completed successfully
Powering on VM prod-web-01...
VM prod-web-01 powered on

Deleting snapshot 'weekly-backup-2024-01-08' from prod-web-01...
Snapshot deleted successfully. Freed 2.1 GB
```

!!! warning "Common errors"
    **`Error: VM prod-web-01 is powered on. Cannot revert snapshot while VM is running.`** — Power off the VM first using `acli vm.off <vm-name>` before attempting snapshot revert.
    **`Error: Snapshot 'app-snap-prod-web-01' requires APPLICATION_CONSISTENT but NGT is not installed on VM prod-web-01.`** — Install Nutanix Guest Tools (NGT) on the VM or use `vm_consistency_type=CRASH_CONSISTENT` instead.
    **`Error: Snapshot 'daily-backup-2024-01-15' not found on VM prod-web-01.`** — Verify the snapshot name with `acli vm.snapshot_list <vm-name>` and ensure you are using the correct VM and snapshot identifiers.
---

## Create and Manage Protection Domains (Legacy DR)

Protection Domains group VMs for coordinated snapshots and replication to a remote cluster.

```bash
# Create a protection domain
ncli pd create name=<pd-name>

# Add VMs to the protection domain
ncli pd add-vms name=<pd-name> vm-names=<vm1>,<vm2>

# Set snapshot schedule
ncli pd set-schedule name=<pd-name> \
  app-consistent=false \
  every-nth=3600 \        # snapshot every 3600 seconds (1 hour)
  num-snaps-to-retain=24  # keep 24 snapshots

# Add remote site for replication
ncli remote-site create name=<remote-name> address-list=<remote-cvm-ip>
ncli pd set-schedule name=<pd-name> remote-site-list=<remote-name>

# Manual snapshot + replicate now
ncli pd snapshot name=<pd-name>
```


```text title="Expected output"
Protection Domain created successfully with UUID: 00051234-1234-1234-1234-123456789abc
Added VMs vm-prod-01, vm-prod-02 to protection domain pd-prod
Schedule set for protection domain pd-prod:
  App-consistent: false
  Snapshot interval: 3600 seconds
  Snapshots to retain: 24
Remote site remote-dr created with address 10.20.30.40
Protection domain pd-prod updated with remote site replication
Snapshot initiated for protection domain pd-prod
Snapshot UUID: 00051567-5678-5678-5678-567890123def
Replication to remote-dr in progress
```

!!! warning "Common errors"
    **`Error: Protection domain 'pd-name' does not exist`** — Replace `<pd-name>` with an actual protection domain name created via `ncli pd list`.
    **`Error: VM 'vm1' not found in cluster`** — Verify VM names match exactly with `ncli vm list` and use comma-separated format without spaces.
    **`Error: Remote site 'remote-name' is unreachable at address 10.20.30.40`** — Confirm the remote CVM IP is correct and network connectivity exists between clusters using `ping` or `ncli remote-site test-connection`.
---

## Register Nutanix Guest Tools (NGT)

NGT installs inside VMs for application-consistent snapshots and in-guest operations.

```text
Prism Element → VM → select VM → Manage NGT → Mount NGT ISO → Install in VM
```

Inside the VM (Windows):
```powershell
# Mount the NGT ISO and run installer
D:\setup.exe /quiet /norestart
```

Inside the VM (Linux):
```bash
mount /dev/sr0 /mnt
/mnt/installer/linux/install_ngt.py
```


```text title="Expected output"
mount: /dev/sr0 is write-protected, mounting read-only
Nutanix Guest Tools Installer v5.18.2.1
Detecting OS: CentOS Linux 7 (Core)
Checking prerequisites...
  ✓ Kernel version: 3.10.0-1160.el7.x86_64
  ✓ Python 2.7.5 detected
  ✓ Required packages: ntp, open-vm-tools
Installing NGT components...
  [████████████████████] 100%
  ✓ Installed: ngt-guest-tools-5.18.2.1-1.el7.x86_64
  ✓ Installed: ngt-guest-tools-iso-5.18.2.1-1.el7.x86_64
NGT installation completed successfully
A reboot is recommended to apply all changes
```

!!! warning "Common errors"
    **`mount: /dev/sr0: No such file or directory`** — Verify the ISO is attached to the VM and the device exists with `ls -la /dev/sr*`.
    **`python: command not found`** — Install Python 2.7 or modify the shebang in install_ngt.py to use `python3` if Python 3 is available.
    **`Permission denied`** — Run the installer with `sudo` or as root: `sudo /mnt/installer/linux/install_ngt.py`.
---

## Increase Container Capacity Limit

```bash
# View current container config
ncli ctr get name=<container-name>

# Raise the reserved capacity (advertised size to datastores)
ncli ctr edit name=<container-name> advertised-capacity=<size-in-bytes>
# e.g. 10 TB = 10995116277760
```


```text title="Expected output"
Container Details:
  Name: prod-container-01
  Advertised Capacity: 5497558138880
  Used Capacity: 2748779069440
  Free Capacity: 2748779069440
  Replication Factor: 2
  Compression Enabled: true
  Deduplication Enabled: true
  RF2 Metadata Reserve %: 5
  Erasure Code: Off
  State: NORMAL
  UUID: a1b2c3d4-e5f6-7890-abcd-ef1234567890

Setting advertised capacity for container prod-container-01 to 10995116277760 bytes...
Container updated successfully.
```

!!! warning "Common errors"
    **`Error: Container 'prod-container-01' not found`** — Verify the exact container name with `ncli ctr ls` and ensure you have the correct spelling.
    **`Error: Invalid advertised-capacity value: value must be greater than used capacity`** — Set the advertised capacity to a value larger than the current used capacity shown in the container details.
---

---

## Verify

- Maintenance mode: target CVM reports `genesis status` shows CVM `UP` again after exit
- LCM upgrade: version shown in Prism matches intended target; NCC post-upgrade run is clean
- Node expansion: new node appears in `ncli host ls` and shows `State: NORMAL`
- Container expansion: new capacity reflected in `ncli storage-pool ls`

---

## See also

- [Nutanix — Health Checks](../health-checks/)
- [Nutanix — Common Issues](../../troubleshooting/common-issues/)
- [Nutanix — CLI Reference](../cli-reference/)
