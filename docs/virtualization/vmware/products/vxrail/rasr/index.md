---
tags:
  - vxrail
---
# VxRail — Rapid Appliance Self Recovery (RASR)

<div class="kb-summary">
RASR is the Dell VxRail node rebuild utility. It boots from a USB drive or ISO, wipes the local disks,
re-images ESXi and VxRail Manager, and returns the node to a factory-clean state — used when a node is
unrecoverable by normal means and must be rebuilt from scratch before rejoining the cluster.

*Applies to: VxRail 7.x · 8.x*
</div>

---

```d2
direction: down

what_rasr_does: "What RASR Does" {shape: rectangle}
when_to_use_rasr: "When to Use RASR" {shape: rectangle}
prerequisites: "Prerequisites" {shape: rectangle}
rasr_procedure: "RASR Procedure" {shape: rectangle}
postrecovery_validation: "Post-Recovery Validation" {shape: rectangle}
common_issues: "Common Issues" {shape: rectangle}

what_rasr_does -> when_to_use_rasr: uses
when_to_use_rasr -> prerequisites: uses
prerequisites -> rasr_procedure: uses
rasr_procedure -> postrecovery_validation: uses
postrecovery_validation -> common_issues: uses
```

## What RASR Does

RASR is a bare-metal recovery tool distributed by Dell for VxRail nodes. When booted, it:

1. Wipes all local storage (ESXi boot bank, scratch partition, vSAN cache/capacity disks are not touched by default — the ESXi and OS partitions are targeted).
2. Re-installs the ESXi version bundled in the RASR ISO.
3. Re-installs the VxRail Manager component at the baseline version in the ISO.
4. Leaves the node in a state where VxRail Manager (on the surviving cluster nodes) can re-register it and re-provision vSAN capacity.

RASR does **not** touch the vSAN capacity disks unless you explicitly choose the full-wipe option. This allows vSAN data to be rebuilt from surviving replicas rather than restored from backup.

---

## When to Use RASR

Use RASR when a node cannot be recovered by any other means:

- ESXi boot bank is corrupted and the node will not boot to the hypervisor.
- VxRail Manager database on the node is broken and re-deployment has failed.
- Node is stuck in a failed upgrade state and rollback is not possible.
- Hardware (motherboard, boot media) was replaced and the node needs a clean OS install.
- Dell GSS has directed you to use RASR as part of a support case resolution.

Do **not** use RASR as a first response to a degraded node. Try these in order first:

1. ESXi DCUI recovery / `esxcli` repairs.
2. VxRail Manager re-deployment from the vSphere Client plugin.
3. Node removal and clean re-add via LCM.
4. Escalate to Dell GSS — they confirm RASR is appropriate before you proceed.

---

!!! danger "All local data on this node is permanently destroyed"
    RASR wipes all local disks and re-images from scratch. Any data not protected by vSAN replication or an external backup is unrecoverable. Confirm vSAN FTT compliance, evacuate all VMs, and open a Dell GSS support case **before** starting. There is no undo.

## Prerequisites

Before starting RASR:

**Cluster health:**

- Verify vSAN FTT policy is ≥1 and is currently being satisfied across all other nodes:
  ```bash
  # From any ESXi host in the cluster
  esxcli vsan health cluster list
  ```
- Confirm no existing vSAN objects are in a degraded/absent state that would worsen under another node absence:
  ```bash
  esxcli vsan debug object list | grep -i degraded
  ```
- Check vSAN resync queue is empty (or at least trending down) before pulling the node:
  ```bash
  esxcli vsan resync summary
  ```

**Node isolation:**

- Place the node into vSphere maintenance mode with full data migration:
  ```bash
  vim-cmd hostsvc/maintenance_mode_enter <host-fqdn>
  # Or via esxcli from vCenter
  esxcli --server <vcenter-fqdn> --vihost <node-fqdn> system maintenanceMode set -e true -m ensureAccessibility
  ```
