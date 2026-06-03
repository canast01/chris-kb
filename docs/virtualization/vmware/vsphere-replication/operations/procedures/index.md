```text
┌──────────────────────────────────────────────────────────────┐
│  Configure Replication           Monitor + Manage                                                     │
│  ┌──────────────────────┐        ┌──────────────────────┐                                             │
│  │ vCenter → [VM] →     │        │ Pause / Resume       │                                             │
│  │  Configure Replication│       │ Sync Now (immediate) │                                             │
│  │  RPO: 5min–24hrs      │       │ Change RPO           │                                             │
│  │  Target DS + VRS      │       │ Change target DS     │                                             │
│  │  Quiesce / encrypt    │       └──────────────────────┘                                             │
│  └──────────────────────┘                                                                             │
│                                                                                                       │
│  Recover VM (standalone)         Add to SRM Protection Group                                          │
│  ┌──────────────────────┐        ┌──────────────────────┐                                             │
│  │ Target Site vCenter  │        │ 1. Configure VR on VM│                                             │
│  │ → Replications →     │        │ 2. Wait for initial  │                                             │
│  │   Recover            │        │    sync (status: OK) │                                             │
│  │   (Test or actual)   │        │ 3. SRM → PG → Add VMs│                                             │
│  └──────────────────────┘        └──────────────────────┘                                             │
└──────────────────────────────────────────────────────────────┘
```
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
```text
vCenter → Site Recovery → Replications → [VM] → right-click → Edit
  RPO: change to new value
  → OK → effective immediately
```
```sql
   SRM → Protection → Protection Groups → [VR-based group] → Add VMs
   Select: the newly replicated VM
   ```

---

## Pause and Resume Replication

Pause replication temporarily (e.g., during storage maintenance):

```

```text
vCenter → Site Recovery → Replications → [VM] → right-click → Pause
```
```bash
vCenter → Site Recovery → Replications → [VM] → right-click → Resume
# VM resumes from last sync point — only delta changes replicated after resume
```
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
```text
vCenter → Site Recovery → Replications → [VM] → right-click → Edit
  Target Location: change to new datastore
  → OK
```
```text
vCenter → Site Recovery → Replications → [VM] → right-click → Remove Replication
  Remove replica files: Yes (clean up .vrepl/.hbr files from target) — recommended
  OR: No (keep files — useful if you plan to use them as a seed for re-configuration)
```
```text
vCenter → Site Recovery → Replications → [VM] → Sync Now
```
```text
vCenter → Site Recovery → vSphere Replication → Replication Servers → Deploy VRS

After deploying VRS, reassign VMs to VRS:
  Replications → [VM] → Edit → VRS: select specific VRS or Auto
```
```text
   VRA VAMI → Configuration → vCenter Server → Unregister
   ```
4. Power off and delete the VRA VM from vCenter
