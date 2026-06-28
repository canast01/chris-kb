---
tags:
  - scenarios
  - vmware
---
# VM Snapshot Consolidation Required

<div class="kb-summary">
One or more VMs display a "Virtual machine disks consolidation is needed" warning in vCenter. This happens
when snapshot delta files exist on disk but are no longer tracked in the VM's snapshot descriptor — caused
by failed snapshot deletions, backup agent errors, or abrupt ESXi host shutdowns. This scenario covers
identifying affected VMs, safely consolidating without data loss, resolving locked-file failures, and
preventing snapshot sprawl through SPBM policy and backup integration.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_identify_all_affected_vms: "1. Identify All Affected VMs" {shape: rectangle}
2_check_snapshot_manager_and_datasto: "2. Check Snapshot Manager and Datastore Disk Usage" {shape: rectangle}
3_attempt_vcenter_consolidation: "3. Attempt vCenter Consolidation" {shape: rectangle}
4_diagnose_consolidation_failures: "4. Diagnose Consolidation Failures" {shape: rectangle}
5_manual_vmkfstools_consolidation_ad: "5. Manual vmkfstools Consolidation (Advanced)" {shape: rectangle}

products_involved -> 1_identify_all_affected_vms: uses
1_identify_all_affected_vms -> 2_check_snapshot_manager_and_datasto: uses
2_check_snapshot_manager_and_datasto -> 3_attempt_vcenter_consolidation: uses
3_attempt_vcenter_consolidation -> 4_diagnose_consolidation_failures: uses
4_diagnose_consolidation_failures -> 5_manual_vmkfstools_consolidation_ad: uses
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | Consolidation-needed warning; Snapshot Manager; Consolidate action |
| ESXi | VMDK file operations; vmkfstools; snapshot file locking via VMFS |
| vSAN | Datastore space consumption; delta file growth on vSAN objects |
| Backup solution (Veeam/VADP) | Most common root cause — failed backup snapshot quiesce triggers orphaned deltas |
| Aria Operations | Can surface VMs with snapshot age or consolidation-needed warnings via custom policies |

---

## 1. Identify All Affected VMs

The consolidation-needed warning appears in the VM summary tab but is easy to miss when managing many VMs. Use PowerCLI to find all affected VMs at once.

```powershell
# Find all VMs flagged with consolidation needed across all clusters
Get-VM | Where-Object { $_.ExtensionData.Runtime.ConsolidationNeeded -eq $true } `
  | Select-Object Name, VMHost, PowerState `
  | Sort-Object Name
```

In vCenter, look for the amber triangle on any VM's **Summary** tab with the text:
```text
Virtual machine disks consolidation is needed.
```

Also check **Aria Operations → Alerts** for any custom symptom targeting `ConsolidationNeeded = true` — this is a useful proactive signal to configure if not already present.

---

## 2. Check Snapshot Manager and Datastore Disk Usage

Before consolidating, understand the current snapshot chain and confirm there is enough free space for the consolidation I/O.

**In vCenter:** Right-click VM → **Snapshots → Manage Snapshots**.

Snapshot Manager should show no snapshots (they were supposed to be deleted). If it shows no snapshots but the warning still appears, orphaned delta files exist on disk — this is the consolidation-needed condition.

```bash
# On the ESXi host or via datastore browser — list snapshot-related files for the VM
find /vmfs/volumes/<datastore-uuid>/<vm-folder>/ -name "*-delta.vmdk" -o -name "*.vmsd"

# Check how large the delta files are
ls -lh /vmfs/volumes/<datastore-uuid>/<vm-folder>/*-delta.vmdk

# Check available space on the datastore
df -h /vmfs/volumes/<datastore-uuid>
```

Look for: delta files larger than the base VMDK indicate the snapshot has been accumulating changes for a long time — consolidation I/O will be heavy and may take hours. Ensure at least 20% free space on the datastore before starting.

---

## 3. Attempt vCenter Consolidation

The vCenter consolidation action is the correct first step — it is safe to run on a powered-on VM and handles file locking through the ESXi VMFS SCSI reservation mechanism.

Right-click VM → **Snapshots → Consolidate**.

Monitor progress in **vCenter → Tasks and Events** — consolidation appears as a "Consolidate virtual machine disk files" task.

```text
Consolidation states:
  In Progress → delta files being merged into parent disk; I/O is slightly elevated
  Success     → warning cleared; disk chain is flat; delta files removed
  Failed      → see task error message for specific failure reason
```

