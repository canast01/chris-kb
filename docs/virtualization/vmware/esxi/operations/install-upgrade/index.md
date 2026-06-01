# ESXi Install & Upgrade


<div class="kb-summary">
ESXi Install & Upgrade reference covering vSphere Update Manager (VUM) — Legacy, Host Upgrade Procedure, ESXi Patch Application (Manual / Standalone), Upgrade and Patching Readiness Checklist, Driver and Firmware Lifecycle and 1 more sections.
</div>

ESXi Upgrade Flow — vLCM Rolling Cluster Upgrade
                           │
              ┌────────────▼────────────┐
              │  vLCM: Set Cluster      │
              │  Desired Image          │
              │  ESXi base + vendor     │
              │  add-on + VIBs          │
              └────────────┬────────────┘
                           │
         ┌─────────────────▼──────────────────┐
         │  For each host (one at a time):     │
         │                                     │
         │  1. Host → Maintenance Mode         │
         │     DRS migrates VMs automatically  │
         │  2. vLCM applies image + reboots    │
         │  3. Host exits Maintenance Mode     │
         │  4. Validate: Connected, no alarms, │
         │     paths active, vSAN healthy      │
         │  5. Wait 15–30 min before next host │
         └─────────────────┬──────────────────┘
                           │ Repeat for all hosts
              ┌────────────▼────────────┐
              │  Post-Upgrade           │
              │  Confirm all hosts on   │
              │  target version         │
              │  All vSAN health green  │
              └─────────────────────────┘
```text
┌───────────────────────────────────── ESXi — Install and Upgrade ──────────────────────────────────────┐
│                                                                                                       │
│  Fresh install via ISO/PXE and in-place upgrade via vLCM baseline or image.                           │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Fresh Install                 │  │                 vLCM Upgrade                │   │
│   │            Boot from ISO/USB/PXE             │  │         Create cluster image in vLCM        │   │
│   │           Accept EULA, select disk           │  │          Attach baseline to cluster         │   │
│   │         Set root password + mgmt IP          │  │          Remediate in rolling order         │   │
│   │           Reboot → add to vCenter            │  │        Maintenance → upgrade → reboot       │   │
│   │          Apply Host Profile config           │  │         Verify version post-upgrade         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Prerequisites → install/upgrade → add to cluster → verify health state.                              │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │                Prerequisites                 │  │                Version Matrix               │   │
│   │            HCL check for hardware            │  │           ESXi 8.0 U3 — current GA          │   │
│   │           vCenter >= ESXi version            │  │           ESXi 7.0 U3 — supported           │   │
│   │          Storage/NIC drivers on HCL          │  │          vCenter must lead ESXi ver         │   │
│   │         Boot disk >= 8 GB (>= 32 GB)         │  │           N-2 upgrade path maximum          │   │
│   │          Mgmt network planned ahead          │  │         Check VMware interop matrix         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  x86 server on HCL, IPMI/iDRAC for PXE, 10 GbE mgmt NIC, boot disk (M.2/SD)                           │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  vLCM     = vSphere Lifecycle Mgr; image-based ESXi patch and upgrade mgmt                            │
│  HCL      = VMware Hardware Compatibility List; validated hardware for ESXi                           │
│  PXE      = Preboot Execution Env; network boot for ESXi install via TFTP                             │
│  Baseline = vLCM patch set; defines target ESXi build for remediation                                 │
│  Remediate= vLCM process: puts host in maintenance + upgrades ESXi                                    │
│  EULA     = End User License Agreement; accepted during ESXi installer                                │
│  N-2 path = VMware supports skipping up to 2 major versions in upgrade                                │
│  Host Profile = desired state config applied after fresh ESXi install                                 │
│  Interop  = VMware Product Interoperability Matrix; validates version combos                          │
│  GA       = General Availability; production-ready official release                                   │
│  Rolling  = upgrade one host at a time; VMs migrated before each upgrade                              │
│  Boot disk = ESXi install target; SD/USB (legacy), M.2 NVMe (recommended)                             │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## vSphere Update Manager (VUM) — Legacy

Baseline-based approach: attach a patch or upgrade baseline to a cluster, scan for compliance, remediate. Still available in vSphere 7; not available in vSphere 8 for cluster-level management.

## Host Upgrade Procedure

**Pre-upgrade checklist:**
- [ ] vCenter already upgraded to target-compatible version
- [ ] Interop matrix checked for vSAN/NSX compatibility
- [ ] HCL verified for target ESXi version + server model
- [ ] vSAN health showing no warnings (if vSAN cluster)
- [ ] HA admission control will allow one host in maintenance mode
- [ ] Backup jobs confirmed paused/not scheduled for upgrade window

**Upgrade order within a cluster:**
1. Put host in maintenance mode (DRS migrates VMs automatically in Fully Automated mode)
2. Verify no VMs remain on host
3. Apply vLCM remediation for host
4. Host reboots and returns to service
5. Exit maintenance mode
6. Validate host: check alerts, storage paths, vmkernel connectivity
7. **Wait 15–30 minutes** before proceeding to next host

Never upgrade all hosts simultaneously — HA and vSAN require quorum hosts.

## ESXi Patch Application (Manual / Standalone)

For hosts not managed by vLCM:

```bash
# Upload patch zip to datastore, then from ESXi shell:
esxcli software sources vib list --depot=/vmfs/volumes/<datastore>/<patch.zip>

