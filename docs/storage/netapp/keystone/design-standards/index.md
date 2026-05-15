# NetApp Keystone Standards

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

---

## Configuration Baseline

### QoS Adaptive Policy-Group Build

Keystone service levels must be represented by ONTAP QoS adaptive policy-groups. NetApp creates these during onboarding, but they should be verified and documented.

```bash
# Verify Keystone QoS adaptive policy-groups exist on the ONTAP cluster
qos adaptive-policy-group show
# Expected output — one policy-group per Keystone tier:
# Name            Absolute Min-IOPS   Peak-IOPS   Expected-IOPS
# extreme-ks      1000 IOPS/TB        12000 IOPS/TB  6000 IOPS/TB
# premium-ks      500 IOPS/TB         4000 IOPS/TB   2000 IOPS/TB
# performance-ks  128 IOPS/TB         2000 IOPS/TB   1000 IOPS/TB
# value-ks        64 IOPS/TB          64 IOPS/TB     64 IOPS/TB

# Assign the correct QoS policy-group to a volume
volume modify \
    -vserver svm_prod \
    -volume vol_oradb01_data \
    -qos-adaptive-policy-group extreme-ks

# Verify the assignment
volume show -vserver svm_prod -volume vol_oradb01_data \
    -fields qos-policy-group,qos-adaptive-policy-group
```

### Volume Provisioning Checklist

Before provisioning a new volume on a Keystone-managed cluster:

- [ ] Service level (tier) confirmed for the workload based on IOPS and latency requirements
- [ ] Available committed capacity verified for the target tier in BlueXP — not triggering burst
- [ ] QoS adaptive policy-group selected and will be applied at volume creation time
- [ ] Volume size accounts for snapshot reserve (add 20% for snapshots if frequent snapshots are expected)
- [ ] Volume comment tagged with application owner, team, and Keystone tier
- [ ] Space guarantee set appropriately: `none` (thin) for most workloads; `volume` (thick) only if required by the application
- [ ] Keystone Collector confirmed running before provisioning — new capacity must be reported accurately

```bash
# Create a volume with Keystone tier QoS applied from the start
volume create \
    -vserver svm_prod \
    -volume vol_newapp_data \
    -aggregate aggr_flash_01 \
    -size 2TB \
    -space-guarantee none \
    -snapshot-policy default \
    -qos-adaptive-policy-group premium-ks \
    -comment "app=newapp owner=it-ops tier=premium keystone=true"

# Confirm the volume has the correct QoS policy
volume show -vserver svm_prod -volume vol_newapp_data \
    -fields qos-adaptive-policy-group,size,space-guarantee
```

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
