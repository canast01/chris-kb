# VM Inaccessible / HA Failover

<div class="kb-summary">
A host fails or loses connectivity and VMs become inaccessible. This scenario covers how to determine
whether vSphere HA has already restarted the VMs, distinguish network partition from hardware failure,
assess vSAN component health during the outage, and confirm the cluster is re-armed before the next failure.
</div>

```text
┌──────────────────────────────── VM Inaccessible / HA Failover — Investigation Flow ──────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: VMs unreachable / Aria Ops alert: host disconnected or not responding                     ││
│   └──────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                              │                                                        │
│                           ┌──────────────────┴──────────────────┐                                     │
│                           ▼                                     ▼                                     │
│              ┌─────────────────────────┐           ┌─────────────────────────┐                        │
│              │  Host disconnected in   │           │  Host isolated (network │                        │
│              │  vCenter — hardware or  │           │  partition) — VMs still │                        │
│              │  management network     │           │  running on host        │                        │
│              └────────────┬────────────┘           └────────────┬────────────┘                        │
│                           │                                     │                                     │
│                           ▼                                     ▼                                     │
│              ┌─────────────────────────┐           ┌─────────────────────────┐                        │
│              │ Check HA restart log:   │           │ Host isolation response │                        │
│              │ vCenter → Cluster →     │           │ policy: power off /     │                        │
│              │ Monitor → vSphere HA    │           │ leave powered on?       │                        │
│              └────────────┬────────────┘           └────────────┬────────────┘                        │
│                           │                                     │                                     │
│                           └──────────────────┬──────────────────┘                                     │
│                                              ▼                                                        │
│              ┌───────────────────────────────────────────────────────────────────────────┐            │
│              │  Check vSAN: Resyncing Objects · APD vs PDL path state · VMCP policy      │            │
│              └───────────────────────────────────────────────────────────────────────────┘            │
│                                              │                                                        │
│                           ┌──────────────────┴──────────────────┐                                     │
│                           ▼                                     ▼                                     │
│              ┌─────────────────────────┐           ┌─────────────────────────┐                        │
│              │  APD: wait for path     │           │  PDL: VMCP triggers     │                        │
│              │  to recover; vSAN will  │           │  immediate HA restart   │                        │
│              │  resync on reconnect    │           │  on surviving hosts     │                        │
│              └─────────────────────────┘           └─────────────────────────┘                        │
│                                              │                                                        │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  CLOSE: Verify VMs running · vSAN health green · HA re-armed · Resync queue draining              ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | Cluster view; HA restart log; host state |
| ESXi | Host failure detection; FDM agent; storage path state |
| vSAN | Component rebuild after host loss; APD/PDL path state |
| vSphere HA (vCenter) | VM restart orchestration; admission control |
| Aria Operations | Initial alert; post-failover validation dashboard |

---

## 1. Identify Which Host Failed and How

Open vCenter and go to **Hosts and Clusters**. Look for hosts in a "Disconnected" or "Not Responding" state.

```text
Host states in vCenter:
  Connected            — normal
  Disconnected         — vCenter lost management network contact
  Not Responding       — heartbeat timeout; HA triggers restart evaluation
  Maintenance Mode     — intentional; HA does not restart VMs here
```

Determine the failure type before taking any action:

| Failure Type | Signs | HA Behaviour |
|---|---|---|
| Hardware / total host failure | Host not responding, ILO/iDRAC unreachable | HA restarts VMs on surviving hosts |
| Network partition (host isolated) | Host heartbeat lost but VMs may still run | Depends on isolation response policy |
| Management network only | Host disconnected but ESXi shell reachable | vSAN and VMs may be fine; reconnect vCenter agent |

---

## 2. Check HA Restart Status

Before taking manual steps, confirm whether HA has already restarted the affected VMs.

Navigate to **Cluster → Monitor → vSphere HA → VM Restarts**.

```text
Fields to check:
  Restart Status   — Completed / In Progress / Not Attempted
  Restart Host     — which host is now running the VM
  Restart Time     — timestamp of HA restart
  Restart Reason   — host failure / isolation / PDL
```

If HA completed restarts, verify VMs are accessible before doing anything else. Unnecessary manual intervention after HA has already acted is a common source of errors.

```bash
# Check FDM (fault domain manager / HA agent) status on a surviving host
/etc/init.d/vmware-fdm status

