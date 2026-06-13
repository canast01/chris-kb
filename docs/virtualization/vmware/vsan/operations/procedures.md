---
tags:
  - operations
  - vmware
  - vsan
  - vsphere-8
---
# vSAN — Procedures


<div class="kb-summary">
Operational how-to guides for day-to-day vSAN management. Each section covers a specific task area with concrete steps, commands, and validation.

*Applies to: vSAN 7.x / 8.x*
</div>

```text
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
```

## Before you begin

- **Access:** vCenter read-only minimum; Administrator role for remediation steps
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Disk Group Management

### Replace a Failed Capacity Disk

A capacity disk failure causes all components on that disk to go absent. vSAN waits for the `clomRepairDelay` timer (default 60 minutes) before triggering a rebuild on another host. Treat this as P1 if FTT=1 — one more failure before rebuild completes means data loss.

**Step 1 — Identify the failed disk**

```bash
esxcli vsan storage list | grep -E "naa\.|Health|State"
esxcli vsan debug object list | grep -v healthy
```

**Step 2 — Remove the disk from its disk group**

**From vCenter UI:**
Cluster → Configure → vSAN → Disk Management → select host → select failed disk → Remove Disk

```bash
esxcli vsan storage remove -d <failed_capacity_naa>
```

**Step 3 — Replace the physical disk**

Follow the vendor hardware replacement procedure (Dell iDRAC guided removal or HPE iLO). Do not power off the host — hot-swap where supported.

**Step 4 — Verify the new disk is visible to ESXi**

```bash
esxcli storage core device list | grep <new_naa>
```

**Step 5 — Add the new disk to the existing disk group**

**From vCenter UI:**
Cluster → Configure → vSAN → Disk Management → select host → Claim Disk → assign capacity role

```bash
esxcli vsan storage add -s <existing_cache_ssd_naa> -d <new_capacity_naa>
```

**Step 6 — Monitor resync to completion**

```bash
watch -n 30 "esxcli vsan debug resync summary get"
```

Do not remove any additional disks until `Active resyncing components = 0`. Expected duration: several hours for a multi-TB disk.

---

### Replace a Failed Cache SSD

A failed cache SSD takes the entire disk group offline. All components on all capacity disks in that group become absent simultaneously — this is higher risk than a single capacity disk failure.

**Step 1 — Identify the failed disk group**

```bash
esxcli vsan storage list | grep -E "Is SSD|Disk Group UUID|naa\."
esxcli vsan debug object list | grep -v healthy
```

**Step 2 — Remove the failed disk group**

Removing the cache SSD removes the entire group. vSAN will start rebuilding all affected components on other hosts once the group is removed.

**From vCenter UI:**
Cluster → Configure → vSAN → Disk Management → select host → select disk group → Remove Disk Group (use Migrate Data if other hosts have capacity)

```bash
esxcli vsan storage remove -s <failed_cache_ssd_naa>
```

**Step 3 — Replace the physical cache SSD**

Follow vendor hardware replacement procedure. Confirm the new SSD model is on the vSAN HCL.

**Step 4 — Verify the new SSD is visible**

```bash
esxcli storage core device list | grep <new_naa>
```

**Step 5 — Recreate the disk group**

**From vCenter UI:**
Cluster → Configure → vSAN → Disk Management → select host → Create Disk Group → assign cache and capacity roles

```bash
esxcli vsan storage add -s <new_cache_ssd_naa> -d <capacity_naa1> -d <capacity_naa2>
```

**Step 6 — Monitor resync to completion**

```bash
watch -n 30 "esxcli vsan debug resync summary get"
```

All objects that had components on this disk group must rebuild. Do not perform any other cluster maintenance until `Active resyncing components = 0`.

### Put a Host in Maintenance Mode

Always use vCenter, not the ESXi shell — vSAN health validation runs automatically before maintenance begins.

**Step 1 — Confirm cluster is healthy and resync is at zero**

```bash
esxcli vsan health cluster get
esxcli vsan debug resync summary get
```

Both must be clean. Entering maintenance during active resync significantly extends resync time.

**Step 2 — Enter maintenance mode**

**From vCenter UI:**
Right-click host → Maintenance Mode → Enter Maintenance Mode

Select the correct data migration option:

| Option | When to use |
|---|---|
| Full data migration | Hardware repair, OS reinstall, decommission. Moves all data off before maintenance. Requires free capacity on remaining hosts. |
| Ensure Accessibility | Short maintenance (driver update, reboot). Keeps one component accessible — faster but reduced protection during maintenance. |
| No data migration | Only for very short non-disruptive reboots on large clusters. Data unprotected during downtime. |

```powershell
$host = Get-VMHost esxi-01.example.com
Set-VMHost -VMHost $host -State Maintenance -VsanDataMigrationMode Full
```

**Step 3 — Confirm data migration is complete**

```bash
esxcli vsan debug resync summary get
# Active resyncing components must be 0 before starting work
```

**Step 4 — Exit maintenance mode after work is complete**

**From vCenter UI:**
Right-click host → Maintenance Mode → Exit Maintenance Mode

```powershell
Set-VMHost -VMHost $host -State Connected
```

Confirm the host rejoins the cluster:

```bash
esxcli vsan cluster get
watch -n 60 "esxcli vsan debug resync summary get"
```

---

## Storage Policies

### Create a Storage Policy

**Step 1 — Open the storage policy editor**

**From vCenter UI:**
vSphere Client → Menu → Policies and Profiles → VM Storage Policies → Create

**Step 2 — Configure rules**

