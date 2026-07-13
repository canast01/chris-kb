---
tags:
  - netapp
---
# NetApp Keystone — Design Standards

```bash
# Set a volume comment to identify application owner and Keystone tier
volume modify \
    -vserver svm_prod \
    -volume vol_oradb01_data \
    -comment "app=oradb01 owner=finance tier=extreme keystone=true"

# List volumes with their comments to verify tagging
volume show -fields vserver,volume,comment | grep keystone
```


```text title="Expected output"
vserver     volume              comment
-------     ------              -------
svm_prod    vol_oradb01_data    app=oradb01 owner=finance tier=extreme keystone=true
svm_prod    vol_oradb02_data    app=oradb02 owner=finance tier=premium keystone=true
svm_prod    vol_mysqldb_logs    app=mysqldb owner=ops tier=standard keystone=true
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: command failed: cannot modify volume vol_oradb01_data: volume is offline` | Bring the volume online with `volume online -vserver svm_prod -volume vol_oradb01_data` before modifying it. |
    | `Error: command failed: cannot modify volume vol_oradb01_data: insufficient privileges for user "admin"` | Ensure your user role has "volume_modify" capability or use an account with cluster admin privileges. |
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

```text title="Expected output"
event config modify -threshold-alerts-enabled true
(no output — command completes silently)

set advanced
(no output — command completes silently)

volume modify -vserver svm_prod -volume vol_oradb01_data -space-nearly-full-threshold-percent 80 -space-full-threshold-percent 95
(no output — command completes silently)

set admin
(no output — command completes silently)

Vserver         Volume                Space Nearly Full   Space Full
                                      Threshold Percent   Threshold Percent
--------------- --------------------- ------------------- -------------------
svm_prod        vol_oradb01_data      80                  95
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: command failed: There is no entry in the event config table.` | Run `event config create -threshold-alerts-enabled true` instead of modify if the event config does not yet exist. |
    | `Error: volume modify: invalid field "space-nearly-full-threshold-percent"` | Verify the exact field name with `volume modify -help` as the parameter name may differ by ONTAP version (e.g., use `nearly-full-threshold-percent` without "space-" prefix). |
    | `Error: This command can only be run in the advanced privilege level.` | Ensure you have executed `set advanced` before running the volume modify command, or use the full path `set -privilege advanced`. |
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

```d2
direction: down

network_controls: "Network Controls" {shape: rectangle}
os_hardening: "OS Hardening" {shape: rectangle}
application_security: "Application Security" {shape: rectangle}
audit_monitoring: "Audit & Monitoring" {shape: rectangle}

network_controls -> os_hardening: hardens
os_hardening -> application_security: hardens
application_security -> audit_monitoring: hardens
```
