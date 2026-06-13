---
tags:
  - scenarios
  - vmware
---
# HA Admission Control Breach / Failover Storm

<div class="kb-summary">
Multiple hosts fail simultaneously or in rapid succession, exhausting vSphere HA's reserved failover
capacity. VMs cannot be restarted because no surviving host has sufficient CPU and memory headroom. Aria
Ops fires cascading alerts as powered-off VMs pile up. This scenario covers confirming the admission
control breach, making hard decisions about which VMs to restart first, temporarily adjusting HA policy
to allow restarts, recovering the cluster, and preventing a recurrence through proper headroom design.
</div>

```text
┌───────────────────────────── HA Admission Control Breach — Response Flow ─────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  Multiple hosts fail simultaneously, exhausting HA reserved failover capacity                         │
│  VMs cannot restart because no surviving host has sufficient CPU and memory headroom                  │
│                                                                                                       │
│  START: Multiple VMs powered off · HA restart status "Insufficient resources" · Cluster red           │
│                                                                                                       │
│  STEP 1 — Assess the Situation                                                                        │
│  How many hosts are down and are they recoverable?                                                    │
│  Remaining capacity vs total VM demand (CPU + RAM)                                                    │
│  Which VMs are priority 1 / critical vs non-critical?                                                 │
│                                                                                                       │
│  STEP 2 — Resolution Options                                                                          │
│  Option A: Restore a failed host → capacity recovers, HA restarts pending VMs                         │
│  Option B: Temporarily lower HA slot reservation policy to allow immediate restarts                   │
│  Option C: Add an emergency host to the cluster to increase available capacity                        │
│                                                                                                       │
│  STEP 3 — Close                                                                                       │
│  All priority VMs running · cluster capacity ≥ N+1 · admission control policy corrected               │
│  Review HA policy sizing to prevent recurrence (minimum N+1 reserve for expected failures)            │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | HA restart status; admission control configuration; cluster resource view |
| ESXi | Surviving hosts; CPU/memory headroom; host hardware recovery |
| vSphere HA | Failover orchestration; restart priority; admission control enforcement |
| Aria Operations | Alert storm; resource exhaustion dashboards; per-VM priority tagging |
| VxRail Manager | Node recovery status on HCI clusters; OMIVV hardware event correlation |

---

## 1. Confirm the Breach — How Many Hosts Failed and What Remains

Go to **vCenter → Cluster → Monitor → vSphere HA** to see the current state of HA and which VMs could not be restarted.

```text
Cluster → Monitor → vSphere HA → Summary
  Protected VMs         — VMs monitored by HA and eligible for restart
  Unprotected VMs       — VMs with HA restart priority = Disabled
  Current failover capacity (%) — how much capacity HA currently has available
  Configured failover capacity (%) — your admission control reservation

If Current < Configured: breach is active. HA is blocking or deferring restarts.
```

Navigate to **Cluster → Monitor → vSphere HA → VM Restarts** and filter by Status = "Insufficient resources" — this lists every VM HA tried to restart but could not place.

```powershell
# Get the HA cluster status including admission control state
$cluster = Get-Cluster "cluster-name"
$das = $cluster.ExtensionData.Configuration.DasConfig
Write-Host "HA Enabled: $($das.Enabled)"
Write-Host "Admission Control Enabled: $($das.AdmissionControlEnabled)"

# List VMs that HA attempted but could not place
$cluster | Get-VMHost | Get-VM `
  | Where-Object { $_.PowerState -eq "PoweredOff" } `
  | Select-Object Name, VMHost, NumCpu, MemoryGB `
  | Sort-Object MemoryGB -Descending
```

---

## 2. Triage — Which VMs Are Critical

Before touching HA policy or attempting manual placement, triage the powered-off VM list into priority tiers. Trying to restart everything at once when resources are constrained will cause all restarts to fail.