Enter a policy name and description. Under Rules, add a vSAN rule set:
- `hostFailuresToTolerate`: FTT value (1 or 2)
- `replicaPreference`: RAID-1, RAID-5, or RAID-6
- `checksumDisabled`: false (keep enabled)

**Step 3 — Create via PowerCLI (alternative)**

```powershell
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

**Step 4 — Verify the policy was created**

```powershell
Get-SpbmStoragePolicy -Name "VSAN-T1-FTT2-RAID6" | Select Name, Description
```

**Standard policy set:**

| Policy Name | FTT | Method | Min Hosts | Use Case |
|---|---|---|---|---|
| `VSAN-T1-FTT2-RAID6` | 2 | RAID-6 | 6 | Tier-1 databases |
| `VSAN-T2-FTT1-RAID5` | 1 | RAID-5 | 4 | General workloads |
| `VSAN-DEV-FTT1-RAID1` | 1 | RAID-1 | 3 | Dev/Test |
| `VSAN-STRETCH-FTT1-SITE` | 1 per site | RAID-1 | 2+2+witness | Stretched cluster |

### Apply a Storage Policy to a VM

**Step 1 — Apply via vCenter UI**

**From vCenter UI:**
Right-click VM → VM Policies → Edit VM Storage Policies → select policy → Apply to all

**Step 2 — Apply to VM home directory (PowerCLI)**

```powershell
$vm = Get-VM "my-vm"
$policy = Get-SpbmStoragePolicy "VSAN-T1-FTT2-RAID6"
Set-SpbmEntityConfiguration -StoragePolicy $policy -Entity $vm
```

**Step 3 — Apply to each virtual disk (PowerCLI)**

```powershell
Get-HardDisk -VM $vm | Set-SpbmEntityConfiguration -StoragePolicy $policy
```

**Step 4 — Monitor resync after policy change**

Policy changes on running VMs trigger component rebuilds:

```bash
esxcli vsan debug resync summary get
```

Wait until `Active resyncing components = 0` before applying further changes.

### Check Policy Compliance

**Step 1 — Check all VMs (PowerCLI)**

```powershell
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" } |
    Select Entity, StoragePolicy, ComplianceStatus
```

**Step 2 — Check a specific VM**

```powershell
Get-SpbmEntityConfiguration -Entity (Get-VM "my-vm") |
    Select Entity, StoragePolicy, ComplianceStatus, ComplianceTaskStatus
```

**Step 3 — Check via vCenter UI**

**From vCenter UI:**
Cluster → Monitor → vSAN → Virtual Objects → filter by Non-compliant

Non-compliant objects mean the policy cannot be satisfied — typically due to insufficient hosts, disk group failures, or capacity pressure. See **Remediate Non-Compliant Objects** for resolution steps.

---

## Resync and Object Health

### Check Resync Status

**Step 1 — Summary view (bytes remaining and operation count)**

```bash
esxcli vsan debug resync summary get
```

**Step 2 — Detailed per-object view**

```bash
esxcli vsan debug resync list
```

**Step 3 — PowerCLI view**

```powershell
Get-VsanResyncStatus -Cluster (Get-Cluster "VSAN-LON-01")
```

**Step 4 — UI view**

**From vCenter UI:**
Cluster → Monitor → vSAN → Resyncing Objects

### Throttle Resync During Production Hours

**Step 1 — Check the current throttle setting**

```bash
esxcli vsan debug resync throttle get
```

0 = unlimited. Any positive value = IOPS cap per host.

**Step 2 — Apply throttle during business hours**

```bash
esxcli vsan debug resync throttle set --throttle 500
```

```powershell
Set-VsanResyncThrottle -Cluster (Get-Cluster "VSAN-LON-01") -IopsForResync 500
```

**Step 3 — Remove throttle during maintenance window**

```bash
esxcli vsan debug resync throttle set --throttle 0
```

### Adjust the Absent Component Timer

The default `clomRepairDelay` is 60 minutes — vSAN waits this long before starting a rebuild for absent components.

**Step 1 — View the current setting**

**From vCenter UI:**
Cluster → Configure → vSAN → Advanced Options → `clomRepairDelay`

**Step 2 — Adjust the value**

**From vCenter UI:**
Cluster → Configure → vSAN → Advanced Options → `clomRepairDelay` → Edit → enter minutes

Recommended values:
- Standard production: `60` minutes
- Frequent short maintenance (rolling reboots): `180` minutes
- Maximum: `240` minutes — do not exceed; objects stay unprotected too long

### Force a Policy Recalculation

If objects remain non-compliant after a cluster change (host added, disk replaced) and the cluster has sufficient capacity:

**Step 1 — Identify non-compliant objects**

```bash
esxcli vsan debug object list | grep -i non-compliant
```

```powershell
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" } |
    Select Entity, StoragePolicy, ComplianceStatus
```

**Step 2 — Re-apply the policy to trigger recalculation**

**From vCenter UI:**
Cluster → Monitor → vSAN → Virtual Objects → select non-compliant object → right-click → Reapply Storage Policy

```powershell
$vm = Get-VM "my-vm"
$policy = Get-SpbmStoragePolicy "VSAN-T1-FTT2-RAID6"
Get-HardDisk -VM $vm | Set-SpbmEntityConfiguration -StoragePolicy $policy
```

**Step 3 — Monitor resync**

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

Allow 15–30 minutes. If objects remain non-compliant, check capacity and host count against the FTT requirement.

---

## Capacity Management

### Check Current Capacity

**Step 1 — Per-host disk summary**

```bash
esxcli vsan storage list
```

**Step 2 — Cluster-level summary**

```bash
esxcli vsan cluster get
```

**Step 3 — Capacity with usage percentage (PowerCLI)**

```powershell
Get-VsanSpaceUsage -Cluster (Get-Cluster "VSAN-LON-01") |
    Select TotalCapacityGB, FreeCapacityGB, UsedCapacityGB,
           @{N='UsedPct';E={[Math]::Round($_.UsedCapacityGB/$_.TotalCapacityGB*100,1)}}
