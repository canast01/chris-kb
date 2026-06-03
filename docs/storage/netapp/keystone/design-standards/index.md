```bash
# Set a volume comment to identify application owner and Keystone tier
volume modify \
    -vserver svm_prod \
    -volume vol_oradb01_data \
    -comment "app=oradb01 owner=finance tier=extreme keystone=true"

# List volumes with their comments to verify tagging
volume show -fields vserver,volume,comment | grep keystone
```

```text
┌───────────────────────────────── NetApp Keystone — Design Standards ──────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │         Design standards: capacity planning, QoS adaptive policies, FabricPool tiering        │   │
│   │             QoS adaptive: auto-assign IOPS/TB ceiling per service level per volume            │   │
│   │             FabricPool: automatic cold-data tiering to S3/StorageGRID object store            │   │
│   │             Capacity: size committed at 70-80% peak; monitor via Active IQ alerts             │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Workload profile -> service level -> QoS adaptive policy -> volume + tiering policy                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │       Capacity Design       │  │          QoS Design         │  │        Tiering Design       │   │
│   │       Committed 70-80%      │  │         Adaptive QoS        │  │          FabricPool         │   │
│   │      Burst headroom 20%     │  │         Min IOPS/TB         │  │        S3 cloud tier        │   │
│   │        Thin provision       │  │         Max IOPS/TB         │  │         StorageGRID         │   │
│   │        Dedup+compress       │  │       Burst allowance       │  │        Cold threshold       │   │
│   │        Quota policies       │  │          QoS group          │  │       Retrieve policy       │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│    Enable dedup+compression on all volumes; typical 2-3x reduction on structured data                 │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Standard     │      Value       │     Apply When    │      Check       │      Notes       │   │
│   │      Dedup       │    Enable all    │    All volumes    │     sis show     │   2-3x saving    │   │
│   │     Compress     │   Inline+post    │     Block data    │     sis show     │     CPU cost     │   │
│   │     Tiering      │  Cold >31 days   │    Capacity vol   │     FP show      │      To S3       │   │
│   │   QoS adaptive   │   Per SL tier    │      All vols     │     qos show     │    Auto-apply    │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: AFF local tier + object store bucket (S3/StorageGRID) for FabricPool                     │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Adaptive QoS     = ONTAP policy that auto-scales IOPS ceiling with volume size                     │
│    FabricPool       = ONTAP feature; automatically moves cold blocks to object tier                   │
│    Tiering policy   = Per-volume: none / snapshot-only / auto / all                                   │
│    StorageGRID      = NetApp on-prem S3 object storage; common FabricPool target                      │
│    Dedup            = Inline deduplication; removes duplicate 4KB blocks on write                     │
│    Compression      = Inline or post-process; reduces physical block footprint                        │
│    Thin provisioning= Volume logical size > physical allocation; grows on write                       │
│    Quota policy     = User/group/qtree disk and file count limits in ONTAP                            │
│    sis show         = Storage Inline Storage cmd; shows dedup/compress status                         │
│    qos show         = ONTAP command; lists QoS policies and current IOPS utilisation                  │
│    Cold threshold   = Days of inactivity before FabricPool moves block to object                      │
│    Retrieve policy  = Controls if tiered data read back to SSD (on-demand vs never)                   │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
```bash
# Set a volume-level space threshold alert at 80% utilisation
# (Keystone billing is based on logical used, but physical capacity matters for planning)
event config modify -threshold-alerts-enabled true

# Configure a volume nearly-full threshold event for Keystone volumes
# ONTAP generates wafl.vol.full.threshold events when volumes reach configured thresholds
set advanced
volume modify \
    -vserver svm_prod \
    -volume vol_oradb01_data \
    -space-nearly-full-threshold-percent 80 \
    -space-full-threshold-percent 95
set admin

# Verify threshold settings
volume show -vserver svm_prod -volume vol_oradb01_data \
    -fields space-nearly-full-threshold-percent,space-full-threshold-percent
```
```bash
# Step 1: Confirm the volume is no longer in use (no active client mounts)
nfs show -vserver svm_prod | grep vol_oldapp
# Verify no NFS exports; check CIFS share list
vserver cifs share show -vserver svm_prod -volume vol_oldapp

# Step 2: Delete all snapshots to release capacity immediately
snapshot delete -vserver svm_prod -volume vol_oldapp -snapshot * -force

# Step 3: Unmount and offline the volume
volume unmount -vserver svm_prod -volume vol_oldapp
volume offline -vserver svm_prod -volume vol_oldapp

# Step 4: Delete the volume
volume delete -vserver svm_prod -volume vol_oldapp -force

# Step 5: Verify the volume no longer appears
volume show -vserver svm_prod -volume vol_oldapp
# Expected: no matching volumes

# Step 6: Confirm the capacity is reflected in the next BlueXP reporting cycle
# (capacity reduction visible in BlueXP within the next Collector collection interval)
```