```text
Priority tier framework:
  Tier 1 — Production-impacting: databases, ERP, identity services, monitoring infrastructure
  Tier 2 — Business-impacting: email, file servers, internal tools
  Tier 3 — Non-critical: test, dev, batch, analytics

HA restart priority levels (configured per VM):
  High        → HA restarts these first
  Medium      → second priority
  Low         → third priority
  Disabled    → HA never restarts; manual action required
  Cluster default → inherits cluster default restart priority setting
```

```powershell
# List all powered-off VMs with their HA restart priority
Get-Cluster "cluster-name" | Get-VM `
  | Where-Object { $_.PowerState -eq "PoweredOff" } `
  | Get-VMRestartPriority `
  | Select-Object VM, RestartPriority `
  | Sort-Object RestartPriority
```

Look for: VMs with `RestartPriority = Disabled` will never be automatically restarted — these require manual intervention regardless of available capacity.

---

## 3. Assess Remaining Cluster Resources

Calculate whether the surviving hosts can physically accommodate Tier 1 VMs even if admission control is temporarily relaxed.

Navigate to **Cluster → Monitor → Utilisation** to view CPU and memory usage per host in real time.

```powershell
# Get per-host CPU and memory stats
Get-Cluster "cluster-name" | Get-VMHost | Select-Object Name, `
  @{N="CPU GHz Free";E={ [math]::Round(($_.CpuTotalMhz - $_.CpuUsageMhz)/1000, 1) }}, `
  @{N="RAM GB Free";E={ [math]::Round($_.MemoryTotalGB - $_.MemoryUsageGB, 1) }}, `
  ConnectionState `
  | Sort-Object "RAM GB Free" -Descending

# Sum the CPU and RAM requirements of all powered-off priority VMs
Get-Cluster "cluster-name" | Get-VM `
  | Where-Object { $_.PowerState -eq "PoweredOff" } `
  | Measure-Object -Property NumCpu, MemoryGB -Sum `
  | Select-Object Property, Sum
```

```text
Decision framework:
  Free RAM on surviving hosts > Sum of Tier 1 VM RAM  → restart Tier 1 first; assess Tier 2 after
  Free RAM barely covers Tier 1                       → restart Tier 1 only; hold Tier 2 until host recovered
  Free RAM insufficient even for Tier 1               → emergency: need a host back or an emergency add
```

---

## 4. Option A — Recover a Failed Host (Best Path)

If the failed hosts are recoverable (power failure, management network loss, transient hardware error), restoring even one host is the fastest path to resolution because it restores both capacity and HA re-arms admission control.

```bash
# Check iDRAC/iLO status of failed hosts
# For Dell VxRail hosts — check iDRAC chassis event log
racadm getsel | tail -30

# For standalone ESXi hosts — verify power state via iDRAC/iLO remote console
# Attempt remote power-on if host is off
racadm serveraction powerup
```

Once a host is recovered and reconnects to vCenter, HA automatically re-evaluates VM placement and restarts any VMs still in "Insufficient resources" state — you do not need to manually trigger restarts.

Monitor reconnection:

```bash
# On the recovering host after SSH access restored
service-control --status --all | grep -i stopped
/etc/init.d/vmware-fdm status
```

---

## 5. Option B — Temporarily Lower Admission Control Reservation

If hosts cannot be immediately recovered and critical VMs must be restarted now, temporarily relax the admission control policy to allow HA to use the remaining capacity.

Navigate to **Cluster → Configure → vSphere Availability → Edit → Admission Control**.

```text
Admission control policy options:
  Cluster resource percentage    → HA reserves X% of cluster CPU and RAM for failover
  Slot policy (number of hosts)  → HA reserves capacity equal to N host failures
  Dedicated failover hosts       → specific hosts kept empty as failover reservation

To temporarily allow restarts beyond the normal reservation:
  1. Change "Host failures cluster tolerates" from 2 to 1 (or 1 to 0 for absolute emergency)
  2. Or: temporarily disable admission control (set to "Disabled")
  3. Power on Tier 1 VMs — HA will now allow placement
  4. Restore admission control setting once a host is recovered