```

**Step 4 — UI view**

**From vCenter UI:**
Cluster → Monitor → vSAN → Capacity

Alert if `UsedPct` exceeds 70% — resync operations require 30% free headroom.

### Identify Large Snapshot Consumers

Snapshots are a common cause of unexpected capacity consumption. Each snapshot creates a delta disk that grows with every write.

**Step 1 — Find VMs with large snapshots**

```powershell
Get-VM | Get-Snapshot | Select VM, Name, SizeGB, Created |
    Sort-Object SizeGB -Descending | Format-Table -AutoSize
```

**Step 2 — Remove snapshots**

**From vCenter UI:**
Right-click VM → Snapshots → Delete All Snapshots

**Step 3 — Consolidate orphaned delta disks**

```powershell
Get-VM "my-vm" | % { $_.ExtensionData.ConsolidateVMDisks() }
```

**Step 4 — Verify capacity freed**

```powershell
Get-VsanSpaceUsage -Cluster (Get-Cluster "VSAN-LON-01") |
    Select TotalCapacityGB, FreeCapacityGB, UsedCapacityGB
```

### Add Capacity to an Existing Cluster

**Option A — Add a new host**

**Step 1 — Validate hardware against the vSAN HCL**

Confirm host model, NIC, SSD, and NVMe devices are on the [VMware Compatibility Guide](https://www.vmware.com/resources/compatibility) for the current ESXi version.

**Step 2 — Add host to vCenter and the cluster**

**From vCenter UI:**
Datacenter → Add Host → enter IP/hostname → root credentials → add to the vSAN cluster

```powershell
Add-VMHost -Name esxi-new.example.com -Location (Get-Cluster "VSAN-LON-01") `
    -User root -Password <password> -Force
```

**Step 3 — Claim disks**

**From vCenter UI:**
Cluster → Configure → vSAN → Disk Management → select new host → Claim Disks

**Step 4 — Monitor rebalance**

vSAN rebalances data automatically. To trigger manually:

```bash
esxcli vsan cluster rebalance start
```

**Option B — Add disks to an existing host**

**Step 1 — Add capacity disks to an existing disk group**

```bash
esxcli vsan storage add -s <existing_cache_ssd_naa> -d <new_capacity_naa>
```

**Step 2 — Verify the disk group**

```bash
esxcli vsan storage list | grep -A5 "Disk Group UUID"
```

---

## Stretched Cluster Operations

### Validate Stretched Cluster Health

**Step 1 — Check fault domain configuration**

```bash
esxcli vsan cluster get
```

```powershell
Get-VsanFaultDomainConfiguration -Cluster (Get-Cluster "VSAN-LON-01")
```

**Step 2 — Test witness host connectivity**

```bash
esxcli vsan debug network test
```

```bash
vmkping -I vmk2 <witness_vsan_vmk_ip>
```

**Step 3 — Verify in vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains

Both data sites and the witness site must show as connected. A partition between a data site and the witness causes that site's VMs to go read-only to prevent split-brain.

### Site Failover Test (Planned)

**Step 1 — Confirm cluster health before starting**

```bash
esxcli vsan health cluster get
esxcli vsan debug resync summary get
```

All objects healthy; zero active resync required.

**Step 2 — Isolate the test site**

**From vCenter UI:**
Put all hosts on the isolated site into Maintenance Mode → **Full data migration**

**Step 3 — Verify VMs migrate to the surviving site**

**From vCenter UI:**
Monitor → vSAN → Virtual Machines — confirm VMs are running on surviving site hosts

**Step 4 — Confirm witness is reachable from the surviving site**

```bash
vmkping -I vmk2 <witness_vsan_vmk_ip>
```

**Step 5 — Return isolated hosts from maintenance mode**

**From vCenter UI:**
Right-click isolated hosts → Maintenance Mode → Exit Maintenance Mode

**Step 6 — Monitor resync to completion**

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

**Never take both data sites offline simultaneously** — the witness cannot serve data and all VMs become inaccessible.

---

## Performance Service

### Enable vSAN Performance Service

**Step 1 — Enable via vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Performance Service → Enable

**Step 2 — Enable via PowerCLI (alternative)**

```powershell
$cluster = Get-Cluster "VSAN-LON-01"
$vsanConfig = Get-VsanClusterConfiguration -Cluster $cluster
Set-VsanClusterConfiguration -Configuration $vsanConfig -PerformanceServiceEnabled $true
```

**Step 3 — Verify the service is running**

```powershell
Get-VsanClusterConfiguration -Cluster (Get-Cluster "VSAN-LON-01") |
    Select PerformanceServiceEnabled
```

### View Performance Metrics

**From vCenter UI:**
Cluster → Monitor → vSAN → Performance → select a view (Cluster, Host, Disk Group, or VM)

Key metrics to monitor:

| Metric | Normal Range | Investigate If |
|---|---|---|
| Read latency | < 2 ms (all-flash) | > 10 ms sustained |
| Write latency | < 5 ms (all-flash) | > 20 ms sustained |
| Congestion | 0 | > 0 sustained |
| Throughput | Varies by workload | Consistently at NIC cap |
| Resync throughput | 0 (idle) | High for > 24h (blocked?) |

### Collect Performance Counters via CLI

**Per-VMDK performance stats:**

```bash
esxcli vsan debug vmdk list
```

