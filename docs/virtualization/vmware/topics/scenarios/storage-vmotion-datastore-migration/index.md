---
tags:
  - scenarios
  - vmware
---
# Storage vMotion / Datastore Migration

<div class="kb-summary">
Storage vMotion (svMotion) migrates a VM's VMDKs from one datastore to another while the VM stays
powered on and serving workloads. It is the correct tool for rebalancing vSAN capacity, migrating
from traditional SAN to vSAN, and decommissioning old datastores. The migration uses the ESXi
storage I/O path and has a measurable performance cost — plan migrations during off-peak hours for
large VMDKs and always verify destination capacity and storage policy before starting.
</div>

```text
┌─────────────────────── Storage vMotion / Datastore Migration — Procedure Flow ────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  svMotion migrates VMDKs while the VM stays powered on — for rebalancing, decommission, SAN→vSAN      │
│  Plan during off-peak hours for large VMDKs; verify destination capacity before starting              │
│                                                                                                       │
│  START: Identify VMs to migrate — capacity rebalance, datastore decommission, or SAN-to-vSAN          │
│                                                                                                       │
│  STEP 1 — Pre-Migration Checks                                                                        │
│  Destination free space ≥ 1.5× source VMDK size · storage policy for target datastore chosen          │
│                                                                                                       │
│  STEP 2 — Initiate Storage vMotion                                                                    │
│  vCenter UI: right-click VM → Migrate → Change storage only                                           │
│  PowerCLI: Move-VM -Datastore <target-datastore>                                                      │
│                                                                                                       │
│  STEP 3 — Monitor                                                                                     │
│  vCenter Recent Tasks: watch migration % completion                                                   │
│  esxtop disk view: DAVG should stay < 30 ms during migration                                          │
│  If performance impact: throttle or reschedule migration to off-peak window                           │
│  If policy update needed: apply target storage policy to migrated VMDKs                               │
│                                                                                                       │
│  STEP 4 — Post-Migration                                                                              │
│  Verify VM on new datastore · storage policy compliant · old datastore empty and ready to unmount     │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter Server | svMotion orchestration — manages the migration task and tracks progress |
| ESXi | Executes the I/O path during migration; hosts both source and destination datastores |
| vSAN | Acts as source or destination datastore; storage policy enforcement on migrated VMDKs |
| Aria Operations | Performance monitoring during migration; confirms no latency spikes affecting other VMs |

---

## 1. Pre-Migration Checks

Verify destination free space and VMDK format before starting — thin-provisioned disks inflate to their full provisioned size during migration.

```powershell
# Check destination datastore free space
Get-Datastore "destination-datastore" | Select Name, FreeSpaceGB, CapacityGB

# Check source VM disk sizes and current format
Get-VM "vm-name" | Get-HardDisk | Select Name, CapacityGB, StorageFormat

# List available storage policies (required if destination is vSAN)
Get-SpbmStoragePolicy | Select Name, Description
```

Expected: destination free space ≥ 1.5× total provisioned VMDK capacity. The 0.5× overhead covers swap file, snapshot delta files, and the temporary mirror copy delta.

---

## 2. Choose Storage Policy for Destination

Always select an explicit SPBM storage policy when migrating to vSAN — omitting one applies the vSAN default policy, which may not match the VM's requirements.

```powershell
# Store target policy in a variable for use in the migration command
$policy = Get-SpbmStoragePolicy "Production-Standard"
```

**Special case — policy change within the same vSAN datastore:** svMotion is not needed. Right-click the VM → **VM Policies** → **Edit VM Storage Policies** → select the new policy → **Apply to All**. vSAN resyncs components in the background to satisfy the new policy.

---

## 3. Initiate svMotion via vCenter UI

Right-click the VM → **Migrate** → select the migration type, then choose the destination datastore and storage policy.

| Migration type | When to use |
|---|---|
| Change storage only | Move VMDKs to a different datastore; VM stays on the same host |
| Change compute resource and storage | Move VM to a different host AND different datastore simultaneously |
| Change compute resource only | Standard vMotion — compute only, no disk movement |

Expected: migration task appears in vCenter Recent Tasks as **Relocate virtual machine** with a progress percentage.

---

## 4. Initiate svMotion via PowerCLI

Use `Move-VM` to migrate via PowerCLI, including bulk migrations of all VMs on a source datastore.

```powershell
# Migrate VMDK to a different datastore (keep same disk format)
Move-VM -VM "vm-name" `
        -Datastore (Get-Datastore "destination-datastore") `
        -DiskStorageFormat Thin

# Migrate to vSAN datastore and apply a specific storage policy
Move-VM -VM "vm-name" `
        -Datastore (Get-Datastore "vsanDatastore") `
        -StoragePolicy (Get-SpbmStoragePolicy "Production-Standard")

