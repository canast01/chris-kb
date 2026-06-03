# Storage vMotion / Datastore Migration

<div class="kb-summary">
Storage vMotion (svMotion) migrates a VM's VMDKs from one datastore to another while the VM stays
powered on and serving workloads. It is the correct tool for rebalancing vSAN capacity, migrating
from traditional SAN to vSAN, and decommissioning old datastores. The migration uses the ESXi
storage I/O path and has a measurable performance cost — plan migrations during off-peak hours for
large VMDKs and always verify destination capacity and storage policy before starting.
</div>

```text
┌──────────────────────────── Storage vMotion / Datastore Migration — Procedure Flow ───────────────────────────────┐
│                                                                                                       │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  START: Identify VMs to migrate — capacity rebalance, datastore decommission, or SAN-to-vSAN migration    ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 1 — Pre-migration checks: destination free space ≥ 1.5× source VMDK, storage policy chosen         ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 2 — Initiate svMotion: vCenter UI (right-click → Migrate) or PowerCLI Move-VM                       ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                                                      ▼                                                │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 3 — Monitor: vCenter Recent Tasks + esxtop disk view (DAVG < 30 ms during migration)                ││
│  └──────────────────────────────────────────────────┬───────────────────────────────────────────────────────┘│
│                                                      │                                                │
│                          ┌───────────────────────────┼───────────────────────────┐                    │
│                          ▼                           ▼                           ▼                    │
│          ┌─────────────────────────┐   ┌─────────────────────────┐  ┌─────────────────────────┐       │
│          │  Migration complete:    │   │  Performance impact:    │  │  Policy update needed:  │       │
│          │  verify new datastore  │   │  throttle or reschedule │  │  apply target policy    │        │
│          └────────────┬────────────┘   └────────────┬────────────┘  └────────────┬────────────┘       │
│                       └────────────────────────────┬─┘──────────────────────────┘                     │
│                                                    ▼                                                  │
│  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│  │  Step 4 — Post-migration: verify VM on new datastore, policy compliant, old datastore empty               ││
│  └────────────────────────────────────────────────────────────────────────────────────────────────────────────┘│
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
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

Before initiating any svMotion, verify destination capacity and understand the VMDK format. Thin
disks inflate to their provisioned size during migration — a 500 GB thin-provisioned disk consuming
only 100 GB of actual space will consume up to 500 GB on the destination during the migration
process.

```powershell
# Check destination datastore free space
Get-Datastore "destination-datastore" | Select Name, FreeSpaceGB, CapacityGB

# Check source VM disk sizes and current format
Get-VM "vm-name" | Get-HardDisk | Select Name, CapacityGB, StorageFormat
```

**Required free space on destination:** at least 1.5× the total provisioned VMDK capacity of all
disks being migrated. The 0.5× overhead covers the swap file, snapshot delta disks that may be
active during migration, and the temporary delta created by the mirror copy process.

If migrating to a vSAN datastore, confirm the target storage policy exists:

```powershell
# List available storage policies
Get-SpbmStoragePolicy | Select Name, Description
```

---

## 2. Choose Storage Policy for Destination

If migrating to vSAN, always select an explicit storage policy. Migrating without specifying a
policy applies the vSAN default policy, which may not match what the VM requires.

```powershell
# Store target policy in a variable for use in the migration command
$policy = Get-SpbmStoragePolicy "Production-Standard"
```

**Special case — migrating within the same vSAN datastore for a policy change:** svMotion is not
needed. vSAN can apply a new storage policy to an existing VMDK without moving data. Right-click
the VM → **VM Policies** → **Edit VM Storage Policies** → select the new policy → **Apply to All**.
vSAN will resync components to satisfy the new policy in the background.

---

## 3. Initiate svMotion via vCenter UI

Right-click the VM → **Migrate** → select the migration type:

| Migration type | When to use |
|---|---|
| Change storage only | Move VMDKs to a different datastore; VM stays on the same host |
| Change compute resource and storage | Move VM to a different host AND different datastore simultaneously |
| Change compute resource only | Standard vMotion — compute only, no disk movement |

For storage-only migration: select **Change storage only** → select the destination datastore →
select the storage policy → **Finish**.

---

## 4. Initiate svMotion via PowerCLI

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

Migration speed depends on VMDK size and the I/O load on both datastores. Reference:

| VMDK size | Typical migration time |
|---|---|
| 100 GB | 10-25 minutes |
| 500 GB | 30-90 minutes |
| 2 TB | 2-6 hours |

---

## 5. Monitor Migration Progress

vCenter → **Recent Tasks** → look for **Relocate virtual machine**. The progress percentage and
estimated time remaining are shown in the task pane.

```bash
# From the ESXi host running the VM — monitor disk latency during migration
# Press 'u' in esxtop to switch to disk view
# DAVG column: average device latency in ms
esxtop
```

If DAVG exceeds 30 ms consistently during migration, the storage I/O path is under excessive
pressure. Options:

- Throttle: pause other storage-intensive workloads on the same datastore
- Reschedule: run the migration during off-peak hours (nights or weekends)
- Stagger: if migrating multiple VMs, run them sequentially rather than in parallel

Aria Operations → **Workload** → **VMs** → watch the source VM's **Disk Read Latency** and
**Disk Write Latency** metrics. Alerts on other VMs on the same datastore during migration
indicate storage contention.

---

## 6. Decommission the Old Datastore (if Applicable)

Once all VMs and VMDKs have been migrated off a datastore, verify it is truly empty before
unmounting or decommissioning.

```powershell
# Verify no VMs remain on the old datastore
Get-Datastore "old-datastore" | Get-VM

# Check for orphaned VMDKs not attached to any VM
Get-Datastore "old-datastore" | Get-HardDisk

# Check for VM swap files (.vswp) — these are not returned by Get-HardDisk
# Browse datastore in vCenter and look for any remaining files
```

All three checks must return empty results. Orphaned VMDKs and swap files are the most commonly
missed items — they are not attached to any VM in inventory but still occupy space and will prevent
datastore decommission.

After verification: unmount the datastore from all hosts before decommissioning the underlying
storage.

```powershell
# Unmount datastore from all hosts
$ds = Get-Datastore "old-datastore"
$ds | Get-VMHost | ForEach-Object {
    $storSys = Get-View -Id $_.ExtensionData.ConfigManager.DatastoreSystem
    $storSys.RemoveDatastore($ds.ExtensionData.MoRef)
}
```

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

## Related Scenarios

- Host Maintenance and Patching
- vSAN Disk or Component Failure
- Capacity Planning
- Enable vSAN Encryption