**Disk-level stats — IOPS, latency, errors:**

```bash
esxcli vsan storage stats get
```

---

## vSAN Witness (2-Node and Stretched Clusters)

### Deploy Witness Appliance

**Step 1 — Download the OVA**

Download the vSAN Witness Appliance OVA from the Broadcom Customer Connect portal. Match the OVA version to the vSAN cluster version.

**Step 2 — Deploy the OVA**

**From vCenter UI:**
Actions → Deploy OVF Template → select the OVA → choose an ESXi host at the witness site → select the appropriate size

| Size | Max VMs | vCPU | vRAM |
|---|---|---|---|
| Tiny | 10 | 2 | 8 GB |
| Small | 500 | 2 | 16 GB |
| Medium | 15,000 | 4 | 32 GB |

**Step 3 — Configure network and identity**

Assign a management IP, DNS name, and gateway during OVA deployment. The witness must be reachable from both data sites on a dedicated vmkernel.

**Step 4 — Register the witness with vCenter**

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains → assign witness host → select the deployed witness appliance

**Step 5 — Validate witness connectivity**

```bash
vmkping -I vmk2 <witness_vsan_vmk_ip>
```

Witness RTT must be < 200 ms from both data sites.

### Validate Witness Connectivity

**Step 1 — Ping witness vmkernel from data site hosts**

```bash
vmkping -I vmk2 <witness_vsan_vmk_ip>
```

**Step 2 — Confirm witness appears in unicast agent list**

```bash
esxcli vsan network ipconfig list
```

The witness vmkernel IP must appear on both data site hosts.

**Step 3 — Check fault domain status in vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains — witness site must show as connected

Test during peak hours, not only in lab conditions.

### Replace a Failed Witness

**Step 1 — Deploy a new witness appliance**

Follow the Deploy Witness Appliance procedure above.

**Step 2 — Replace the witness in vCenter**

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains → Edit → select the witness site → replace the witness host with the new appliance

**Step 3 — Verify fault domain configuration**

```powershell
Get-VsanFaultDomainConfiguration -Cluster (Get-Cluster "VSAN-LON-01")
```

**Step 4 — Test connectivity from both data sites**

```bash
vmkping -I vmk2 <new_witness_vsan_vmk_ip>
```

**Step 5 — Verify cluster health**

```bash
esxcli vsan health cluster get
```

---

## On-Disk Format Upgrade

vSAN on-disk format (ODF) must be upgraded manually after upgrading ESXi hosts. New format versions unlock features and performance improvements but the upgrade is irreversible.

### Prerequisites

- All ESXi hosts in the cluster must be upgraded to the target ESXi version first.
- Cluster health must be green — no degraded or absent objects.
- Minimum 30% free capacity (the upgrade triggers a rolling resync).
- Take a snapshot or backup of critical VMs before starting.

### Check Current Format Version

**Step 1 — Check via CLI**

```bash
esxcli vsan cluster get | grep -i "disk format\|version"
```

**Step 2 — Check via vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → On-disk Format Upgrade — shows current version and the next available version

### Run the Upgrade

**Step 1 — Run the pre-check**

**From vCenter UI:**
Cluster → Configure → vSAN → On-disk Format Upgrade → Pre-check

The pre-check validates cluster health and capacity. Resolve all failures before proceeding.

**Step 2 — Check upgrade eligibility via PowerCLI (optional)**

```powershell
$cluster = Get-Cluster "VSAN-LON-01"
Get-VsanDiskFormatVersion -Cluster $cluster
```

**Step 3 — Start the upgrade**

**From vCenter UI:**
Cluster → Configure → vSAN → On-disk Format Upgrade → Upgrade

The upgrade runs host-by-host — each host's disk groups are upgraded one at a time while the cluster remains online.

### Monitor Progress

**Step 1 — Monitor resync during the upgrade**

Resync activity is expected — disk groups are being reformatted:

```bash
watch -n 30 "esxcli vsan debug resync summary get"
```

**Step 2 — Verify format version after completion**

```bash
esxcli vsan storage list | grep -i "format\|version"
```

All disk groups must report the new format version. Expected duration: 1–4 hours for a 6-node cluster. Do not perform other cluster changes during the upgrade.

---

## Add a New Host to the Cluster

Adding a host expands cluster capacity and can increase FTT headroom.

**Step 1 — Hardware Validation**

Before racking the host, verify it is on the vSAN Hardware Compatibility List (HCL):