Look for: consolidation on large delta files (>100 GB) can take 30–60 minutes and will generate elevated disk I/O on the datastore. Monitor datastore latency via **vCenter → Monitor → Performance** during the operation.

---

## 4. Diagnose Consolidation Failures

If vCenter consolidation fails, the task error message points to one of four common causes.

**Cause 1: File locked by another process**

```text
Error: Failed to lock the file
Error: Unable to access file since it is locked
```

Check which host holds the lock:

```bash
# From any ESXi host in the cluster — find which host has the file open
vmkfstools -D /vmfs/volumes/<datastore-uuid>/<vm-folder>/<vm-flat.vmdk>

# Output includes the MAC address of the host holding the lock
# Cross-reference MAC to identify which host to check
```

A backup agent (VADP proxy) or a stale ESXi process may hold the lock. Check active backup jobs in your backup console and terminate any that are stuck on this VM.

**Cause 2: Insufficient disk space**

```text
Error: There is no more space for virtual disk <vm>.vmdk
```

Free space on the datastore before retrying — Storage vMotion the VM to a datastore with more headroom, then consolidate.

```powershell
# Move VM to a larger datastore first
Move-VM -VM "vm-name" -Datastore (Get-Datastore "larger-datastore")
```

**Cause 3: Stale or corrupt snapshot descriptor**

The `.vmsd` file (snapshot descriptor) contains references to snapshot states. If it is corrupt or references deleted files, consolidation fails.

```bash
# Inspect the snapshot descriptor
cat /vmfs/volumes/<datastore-uuid>/<vm-folder>/<vm>.vmsd

# A clean (no snapshots) .vmsd looks like this:
# .encoding = "UTF-8"
# snapshot.lastUID = "0"
# snapshot.current = "0"
# (no snapshot.XXX.uid entries)

# If delta files exist but .vmsd shows no snapshots, this is the orphan condition
```

**Cause 4: VM has active write I/O that cannot be quiesced**

Temporarily stun (quiesce) the VM by migrating it off the host with vMotion or briefly suspending it during off-hours before consolidating — this is a last resort and should be planned as a maintenance window.

---

## 5. Manual vmkfstools Consolidation (Advanced)

If vCenter consolidation fails and the backup agent is not involved, vmkfstools can merge delta files directly. This procedure requires the VM to be powered off or suspended.

```bash
# 1. Power off the VM (plan a maintenance window)
# 2. SSH to the ESXi host owning the VM

# Identify the full disk chain
vmkfstools -v 10 -i /vmfs/volumes/<ds>/<vm>/<vm>-000001.vmdk /vmfs/volumes/<ds>/<vm>/<vm>-flat-merged.vmdk

# -i = inflate / clone: this creates a new flat VMDK merging all delta layers
# The -000001 suffix is the most recent snapshot delta; adjust number as needed

# 3. Rename original base disk to a backup name
mv /vmfs/volumes/<ds>/<vm>/<vm>.vmdk /vmfs/volumes/<ds>/<vm>/<vm>-original.vmdk
mv /vmfs/volumes/<ds>/<vm>/<vm>-flat.vmdk /vmfs/volumes/<ds>/<vm>/<vm>-flat-original.vmdk

# 4. Rename merged disk to the original name
mv /vmfs/volumes/<ds>/<vm>/<vm>-flat-merged.vmdk /vmfs/volumes/<ds>/<vm>/<vm>-flat.vmdk

# 5. Update the .vmdk descriptor to point to the flat file (open in vi and verify)
# 6. Remove old delta files only after confirming VM boots successfully
# 7. Power on VM and verify — do NOT remove originals until validation passes
```

Look for: this procedure should only be used when vCenter consolidation is unavailable and the VM cannot be restored from backup. Always retain original files until the VM is confirmed healthy.

---

## 6. PowerCLI — Bulk Consolidation

For environments with multiple VMs needing consolidation, PowerCLI can trigger consolidation across all affected VMs sequentially.

```powershell
# Find and consolidate all VMs with consolidation needed
$vmsToConsolidate = Get-VM | Where-Object { $_.ExtensionData.Runtime.ConsolidationNeeded -eq $true }

foreach ($vm in $vmsToConsolidate) {
    Write-Host "Consolidating: $($vm.Name)"
    $vm.ExtensionData.ConsolidateVMDisks_Task()
}

# Wait and check results
Start-Sleep -Seconds 30
$vmsToConsolidate | ForEach-Object {
    $status = (Get-VM $_.Name).ExtensionData.Runtime.ConsolidationNeeded
    Write-Host "$($_.Name): ConsolidationNeeded = $status"
}
```