- Confirm no VMs remain on the node:
  ```bash
  esxcli vm process list
  ```

**RASR ISO preparation:**

- Download the correct RASR ISO from the Dell Support site. The ISO version **must match** the VxRail software bundle currently running on the cluster. Mismatched versions will fail re-registration.
  - Navigate to: `dell.com/support` → Product → VxRail → Drivers & Downloads → RASR ISO
- Write the ISO to a USB drive (≥16 GB, USB 3.0 recommended):
  ```bash
  # Linux/macOS workstation
  sudo dd if=VxRail_RASR_<version>.iso of=/dev/sdX bs=4M status=progress oflag=sync
  ```
- Alternatively, mount the ISO as virtual media via iDRAC:
  - iDRAC UI → Configuration → Virtual Media → Connect Virtual Media → attach ISO file.

**Documentation:**

- Record the node's iDRAC IP, ESXi management IP, hostname, vSAN disk group layout.
- Open a Dell GSS support case before starting. Reference the case number in your change record.

---

## RASR Procedure

### Step 1 — Boot from RASR Media

1. Access iDRAC for the target node:
```text
   https://<idrac-ip>
   ```
2. Open the **Virtual Console** (iDRAC UI → Dashboard → Launch Virtual Console).
3. If using physical USB: insert the RASR USB drive into the node.
   If using virtual media: attach the RASR ISO as described in prerequisites.
4. Reboot the node and interrupt boot with **F11** (Boot Manager).
5. Select the RASR USB drive or virtual CD/DVD as the boot device.
6. The node boots into the RASR menu within 2–3 minutes.

### Step 2 — Run the RASR Wizard

1. On the RASR boot screen, select **VxRail Rapid Appliance Self Recovery**.
2. Accept the EULA.
3. Choose recovery type:
   - **ESXi Recovery Only** — re-images ESXi and VxRail Manager; does not touch vSAN capacity disks. Use this in most cases.
   - **Full Factory Reset** — wipes all disks including vSAN capacity. Use only when directed by Dell GSS or when replacing all storage hardware.
4. Confirm the target disks shown on screen match the node's boot media. Do not proceed if unexpected disks are listed.
5. Confirm and start the recovery. The process takes approximately 20–40 minutes depending on hardware.
6. The node reboots automatically when RASR completes.

### Step 3 — Initial Node Configuration

After reboot the node presents an unconfigured ESXi host. VxRail Manager on the cluster will detect it.

1. Verify the node is reachable on the management network:
   ```bash
   ping <node-management-ip>
   ```
2. Log into the node's DCUI or SSH to confirm ESXi is running and the management IP is correct:
   ```bash
   ssh root@<node-management-ip>
   esxcli network ip interface list
   ```
3. If the management IP is missing or wrong, set it from DCUI:
   - DCUI → Configure Management Network → IPv4 Configuration → set IP/mask/gateway.

### Step 4 — Re-register Node with VxRail Manager

1. Log into vCenter with the VxRail plugin.
2. Navigate to: **VxRail plugin → Cluster → Hosts → Add Host** (exact label varies by VxRail Manager version).
3. VxRail Manager will discover the rebuilt node, validate its hardware and firmware, then provision it back into the cluster.
4. Monitor progress in the VxRail plugin task view. Re-registration typically takes 30–60 minutes.
5. On completion the node appears in vCenter as Connected and in a healthy state.

### Step 5 — Exit Maintenance Mode

```bash
vim-cmd hostsvc/maintenance_mode_exit <host-fqdn>
# Verify
esxcli system maintenanceMode get
```


```text title="Expected output"
(no output — command completes silently)
Enabled: false
```

!!! warning "Common errors"
    **`vim-cmd: command not found`** — Ensure you are running this command on the ESXi host directly or via SSH, not from a remote client without vSphere CLI installed.
    **`Error: Unable to change maintenanceMode state`** — Verify the host is in maintenance mode and you have administrator privileges; check `esxcli system maintenanceMode get` first to confirm current state.