- Check the [VMware Compatibility Guide](https://www.vmware.com/resources/compatibility) for the host model, NIC, HBA, SSD, and NVMe devices.
- Confirm disk model and firmware match HCL entries exactly — firmware version matters.
- Verify NIC speed (minimum 10 GbE; 25 GbE recommended).

**Step 2 — Install and Configure ESXi**

Install ESXi matching the cluster version (same build recommended). Configure management network, NTP, and DNS on first boot:

```bash
esxcli network ip interface ipv4 set -i vmk0 -I <mgmt_ip> -N <netmask> -t static
esxcli system hostname set --fqdn esxi-new.example.com
esxcli system ntp set --server ntp1.example.com --server ntp2.example.com
esxcli system ntp set --enabled true
```

**Step 3 — Add to vCenter and Cluster**

**From vCenter UI:**
Datacenter → Add Host → enter IP/hostname → provide root credentials → add to the vSAN cluster

```powershell
Add-VMHost -Name esxi-new.example.com -Location (Get-Cluster "VSAN-LON-01") `
    -User root -Password <password> -Force
```

**Step 4 — Configure vSAN VMkernel**

The new host needs a vSAN-tagged vmkernel before disk claim. Verify the tag:

```bash
esxcli network ip interface tag get -i vmk2
```

If the VSAN tag is missing, add it from vCenter:

**From vCenter UI:**
Host → Configure → Networking → VMkernel adapters → Edit → enable vSAN traffic

**Step 5 — Claim Disks**

**From vCenter UI:**
Cluster → Configure → vSAN → Disk Management → select new host → Claim Disks

Assign cache and capacity roles (OSA) or accept automatic assignment (ESA). Verify the disk group was created:

```bash
esxcli vsan storage list | grep -A5 "Disk Group UUID"
```

**Step 6 — Verify Rebalance and FTT Compliance**

Confirm the new host joined the cluster:

```bash
esxcli vsan cluster get
```

Monitor rebalance — vSAN redistributes data automatically; may take several hours:

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

Verify all objects are compliant after rebalance:

```powershell
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" } |
    Select Entity, StoragePolicy, ComplianceStatus
```

**From vCenter UI:**
Cluster → Monitor → vSAN → Virtual Objects — all should show "Compliant" within 24 hours.

---

## Permanently Decommission a Host

Decommissioning removes a host from the cluster and redistributes all its data. This is irreversible — plan capacity before starting.

### Prerequisites

- Verify remaining cluster meets FTT policy without this host (e.g., FTT=1 RAID-5 requires minimum 4 hosts — removing one from a 4-node cluster breaks compliance).
- Confirm free capacity on remaining hosts exceeds data volume being moved.
- Schedule during a maintenance window — full evacuation takes hours for large datasets.

**Step 1 — Full Data Evacuation**

**From vCenter UI:**
Right-click host → Maintenance Mode → Enter Maintenance Mode → **Full data migration**

```powershell
Set-VMHost -VMHost (Get-VMHost esxi-decom.example.com) `
    -State Maintenance -VsanDataMigrationMode Full
```

Monitor evacuation — do not proceed until resync is at zero:

```bash
watch -n 30 "esxcli vsan debug resync summary get"
```

**Step 2 — Remove Disk Groups**

**From vCenter UI:**
Cluster → Configure → vSAN → Disk Management → select host → Remove Disk Groups

```bash
esxcli vsan storage remove -s <cache_ssd_naa>
```

**Step 3 — Remove Host from Cluster**

**From vCenter UI:**
Right-click host → Remove from Inventory (or Move to another datacenter)

```powershell
Remove-VMHost -VMHost (Get-VMHost esxi-decom.example.com) -Confirm:$false
```

**Step 4 — Verify No Orphaned Objects**

```bash
esxcli vsan debug object list | grep -iv healthy
```

```powershell
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" }
```

Both commands should return no output.

---

## Deduplication and Compression

Deduplication and compression (dedup+compression) reduces capacity consumption but has strict requirements and performance trade-offs.

### Requirements and Restrictions

| Requirement | Detail |
|---|---|
| Architecture | OSA all-flash only (NVMe or SSD cache + SSD capacity). Not supported on hybrid (SSD cache + HDD capacity). |
| Scope | Cluster-wide — all hosts must have compatible hardware. Cannot enable on individual hosts. |
| Encryption | Mutually exclusive — you cannot have both dedup+compression and encryption at rest enabled simultaneously. |
| Space overhead | Enabling triggers a full cluster resync. Requires >30% free capacity. |
| Performance impact | Increases CPU load on all hosts. Test in dev/test before enabling in production. |

### Enable Deduplication and Compression

**Step 1 — Verify prerequisites**

Confirm all-flash OSA, encryption disabled, and > 30% free capacity:

```powershell
Get-VsanSpaceUsage -Cluster (Get-Cluster "VSAN-LON-01") |
    Select TotalCapacityGB, FreeCapacityGB
```

**Step 2 — Enable via vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Deduplication and Compression → Enable

**Step 3 — Enable via PowerCLI (alternative)**

```powershell
$cluster = Get-Cluster "VSAN-LON-01"
$vsanConfig = Get-VsanClusterConfiguration -Cluster $cluster
Set-VsanClusterConfiguration -Configuration $vsanConfig -SpaceEfficiencyEnabled $true
```

**Step 4 — Monitor the resync**

Data is rewritten in deduplicated form — expect hours of activity:

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

### Disable Deduplication and Compression

Disabling triggers a full cluster resync as data is rewritten without dedup.

**Step 1 — Disable via vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Deduplication and Compression → Disable

**Step 2 — Monitor the resync**

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

Allow 4–8 hours for resync to complete before performing any other cluster changes.

### Check Space Savings

**Step 1 — Check via vCenter UI**

**From vCenter UI:**
Cluster → Monitor → vSAN → Capacity — shows deduplicated and compressed savings ratio

**Step 2 — Check via PowerCLI**

```powershell
Get-VsanSpaceUsage -Cluster (Get-Cluster "VSAN-LON-01") |
    Select TotalCapacityGB, UsedCapacityGB, DeduplicationSavingsGB, CompressionSavingsGB
```

---

## Encryption at Rest

vSAN Data at Rest Encryption (D@RE) encrypts all data on vSAN capacity disks. It requires an external Key Management Server (KMS).

### Prerequisites

- External KMS configured and reachable from all cluster hosts (e.g., HyTrust KeyControl, Thales, HashiCorp Vault with KMIP).
- KMS registered in vCenter: vCenter → Administration → Key Providers → Add Standard Key Provider.
- All hosts must have TPM 2.0 or HW key caching supported.
- Encryption and dedup+compression are mutually exclusive — disable dedup+compression first if enabled.

### Register KMS in vCenter

**Step 1 — Add the KMS provider**

**From vCenter UI:**
vCenter → Administration → Key Providers → Add Standard Key Provider → enter KMS name, server IP, port → Establish Trust

**Step 2 — Verify KMS connectivity**

```powershell
Get-KeyManagementServer
```

All KMS nodes should show as connected. Confirm at least 2 KMS nodes for HA.

### Enable Encryption

**Step 1 — Confirm dedup+compression is disabled**

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Deduplication and Compression — must show Disabled

**Step 2 — Enable encryption**

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Data-at-Rest Encryption → Enable → select KMS cluster → Finish

vSAN performs a rolling disk group reformat — all data is re-encrypted. This triggers a full resync.

**Step 3 — Monitor encryption resync**

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

Expected duration: several hours. Do not add or remove hosts during encryption enablement.

### Rotate Encryption Keys

**Step 1 — Initiate key rotation via vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Data-at-Rest Encryption → Rekey

**Step 2 — Initiate via PowerCLI**

```powershell
Invoke-VsanEncryptionRekey -Cluster (Get-Cluster "VSAN-LON-01") -DeepRekey
```

`-DeepRekey` re-encrypts all data. Without it, only the DEK is rotated, not the KEK.

**Step 3 — Verify rekey completed**

```bash
esxcli vsan storage list | grep -i encrypt
```

### Verify Encryption Status

**Step 1 — Check disk group encryption state via CLI**

```bash
esxcli vsan storage list | grep -i encrypt
```

**Step 2 — Check via vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → Services → Data-at-Rest Encryption — shows enabled/disabled per host and KMS connection status

---

## Remediate Non-Compliant Objects

Non-compliant objects are vSAN objects that do not meet their assigned storage policy. Left unresolved, they represent under-protected VMs.

### Identify Non-Compliant Objects

**Step 1 — Check via CLI**

```bash
esxcli vsan debug object list | grep -i "non-compliant\|degraded\|absent"
```

**Step 2 — Full report with VM names (PowerCLI)**

```powershell
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" } |
    Select-Object Entity, StoragePolicy, ComplianceStatus |
    Sort-Object Entity
```

**Step 3 — Check via vCenter UI**

**From vCenter UI:**
Cluster → Monitor → vSAN → Virtual Objects → filter Non-compliant

### Diagnose the Cause

| Symptom | Likely Cause | Fix |
|---|---|---|
| Objects non-compliant after host failure | FTT policy cannot be met with current host count | Add host or lower FTT policy temporarily |
| Non-compliant after disk replacement | Resync still in progress | Wait — allow up to 24h for large datasets |
| Non-compliant with sufficient hosts | Capacity pressure (>70% used) | Free capacity or add storage |
| Non-compliant for specific VMs only | Incorrect or inapplicable policy assigned | Re-assign correct policy |
| Stale non-compliant (policy met, UI wrong) | vCenter cache stale | Re-apply policy to trigger recalculation |

### Force Re-evaluation

If the cluster has sufficient capacity and hosts but objects remain non-compliant:

**Step 1 — Re-apply policy via vCenter UI**

**From vCenter UI:**
Virtual Objects → select non-compliant object → right-click → Reapply Storage Policy

**Step 2 — Re-apply via PowerCLI**

```powershell
$vm = Get-VM "my-vm"
$policy = Get-SpbmStoragePolicy "VSAN-T1-FTT2-RAID6"
Get-HardDisk -VM $vm | Set-SpbmEntityConfiguration -StoragePolicy $policy
```

**Step 3 — Monitor resync**

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

### Bulk Remediation

**Step 1 — Re-apply policy to all non-compliant VMs**

```powershell
$noncompliant = Get-SpbmEntityConfiguration |
    Where-Object { $_.ComplianceStatus -ne "compliant" -and $_.Entity -is [VMware.VimAutomation.ViCore.Types.V1.Inventory.VirtualMachine] }

foreach ($item in $noncompliant) {
    $policy = $item.StoragePolicy
    Get-HardDisk -VM $item.Entity | Set-SpbmEntityConfiguration -StoragePolicy $policy
    Write-Host "Re-applied policy to: $($item.Entity.Name)"
}
```

**Step 2 — Monitor resync after bulk re-application**

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

Each re-apply may trigger component rebuilds. Allow 30–60 minutes per VM.

---

## Configure Fault Domains

Fault domains map ESXi hosts to physical boundaries (racks, PDUs) so vSAN places object components across domains, protecting against rack-level failures.

### When to Use Fault Domains

Use fault domains when your cluster spans multiple racks or power domains. Without fault domains, vSAN may place both copies of a RAID-1 object on hosts sharing the same rack or PDU — a single rack failure could cause data loss.

**Minimum requirement:** At least 3 fault domains for FTT=1; 5+ for FTT=2.

### Create Fault Domains

**Step 1 — Open fault domain configuration**

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains → Add Fault Domain

**Step 2 — Create domains and assign hosts**

**From vCenter UI:**
Add Fault Domain → name the domain (e.g., "Rack-A") → add hosts → repeat for each rack

```powershell
$cluster = Get-Cluster "VSAN-LON-01"
New-VsanFaultDomain -Name "Rack-A" -VMHost (Get-VMHost esxi-01, esxi-02) -Cluster $cluster
New-VsanFaultDomain -Name "Rack-B" -VMHost (Get-VMHost esxi-03, esxi-04) -Cluster $cluster
New-VsanFaultDomain -Name "Rack-C" -VMHost (Get-VMHost esxi-05, esxi-06) -Cluster $cluster
```

**Step 3 — Monitor rebalance**

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

### Verify Fault Domain Configuration

**Step 1 — List domains and member hosts**

```powershell
Get-VsanFaultDomainConfiguration -Cluster (Get-Cluster "VSAN-LON-01") |
    Select Name, @{N='Hosts';E={$_.Hosts.Name -join ', '}}
```

**Step 2 — Verify in vCenter UI**

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains — verify each host is in a named domain; no hosts should be in the "Default" (ungrouped) domain.

### Update Fault Domains After Hardware Changes

**Step 1 — Assign new host to the correct domain**

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains → drag host to correct domain

A host in the "Default" domain is treated as its own single-host fault domain and causes non-compliance warnings on FTT policies.

**Step 2 — Verify no hosts remain in the Default domain**

```powershell
Get-VsanFaultDomainConfiguration -Cluster (Get-Cluster "VSAN-LON-01") |
    Where-Object { $_.Name -eq "Default" } |
    Select Name, @{N='Hosts';E={$_.Hosts.Name -join ', '}}
# Expected: no output
```

---

## Pre-Upgrade Validation Routine

Run this routine before any ESXi host or vSphere upgrade. It confirms the cluster is healthy and has enough headroom to survive a rolling upgrade where one host at a time is taken offline.

### Step 1 — Cluster Health

```bash
# Run from any host in the cluster
esxcli vsan health cluster get

# All tests must pass. Investigate any failures before proceeding.
```

**From vCenter UI:**
Cluster → Monitor → vSAN → Skyline Health — resolve all errors and warnings before upgrading.

### Step 2 — Object Health

```bash
# Confirm no degraded, absent, or non-compliant objects
esxcli vsan debug object list | grep -iv healthy
# Expected: no output
```

```powershell
Get-SpbmEntityConfiguration | Where-Object { $_.ComplianceStatus -ne "compliant" }
# Expected: no output
```

### Step 3 — Capacity Headroom

```powershell
$usage = Get-VsanSpaceUsage -Cluster (Get-Cluster "VSAN-LON-01")
$pct = [Math]::Round($usage.UsedCapacityGB / $usage.TotalCapacityGB * 100, 1)
Write-Host "Used: $pct%"
# Must be below 60% — upgrade rebalance needs 30%+ headroom
```

### Step 4 — HCL Compliance

**From vCenter UI:**
Cluster → Monitor → vSAN → Skyline Health → Hardware Compatibility — all disks and NICs must show as HCL-compliant for the target ESXi version.

### Step 5 — Active Resync Check

```bash
esxcli vsan debug resync summary get
# Active resyncing components must be 0 before starting upgrade
```

### Step 6 — Snapshot Inventory

```powershell
# Find VMs with snapshots — consolidate before upgrade
Get-VM | Get-Snapshot | Select VM, Name, Created, SizeGB | Sort-Object SizeGB -Descending
# Consolidate all snapshots before starting — snapshots increase resync time
```

### Step 7 — Compatibility Check

Run the vSphere Lifecycle Manager (vLCM) pre-check or the upgrade compatibility checker:

**From vCenter UI:**
Cluster → Updates → Run Pre-check — reports any blockers for the target version.

**Pass criteria to proceed with upgrade:**
- All health checks green
- Zero degraded/non-compliant objects
- Capacity < 60% used
- Zero active resync
- All snapshots consolidated
- HCL compliant for target ESXi version

---

## Performance Investigation Workflow

Use this workflow when a VM reports slow storage performance. Work through each step in order — stop when you find the cause.

### Step 1 — Check vSAN Cluster Health

Rule out infrastructure-level issues first:

```bash
esxcli vsan health cluster get | grep -i fail
```

**From vCenter UI:**
Cluster → Monitor → vSAN → Skyline Health — any red/yellow items here can cause performance problems cluster-wide.

### Step 2 — Check for Active Resync

Resync consumes significant I/O bandwidth and raises latency for all VMs:

```bash
esxcli vsan debug resync summary get
# If high resync: throttle or wait for it to complete before investigating further
```

### Step 3 — Check Congestion

Congestion > 0 indicates the vSAN I/O stack is backed up:

```bash
# Congestion per disk group — should be 0
esxcli vsan debug disk list | grep -i congestion
```

**From vCenter UI:**
Cluster → Monitor → vSAN → Performance → Disk Group view → Congestion metric

### Step 4 — Check Front-End Latency for the VM

```bash
esxcli vsan debug vmdk list
# Look for the affected VM's VMDKs — note read/write latency (ms)
```

**From vCenter UI:**
Cluster → Monitor → vSAN → Performance → Virtual Machine view → select the affected VM

Alert thresholds:
- Read latency > 10 ms sustained → storage or network issue
- Write latency > 20 ms sustained → cache pressure, network, or congestion

### Step 5 — Check Cache Hit Rate (OSA Clusters)

For OSA (hybrid or all-flash with a separate cache tier), a low cache hit rate means reads are going to capacity disks:

```bash
# Cache write buffer utilisation (OSA) — high value indicates cache pressure
esxcli vsan debug disk list | grep -i "cache\|write buffer"
```

Cache write buffer > 95% sustained = cache SSD is a bottleneck. Consider adding capacity disks or a larger cache SSD.

### Step 6 — Identify Noisy Neighbours

If overall cluster health is good but one VM is slow, check if another VM is saturating the cluster:

```powershell
# Top 10 VMs by write IOPS (last 1 hour)
$cluster = Get-Cluster "VSAN-LON-01"
$end = Get-Date; $start = $end.AddHours(-1)

Get-VM -Location $cluster | ForEach-Object {
    $stats = Get-Stat -Entity $_ -Stat "disk.write.average" `
        -Start $start -Finish $end -IntervalMins 5 -ErrorAction SilentlyContinue
    if ($stats) {
        [PSCustomObject]@{
            VM = $_.Name
            AvgWriteKBps = [Math]::Round(($stats | Measure-Object -Property Value -Average).Average, 0)
        }
    }
} | Sort-Object AvgWriteKBps -Descending | Select -First 10
```

### Step 7 — Check vSAN Network

High network latency between hosts causes write latency (all writes go to at least 2 hosts):

```bash
# Test MTU and latency to all peers
PEERS="192.168.100.11 192.168.100.12 192.168.100.13"
for p in $PEERS; do
    echo -n "Peer $p RTT: "
    vmkping -I vmk2 -d -s 8972 $p -c 10 2>&1 | grep -E "loss|avg"
