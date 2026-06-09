# VxRail — Rapid Appliance Self Recovery (RASR)

<div class="kb-summary">
RASR is the Dell VxRail node rebuild utility. It boots from a USB drive or ISO, wipes the local disks,
re-images ESXi and VxRail Manager, and returns the node to a factory-clean state — used when a node is
unrecoverable by normal means and must be rebuilt from scratch before rejoining the cluster.
</div>

```text
┌──────────────────────────── VxRail — RASR (Rapid Appliance Self Recovery) ────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │                     RASR rebuilds a VxRail node that is unrecoverable by normal means                 ││
│   │     Boot node from RASR USB/ISO · wipe local disks · re-image ESXi and VxRail Manager baseline       ││
│   │              Cluster must tolerate the node being absent for the full rebuild duration                ││
│   │         vSAN FTT policy and object rebuild health verified before and after the procedure             ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                                       │
│                ▼                                 ▼                                 ▼                  │
│                                                                                                       │
│   ┌───────────────────────────┐   ┌───────────────────────────┐   ┌───────────────────────────┐       │
│   │      Pre-RASR checks      │   │       RASR execution       │   │    Post-RASR validation   │      │
│   │    vSAN FTT compliance    │   │    Boot from USB/ISO       │   │    Node rejoins cluster   │      │
│   │  Cluster degraded health  │   │    Disk wipe + re-image    │   │    vSAN object rebuild    │      │
│   │    Backup node config     │   │    ESXi baseline install   │   │    Alarms cleared         │      │
│   │    RASR ISO version match │   │    VxRail Mgr re-register  │   │    iDRAC + FW verified    │      │
│   │    Dell GSS case open     │   │    Return node to cluster  │   │    Health check passed    │      │
│   └───────────────────────────┘   └───────────────────────────┘   └───────────────────────────┘       │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  ESXi corrupt/unbootable  │  VxRail Mgr DB broken  │  Node stuck post-upgrade  │  Hardware swap      ││
│   │  RASR USB prepared        │  ISO matches cluster   │  vSAN FTT ≥1 before start │  Cluster tolerates  ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────────┘│
│                                                                                                       │
│  Physical Infrastructure:                                                                             │
│  Dell PowerEdge node · iDRAC vConsole/vMedia · USB 3.0 drive ≥16 GB · ToR switch port (node stays cabled)│
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  RASR ISO         = Dell-supplied bootable image containing ESXi installer + VxRail Manager baseline build│
│  RASR USB         = USB drive written with RASR ISO; inserted into node or mounted via iDRAC virtual media│
│  Re-image         = Full wipe and reinstall of all local disks including ESXi boot bank and cache partition│
│  Cluster FTT      = Failures To Tolerate; vSAN policy requiring ≥1 so cluster survives one node absent│
│  Node re-register = VxRail Manager re-adds rebuilt node to the cluster and re-provisions vSAN capacity│
│  vMedia           = iDRAC feature to mount a remote ISO as a virtual USB device without physical media│
│  LCM baseline     = The exact ESXi + VxRail Manager build version the RASR ISO must match             │
│  Object rebuild   = vSAN re-replicates data components onto the returned node after it rejoins        │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

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

---

## Post-Recovery Validation

Run these checks after the node has rejoined the cluster:

**vSAN health:**

```bash
# From any cluster ESXi host
esxcli vsan health cluster list
# All checks should return: green
```

```bash
# Check object resync has started and is completing
esxcli vsan resync summary
# BytesToSync should be decreasing; allow time for full resync before calling done
```

**Node health in vCenter:**

- vCenter → Hosts and Clusters → select rebuilt node → Monitor → Hardware Health — confirm no hardware alerts.
- VxRail plugin → cluster view → verify node shows healthy status and correct firmware baseline.

**iDRAC and firmware:**

```bash
# SSH into rebuilt node
esxcli software vib list | grep -i dell
# Compare VIB versions to cluster baseline
```

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

Contact Dell GSS before manually recreating disk groups.

**RASR halts with "disk not found" error**
: Boot media (M.2 or SD card) is faulty or missing. Replace the boot media, reseat it, and retry RASR.

**Node fails maintenance mode exit — vSAN objects not compliant**
: vSAN resync is still in progress. Wait for `esxcli vsan resync summary` to show `BytesToSync: 0` before exiting maintenance mode.

**iDRAC firmware out of compliance after RASR**
: RASR installs a baseline that may be older than the cluster's current firmware level. Run LCM remediation from VxRail Manager immediately after the node is healthy to close the firmware gap.