```

```powershell
# Check current admission control setting
$cluster = Get-Cluster "cluster-name"
$das = $cluster.ExtensionData.Configuration.DasConfig
$das.AdmissionControlPolicy

# Disable admission control temporarily via SDK (requires vCenter SDK / REST API)
# UI navigation is recommended for this one-time emergency action
# Always document the change and set a calendar reminder to restore it
```

Warning: with admission control disabled or reduced, the cluster has no guaranteed failover capacity. A second host failure during this window may cause further VM data loss or corruption. Restore the policy immediately after Tier 1 VMs are recovered.

---

## 6. Option C — Add an Emergency Host

On VxRail or when spare hardware is available, adding a host to the cluster immediately expands capacity and re-arms HA admission control.

```text
Emergency host addition paths:
  VxRail: VxRail Manager → Cluster Expansion wizard (adds node with LCM-validated config)
  Standalone ESXi: Install ESXi → Join vCenter → Join cluster → Wait for HA re-arm
  Loaner host: ensure ESXi version matches cluster EVC baseline before joining
```

After a new host joins and HA re-arms:

```text
vCenter → Cluster → Monitor → vSphere HA → Summary
  Current failover capacity should now show ≥ Configured failover capacity
  VM Restarts list should show all VMs with status = Completed
```

---

## 7. Post-Incident — Prevent Recurrence

An admission control breach is a design failure: the cluster was not sized to tolerate the number of hosts that actually failed. Address the root cause before the next failure.

**Correct HA restart priorities for every VM:**

```powershell
# Set restart priority to High for all VMs tagged as production in vCenter
$productionVMs = Get-VM | Where-Object { (Get-TagAssignment -Entity $_ | Where-Object { $_.Tag.Name -eq "Production" }) }
$productionVMs | ForEach-Object {
    $spec = New-Object VMware.Vim.ClusterDasVmConfigSpec
    $spec.Info = New-Object VMware.Vim.ClusterDasVmConfigInfo
    $spec.Info.DasSettings = New-Object VMware.Vim.ClusterDasVmSettings
    $spec.Info.DasSettings.RestartPriority = [VMware.Vim.ClusterDasVmSettingsRestartPriority]::high
    $spec.Info.Key = $_.ExtensionData.MoRef
    $spec.Operation = [VMware.Vim.ArrayUpdateOperation]::edit
    Write-Host "Setting High priority: $($_.Name)"
}
```

**Sizing rule for admission control:**

```text
N+1 design: cluster must tolerate 1 host failure and still have capacity to run all VMs
N+2 design: tolerate 2 simultaneous host failures (required for stretched clusters)

Minimum cluster size for N+1:
  vSAN RAID-1 FTT=1: minimum 3 hosts — HA needs 4+ for comfortable headroom
  vSAN RAID-5 FTT=1: minimum 4 hosts — HA needs 5+
  Standard VMFS/NFS:  size based on VM resource demand + 1 host equivalent reservation

Admission control percentage = (1 / number-of-hosts) × 100
  4-host cluster: 25% reservation → 1 host failure tolerated
  5-host cluster: 20% reservation → 1 host failure tolerated with headroom
  6-host cluster: 33% reservation → 2 host failures tolerated