done

# Check for NIC errors
esxcli network nic stats get -n vmnic2 | grep -E "errors|drops"
```

### Step 8 — Check Physical Disk Health

Degraded disks cause latency spikes even before complete failure:

```bash
# SMART data for capacity disks on the host running the affected VM
esxcli storage core device smart get -d <naa>
# Any non-zero Reallocated Sectors or Pending Sectors = failing disk
```

### Decision tree summary

| Finding | Action |
|---|---|
| Health errors | Fix infrastructure issue first |
| Active resync | Throttle or wait; schedule investigation after resync |
| Congestion > 0 | Reduce IOPS load; check for runaway VMs |
| High front-end latency, low congestion | Disk or network issue — proceed to steps 5–8 |
| Low cache hit rate | Cache tier undersized; add capacity or upgrade cache SSD |
| One VM high IOPS | Apply storage policy IOPS limit to the noisy VM |
| Network errors | Fix NIC or switch; check MTU end-to-end |
| SMART errors | Replace disk proactively before failure |

---

## 2-Node ROBO Cluster

A 2-node vSAN cluster uses a witness appliance at a third site to form quorum. This design is for remote/branch offices (ROBO) with limited hardware budget.

### Architecture


- Each data node holds a full copy of all objects (effective RAID-1 across 2 nodes).
- The witness holds metadata only — no VM data. It provides quorum when one data node fails.
- If either data node fails, the surviving node + witness form a majority and VMs continue running.
- If the witness fails, both data nodes remain available but the cluster cannot tolerate a second failure.

### Prerequisites

- 2 ESXi hosts at the primary site (or across 2 sites).
- 1 vSAN witness appliance at a separate site or management network.
- Witness appliance reachable from both data nodes (RTT < 200 ms recommended).
- vSAN license that supports 2-node ROBO (check your licence tier).

### Enable 2-Node vSAN

**Step 1 — Create the cluster and enable vSAN**

**From vCenter UI:**
Create a new cluster with both ESXi hosts → Cluster → Configure → vSAN → Configuration → Enable vSAN → select **2-node cluster**

**Step 2 — Deploy and register the witness appliance**

Follow the **Deploy Witness Appliance** procedure above.

**Step 3 — Assign the witness host**

**From vCenter UI:**
Cluster → Configure → vSAN → Fault Domains → assign witness

**Step 4 — Claim disks on both data hosts**

**From vCenter UI:**
Cluster → Configure → vSAN → Disk Management → select each data host → Claim Disks

**Step 5 — Verify the cluster configuration**

```powershell
Get-VsanClusterConfiguration -Cluster (Get-Cluster "VSAN-ROBO-01") |
    Select StretchedClusterEnabled, WitnessHost