---

## 7. Prevention — Snapshot Policy and Backup Integration

Consolidation-needed warnings are almost always caused by backup agent failures leaving orphaned snapshots.

```text
Prevention checklist:
  [ ] Configure Aria Operations alert on ConsolidationNeeded = true
  [ ] Set snapshot retention policy: maximum age 72 hours, maximum 3 snapshots per VM
  [ ] Configure backup solution to alert on failed quiesce / snapshot delete operations
  [ ] Review backup job failure reports weekly — failed jobs silently leave delta files
  [ ] For VADP backups: verify "Remove Snapshot after backup" is always enabled
  [ ] Monitor vSAN or datastore space: delta files can fill a datastore if undetected for weeks
```

In vCenter, create an alarm:
- **vCenter → Cluster → Configure → Alarm Definitions → New Alarm**
- Trigger: VM Configuration Issue with consolidation-needed condition
- Action: Send email / Aria Ops notification

---

## Key Terms

| Term | Definition |
|---|---|
| Snapshot delta file | A VMDK file with a `-000001` (or higher) suffix that captures all writes made after the snapshot was taken; the base disk is frozen and all new I/O goes to the delta |
| Consolidation | The process of merging one or more delta files back into the base VMDK disk chain, resulting in a single flat disk and no snapshot overhead |
| ConsolidationNeeded | A vCenter runtime property on a VM indicating that orphaned snapshot files exist on disk that are not tracked in the snapshot descriptor; the consolidation-needed warning reflects this state |
| .vmsd file | The snapshot descriptor file (per VM) that tracks all snapshot metadata including snapshot name, creation time, parent/child chain, and which VMDK delta files belong to each snapshot |
| .vmdk descriptor | The text header file for a virtual disk; references the corresponding -flat.vmdk binary data file and the disk geometry/adapter type |
| -flat.vmdk | The binary data file containing the actual raw disk contents; the corresponding .vmdk descriptor points to it |
| Orphaned snapshot | A delta file that exists on disk but has no corresponding entry in the .vmsd descriptor; this is the precise condition that triggers the consolidation-needed warning |
| VADP | vSphere APIs for Data Protection — the VMware API framework used by backup products (Veeam, Commvault, etc.) to quiesce VMs, take snapshots, and stream disk data for backup without agents inside the guest |
| vmkfstools | ESXi CLI tool for VMDK operations including cloning, inflating, converting, and inspecting virtual disk files; the primary tool for manual disk chain repair |
| VMFS SCSI reservation | The SCSI reservation mechanism used by VMFS to lock a file for exclusive access during operations like snapshot consolidation; a stale reservation (from a crashed host or backup agent) is a common cause of "file locked" errors |
| Disk chain | The ordered sequence of VMDK files (base flat + one or more delta files) that represents the complete current disk state; read operations fan through the chain from newest to oldest delta to find the most recent write |

---

## Common Mistakes

- **Deleting delta files manually without consolidating.** Removing a `-000001.vmdk` delta file directly corrupts the VM — all writes since the snapshot was taken are in that file. Always use vCenter Consolidate or vmkfstools, never manual delete.
- **Starting consolidation without checking datastore space.** Consolidation temporarily requires space equal to the largest delta file being merged. A datastore with less than 20% free may fail mid-consolidation, leaving the VM in an inconsistent state.
- **Not investigating why the snapshot was orphaned.** The consolidation-needed warning is a symptom. If the root cause (failing backup job, backup agent crash) is not fixed, new orphaned snapshots will appear after each backup run.
- **Running backup jobs while consolidation is in progress.** A backup agent taking a new snapshot during an ongoing consolidation operation can cause the consolidation to fail or produce a corrupt delta chain.
- **Confusing "Delete All Snapshots" with "Consolidate."** Delete All Snapshots commits snapshots and removes their tracking metadata — it should clear the warning. If the warning persists after Delete All, genuine orphaned files exist and Consolidate is needed.

---

## Related Scenarios

- [Storage APD — Datastore Inaccessible](storage-apd-datastore-inaccessible/index.md) — APD events often leave orphaned delta files behind that trigger the consolidation-needed warning post-recovery.
- [Datastore Full / Capacity Alarm](datastore-full-capacity-alarm/index.md) — Large undetected delta files are one of the most common causes of sudden datastore space exhaustion.
- [VM Performance Degraded](vm-performance-degraded/index.md) — VMs running on a long delta chain (many snapshots or a very large delta) experience elevated read latency because all reads fan through the snapshot chain.
