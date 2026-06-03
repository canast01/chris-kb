# Datastore Full / Capacity Alarm

<div class="kb-summary">
A full datastore stops VMs from writing to disk — they pause or crash within seconds of the
datastore becoming completely full. On vSAN, the write-stop threshold is 80% capacity, not 100%.
Snapshots are the most common cause of sudden unexpected capacity consumption. This scenario covers
finding what is consuming space, recovering quickly, and setting up proactive capacity monitoring
to prevent recurrence.
</div>

```text
┌───────────────────────────── Datastore Full / Capacity Alarm — Investigation Flow ─────────────────────────┐
│                                                                                                       │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: vCenter capacity alarm fires OR VMs pause / report disk write errors                        ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                   ┌────────────────────────────┼────────────────────────────┐                         │
│                   ▼                            ▼                            ▼                         │
│   ┌───────────────────────────┐   ┌───────────────────────────┐  ┌───────────────────────────┐        │
│   │  VMFS datastore full      │   │  vSAN datastore > 80%     │  │  NFS datastore full       │        │
│   │  → find large VMDKs,      │   │  → writes stop; VMs pause │  │  → check NFS volume on    │        │
│   │    snapshots, orphans     │   │    find snapshots first   │  │    storage array           │       │
│   └────────────┬──────────────┘   └────────────┬──────────────┘  └────────────┬──────────────┘        │
│                └───────────────────────────────┬┘                              │                      │
│                                                ▼                               │                      │
│   ┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  Find the space consumers: snapshots → large VMDKs → orphaned files → thick-provisioned disks      ││
│   └────────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                                │                                                      │
│                   ┌────────────────────────────┼────────────────────────────┐                         │
│                   ▼                            ▼                            ▼                         │
│   ┌───────────────────────────┐   ┌───────────────────────────┐  ┌───────────────────────────┐        │
│   │  Delete stale snapshots   │   │  Remove orphaned VMDKs    │  │  Expand datastore or      │        │
│   │  (confirm with VM owner)  │   │  after confirming no VM   │  │  add capacity to vSAN     │        │
│   │                           │   │  references them          │  │  cluster                  │        │
│   └───────────────────────────┘   └───────────────────────────┘  └───────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | Datastore capacity alarm; snapshot management; VMDK inventory |
| vSAN | vSAN-specific 80% write-stop threshold; SPBM policy compliance |
| ESXi | Direct filesystem access for orphan detection; snapshot delta file location |
| Aria Operations | Capacity trending, "Days Remaining to Full" projection, historical growth rate |

---

## 1. Identify the Alarm and Affected Datastore

vCenter → **Storage** → **Datastores** → sort by **Free Space** ascending. The lowest-free-space
datastore is the immediate problem.

For vSAN: there is one vSAN datastore per cluster. vCenter → Cluster → **Monitor** → **vSAN** →
**Capacity**. This view shows used vs available and the percentage consumed.

vSAN write-stop thresholds (default):

| Capacity used | vSAN behaviour |
|---|---|
| < 70% | Normal operation |
| 70% | Warning alarm fires |
| 80% | vSAN stops accepting new write I/O — VMs pause immediately |
| 80%+ | No new VMs can be created; no snapshot creation possible |

If vSAN is already above 80%: VM recovery is urgent. Proceed directly to Step 3 to find and
remove snapshots as the fastest way to recover space.

---

## 2. Check What Is Consuming Space

The most common causes of sudden capacity consumption, in order of frequency:

1. **Snapshots** — snapshot delta files (.vmdk-delta) grow with every write to the VM while
   the snapshot exists. A busy VM can generate tens of GB per hour in delta files.
2. **Thin-provisioned VMDKs inflating** — thin disks start small and grow as data is written.
   A VM that was thin-provisioned at 100 GB can reach 100 GB of actual allocation over time.
3. **Orphaned VMDKs** — VMDK files left on the datastore from deleted or migrated VMs with no
   corresponding VM record in vCenter.
4. **Thick-provisioned VMDKs** — thick-eager VMDKs consume their full allocation immediately on
   creation. A recently provisioned thick VM consumes space whether the guest OS is using it
   or not.

---

## 3. Find Large Snapshots — PowerCLI

Snapshots are the fastest path to recovering space. Always get the VM owner's confirmation
before deleting, but treat snapshots older than your retention policy (typically 7 days) as
candidates for immediate removal.

```powershell
# Find all snapshots, sorted by size descending — top 20
Get-VM | Get-Snapshot | `
  Select-Object VM, Name, SizeMB, Created | `
  Sort-Object SizeMB -Descending | `
  Select-Object -First 20
```

```powershell
# Find snapshots older than 7 days across all VMs
Get-VM | Get-Snapshot | Where-Object {$_.Created -lt (Get-Date).AddDays(-7)} | `
  Select-Object VM, Name, SizeMB, Created | Sort-Object Created
