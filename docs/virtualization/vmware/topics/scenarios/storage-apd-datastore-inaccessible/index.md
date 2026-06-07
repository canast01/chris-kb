# Storage APD — Datastore Inaccessible

<div class="kb-summary">
All storage paths to a VMFS or NFS datastore are lost. VMs freeze or become inaccessible, vCenter shows
the datastore as unavailable, and ESXi enters the APD (All Paths Down) path-loss state. This scenario
covers identifying the scope of path loss, distinguishing APD from PDL, responding to the VMCP timeout,
restoring paths, and recovering VMs that were force-powered-off by VMCP.
</div>

```text
┌────────────────────────────── Storage APD — Investigation Flow ─────────────────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  START: Datastore shows grey/unavailable in vCenter · VMs freeze · Aria Ops storage alert         ││
│   └──────────────────────────────────────────┬────────────────────────────────────────────────────────┘│
│                                              │                                                        │
│                           ┌──────────────────┴──────────────────┐                                     │
│                           ▼                                     ▼                                     │
│              ┌─────────────────────────┐           ┌─────────────────────────┐                        │
│              │  ALL hosts affected?    │           │  Subset of hosts only?  │                        │
│              │  → Fabric / SAN / NFS   │           │  → Per-host HBA/NIC,    │                        │
│              │    server failure       │           │    zoning, or cable      │                       │
│              └────────────┬────────────┘           └────────────┬────────────┘                        │
│                           │                                     │                                     │
│                           └──────────────────┬──────────────────┘                                     │
│                                              ▼                                                        │
│              ┌───────────────────────────────────────────────────────────────────────────┐            │
│              │  esxcli storage core device list · Check path state: APD vs PDL           │            │
│              └───────────────────────────────┬───────────────────────────────────────────┘            │
│                                              │                                                        │
│                           ┌──────────────────┴──────────────────┐                                     │
│                           ▼                                     ▼                                     │
│              ┌─────────────────────────┐           ┌─────────────────────────┐                        │
│              │  APD: paths recoverable │           │  PDL: device gone       │                        │
│              │  Restore fabric / NFS   │           │  VMCP power-off → HA    │                        │
│              │  paths → VMs resume     │           │  restart on other store │                        │
│              └────────────┬────────────┘           └────────────┬────────────┘                        │
│                           └──────────────────┬──────────────────┘                                     │
│                                              ▼                                                        │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────────┐│
│   │  CLOSE: Paths restored · All VMs running · Datastore green · VMCP policy reviewed                 ││
│   └───────────────────────────────────────────────────────────────────────────────────────────────────┘│
└───────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Products Involved

| Product | Role in This Scenario |
|---|---|
| vCenter | Datastore status; VMCP configuration; HA restart coordination |
| ESXi | Storage path state; HBA/NIC health; NFS mount state |
| vSphere HA / VMCP | APD timeout policy; PDL immediate power-off; VM restart on surviving storage |
| Aria Operations | Initial storage path loss alert; datastore availability dashboard |
| Storage fabric (SAN/NAS) | Physical root cause: switch, HBA, array controller, NFS server |

---

## 1. Confirm the Scope — How Many Hosts and Datastores Affected

Go to **vCenter → Storage → Datastores** and check which datastores are in an error state, then correlate with which hosts are affected.

```text
Datastore states in vCenter:
  Normal (green)       — all paths healthy
  Degraded (yellow)    — some paths lost but storage still accessible
  Inaccessible (red)   — all paths lost; APD or PDL active
  Unmounted            — intentional admin action; not a failure
```

| Scope | Likely Root Cause |
|---|---|
| Single datastore, all hosts | Array LUN/volume offline; NFS export removed |
| Single datastore, subset of hosts | Per-host HBA, cable, zone, or NFS mount failure |
| All datastores, all hosts | Core fabric failure (top-of-rack switch, FC director) |
| All datastores, one host | Local HBA failure, incorrect zoning, host NIC failure |

---

## 2. Check Path State on ESXi — APD vs PDL

SSH to an affected ESXi host and identify whether ESXi considers paths recoverable (APD) or permanently gone (PDL).

```bash
# List all storage devices and their path state
esxcli storage core device list | grep -E "Display Name|State|Status"

# Check path count per device — 0 active paths = APD in progress
esxcli storage core path list | grep -E "Device|State|Runtime State"

# For NFS — check mounted filesystems
esxcli storage nfs list

# Check APD timeout counter (how long paths have been down)
esxcli storage core device list -d <device-id> | grep -i "APD"
```

```text
APD — All Paths Down (temporary)
  State: off / dead but device known.
  ESXi queues I/O internally and waits for the APD timeout (default 140 seconds).
  After timeout, configurable VMCP response kicks in.
  Root cause: switch, cable, fabric, or NFS server disruption — expected to recover.

