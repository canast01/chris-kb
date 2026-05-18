# ESXi Install & Upgrade

```
ESXi Upgrade Flow — vLCM Rolling Cluster Upgrade
┌─────────────────────────────────────────────────────────┐
│  Pre-Upgrade                                            │
│  ├── Confirm vCenter already at target-compatible ver   │
│  ├── Check HCL for target ESXi + server model           │
│  ├── Verify vSAN / NSX interop matrix                   │
│  └── Take vCenter file-based backup                     │
└──────────────────────────┬──────────────────────────────┘
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
```

## Version and Support Matrix

| Version | Release | General Support End | Technical Guidance End |
|---|---|---|---|
| ESXi 6.5 | 2016-11 | 2022-10-15 | 2023-11-15 |
| ESXi 6.7 | 2018-04 | 2022-10-15 | 2023-11-15 |
| ESXi 7.0 | 2020-04 | 2025-04-02 | 2027-04-02 |
| ESXi 7.0 U3 | 2021-10 | 2025-04-02 | 2027-04-02 |
| ESXi 8.0 | 2022-10 | 2027-10 (est.) | 2029-10 (est.) |
| ESXi 8.0 U1 | 2023-04 | 2027-10 (est.) | 2029-10 (est.) |
| ESXi 8.0 U2 | 2023-09 | 2027-10 (est.) | 2029-10 (est.) |
| ESXi 8.0 U3 | 2024-06 | 2027-10 (est.) | 2029-10 (est.) |

Always check at [Broadcom Product Lifecycle](https://support.broadcom.com/group/ecx/productlifecycle).

## Patch Cadence

VMware follows a **quarterly patch cadence** for ESXi. Patches are delivered as:

- **General Release (GA)**: Quarterly cumulative patches
- **Security Patches**: Out-of-band for VMSA advisories; apply based on CVSSv3 score
- **Async Drivers**: Hardware driver updates decoupled from ESXi base version

Subscribe to [Broadcom Security Advisories](https://support.broadcom.com/web/ecx/security-advisory) for immediate notification of critical VMSA advisories.

## Lifecycle Management Tools

### vSphere Lifecycle Manager (vLCM) — Recommended

vLCM manages ESXi hosts using a **desired-state cluster image**:

```
Cluster Image = ESXi Base Version
              + Vendor Add-ons (OEM driver bundle)
              + Components (individual VIBs)
```

**Workflow:**
1. Set cluster image (select base ESXi version + add-ons)
2. Run **Check Compliance** — shows drift between running state and desired image
3. **Remediate** — vLCM puts host in maintenance mode, applies image, reboots, exits maintenance mode

Verify image depot is synced:
```
vCenter → Lifecycle Manager → Settings → Patch Setup → Sync Updates
```

### vSphere Update Manager (VUM) — Legacy

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