```

```powershell
# Remove a specific VM's stale snapshots (confirm with owner first)
Get-VM "vm-name" | Get-Snapshot | `
  Where-Object {$_.Created -lt (Get-Date).AddDays(-7)} | `
  Remove-Snapshot -Confirm:$false
```

Snapshot consolidation (committing delta files back to the base VMDK) temporarily requires
additional free space equal to the delta file size. If the datastore is completely full,
consolidation may fail. In that case, free a small amount of space first (move a VM to another
datastore via Storage vMotion), then consolidate.

---

## 4. Find Orphaned VMDKs on the Datastore

Orphaned VMDKs are VMDK files on the datastore with no corresponding VM registered in vCenter.
These are safe to remove but must be confirmed carefully.

```bash
# SSH to ESXi host — list all VMDK files on a datastore
find /vmfs/volumes/<datastore-name>/ -name "*.vmdk" -not -name "*-flat.vmdk" | sort

# Find large delta files (snapshot deltas over 10 GB)
find /vmfs/volumes/<datastore-name>/ -name "*-delta.vmdk" -size +10G
```

Cross-reference each VMDK path with vCenter. Any VMDK that does not appear in a VM's
**Edit Settings** → **Hard Disk** list and is not a system snapshot is a candidate orphan.

**Never delete a VMDK from the filesystem directly without confirming it is not registered
to any VM in vCenter.** If in doubt, move it to a holding folder and monitor for 72 hours
before permanent deletion.

---

## 5. Expand Capacity or Storage vMotion VMs

If removing snapshots and orphans is not enough:

- **Storage vMotion** — move the largest VMs to a datastore with more free space. This frees
  space on the full datastore without any VM downtime.

```powershell
# Move a VM's storage to a different datastore (no downtime)
Move-VM -VM "vm-name" -Datastore "target-datastore" -DiskStorageFormat Thin
```

- **vSAN capacity expansion** — add a host or additional disk capacity to the vSAN cluster. New
  capacity is immediately available after the disk is added and the disk group is rebuilt.

---

## 6. vSAN SPBM Policy Compliance

When vSAN capacity drops below the threshold required to satisfy storage policies (for example,
FTT=1 requires enough capacity to hold two copies of each object), vSAN marks affected VMs as
**Non-Compliant**.

Check compliance: vCenter → Cluster → **Monitor** → **vSAN** → **Virtual Objects** → filter
for **Non-Compliant**.

Non-compliance is automatically resolved once capacity is recovered and vSAN has enough room to
rebuild the required copies. You do not need to reapply policies manually.

---

## 7. Aria Ops Capacity Trending — Get Ahead of the Next Alarm

After recovering space, use Aria Operations to project when the datastore will fill again:

Aria Operations → **Capacity** → **vSAN Cluster** → **Time Remaining**.

If **Days Remaining to Full** is under 30 days: raise a capacity expansion request immediately.
If under 7 days: treat it as an urgent incident.

```bash
# Aria Ops REST API — get capacity remaining for a specific resource
curl -sk -X GET \
  "https://ariaops.domain.local/suite-api/api/resources/<resource-uuid>/stats?statKey=summary|capacity_remaining" \
  -H "Authorization: Bearer <token>" \
  | jq '.values[].statList.stat[] | {timestamp: .timestamps[], value: .data[]}'
```

Set a proactive alarm threshold: vCenter → **Cluster** → **Monitor** → **vSAN** → **Configure** →
**Advanced Options** — adjust the warning threshold to 60% and the error threshold to 70% for
production clusters. This gives a wider lead time before hitting the 80% write-stop.

---

## Common Mistakes

- **Deleting snapshots without notifying the VM owner.** Snapshots are often taken deliberately
  before patching or application changes. Deleting them without warning removes the rollback
  option while the change window is still open.
- **Not checking Aria Ops trends before the alarm fires.** Capacity issues are predictable.
  A datastore growing at a consistent rate will hit 80% at a calculable date. Aria Ops shows this
  — use it proactively rather than reactively.
- **Letting vSAN hit 80%.** At 80%, write operations stop and VMs pause immediately. There is no
  grace period. Production clusters should never exceed 70% under normal operating conditions.
- **Attempting snapshot consolidation when the datastore is completely full.** Consolidation
  needs working space. Free a few GB first (Storage vMotion one VM off the datastore), then
  consolidate.

---

## Related Scenarios

- [vSAN Stretched Cluster Split-Brain](../vsan-stretched-cluster-split-brain/index.md) — vSAN resync after a partition consumes capacity; a near-full cluster can hit write-stop during resync.
- [SRM Replication Lag / RPO Violation](../srm-replication-lag-rpo-violation/index.md) — Full datastores on the DR site prevent vSphere Replication from writing replicated data, causing RPO violations.
- [Aria Ops Alert Storm](../aria-ops-alert-storm/index.md) — Datastore alarms often appear as part of a larger alert storm triggered by sudden snapshot growth or VM provisioning events.