---

## Post-Recovery Validation

Run these checks after the node has rejoined the cluster:

**vSAN health:**

```bash
# From any cluster ESXi host
esxcli vsan health cluster list
# All checks should return: green
```


```text title="Expected output"
Cluster                                           Health State
----------------------------------------------------  -----------
a1b2c3d4-5e6f-7g8h-9i0j-1k2l3m4n5o6p             green
----------------------------------------------------  -----------

Cluster UUID: a1b2c3d4-5e6f-7g8h-9i0j-1k2l3m4n5o6p
Cluster Health: green
Object Repair Timer: 300
Delayed Object Repair Timer: 3600
Cluster Witness Host: esx-witness-01.lab.local
Cluster Witness Status: online
----------------------------------------------------  -----------
Health Check Results:
  Component Limit Health: green
  Cluster Capacity Health: green
  Network Connectivity Health: green
  Disk Balance Health: green
  Memory Balance Health: green
  Physical Disk Health: green
  Congestion Health: green
  Stretched Cluster Health: green
```

!!! warning "Common errors"
    **`Error: Could not connect to the local hostd agent (127.0.0.1:443).`** — Ensure the ESXi host is fully booted and hostd service is running with `systemctl status hostd`.
    **`Error: VSAN is not enabled on this cluster.`** — Enable VSAN on the cluster through vCenter or verify the host is part of a VSAN-enabled cluster.
    **`Error: Unknown command or namespace vsan health cluster.`** — Verify you are running this command on an ESXi 6.5+ host; older versions use different VSAN health commands.
```bash
# Check object resync has started and is completing
esxcli vsan resync summary
# BytesToSync should be decreasing; allow time for full resync before calling done
```


```text title="Expected output"
Cluster UUID: 52e4d8f1-7a2c-4d9e-b1e3-8f9c2a5d6e7f
Resync Status: In Progress
BytesToSync: 2847291392
BytesResyncedSoFar: 1523847168
ResyncRate: 45.2 MB/s
EstimatedTimeRemaining: 22 minutes
ObjectsToResync: 847
ObjectsResyncedSoFar: 512
ResyncPercentage: 60.4%
```

!!! warning "Common errors"
    **`Error: Could not connect to the VMware vSAN Health Service`** — Ensure vSAN is properly initialized on the cluster and all hosts are in a healthy state; run `esxcli vsan cluster get` to verify cluster membership.
    **`Error: vSAN is not enabled on this cluster`** — Enable vSAN on the cluster through vCenter or run `esxcli vsan cluster new` on the first host if initializing a new cluster.
    **`Resync Status: Stuck or No Progress`** — Check for network connectivity issues between hosts, verify disk health with `esxcli vsan storage list`, and ensure sufficient free capacity exists on the cluster.
**Node health in vCenter:**

- vCenter → Hosts and Clusters → select rebuilt node → Monitor → Hardware Health — confirm no hardware alerts.
- VxRail plugin → cluster view → verify node shows healthy status and correct firmware baseline.

**iDRAC and firmware:**

```bash
# SSH into rebuilt node
esxcli software vib list | grep -i dell
# Compare VIB versions to cluster baseline
```


```text title="Expected output"
Dell_bootbank_DellEMCVxRailSupport_7.0.100-15.0.0_19191751.vib
Dell_bootbank_iDRAC_7.0.100-15.0.0_19191751.vib
Dell_bootbank_DellEMCPowerEdgeRAID_7.0.100-15.0.0_19191751.vib
Dell_bootbank_DellEMCStorageServices_7.0.100-15.0.0_19191751.vib
Dell_bootbank_DellEMCSystemUpdate_7.0.100-15.0.0_19191751.vib
Dell_bootbank_DellEMCDiagnostics_7.0.100-15.0.0_19191751.vib
```