# Migrate multiple VMs to a destination datastore in sequence
Get-Datastore "source-datastore" | Get-VM | ForEach-Object {
    Move-VM -VM $_ -Datastore (Get-Datastore "destination-datastore") -DiskStorageFormat Thin
}
```

Reference migration times:

| VMDK size | Typical migration time |
|---|---|
| 100 GB | 10-25 minutes |
| 500 GB | 30-90 minutes |
| 2 TB | 2-6 hours |

---

## 5. Monitor Migration Progress

Watch disk latency during migration to detect storage pressure that affects other VMs on the same datastore.

```bash
# Press 'u' in esxtop to switch to disk view; DAVG = average device latency in ms
esxtop
```

Look for: DAVG stays below 30 ms. If DAVG exceeds 30 ms consistently: throttle concurrent workloads, reschedule to off-peak hours, or stagger multi-VM migrations to run sequentially. Monitor Aria Operations → **Workload** → **VMs** for disk latency alerts on neighbouring VMs.

---

## 6. Decommission the Old Datastore (if Applicable)

Verify the source datastore is completely empty before unmounting — orphaned VMDKs and swap files are not visible in standard inventory views.

```powershell
# Verify no VMs remain on the old datastore
Get-Datastore "old-datastore" | Get-VM

# Check for orphaned VMDKs not attached to any VM
Get-Datastore "old-datastore" | Get-HardDisk

# Unmount datastore from all hosts
$ds = Get-Datastore "old-datastore"
$ds | Get-VMHost | ForEach-Object {
    $storSys = Get-View -Id $_.ExtensionData.ConfigManager.DatastoreSystem
    $storSys.RemoveDatastore($ds.ExtensionData.MoRef)
}
```

Expected: all three checks return empty results. Also browse the datastore in vCenter to confirm no `.vswp` swap files remain — `Get-HardDisk` does not return swap files.

---

## Post-Task Validation

| Check | Command / Location | Expected Result |
|---|---|---|
| VM on new datastore | `Get-VM "vm-name" \| Get-HardDisk` | New datastore name shown |
| Storage policy applied | `Get-SpbmEntityConfiguration -Entity (Get-VM "vm-name")` | Target policy, Compliant |
| VM still running | vCenter inventory | Powered On, no alarms |
| No disk errors on host | `esxcli storage core device list` | No error state on any device |
| Old datastore empty | `Get-Datastore "old-ds" \| Get-VM` | No output |
| Aria Ops alerts | Aria Operations → Alerts | No new storage latency alerts |

---

## Common Mistakes

- **Not checking destination free space before starting.** If the destination runs out of space
  mid-migration, the task fails while the mirror copy is in a partial state. The VM remains on the
  source but may show storage errors. Recovery requires cleaning up the partial destination files
  manually.
- **Forgetting to update the storage policy after migration.** The VM migrates successfully but
  retains the old policy. On vSAN, this means the VM may be running with different redundancy or
  caching settings than intended. The policy mismatch only surfaces when vSAN evaluates compliance.
- **Decommissioning the source datastore before verifying all files have moved.** VM swap files,
  memory snapshots, and orphaned VMDKs are not always visible in standard inventory views.
  Decommissioning with files remaining causes data loss.
- **Running parallel svMotions on the same datastore.** Multiple simultaneous migrations to or
  from the same datastore compound I/O pressure and can cause DAVG spikes that affect all VMs on
  that datastore, not just the ones being migrated.

---

---

## Key Terms

| Term | Definition |
|---|---|
| svMotion | Storage vMotion — the vSphere feature that migrates a VM's VMDKs between datastores while the VM remains powered on and serving workloads without interruption |
| SPBM | Storage Policy-Based Management — the vSphere framework that defines and enforces VM storage requirements (redundancy, caching, encryption) via named policies assigned to VMDKs |
| Thin provisioning | A VMDK format that allocates disk space on demand as data is written, rather than reserving the full provisioned size upfront; inflates toward full provisioned size during svMotion |
| Thick eager zeroed | A VMDK format where the full provisioned size is allocated and zeroed at creation time; required for some workloads (e.g. VMware Fault Tolerance); migrates as-is, not inflated |
| VMDK | Virtual Machine Disk — the file format that stores a VM's disk data on a datastore; each virtual hard disk attached to a VM is a VMDK file |
| Delta file | A snapshot delta disk that captures writes made to a VMDK after a snapshot is taken; active delta files are included in the space overhead during svMotion |
| Datastore decommission | The process of unmounting a datastore from all hosts and removing the underlying LUN or NFS export after all VMs and files have been migrated off |
| DAVG | Device Average latency — the average I/O completion time in milliseconds for a storage device, visible in esxtop disk view; a value above 30 ms during svMotion indicates storage pressure |
| vSAN policy compliance | The state of a VM's storage policy requirements being met by vSAN component placement; a non-compliant state means vSAN cannot fulfil the requested redundancy or caching settings |
| Orphaned VMDK | A VMDK file that exists on a datastore but is not registered to any VM in vCenter inventory; invisible to `Get-VM` but still consumes space and blocks datastore decommission |
| NFC | Network File Copy — the ESXi protocol used to transfer VMDK data between datastores during svMotion; operates over the management or vMotion VMkernel network |
| Datastore browser | The vCenter UI view (right-click datastore → Browse Files) that shows all files on a datastore regardless of whether they are attached to a VM — the only view that reveals orphaned VMDKs and swap files |

## Related Scenarios

- Host Maintenance and Patching
- vSAN Disk or Component Failure
- Capacity Planning
- Enable vSAN Encryption