```

### Storage Policy for 2-Node

Do not use RAID-5 or RAID-6 — they require a minimum of 4 and 6 nodes respectively.

**Step 1 — Create the 2-node storage policy**

```powershell
New-SpbmStoragePolicy -Name "VSAN-ROBO-FTT1" `
    -Description "2-node ROBO: RAID-1 across both data nodes" `
    -AnyOfRuleSets @(
        New-SpbmRuleSet -AllOfRules @(
            New-SpbmRule -AnyOfCapabilities @(
                New-SpbmCapability -Name "VSAN.hostFailuresToTolerate" -Value 1
            )
        )
    )
```

**Step 2 — Apply the policy to all VMs**

```powershell
$policy = Get-SpbmStoragePolicy "VSAN-ROBO-FTT1"
Get-VM | ForEach-Object {
    Get-HardDisk -VM $_ | Set-SpbmEntityConfiguration -StoragePolicy $policy
}
```

### Validate the 2-Node Setup

**Step 1 — Confirm witness is a cluster member**

```bash
esxcli vsan cluster get
```

**Step 2 — Test witness connectivity from both data nodes**

```bash
vmkping -I vmk2 <witness_vsan_vmk_ip>
```

**Step 3 — Check 2-node-specific health checks**

**From vCenter UI:**
Cluster → Monitor → vSAN → Skyline Health → 2-Node cluster checks — all should be green.

### Simulate Failure (Test)

**Step 1 — Put one data node into maintenance mode**

Use **Ensure Accessibility** — not Full Migration (2-node has no third data node to migrate to).

**From vCenter UI:**
Right-click data node → Maintenance Mode → Enter Maintenance Mode → Ensure Accessibility

**Step 2 — Confirm VMs continue running on the surviving node**

**From vCenter UI:**
Monitor → vSAN → Virtual Machines — all VMs should remain running

**Step 3 — Confirm witness is reachable**

```bash
vmkping -I vmk2 <witness_vsan_vmk_ip>
```

**Step 4 — Exit maintenance mode and verify resync**

**From vCenter UI:**
Right-click the maintenance node → Maintenance Mode → Exit Maintenance Mode

```bash
watch -n 60 "esxcli vsan debug resync summary get"
```

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
