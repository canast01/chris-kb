---
tags:
  - nutanix
  - operations
  - procedures
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

**Expected:** Host shows `MAINTENANCE_MODE` state. No VMs running on it.

```bash
# After work is complete, exit maintenance mode
acli host.exit_maintenance_mode <host-name>

# Verify VMs rebalance back (DRS equivalent — Nutanix doesn't auto-rebalance;
# VMs remain on other hosts until manually migrated or until next power cycle)
```

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

**After node is added:**
```bash
# Verify new disks are claimed
ncli disk list | grep <new-host-serial>

# Check data is rebalancing to new node (Curator will trigger automatically)
curator_cli display_curator_tasks | grep rebalance
```

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

---

## Increase Container Capacity Limit

```bash
# View current container config
ncli ctr get name=<container-name>

# Raise the reserved capacity (advertised size to datastores)
ncli ctr edit name=<container-name> advertised-capacity=<size-in-bytes>
# e.g. 10 TB = 10995116277760
```

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