PDL — Permanent Device Loss
  SCSI sense code 0x05/0x25 (logical unit not supported) received.
  ESXi knows the device is permanently gone.
  VMCP immediately powers off VMs using that device to enable HA restart.
  Root cause: LUN deleted on array, volume decommissioned, NFS export removed.
```

Look for: `State = dead` with no SCSI sense code typically means APD; a PDL SCSI sense code in `/var/log/vmkernel.log` confirms PDL.

---

## 3. Read vmkernel.log for Path Loss Events

The vmkernel log is the ground truth for storage path events — read it to confirm the timeline and root cause before escalating to the storage team.

```bash
# On the affected ESXi host:
grep -i "APD\|PDL\|Lost Path\|path state change\|scsi sense" /var/log/vmkernel.log | tail -50

# Look for the first occurrence to establish when paths were lost
grep -i "APD\|path.*dead" /var/log/vmkernel.log | head -20
```

Common vmkernel.log entries:

```text
NMP: nmp_PathDetermineState: ... path state changed to dead
     → Individual path to device marked dead

vmw_psp_rr: psp_rr_get_path_fn: ... No more paths available
     → All paths to a device exhausted — APD begins

ScsiDeviceIO: ... Failed to complete IO: H:0x0 D:0x2 P:0x0
     → I/O error being returned to guest; VM will freeze

APD START ... device already in APD state for <N> seconds
     → APD timer started; VMCP countdown begins
```

---

## 4. Check the Fabric — FC, iSCSI, or NFS Root Cause

Work from ESXi outward to find where path loss originated.

**Fibre Channel:**

```bash
# List FC HBAs and their link state
esxcli storage san fc list | grep -E "HBA|LinkState|PortName"

# Check FC target path status
esxcli storage san fc events get

# Log location for FC events
grep -i "FC\|fibre\|hba" /var/log/vmkernel.log | tail -30
```

**iSCSI:**

```bash
# List iSCSI adapters and sessions
esxcli iscsi adapter list
esxcli iscsi session list

# Check iSCSI discovery targets
esxcli iscsi adapter discovery sendtarget list -A vmhba64

# Verify vmknic used for iSCSI binding
esxcli iscsi networkportal list
```

**NFS:**

```bash
# Check NFS mount status
esxcli storage nfs list

# Re-mount an NFS datastore that dropped
esxcli storage nfs remove -v <volume-label>
esxcli storage nfs add -H <nfs-server-ip> -s /path/to/export -v <volume-label>

# Check NFS server connectivity
vmkping -I vmk1 <nfs-server-ip>
```

Look for: if FC HBA shows `LinkState = Link Down`, the issue is the physical link or SFP. If iSCSI sessions are absent, check network reachability from the VMkernel port. For NFS, a ping failure to the NFS server confirms a network or server outage.

---

## 5. VMCP Policy — APD Timeout Behaviour

Check what your cluster is configured to do when APD timeout expires, so you understand whether VMCP has already acted on VMs.

Navigate to **Cluster → Configure → vSphere Availability → Failures and Responses → Datastore with APD**.

```text
VMCP APD response options:
  Disabled                         — ESXi queues I/O indefinitely; VMs freeze until paths recover
  Issue events only                — alerts fire; no automatic action
  Power off and restart VMs        — after APD timeout, power off VMs; HA restarts on hosts with storage access
```

```bash
# Check VMCP configuration via PowerCLI
$cluster = Get-Cluster "cluster-name"
$das = $cluster.ExtensionData.Configuration.DasConfig
$das.DefaultVmSettings.VmComponentProtectionSettings
```

Look for: `vmReactionOnAPDCleared = reset` means vCenter automatically restores VMs when paths recover — monitor whether this triggers correctly after fabric is restored.

---

## 6. Restore Storage Paths

Once the root cause is identified and remediated (fabric link up, switch recovered, NFS server back), force ESXi to re-scan for the recovered paths.

```bash
# Re-scan all HBAs on the host for storage devices
esxcli storage core adapter rescan --all

# Or target a specific HBA
esxcli storage core adapter rescan -A vmhba0

# For NFS — verify mount recovers automatically; if not, remount
esxcli storage nfs list
```

In vCenter: **Storage → Datastores → right-click affected datastore → Rescan Storage**.

After paths recover, monitor vmkernel.log:

```bash
grep -i "path.*active\|APD cleared\|PDL cleared" /var/log/vmkernel.log | tail -20
```

Look for: `APD cleared` entries confirm all paths are restored. VMs that were not powered off by VMCP will resume I/O automatically within seconds.

---

## 7. Recover VMs Powered Off by VMCP

If VMCP issued a power-off (PDL or APD timeout with power-off policy), some VMs will be powered off and waiting for HA restart. Check HA restart status before manually powering on anything.

Navigate to **Cluster → Monitor → vSphere HA → VM Restarts**.

```text
Check:
  Restart Status = Completed     → VM is already running on another host; verify via console
  Restart Status = Insufficient resources → HA could not find a host with storage access; manual action needed
  Restart Status = Not Attempted → HA restart priority = Disabled on this VM; power on manually