```

**Aria Operations alert configuration:**

Navigate to **Aria Ops → Alerts → Alert Definitions → New Alert Definition**:
- Symptom: Cluster `haCurrentFailoverLevel < haConfiguredFailoverLevel`
- Alert name: "HA Admission Control Breach — Insufficient Failover Capacity"
- Severity: Critical
- Action: Immediate page to on-call

---

## 8. Post-Recovery Validation Checklist

```text
[ ] All Tier 1 VMs running and application-verified by owner
[ ] HA VM Restarts list shows no VMs with status "Insufficient resources"
[ ] vCenter Cluster Summary shows Current failover capacity ≥ Configured failover capacity
[ ] vSAN resync queue is draining (host failures leave absent components)
[ ] Admission control policy restored to pre-incident setting (if temporarily relaxed)
[ ] Failed hosts: either repaired and returned, or permanently removed from cluster
[ ] HA restart priorities audited and corrected for all VMs
[ ] Post-incident review scheduled — root cause of multi-host failure documented
```

---

## Key Terms

| Term | Definition |
|---|---|
| Admission control | vSphere HA feature that reserves a portion of cluster CPU and RAM to guarantee enough capacity to restart VMs after the configured number of host failures |
| Admission control breach | The state where the cluster no longer has enough reserved capacity to meet the configured failover guarantee; HA may block or defer VM power-ons to protect the reservation |
| HA restart priority | Per-VM setting (High / Medium / Low / Disabled / Cluster default) that determines the order in which HA restarts VMs after a host failure; VMs with Disabled priority are never restarted automatically |
| Failover capacity | The portion of cluster CPU and RAM that admission control holds in reserve; expressed as a percentage of total cluster resources or as a number of host failures to tolerate |
| Slot policy | An admission control model where HA calculates a "slot" size based on the largest VM reservation in the cluster and reserves enough slots for failover; can be overly conservative in clusters with a few large VMs |
| Cluster resource percentage | The admission control model that reserves a fixed percentage of total cluster CPU and RAM; more predictable than slot policy for mixed VM sizes |
| FDM | Fault Domain Manager — the HA agent running on each ESXi host; coordinates VM restart decisions and tracks heartbeat state for all hosts in the cluster |
| N+1 | Cluster sizing philosophy where the cluster retains enough capacity across N surviving hosts to run all workloads after 1 host fails; the minimum acceptable HA design |
| N+2 | Cluster sizing where capacity supports 2 simultaneous host failures; required for vSAN stretched cluster designs and high-availability SLAs |
| Insufficient resources | The HA restart status displayed in vCenter when a VM's restart attempt was made but no surviving host had enough free CPU or RAM to accommodate it |
| EVC mode | Enhanced vMotion Compatibility — a cluster-level CPU feature mask that allows VMs to vMotion between hosts with different CPU generations; new hosts added during an emergency must match the cluster EVC baseline |

---

## Common Mistakes

- **Trying to restart all VMs simultaneously when resources are tight.** Attempting to power on 50 VMs at once when the cluster has headroom for 20 means all 50 will fight for slots and most will fail. Stage restarts by priority tier.
- **Disabling admission control and forgetting to re-enable it.** Admission control disabled means the next single host failure has no guaranteed restart capacity. Set a calendar reminder or a monitoring alert for this state.
- **Not having HA restart priorities set before an incident.** If all VMs have "Cluster default" priority, HA has no way to prefer critical databases over test VMs. Set priorities during steady state, not during the incident.
- **Restoring failed hosts one at a time without checking vSAN resync first.** Each failed host leaves vSAN components absent. Returning a host triggers resync. If the cluster is already resource-constrained, multiple simultaneous resyncs can worsen the CPU and network load.
- **Assuming vMotion DRS will fix the overloaded hosts automatically.** DRS is disabled during HA restart operations. After HA completes, run DRS manually to rebalance VMs across recovered hosts before declaring the incident resolved.

---

## Related Scenarios

- [VM Inaccessible / HA Failover](vm-inaccessible-ha-failover/index.md) — Single host failure with sufficient capacity; this scenario extends that to multi-host failure and capacity exhaustion.
- [vSAN Disk or Component Failure](vsan-disk-component-failure/index.md) — Multi-host failure leaves many vSAN components absent; the resync risk window compounds the admission control breach.
- [Aria Ops Alert Storm](aria-ops-alert-storm/index.md) — A failover storm fires dozens of alerts simultaneously; alert correlation and noise suppression are critical to triage quickly.
- [Capacity Planning](capacity-planning/index.md) — Correct N+1 sizing prevents admission control breaches; this scenario and capacity planning are tightly linked.
