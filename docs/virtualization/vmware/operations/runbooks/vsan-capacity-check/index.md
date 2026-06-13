---
tags:
  - operations
  - vmware
  - vsan
  - vsphere-8
---
# vSAN Capacity Review Runbook

<div class="kb-summary">

| Field | Value |
|---|---|
| Risk | Low — read-only capacity audit; no changes made during the review step |
| Approval | No change required for the review; procurement request required if expansion is needed |
| Estimated time | 30–60 minutes for a full capacity review and forecast |
| Impact | None — review is non-disruptive |

*Applies to: vSAN 7.x / 8.x*
</div>

```text
┌──────────────────────────────── vSAN Capacity Review — Runbook ───────────────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  vSAN capacity review: assess current usage, growth trend, and forecast time-to-full                  │
│  Trigger: weekly scheduled review, or when a capacity alarm fires (>70% used)                         │
│  Output: capacity report with growth rate and recommended action (no action / order disks / add host) │
│                                                                                                       │
│  THRESHOLDS                                                                                           │
│  Green:  < 60% used — healthy; monitor                                                                │
│  Amber:  60–80% used — investigate growth rate; plan expansion within next quarter                    │
│  Red:    > 80% used — immediate expansion or workload migration required                              │
│                                                                                                       │
│  ACTION LADDER                                                                                        │
│  1. Reclaim wasted space: delete orphaned VMs, old snapshots, stale ISOs                              │
│  2. Enable deduplication/compression if not already active (requires all-flash cluster)               │
│  3. Add capacity disks to existing disk groups                                                        │
│  4. Add new hosts to the cluster                                                                      │
│                                                                                                       │
│  Key terms:                                                                                           │
│  Raw capacity     = total physical disk capacity contributed by all hosts                             │
│  Usable capacity  = raw capacity minus overhead for FTT, RAID, and vSAN metadata                      │
│  Slack space      = 30% of usable capacity reserved; vSAN requires slack to rebuild                   │
│  FTT              = Failures to Tolerate; FTT=1 halves usable capacity vs. raw                        │
│  Resync           = component rebuild after a failure; requires available slack space                 │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Run This Routine

1. **Check current capacity** — vCenter → Cluster → Monitor → vSAN → Capacity:
   - Note: Used, Free, and Reserved (slack) values
   - Note: Efficiency ratio if dedup/compression is enabled

2. **CLI capacity summary**:
   ```bash
   # SSH to any ESXi host in the cluster
   esxcli vsan storage list
   esxcli vsan cluster get
   python3 /usr/lib/vmware/vsan/bin/vsan-health-status.py -c
   ```

3. **Check disk group health** — confirm no disks are in a degraded state:
   ```bash
   esxcli vsan storage list | grep -E "^Disk|Status|Tier"
   ```
   All cache and capacity disks must show `Status: Normal`.

4. **Review object policy compliance** — vCenter → Cluster → Monitor → vSAN → Virtual Objects:
   - Objects showing "Non-compliant" or "Degraded" are consuming slack space for rebuilds

5. **Check for snapshots older than 72 hours**:
   ```powershell
   Connect-VIServer -Server vcenter.example.local
   Get-VM | Get-Snapshot | Where-Object { $_.Created -lt (Get-Date).AddDays(-3) } |
     Select VM, Name, Created, @{N="SizeGB";E={[math]::Round($_.SizeGB,1)}} |
     Sort-Object SizeGB -Descending
   ```
   Old snapshots are a common cause of unexpected capacity growth.

6. **Check for orphaned VMs** — vCenter → Storage → select vSAN datastore → Files tab → look for `.vmdk` files with no associated VM.

7. **Calculate growth rate** — compare this week's usage with last week (from Aria Operations or vCenter capacity history):
   ```text
   Growth rate example:
     Week 1: 12.4 TB used / 20 TB usable = 62%
     Week 2: 12.9 TB used / 20 TB usable = 64.5%
     Weekly growth: 0.5 TB/week → time-to-80%: (20×0.8 - 12.9) / 0.5 = ~9 weeks
   ```

8. **Record findings** and raise a procurement request if time-to-80% is less than 90 days.

---

## Expansion Options

### Option A — Add capacity disks to existing disk groups

Prerequisites: available NVMe/SSD slots in existing hosts; same disk model recommended.

```bash
# After physically installing the disk, claim it in vSAN
esxcli vsan storage add -s <device-id> -d <cache-device-id>
# or use vCenter: Cluster → Configure → vSAN → Disk Management → claim unclaimed disks
```

### Option B — Add a new host to the cluster

1. Follow the [ESXi Host Maintenance Mode Runbook](../esxi-host-maintenance/) for any pre-work on the new host.
2. Add host to cluster in vCenter: Cluster → Add Host.
3. vSAN auto-discovers the new host's disks; claim them via Disk Management.
4. Policy rebalance runs automatically; monitor object rebuild in vSAN Health.

---

## Capacity Alarms

Default vSAN capacity alarms (set in vCenter):
- `vSAN datastore disk usage` — triggers at 70% and 80%

Custom alarm via PowerCLI:
```powershell
# Create a custom alarm on the cluster for vSAN capacity > 75%
$alarmMgr = Get-View AlarmManager
$spec = New-Object VMware.Vim.AlarmSpec
$spec.Name = "vSAN Capacity > 75%"
$spec.Description = "Capacity review runbook trigger"
$spec.Enabled = $true
# ... (configure expression, action, and register alarm on cluster object)
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Capacity shows 100% but VMs are healthy | Resync consuming slack | Check Objects view — degraded objects cause resync; wait for resync to complete; do not add load |
| Dedup/compression ratio < 1.1× | Workload not compressible (databases, encrypted disks) | This is expected for some workloads; do not rely on efficiency for capacity planning |
| Capacity drops sharply after snapshot deletion | Snapshots were large | Normal; delta disks are freed on deletion; verify with `esxcli storage vmfs extent list` |
| New disks not claimed after adding to host | Disks not visible to vSAN | Check disk health in BIOS; verify disk is not in a foreign state: `esxcli vsan storage list` |

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier
