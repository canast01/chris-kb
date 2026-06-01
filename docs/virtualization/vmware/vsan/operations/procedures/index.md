# vSAN — Procedures

Operational how-to guides for day-to-day vSAN management. Each section covers a specific task area with concrete steps, commands, and validation.

```text
KEY PROCEDURE FLOWS

  DISK REPLACEMENT (capacity disk)          HOST MAINTENANCE MODE
  ─────────────────────────────────         ────────────────────────────────
  Alert: capacity disk failed               Decision: Full Migration vs
         │                                            Ensure Accessibility
         ▼                                           │
  esxcli vsan storage remove -d <naa>               ▼
         │                               Full Data Migration
         ▼                               ├── All components evacuated
  Replace physical disk                   │   before host goes offline
         │                               │   (safe, slow)
         ▼                               └── Ensure Accessibility
  esxcli vsan storage add                     ├── One copy per object
    -s <cache_naa> -d <new_naa>               │   kept accessible
         │                                   │   (faster, reduced protection)
         ▼                                   └── Use for short reboots only
  Monitor resync
  esxcli vsan debug resync summary get

  STORAGE POLICY CHANGE                     RESYNC THROTTLE
  ──────────────────────────────            ────────────────────────────────
  Old policy → New policy                   Business hours:
  applied to running VM                     esxcli vsan debug resync
         │                                    throttle set --throttle 500
         ▼                                           │
  CLOM detects non-compliance                        ▼
         │                               Maintenance window:
         ▼                               esxcli vsan debug resync
  Resync triggered automatically           throttle set --throttle 0
  (components rebuilt to new policy)
         │
         ▼
  Monitor until compliant
```
┌────────────────────────────────────── vSAN — Common Procedures ───────────────────────────────────────┐
│                                                                                                       │
│  vSAN operational procedures: disk replacement, host removal, policy update,                          │
│  rebalancing, decommission, and storage policy compliance remediation.                                │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │               Disk Replacement               │  │              Host Decommission              │   │
│   │            Mark disk failed in UI            │  │          Full data evacuation mode          │   │
│   │              Remove disk group               │  │           Wait for resync complete          │   │
│   │           Physically replace disk            │  │             Remove from cluster             │   │
│   │             Claim new disk in UI             │  │          Verify no degraded objects         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Always mark disk as failed before physical removal to trigger safe data migration.                   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌──────────────────────────────────────────────┐  ┌─────────────────────────────────────────────┐   │
│   │             Policy & Rebalancing             │  │             Capacity Management             │   │
│   │       Edit policy: Policies & Profiles       │  │           Check usage in Health UI          │   │
│   │          Apply policy to VM storage          │  │           Rebalance if imbalanced           │   │
│   │        Compliance: fix non-compliant         │  │           Add host: expand cluster          │   │
│   │           Re-apply: right-click VM           │  │          Decommission disk: gradual         │   │
│   └──────────────────────────────────────────────┘  └─────────────────────────────────────────────┘   │
│                                                                                                       │
│  Physical Infrastructure (the hardware everything above runs on):                                     │
│  All vSAN disk operations trigger resync; ensure >30% free space before starting;                     │
│  replacements must use HCL-approved disk models.                                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│                                                                                                       │
│  Mark failed    = UI action; moves data off disk before physical removal                              │
│  Full evacuation= moves all data off host before decommission                                         │
│  Resync         = rebuild missing components after disk/host change                                   │
│  Policy compliance= VM storage matches defined FTT/RAID policy                                        │
│  Non-compliant  = policy not met; often after host failure or disk loss                               │
│  Rebalance      = redistribute objects across hosts for even utilisation                              │
│  Policies & Profiles= VC area for defining storage policies                                           │
│  Re-apply policy= recalculate placement to restore compliance                                         │
│  Decommission disk= graceful removal with data migration                                              │
│  Claim disk     = assign new physical disk to vSAN cache/capacity role                                │
│  Disk group     = one cache + up to 7 capacity disks per ESXi host                                    │
│  30% free       = minimum headroom for resync operations                                              │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

## Add a Disk Group to an Existing Host

Adding a disk group increases per-host storage capacity and I/O parallelism.

**Prerequisites:**
- Physical disks are installed and visible to the ESXi host.
- Disks are on the vSAN HCL for the installed ESXi version.
- No active resync in progress on the cluster.

```bash
# 1. Identify unclaimed disks on the host
esxcli storage core device list | grep -v "Is Local SAS Disk"
esxcli vsan storage list          # compare — unclaimed disks won't appear here

# 2. Identify device NAA IDs for new disks
esxcli storage core device list | grep -E "Display Name|naa\."

# 3. Create the disk group (cache SSD + one or more capacity disks)
esxcli vsan storage add -s <cache_ssd_naa> -d <capacity_naa1> -d <capacity_naa2>

# 4. Verify the disk group was created
esxcli vsan storage list

# 5. Check health — new disk group should appear healthy
esxcli vsan health cluster list
```

**From vCenter UI:**
vSphere Client → Cluster → Configure → vSAN → Disk Management → Claim Disks

### Replace a Failed Capacity Disk

A capacity disk failure causes components on that disk to go absent. vSAN waits for the `clomRepairDelay` timer (default 60 minutes) before rebuilding.

```bash
# 1. Identify the failed disk
esxcli vsan storage list | grep -E "naa\.|Health|State"

# 2. Check which objects are degraded
esxcli vsan debug object list | grep -v healthy

# 3. Remove the failed capacity disk from its disk group
esxcli vsan storage remove -d <failed_capacity_naa>

# 4. Physically replace the disk in the server chassis
# (Follow vendor hardware replacement procedure)

# 5. Verify the new disk is visible
esxcli storage core device list

# 6. Add the new disk to the existing disk group
esxcli vsan storage add -s <existing_cache_ssd_naa> -d <new_capacity_naa>

# 7. Monitor resync — data rebuilds onto the new disk
esxcli vsan debug resync summary get
```

Expected resync time: several hours for a multi-TB disk. Monitor throughput and do not remove additional disks during the rebuild.

### Replace a Failed Cache SSD

A failed cache SSD takes the entire disk group offline. All components on all capacity disks in that group become absent simultaneously.

```bash
# 1. Identify the failed disk group and cache SSD
esxcli vsan storage list | grep -E "Is SSD|Disk Group UUID|naa\."

# 2. Remove the failed disk group (removing the cache SSD removes the whole group)
esxcli vsan storage remove -s <failed_cache_ssd_naa>

# 3. Physically replace the cache SSD

# 4. Verify the new SSD is visible
esxcli storage core device list

# 5. Recreate the disk group with the new cache SSD and the existing capacity disks
esxcli vsan storage add -s <new_cache_ssd_naa> -d <capacity_naa1> -d <capacity_naa2>

# 6. Monitor resync — all objects that were on this disk group rebuild
esxcli vsan debug resync summary get
watch -n 30 "esxcli vsan debug resync summary get"
```

**Note:** Cache SSD failure on a single-disk-group host puts all data on that host at risk. With FTT=1, all affected objects are degraded (one component is absent). No data loss occurs unless a second failure happens before rebuild completes. Treat cache SSD replacement as a P1 task.

### Put a Host in Maintenance Mode

Always put vSAN hosts into maintenance mode through vCenter, not via the ESXi shell, so vSAN health validation runs automatically.

**From vCenter UI:**
Right-click host → Maintenance Mode → Enter Maintenance Mode

**Select the correct data migration option:**

| Option | When to use |
|---|---|
| Full data migration | Hardware repair, OS reinstall, decommission. Moves all data off the host before maintenance begins. Requires sufficient capacity on remaining hosts. |
| Ensure Accessibility | Short maintenance (driver update, reboot). Keeps one component accessible — faster but leaves the cluster at reduced protection during maintenance. |
| No data migration | Not recommended except for very short, non-disruptive reboots on large clusters. Data remains unprotected during downtime. |

```powershell
# PowerCLI — enter maintenance mode with full data migration
$host = Get-VMHost esxi-01.example.com
Set-VMHost -VMHost $host -State Maintenance -VsanDataMigrationMode Full
```

**Verify maintenance mode entry completes successfully:**

```bash
# From any other host in the cluster
esxcli vsan debug resync summary get
# All resync must complete before performing any further changes
```

**Exit maintenance mode after work is complete:**

```powershell
Set-VMHost -VMHost $host -State Connected
```

---

## Storage Policies

### Create a Storage Policy

Storage policies are created in vCenter and applied to VMs at provisioning time or changed on running VMs.

**From vCenter UI:**
vSphere Client → Menu → Policies and Profiles → VM Storage Policies → Create

```powershell
# PowerCLI — create a Tier-1 FTT=2 RAID-6 policy
Connect-VIServer <vcenter>

New-SpbmStoragePolicy -Name "VSAN-T1-FTT2-RAID6" `
    -Description "Tier-1 databases: FTT=2 RAID-6 (6+ node cluster)" `
    -AnyOfRuleSets @(
        New-SpbmRuleSet -AllOfRules @(
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.hostFailuresToTolerate" -Value 2
            ),
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.replicaPreference" -Value "RAID-6"
            ),
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.checksumDisabled" -Value $false
            )
        )
    )
```

**Standard policy set:**

| Policy Name | FTT | Method | Min Hosts | Use Case |
|---|---|---|---|---|
| `VSAN-T1-FTT2-RAID6` | 2 | RAID-6 | 6 | Tier-1 databases |
| `VSAN-T2-FTT1-RAID5` | 1 | RAID-5 | 4 | General workloads |
| `VSAN-DEV-FTT1-RAID1` | 1 | RAID-1 | 3 | Dev/Test |
| `VSAN-STRETCH-FTT1-SITE` | 1 per site | RAID-1 | 2+2+witness | Stretched cluster |

### Apply a Storage Policy to a VM

```powershell
# Apply policy to all disks of a VM
$vm = Get-VM "my-vm"
$policy = Get-SpbmStoragePolicy "VSAN-T1-FTT2-RAID6"

# Apply to VM home directory
Set-SpbmEntityConfiguration -StoragePolicy $policy -Entity $vm

# Apply to each virtual disk
Get-HardDisk -VM $vm | Set-SpbmEntityConfiguration -StoragePolicy $policy
```

Policy changes on running VMs trigger a resync — existing object components are rebuilt to meet the new policy. Monitor resync after applying policy changes:

```bash
esxcli vsan debug resync summary get
```

### Check Policy Compliance

```powershell
# Check compliance for all VMs
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" } |
    Select Entity, StoragePolicy, ComplianceStatus

# Check compliance for a specific VM
Get-SpbmEntityConfiguration -Entity (Get-VM "my-vm") |
    Select Entity, StoragePolicy, ComplianceStatus, ComplianceTaskStatus
```

**From vCenter UI:**
Cluster → Monitor → vSAN → Virtual Objects → filter by Non-compliant

Non-compliant objects mean the current storage policy cannot be satisfied — typically due to insufficient hosts, disk group failures, or capacity pressure.

---

## Resync and Object Health

### Check Resync Status

```bash
# Summary — bytes remaining and operation count
esxcli vsan debug resync summary get

# Detailed list — per-object resync operations
esxcli vsan debug resync list
```

```powershell
# PowerCLI resync status
Get-VsanResyncStatus -Cluster (Get-Cluster "VSAN-LON-01")
```

**From vCenter UI:**
Cluster → Monitor → vSAN → Resyncing Objects

### Throttle Resync During Production Hours

```bash
# Check current throttle (0 = unlimited)
esxcli vsan debug resync throttle get

# Limit resync to 500 IOPS per host during business hours
esxcli vsan debug resync throttle set --throttle 500

# Remove throttle during maintenance window (unlimited)
esxcli vsan debug resync throttle set --throttle 0
```

```powershell
# PowerCLI throttle management
Set-VsanResyncThrottle -Cluster (Get-Cluster "VSAN-LON-01") -IopsForResync 500
```

### Adjust the Absent Component Timer

The default timer is 60 minutes — vSAN waits this long before starting a rebuild on absent components. Increasing this value reduces unnecessary rebuilds during short maintenance.

**From vCenter UI:**
Cluster → Configure → vSAN → Advanced Options → `clomRepairDelay`

Recommended values:
- Standard production: `60` minutes
- Frequent short maintenance (rolling reboots): `180` minutes
- Never increase above 240 minutes — leaves data unprotected for too long

### Force a Policy Recalculation

If objects are non-compliant after a cluster change (host added, disk replaced):

```bash
# From any ESXi host — trigger CLOM rescan
esxcli vsan debug object list | grep non-compliant
# Non-compliant objects resync automatically — allow 15-30 minutes
# If no progress, check capacity and policy eligibility
```

---

## Capacity Management

### Check Current Capacity

```bash
# Per-host disk summary
esxcli vsan storage list

# Cluster-level summary
esxcli vsan cluster get
```

```powershell
# Capacity overview per cluster
Get-VsanSpaceUsage -Cluster (Get-Cluster "VSAN-LON-01") |
    Select TotalCapacityGB, FreeCapacityGB, UsedCapacityGB,
           @{N='UsedPct';E={[Math]::Round($_.UsedCapacityGB/$_.TotalCapacityGB*100,1)}}
```

**From vCenter UI:**
Cluster → Monitor → vSAN → Capacity

### Identify Large Snapshot Consumers

Snapshots are a common cause of unexpected capacity consumption on vSAN. Each snapshot creates a delta disk that grows with every write.

```powershell
# Find VMs with snapshots sorted by snapshot size
Get-VM | Get-Snapshot | Select VM, Name, SizeGB, Created |
    Sort-Object SizeGB -Descending | Format-Table -AutoSize
```