# Restart FDM if it shows stopped (rare; use only if HA appears stuck)
/etc/init.d/vmware-fdm restart
```

---

## 3. Determine Storage Path State — APD vs PDL

When a host loses access to vSAN or shared storage, the path state determines HA behaviour.

```text
APD — All Paths Down (temporary)
  Storage paths lost but device identity still known.
  ESXi waits for paths to recover.
  HA does not immediately restart VMs.
  VMCP can be configured to restart after APD timeout.

PDL — Permanent Device Loss
  Device reports it is gone permanently (SCSI sense code).
  ESXi knows paths will not recover.
  VMCP triggers immediate HA VM restart on surviving hosts.
```

```bash
# Check storage device state on the affected or surviving host
esxcli storage core device list | grep -E "State|Device|Display"

# For vSAN specifically — list objects and health
esxcli vsan debug object list | grep -i degraded

# Check which host owns degraded components
esxcli vsan debug object list | grep -E "Host|Health|UUID"
```

VMCP (VM Component Protection) policy is set in **Cluster → Configure → vSphere Availability → Failures and Responses → Datastore with PDL / Datastore with APD**. Confirm the policy matches your RTO requirements.

---

## 4. Check vSAN Resyncing Objects

After a host loss, vSAN immediately begins rebuilding absent components on surviving hosts. Go to **vSAN → Monitor → Resyncing Objects**.

```text
Columns to check:
  Bytes to Sync    — total data to rebuild (can be TB on large clusters)
  ETA              — rebuild time estimate
  Policy Status    — Non-compliant = protection gap exists right now
```

```bash
# Check resync progress from ESXi CLI
esxcli vsan debug resync summary get

# Sample output fields:
#   BytesToResync   — remaining bytes
#   ResyncType      — REPAIR / REBALANCE / POLICY_CHANGE
#   ObjectsToResync — number of VM objects still rebuilding
```

Do not put additional hosts into maintenance mode while the resync queue is non-empty and any VM is at FTT=1 with one component absent. That creates a second failure before the first is healed.

---

## 5. PowerCLI — Validate Post-Failover State

```powershell
# List all VMs on surviving hosts and confirm power state
Get-Cluster "cluster-name" | Get-VMHost | Get-VM `
  | Where-Object { $_.PowerState -eq "PoweredOn" } `
  | Select-Object Name, VMHost, PowerState | Sort-Object VMHost

# Confirm HA is enabled and admission control is active
Get-Cluster "cluster-name" `
  | Select-Object Name, HAEnabled, HAAdmissionControlEnabled, DrsEnabled

# Check if any VM has no HA restart priority set (override = None)
Get-Cluster "cluster-name" | Get-VM `
  | Get-VMRestartPriority `
  | Where-Object { $_.RestartPriority -eq "Disabled" }
```

---

## 6. Post-Failover Validation Checklist

```text
[ ] All VMs previously on failed host are now running on surviving hosts
[ ] HA restart log shows "Completed" for all affected VMs
[ ] vSAN health shows green (no red checks)
[ ] vSAN resync queue is draining (ETA visible and decreasing)
[ ] No VM is showing Policy Status = Non-Compliant after resync completes
[ ] HA admission control is re-armed (cluster has capacity headroom)
[ ] Failed host is either repaired/returned or removed from cluster inventory
```

---

## Common Mistakes

- **Panicking and manually restarting VMs before checking HA.** HA may have already restarted the VMs on another host. Manually powering them on again creates a split-brain (two instances of the same VM running).
- **Not checking the vSAN resync queue before doing maintenance.** Placing another host in maintenance during an active resync can drop a second component and make VMs non-compliant.
- **Ignoring the APD/PDL distinction.** APD is temporary and waiting is often correct. PDL is permanent and VMCP must be configured to restart VMs quickly — check your VMCP policy before an incident.
- **Forgetting to verify HA re-armed.** After the failed host is removed or repaired, confirm HA admission control has enough headroom to tolerate the next failure.

---

## Related Scenarios

- [vSAN Disk or Component Failure](../vsan-disk-component-failure/index.md) — Host failure and disk failure produce similar vSAN resync queues; the disk failure scenario covers component-level rebuild in depth.
- [VM Performance Degraded](../vm-performance-degraded/index.md) — Surviving hosts may be overloaded after an HA failover, leading to elevated CPU ready on restarted VMs.
- [vMotion Failing](../vmotion-failing/index.md) — DRS may attempt to rebalance VMs after HA restarts; vMotion failures here compound the recovery.
