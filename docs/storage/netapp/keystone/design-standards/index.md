# NetApp Keystone Standards


<div class="kb-summary">
NetApp Keystone Standards reference covering Service Level Selection, Naming Conventions, Capacity Management Thresholds, Monthly Operational Standards, Decommission Standards.
</div>

## Service Level Selection

Assign workloads to the appropriate Keystone service tier before provisioning. Tier selection directly affects billing — workloads on a higher-performance tier than needed incur unnecessary cost, while workloads under-tiered will breach SLA latency targets.

| Service Level | Target Workloads | IOPS/TB | Latency |
|---|---|---|---|
| Extreme | Oracle, SQL Server, SAP HANA, high-IOPS transactional | Up to 12,000 | < 1 ms |
| Premium | Mixed workloads, VMware vSphere, ERP secondary tiers | Up to 4,000 | < 1 ms |
| Performance | General-purpose file and block, NAS shares | Up to 2,000 | < 2 ms |
| Value | Backup targets, archive, infrequent access | Up to 64 | < 17 ms |
| Object (StorageGRID) | Unstructured data, S3 object, media repositories | S3 throughput | SLA per contract |

- Map each application to a tier at provisioning time; document the tier in the CMDB or a capacity register
- Do not downgrade a workload from a higher-performance tier to a lower tier mid-subscription — plan service level assignments at provisioning time
- Review burst usage monthly; persistent burst signals that committed capacity on the tier should be increased at the next amendment opportunity

---

## Naming Conventions

| Object | Standard | Example |
|---|---|---|
| QoS adaptive policy-group | `<tier>-ks` | `extreme-ks`, `premium-ks`, `performance-ks`, `value-ks` |
| Volume | Site naming standard + `-ks` suffix if needed for identification | `vol_oradb01_data`, not overridden for Keystone |
| Volume comment | Include application owner and Keystone tier | `app=oradb01 team=finance tier=extreme` |
| SVM | Standard SVM naming; tag SVM description with `keystone=true` | `svm_prod_ks` or `svm_prod` with comment tag |
| Snapshot | Standard ONTAP naming via snapshot policy; no Keystone-specific deviation | `hourly.2025-05-07_0800` |

### Volume Tagging via Comments

```bash
# Set a volume comment to identify application owner and Keystone tier
volume modify \
    -vserver svm_prod \
    -volume vol_oradb01_data \
    -comment "app=oradb01 owner=finance tier=extreme keystone=true"

# List volumes with their comments to verify tagging
volume show -fields vserver,volume,comment | grep keystone
```
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
```text

---

## Capacity Management Thresholds

| Threshold | Trigger | Action | Owner |
|---|---|---|---|
| 70% of committed | Capacity review trigger | Forecast growth; estimate time to burst | Storage team |
| 80% of committed | Warning threshold | Begin capacity amendment process with KSM; set EMS alert | Storage + KSM |
| 90% of committed | Near-burst | Escalate to KSM; accelerate amendment; review for quick decommissions | KSM + storage team |
| 100% of committed | Burst billing begins | Emergency amendment; identify and remove idle volumes or snapshots | KSM + management |
| Burst limit reached | Provisioning blocked | Emergency amendment or service-level adjustment required | KSM + storage team |

### ONTAP EMS Threshold Alerts

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

---

## Monthly Operational Standards

| Activity | Frequency | Owner | Output |
|---|---|---|---|
| Capacity consumption review vs. committed | Monthly (before billing close) | Storage team | Confirmed no unexpected burst |
| Consumption report download and archive | Monthly | Storage team | Archived report for chargeback / audit |
| Unclassified volume audit | Monthly | Storage team | Zero volumes without QoS policy-group |
| Snapshot usage review on premium tiers | Monthly | Storage team | Excessive snapshots identified and addressed |
| BlueXP burst trend review | Monthly | Storage team + KSM | Amendment plan if burst trending upward |
| Service level appropriateness review | Quarterly | Storage team + application owners | Workloads not over or under-tiered |
| KSM engagement | Quarterly | Storage team | Capacity forecast; subscription alignment |

---

## Decommission Standards

When decommissioning volumes on Keystone-managed clusters, capacity is freed from the billing tier as soon as the volume is deleted and the Collector reports the next collection cycle. Ensure the following before decommissioning:

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

Note: if decommissioning occurs after the monthly billing close, the capacity is still billed for that period. Time decommissions before the billing close date to capture the reduction in the current invoice period.