```

```powershell
# List VMs in powered-off state after APD event
Get-Cluster "cluster-name" | Get-VM | Where-Object { $_.PowerState -eq "PoweredOff" } `
  | Select-Object Name, VMHost, PowerState

# Check HA restart priority per VM
Get-Cluster "cluster-name" | Get-VM `
  | Get-VMRestartPriority `
  | Where-Object { $_.RestartPriority -eq "Disabled" }
```

Look for: any VM with `RestartPriority = Disabled` will not be automatically restarted by HA — these require a manual power-on after storage is confirmed accessible from the target host.

---

## 8. Post-Recovery Validation Checklist

```text
[ ] All storage paths showing Active (not dead/off) on all hosts
[ ] Datastore shows green in vCenter Storage view
[ ] esxcli storage core device list — no device in APD state
[ ] All VMs are running (HA restarted or manual power-on confirmed)
[ ] vmkernel.log shows "APD cleared" for all affected devices
[ ] No VM is showing "Virtual machine disks consolidation is needed" (check after recovery)
[ ] VMCP policy reviewed and set appropriately for your RTO requirements
[ ] Root cause documented: switch port, HBA, cable, NFS server, or array LUN
```

---

## Key Terms

| Term | Definition |
|---|---|
| APD | All Paths Down — transient storage path loss; ESXi still knows the device identity and queues I/O internally while waiting for paths to recover |
| PDL | Permanent Device Loss — storage device signals via SCSI sense code that it is permanently gone; ESXi stops queuing I/O immediately |
| VMCP | VM Component Protection — vSphere HA extension that responds to APD timeout and PDL events by powering off affected VMs to enable HA restart on hosts with storage access |
| APD timeout | The configurable period (default 140 seconds) ESXi waits in APD state before allowing VMCP to take action; during this time VMs are frozen but data is safe |
| vmkernel.log | Primary ESXi system log containing storage path events, SCSI sense codes, and network events; first diagnostic stop for any storage or network path issue |
| SCSI sense code | Low-level SCSI response from a storage device indicating its state; sense code 0x05/0x25 (Illegal Request / Logical Unit Not Supported) is the definitive PDL indicator |
| HBA | Host Bus Adapter — the physical FC or iSCSI adapter in an ESXi host that connects to the storage fabric |
| FC zoning | Fibre Channel fabric access control that defines which HBA WWPNs can see which storage array ports; incorrect or missing zones are a common cause of path loss after changes |
| NMP | Native Multipathing Plugin — the ESXi storage path management layer; logs path state changes and I/O errors; visible in vmkernel.log as `NMP:` prefixed lines |
| PSP | Path Selection Policy — the per-device policy (Round Robin, Fixed, Most Recently Used) that determines which active path ESXi uses for I/O |
| vmkping | VMware CLI tool to test VMkernel port connectivity (similar to ping but uses a specific VMkernel NIC); used to verify NFS server reachability from the storage VMkernel |

---

## Common Mistakes

- **Immediately powering VMs on manually when VMCP has already acted.** Check HA restart status first. VMCP may have powered VMs off and HA may have already restarted them on another host. Manual power-on creates a split-brain if the storage recovers and two instances run simultaneously.
- **Not distinguishing APD from PDL before acting.** APD is "wait and recover" — the correct action is often to restore the fabric and let paths recover. PDL is "storage is gone" — waiting achieves nothing and prolongs the outage.
- **Skipping vmkernel.log and going straight to the array.** The path loss timeline in vmkernel.log often points directly to whether the loss started at the host (HBA event) or at the fabric (all HBAs lost paths simultaneously).
- **Not resetting VMCP policy after the incident.** The default VMCP policy is often "Disabled" — if you only reviewed it during the incident, update it to "Power off and restart VMs" for future protection.
- **Rescanning storage while paths are still in APD.** A rescan during APD can generate I/O errors and stall. Wait for path recovery confirmation in vmkernel.log before triggering a rescan.

---

## Related Scenarios

- [VM Inaccessible / HA Failover](../vm-inaccessible-ha-failover/index.md) — Host failure also triggers VMCP; the distinction is that APD/PDL affects VMs on the lost storage while host failure affects all VMs on that host.
- [Datastore Full / Capacity Alarm](../datastore-full-capacity-alarm/index.md) — A nearly full VMFS datastore can cause write failures that look like path issues; always check capacity alongside path state.
- [vSAN Disk or Component Failure](../vsan-disk-component-failure/index.md) — For vSAN clusters, the disk component failure scenario covers the equivalent storage loss scenario; APD/PDL applies to traditional SAN and NFS datastores.
- [VM Snapshot Consolidation Required](../vm-snapshot-consolidation-required/index.md) — APD events frequently leave orphaned snapshot delta files that trigger a consolidation-needed warning post-recovery.