**Remove orphaned snapshots:**

```powershell
# Consolidate a VM (removes orphaned delta disks)
Get-VM "my-vm" | % { $_.ExtensionData.ConsolidateVMDisks() }
```

### Add Capacity to an Existing Cluster

**Add a new host to the cluster:**

1. Ensure new host meets hardware requirements and is on the vSAN HCL.
2. Add host to vCenter and the vSAN cluster.
3. Claim disks for vSAN via Cluster → Configure → vSAN → Disk Management.
4. vSAN automatically rebalances data across the new host over time.

```bash
# Trigger manual rebalance (optional — vSAN rebalances automatically over time)
esxcli vsan cluster rebalance start
```

**Add disks to an existing host:**

```bash
# Add capacity disks to an existing disk group
esxcli vsan storage add -s <existing_cache_ssd_naa> -d <new_capacity_naa>
```

---

## Stretched Cluster Operations

### Validate Stretched Cluster Health

```bash
# Check fault domain configuration
esxcli vsan cluster get

# Verify witness host connectivity
esxcli vsan debug network test
```

```powershell
# PowerCLI — fault domain and witness status
Get-VsanFaultDomainConfiguration -Cluster (Get-Cluster "VSAN-LON-01")
```

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains

Both data sites and the witness site must show as connected. A partition between a data site and the witness will cause that data site's VMs to become read-only to prevent split-brain.

### Site Failover Test (Planned)

**Planned failover procedure (test or maintenance):**

1. Confirm cluster health — all objects healthy, no active resync.
2. Isolate Site A (or Site B) by taking those hosts into maintenance mode with Full Data Migration.
3. Verify VMs on the isolated site migrate to the surviving site.
4. Confirm witness is reachable from the surviving site.
5. Verify VM access on the surviving site is uninterrupted.
6. Return isolated hosts from maintenance mode and confirm resync.

**Never take both data sites offline simultaneously** — the witness cannot serve data and all VMs become inaccessible.

---

## Performance Service

### Enable vSAN Performance Service

The Performance Service must be enabled to collect per-VM and per-disk-group metrics visible in the vSphere Client performance charts.

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Performance Service → Enable

```powershell
# Enable via PowerCLI
$cluster = Get-Cluster "VSAN-LON-01"
$vsanConfig = Get-VsanClusterConfiguration -Cluster $cluster
Set-VsanClusterConfiguration -Configuration $vsanConfig -PerformanceServiceEnabled $true
```

### View Performance Metrics

**From vCenter UI:**
Cluster → Monitor → vSAN → Performance → select a view (Cluster, Host, Disk Group, or VM)

Key metrics to review:

| Metric | Normal Range | Investigate If |
|---|---|---|
| Read latency | < 2 ms (all-flash) | > 10 ms sustained |
| Write latency | < 5 ms (all-flash) | > 20 ms sustained |
| Congestion | 0 | > 0 sustained |
| Throughput | Varies by workload | Consistently at NIC cap |
| Resync throughput | 0 (idle) | High for > 24h (blocked?) |

### Collect Performance Counters via CLI

```bash
# vSAN performance stats from ESXi host
esxcli vsan debug vmdk list

# Disk-level stats (IOPS, latency, errors)
esxcli vsan storage stats get
```

---

## vSAN Witness (2-Node and Stretched Clusters)

### Deploy Witness Appliance

1. Download the vSAN Witness Appliance OVA from the Broadcom portal.
2. Deploy to a separate ESXi host at the witness site (vSphere Client → Actions → Deploy OVF Template).
3. Select the appropriate appliance size (Tiny/Small/Medium) based on VM count.
4. Assign a management IP and DNS name.
5. Register the witness with the vCenter managing the 2-node or stretched cluster.

**Witness appliance sizing:**

| Size | Max VMs | vCPU | vRAM |
|---|---|---|---|
| Tiny | 10 | 2 | 8 GB |
| Small | 500 | 2 | 16 GB |
| Medium | 15,000 | 4 | 32 GB |

### Validate Witness Connectivity

```bash
# From a data site host — ping witness vmkernel IP
vmkping -I vmk2 <witness_vsan_vmk_ip>

# Check unicast agent list — witness should appear
esxcli vsan network ipconfig list
```

Witness RTT must be < 200 ms from both data sites. Test during peak hours, not only during lab conditions.

### Replace a Failed Witness

1. Deploy a new witness appliance.
2. In vCenter: Cluster → Configure → vSAN → Fault Domains → Edit.
3. Select the witness site and replace the witness host with the new appliance.
4. Verify fault domain configuration is valid.
5. Test connectivity from both data sites.
