# Capacity Review


<div class="kb-summary">
Run this check weekly or after any significant workload addition.
</div>

```text
Capacity Check Flow
═══════════════════════════════════════════════════════════

  ┌─────────────────────────────────────────────────────┐
  │                  CPU Headroom                       │
  │  Cluster avg < 70% → OK   ≥ 70% → investigate      │
  └──────────────────────────┬──────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────┐
  │                 RAM Headroom                        │
  │  Balloon = 0    → OK   Balloon > 0 → action now    │
  │  Swap = 0       → OK   Swap > 0   → immediate P1   │
  └──────────────────────────┬──────────────────────────┘
                             │
                             ▼
  ┌────────────────────────────────────────────────────┐
  │              Datastore Capacity                    │
  │  < 70% used → OK                                   │
  │  70–80% used → plan expansion (2 weeks)            │
  │  > 80% used  → alert: schedule immediate action    │
  │  > 90% used  → critical: no new VMs until resolved │
  └──────────────────────────┬─────────────────────────┘
                             │
                             ▼
  ┌─────────────────────────────────────────────────────┐
  │                  vSAN Capacity                      │
  │  < 60% used → OK                                   │
  │  60–70% used → plan capacity expansion             │
  │  > 70% used  → critical: rebuild may fail if disk  │
  │                fails — expand immediately           │
  └─────────────────────────────────────────────────────┘
```
┌─────────────────────────────── Capacity Review — Weekly Resource Check ───────────────────────────────┐
│                                                                                                       │
│    Run weekly and after any significant workload addition; forecast 90 days ahead                     │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │     Resource     │      Green       │   Amber — action  │  Red — escalate  │    Frequency     │   │
│   │  ──────────────  │  ──────────────  │  ───────────────  │  ──────────────  │  ──────────────  │   │
│   │   CPU cluster    │    < 70% avg     │   70-85% → plan   │  85%+ → P1 now   │  Daily + weekly  │   │
│   │   RAM balloon    │    0 balloon     │  Any → investig.  │  > 0 swap → P1   │      Daily       │   │
│   │    Datastore     │    < 75% used    │   75-85% → free   │  85%+ → expand   │      Daily       │   │
│   │  vSAN capacity   │    < 70% used    │   70-80% → plan   │  80%+ → P1 now   │      Weekly      │   │
│   │    Licensing     │   All covered    │   Expiry < 60 d   │  Expiry < 30 d   │     Monthly      │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Balloon    = Memory reclaim driver inflates inside the VM; signals host memory pressure            │
│    Swap       = Host swaps VM memory to disk; severe performance impact; treat as P1                  │
│    Headroom   = Spare capacity after HA failover reservation is accounted for                         │
│    Thin prov. = Allocating more virtual disk than physical; monitor actual used, not alloc            │
│    Forecast   = Project current growth rate 90 days; order hardware before hitting amber              │
│    vSAN slack = vSAN requires ~25% free space for rebuild operations; do not fill beyond 70%          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘

Thresholds:
- CPU > 70% average across cluster → investigate workload distribution
- Memory balloon/swap > 0 on any host → immediate action required

## Datastore Free Space

```powershell
Get-Datastore | Select-Object Name, FreeSpaceGB, CapacityGB, @{
    N="Used%"; E={[math]::Round((1-($_.FreeSpaceGB/$_.CapacityGB))*100,1)}
} | Sort-Object "Used%" -Descending | Format-Table -AutoSize
```

Alert thresholds:
- > 75% used: review and plan expansion
- > 85% used: immediate action — thin provisioned disks may fail to inflate

## vSAN Capacity

```bash
# On any cluster ESXi host
esxcli vsan storage capacity get
# Review: total capacity, used, free, and "slack" (reserved for rebuild)

# Via vCenter UI: vSAN cluster → Monitor → Capacity
# Check "Used Capacity" — keep below 70% to allow object rebuild headroom
```

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