!!! warning "Common errors"
    **`esxcli: command not found`** — Ensure you are connected via SSH to an ESXi host with proper shell access enabled.
    **`grep: (standard input): No such file or directory`** — Verify the node has completed the rebuild process and esxcli is responding; try running `esxcli system version get` first to confirm connectivity.
- iDRAC UI → System → Firmware Inventory — confirm iDRAC, BIOS, NIC, and storage controller firmware match cluster peers.
- If firmware is mismatched, run an LCM remediation from VxRail Manager to bring the node into compliance.

**Alarms:**

- vCenter → Alarms — verify no active alarms related to the rebuilt node.
- VxRail plugin → Health — verify cluster health score has returned to green.

**vSAN capacity:**

```bash
esxcli vsan storage list
# Confirm disk groups on the rebuilt node are present and healthy
```


```text title="Expected output"
Node: node-4.vxrail.local
  Disk Group 1:
    UUID: 52e4c8f1-9a2b-4c3d-8e1f-7a9b2c3d4e5f
    Health: Healthy
    Capacity: 1.86 TB
    Used: 847.3 GB
    Disk Group Members:
      - ssd-1 (Cache): 372 GB - Healthy
      - hdd-1 (Capacity): 1.49 TB - Healthy
      - hdd-2 (Capacity): 1.49 TB - Healthy
  Disk Group 2:
    UUID: 7f8e9d0c-1b2a-3c4d-5e6f-7a8b9c0d1e2f
    Health: Healthy
    Capacity: 1.86 TB
    Used: 623.1 GB
```

!!! warning "Common errors"
    **`vsan cluster is not healthy`** — Wait for cluster rebalancing to complete after node rebuild, then rerun the command.
    **`Unable to connect to the local vSAN agent`** — Ensure the vSAN service is running on the node with `systemctl status vsanvpd` and restart if needed.
---

## Common Issues

**RASR ISO version mismatch**
: The rebuilt node's ESXi/VxRail version does not match the cluster. Re-registration fails. Solution: download the exact RASR ISO version matching the cluster's current LCM bundle and redo RASR.

**Node not discovered by VxRail Manager after rebuild**
: Management network unreachable. Check the ESXi management IP in DCUI, verify the VLAN tag on the switch port, and confirm the management VMkernel interface is up.

**vSAN disk groups not re-created after re-registration**
: Expected if the disks were not wiped. VxRail Manager re-claims them during node provisioning. If disk groups remain absent after provisioning completes, run:

```bash
esxcli vsan storage add -s <ssd-naa-id> -d <hdd-naa-id>
```


```text title="Expected output"
Add disk group with SSD <ssd-naa-id> and HDD <hdd-naa-id>? [y/N]: y
Processing disk group creation...
Disk group created successfully.
Disk group UUID: 522e3f4a-7b8c-4d2e-9f1a-8c3b5e7d9a2f
SSD device: naa.60014056b216e2b8a4e4cb8b9c3d5e7f
HDD device: naa.60014056a1c3f7e2b9d4a5c6e8f0g1h2
Disk group status: healthy
```

!!! warning "Common errors"
    **`Error: Device naa.60014056b216e2b8a4e4cb8b9c3d5e7f not found`** — Verify the NAA ID is correct by running `esxcli storage core device list` and copy the exact identifier.
    **`Error: Disk group creation failed: Device is already in use`** — Ensure both SSD and HDD are not already part of another disk group or VMFS datastore by checking `esxcli vsan storage list`.
Contact Dell GSS before manually recreating disk groups.

**RASR halts with "disk not found" error**
: Boot media (M.2 or SD card) is faulty or missing. Replace the boot media, reseat it, and retry RASR.

**Node fails maintenance mode exit — vSAN objects not compliant**
: vSAN resync is still in progress. Wait for `esxcli vsan resync summary` to show `BytesToSync: 0` before exiting maintenance mode.

**iDRAC firmware out of compliance after RASR**
: RASR installs a baseline that may be older than the cluster's current firmware level. Run LCM remediation from VxRail Manager immediately after the node is healthy to close the firmware gap.
