---
tags:
  - operations
description: "Run this check weekly or after any significant workload addition."
---
# Capacity Review

<div class="kb-summary">
Run this check weekly or after any significant workload addition.

*Applies to: vSphere 7.x / 8.x*
</div>

Alert thresholds:
- > 75% used: review and plan expansion
- > 85% used: immediate action — thin provisioned disks may fail to inflate

```d2
direction: right

begin_checks: "Begin Checks" {shape: oval}
vsan_capacity: "vSAN Capacity" {shape: rectangle}
snapshot_growth: "Snapshot Growth" {shape: rectangle}
thin_provisioning_risk: "Thin Provisioning Risk" {shape: rectangle}
backup_repository_usage: "Backup Repository Usage" {shape: rectangle}
verify: "Verify" {shape: rectangle}
generate_report: "Generate Report" {shape: oval}

begin_checks -> vsan_capacity
vsan_capacity -> snapshot_growth
snapshot_growth -> thin_provisioning_risk
thin_provisioning_risk -> backup_repository_usage
backup_repository_usage -> verify
verify -> generate_report
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## vSAN Capacity

```bash
# On any cluster ESXi host
esxcli vsan storage capacity get
# Review: total capacity, used, free, and "slack" (reserved for rebuild)

# Via vCenter UI: vSAN cluster → Monitor → Capacity
# Check "Used Capacity" — keep below 70% to allow object rebuild headroom
```


```text title="Expected output"
Cluster UUID: 52d4a8f1-7c2e-41e2-9a3f-8b1d6e9c2f4a
Physical capacity: 12.34 TB
Capacity used: 8.12 TB (65.8%)
Capacity free: 4.22 TB (34.2%)
Slack space (reserved): 2.10 TB
Dedup and compression savings: 1.87 TB
```

!!! warning "Common errors"
    **`Error: Unable to connect to the vSAN cluster`** — Verify the ESXi host is part of an active vSAN cluster and network connectivity to cluster members is available.
    **`Error: vSAN service is not running`** — Enable vSAN on the cluster or restart the vSAN service with `systemctl restart vsanvpd` on the affected host.
vSAN capacity thresholds:
- > 60% used: plan capacity expansion
- > 70% used: critical — rebuild operations may fail if a disk fails

## Snapshot Growth

```powershell
# Find VMs with large or old snapshots
Get-VM | Get-Snapshot | Where-Object {$_.SizeMB -gt 10240 -or $_.Created -lt (Get-Date).AddDays(-7)} |
    Select-Object VM, Name, Created, SizeMB | Sort-Object SizeMB -Descending
```

Action: snapshots older than 7 days should be reviewed with the VM owner; snapshots > 50 GB should be removed if not actively in use.

## Thin Provisioning Risk

```powershell
# Compare provisioned vs. actual used space per datastore
Get-Datastore | Where-Object {$_.Type -eq "VMFS"} | ForEach-Object {
    $ds = $_
    $vms = Get-VM -Datastore $ds
    $provGB = ($vms | Get-HardDisk | Measure-Object -Property CapacityGB -Sum).Sum
    [PSCustomObject]@{
        Datastore = $ds.Name
        CapacityGB = [math]::Round($ds.CapacityGB, 1)
        ProvisionedGB = [math]::Round($provGB, 1)
        OvercommitRatio = [math]::Round($provGB / $ds.CapacityGB, 2)
    }
} | Sort-Object OvercommitRatio -Descending
```

Alert if overcommit ratio > 2.0 on a datastore approaching 70% usage.

## Backup Repository Usage

Check primary and SOBR capacity tier fill levels — alert operators when performance tier > 80% full:
- CommVault: Command Center → Storage → Disk Libraries
- Veeam: VBR console → Backup Infrastructure → Repositories
- NetBackup: OpsCenter → Reports → Storage Unit Utilization

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Alert Health Check](alert-review.md)
- [Daily Health Check](daily-health-check.md)
- [Management Access Check](management-access-check.md)
- [Virtualization Health Checks](index.md)
