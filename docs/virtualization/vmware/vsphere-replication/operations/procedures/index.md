# vSphere Replication — Procedures

```text
  Key Operational Procedures
┌──────────────────────────────────────────────────────────────┐
│  Configure Replication           Monitor + Manage            │
│  ┌──────────────────────┐        ┌──────────────────────┐    │
│  │ vCenter → [VM] →     │        │ Pause / Resume       │    │
│  │  Configure Replication│       │ Sync Now (immediate) │    │
│  │  RPO: 5min–24hrs      │       │ Change RPO           │    │
│  │  Target DS + VRS      │       │ Change target DS     │    │
│  │  Quiesce / encrypt    │       └──────────────────────┘    │
│  └──────────────────────┘                                    │
│                                                              │
│  Recover VM (standalone)         Add to SRM Protection Group │
│  ┌──────────────────────┐        ┌──────────────────────┐    │
│  │ Target Site vCenter  │        │ 1. Configure VR on VM│    │
│  │ → Replications →     │        │ 2. Wait for initial  │    │
│  │   Recover            │        │    sync (status: OK) │    │
│  │   (Test or actual)   │        │ 3. SRM → PG → Add VMs│    │
│  └──────────────────────┘        └──────────────────────┘    │
└──────────────────────────────────────────────────────────────┘
```

---

## Configure Replication on a VM

```yaml
vCenter → [VM] → right-click → vSphere Replication → Configure

  Step 1: Target site
    Select: amsterdam (recovery site)

  Step 2: Target location
    vCenter: vcenter-amsterdam.example.local
    Datastore: target-datastore-01

  Step 3: Replication settings
    RPO: 1 Hour (range: 5 minutes – 24 hours)
    Recovery point instances: 3 (range: 1–24)
    Quiesce: Yes (for application consistency — requires VMware Tools)
    Network compression: Yes (reduces bandwidth, adds CPU)
    Encryption: Yes (if replicating over WAN)
    VRS: Auto (or select specific VRS)

  Step 4: Seeds
    Use existing data at target (if VM was previously copied to target site): saves initial sync time

  → Finish
```

Initial sync begins immediately. Monitor in Site Recovery → Replications.

---

## Change RPO for a Replicated VM

```text
vCenter → Site Recovery → Replications → [VM] → right-click → Edit
  RPO: change to new value
  → OK → effective immediately
```

---

## Add VM to SRM Protection Group After VR Configured

For vSphere Replication-based SRM protection:

1. Configure VR replication on the VM (see above)
2. Wait for initial sync to complete (status: OK)
3. Then:
   ```
   SRM → Protection → Protection Groups → [VR-based group] → Add VMs
   Select: the newly replicated VM
   ```

---

## Pause and Resume Replication

Pause replication temporarily (e.g., during storage maintenance):

```text
vCenter → Site Recovery → Replications → [VM] → right-click → Pause
```

Resume:
```bash
vCenter → Site Recovery → Replications → [VM] → right-click → Resume
# VM resumes from last sync point — only delta changes replicated after resume
```

---

## Recover a VM (Standalone VR)

For recovery without SRM — manual process:

```text
vCenter (Target Site) → Site Recovery → Replications → [VM]
  → Recover
    Recovery type: Recovery (destructive — intended for actual DR)
    Recovery Point: select from available instances
    Target host/cluster/resource pool: select at recovery site
    Power on after recovery: Yes

OR for testing (non-destructive):
    Recovery type: Test (creates a copy in an isolated network)
```

After recovery, the replication relationship is terminated. Re-configure replication if you want to replicate back (reverse protection).

---

## Change Replication Target Datastore

Move replica files to a different datastore at the target site:

```text
vCenter → Site Recovery → Replications → [VM] → right-click → Edit
  Target Location: change to new datastore
  → OK
```

VR migrates the replica files to the new datastore during the next sync cycle. No replication interruption.

---

## Remove Replication from a VM

```text
vCenter → Site Recovery → Replications → [VM] → right-click → Remove Replication
  Remove replica files: Yes (clean up .vrepl/.hbr files from target) — recommended
  OR: No (keep files — useful if you plan to use them as a seed for re-configuration)
```

After removing, the replica VMDK files on the target datastore are deleted (if "Yes" selected).

---

## Force Sync (Initial Sync for Large VMs)

For VMs with large disks, the initial full sync can take many hours. Schedule during off-peak:

```text
vCenter → Site Recovery → Replications → [VM] → Sync Now
```

This triggers an out-of-schedule sync. The VM must not be powered off during sync unless quiescing.

---

## Add a VRS to Distribute Load

When a VRA is handling >400 VMs:

```text
vCenter → Site Recovery → vSphere Replication → Replication Servers → Deploy VRS

After deploying VRS, reassign VMs to VRS:
  Replications → [VM] → Edit → VRS: select specific VRS or Auto
```

Auto-assignment spreads new replications across all available VRS instances.

---

## Decommission a VRA

Before decommissioning a site or replacing a VRA appliance:

1. Migrate all VM replications to a different VRA/VRS (Edit → change VRS assignment)
2. Verify zero replications remain on the VRA
3. Unregister from vCenter:
   ```
   VRA VAMI → Configuration → vCenter Server → Unregister
   ```
4. Power off and delete the VRA VM from vCenter