# Install the patch
esxcli software vib update --depot=/vmfs/volumes/<datastore>/<patch.zip>

# Check result and reboot
esxcli software vib list | grep -i <vib-name>
reboot
```

## Upgrade and Patching Readiness Checklist

### Current State
- Confirm current ESXi version and build on all hosts
- Note any hosts on a different version than the cluster standard

### Target Image or Baseline
- Identify the target ESXi image or patch baseline
- Confirm the image is compatible with the hardware (HCL)
- Confirm driver and firmware compatibility for NIC, HBA, and storage adapters

### Cluster Capacity
- Confirm the cluster has sufficient headroom to evacuate one host at a time
- Confirm DRS is enabled and set to at least Partially Automated

### Backup and Config Export
- Confirm vCenter file-based backup is current
- Export ESXi host configuration if required for the change record

### Remediation Order

For clusters with multiple hosts:
1. Patch one host at a time
2. Wait for each host to return from maintenance mode and vSAN to stabilize before patching the next
3. Do not patch all hosts simultaneously

### Post-Patch Validation
- Confirm host is Connected in vCenter
- Confirm ESXi version matches the target
- Confirm no new hardware or service alerts
- Confirm vSAN health is green if vSAN is used
- Confirm VMs are running normally

## Driver and Firmware Lifecycle

ESXi drivers (NIC, HBA, RAID) must match the versions in the VMware HCL for the ESXi version in use. Driver updates are delivered as:

- **VIBs** within the ESXi patch bundle
- **Vendor Add-on** packages in vLCM (e.g., Dell OpenManage, HPE SPP)
- **Async driver release** — standalone VIB from vendor (e.g., Broadcom bnxt_en, Intel igbn)

Firmware updates (BIOS, NIC firmware, HBA firmware) are handled out-of-band via:
- Dell iDRAC / Repository Manager
- HPE iLO / SPP (Service Pack for ProLiant)
- Server management tools (Lenovo XClarity, Cisco UCS Manager)

## Rollback Considerations

ESXi does not support in-place downgrade. Options if a patch causes issues:

1. **Stateless ESXi (Auto Deploy)**: Re-deploy with previous image profile — fast rollback
2. **Stateful ESXi**: Restore from ESXi backup (not standard) or reinstall — time-consuming
3. **vLCM**: Remove the new component/VIB from the cluster image and remediate — reverts the specific change

For vSAN clusters: if ESXi 8.x is rolled back, vSAN on-disk format may need downgrade — contact VMware Support before attempting.
