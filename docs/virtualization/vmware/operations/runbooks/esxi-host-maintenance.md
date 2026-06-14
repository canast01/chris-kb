---
tags:
  - esxi
  - operations
  - vmware
  - vsphere-8
---
# ESXi Host Maintenance Mode Runbook

<div class="kb-summary">

| Field | Value |
|---|---|
| Risk | Medium — VMs migrated off host; cluster capacity temporarily reduced |
| Approval | Change ticket required for production hosts |
| Estimated time | 15–60 minutes (DRS drain depends on VM count) |
| Impact | Host-local VMs migrate; no service interruption when DRS is enabled |

*Applies to: vSphere 7.x / 8.x*
</div>

```text
┌──────────────────────────── ESXi Host Maintenance Mode — Runbook ─────────────────────────────────────┐
│                                                                                                       │
│  OVERVIEW                                                                                             │
│  Maintenance mode evacuates all running VMs before any patching, hardware work, or host removal       │
│  DRS must be enabled (at least partially automated) for automatic migration                           │
│  Pre-check: confirm cluster has capacity to absorb the host's VMs before entering maintenance         │
│                                                                                                       │
│  FLOW                                                                                                 │
│  Pre-checks → Enter maintenance mode → Wait for DRS evacuation → Perform work                         │
│  → Verify host is ready → Exit maintenance mode → Confirm VMs re-balanced                             │
│                                                                                                       │
│  ROLLBACK                                                                                             │
│  Exit maintenance mode at any point before patching                                                   │
│  After patching: rollback requires re-running original firmware/patch via vLCM                        │
│                                                                                                       │
│  Key terms:                                                                                           │
│  Maintenance mode  = ESXi state where vSphere migrates all VMs off the host                           │
│  DRS drain         = DRS auto-migrates VMs via vMotion before maintenance completes                   │
│  Remediation       = vLCM applying a patch baseline or cluster image to the host                      │
│  Admission control = HA policy that reserves failover capacity; check before removing a host          │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

!!! warning "Host enters maintenance mode — VMs evacuate and the host reboots"
    Placing a host in maintenance mode triggers DRS to vMotion all VMs to other cluster members. Verify the cluster has sufficient CPU and memory headroom to absorb the workload before proceeding. If HA admission control is tight, maintenance mode will be blocked until you increase headroom or temporarily adjust the HA policy.

## Run This Routine

1. **Check cluster capacity** — confirm the remaining hosts can absorb the host's workload:
   ```powershell
   Connect-VIServer -Server vcenter.example.local
   Get-Cluster "Production" | Get-VMHost | Select Name, CpuUsageMhz, MemoryUsageMB, ConnectionState
   ```
   Rule of thumb: cluster CPU and RAM usage must be below 70% before removing a host.

2. **Check HA admission control** — in vCenter: Cluster → Configure → vSphere Availability → Admission Control. Confirm the policy will still be satisfied with N-1 hosts.

3. **Check vSAN health** (if vSAN cluster):
   ```bash
   esxcli vsan cluster get
   esxcli vsan health cluster list
   ```
   All health checks must be green before entering maintenance mode.

4. **Check for VMs with DRS override set to Manual or Disabled** — these will not auto-migrate:
   ```powershell
   Get-VM | Where-Object { $_.DrsAutomationLevel -ne "FullyAutomated" }
   ```
   Manually vMotion any VMs that DRS will not migrate.

5. **Enter maintenance mode** — via vCenter UI: right-click host → Enter Maintenance Mode → select "Move powered-on virtual machines to other hosts in the cluster" → OK.

   Or via PowerCLI:
   ```powershell
   Get-VMHost "esxi-01.example.local" | Set-VMHost -State Maintenance
   ```

6. **Monitor DRS migration** — vCenter Events tab or:
   ```powershell
   Get-VMHost "esxi-01.example.local" | Get-VM
   ```
   Wait until no VMs remain on the host. Duration depends on VM count and network bandwidth.

7. **Confirm maintenance mode state**:
   ```powershell
   Get-VMHost "esxi-01.example.local" | Select Name, ConnectionState, PowerState
   ```
   Expected: `ConnectionState = Connected`, `PowerState = PoweredOn`, state = Maintenance.

8. **Perform host work** — apply patch, replace hardware, update firmware, etc.

9. **Exit maintenance mode** — via vCenter UI: right-click host → Exit Maintenance Mode.

   Or via PowerCLI:
   ```powershell
   Get-VMHost "esxi-01.example.local" | Set-VMHost -State Connected
   ```

10. **Verify host rejoins cluster** — confirm host shows Connected and DRS re-balances VMs within a few minutes.

---

## vLCM Remediation Path

When using vLCM (Lifecycle Manager) to patch a host, the remediation workflow handles maintenance mode automatically:

```text
Cluster → Updates → Hosts → check host compliance
  Non-compliant hosts → Remediate
  vLCM enters maintenance mode → applies patch → exits maintenance mode
  Each host remediated sequentially by default (parallel optional)
```

Monitor progress: Cluster → Monitor → Tasks.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Host stuck entering maintenance | VM cannot be migrated (anti-affinity rule, no datastore space at destination) | Check DRS migration recommendations; override manually |
| vSAN health goes degraded | Object rebuilding paused during maintenance | Use vSAN "No data migration" mode only for very brief hardware tasks with no risk; ensure full evacuation for longer work |
| HA admission control prevents maintenance | Cluster would violate HA policy | Temporarily adjust admission control policy (record original values) or migrate some VMs to another cluster |
| PowerCLI Set-VMHost hangs | DRS not completing evacuation | Verify no VM is stuck in vMotion; check DRS history for migration failures |

---

## Verify

- **Alarms:** vSphere Client → Home → Alarms — no new critical alarms after the operation
- **Events:** monitor the vCenter Events view for the affected object for 5 minutes
- **Health check:** run the morning health-check sequence for the affected product tier

## See also

- [VMware Backup Failure Runbook](backup-failure.md)
- [VMware Certificate Renewal Runbook](certificate-renewal-planning.md)
- [vCenter Certificate Rotation Runbook](certificate-rotation.md)
- [Virtualization Runbooks](index.md)
