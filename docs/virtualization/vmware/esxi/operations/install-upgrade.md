---
tags:
  - esxi
  - operations
  - vmware
  - vsphere-8
---
# ESXi Install & Upgrade


<div class="kb-summary">
ESXi Install & Upgrade reference covering vSphere Update Manager (VUM) — Legacy, Host Upgrade Procedure, ESXi Patch Application (Manual / Standalone), Upgrade and Patching Readiness Checklist, Driver and Firmware Lifecycle and 1 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>

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

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

!!! warning "Host enters maintenance mode"
    ESXi remediation puts hosts into maintenance mode, triggering DRS evacuation. Confirm DRS is Fully Automated and HA admission control is satisfied before starting.

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

---

## See also

- [ESXi — Health Checks](health-checks/)
- [ESXi — Common Issues](../troubleshooting/common-issues/)
- [ESXi — Procedures](procedures/)

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
