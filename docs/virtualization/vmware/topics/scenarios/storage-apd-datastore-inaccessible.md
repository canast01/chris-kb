---
tags:
  - scenarios
  - vmware
description: "All storage paths to a VMFS or NFS datastore are lost. VMs freeze or become inaccessible, vCenter shows the datastore as unavailable, and ESXi enters the..."
---
# Storage APD — Datastore Inaccessible

<div class="kb-summary">
All storage paths to a VMFS or NFS datastore are lost. VMs freeze or become inaccessible, vCenter shows
the datastore as unavailable, and ESXi enters the APD (All Paths Down) path-loss state. This scenario
covers identifying the scope of path loss, distinguishing APD from PDL, responding to the VMCP timeout,
restoring paths, and recovering VMs that were force-powered-off by VMCP.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

products_involved: "Products Involved" {shape: rectangle}
1_confirm_the_scope_how_many_hosts_a: "1. Confirm the Scope — How Many Hosts and\nDatastores Affecte" {shape: rectangle}
2_check_path_state_on_esxi_apd_vs_pd: "2. Check Path State on ESXi — APD vs PDL" {shape: rectangle}
3_read_vmkernellog_for_path_loss_eve: "3. Read vmkernel.log for Path Loss Events" {shape: rectangle}
4_check_the_fabric_fc_iscsi_or_nfs_r: "4. Check the Fabric — FC, iSCSI, or NFS Root Cause" {shape: rectangle}
5_vmcp_policy_apd_timeout_behaviour: "5. VMCP Policy — APD Timeout Behaviour" {shape: rectangle}

products_involved -> 1_confirm_the_scope_how_many_hosts_a: uses
1_confirm_the_scope_how_many_hosts_a -> 2_check_path_state_on_esxi_apd_vs_pd: uses
2_check_path_state_on_esxi_apd_vs_pd -> 3_read_vmkernellog_for_path_loss_eve: uses
3_read_vmkernellog_for_path_loss_eve -> 4_check_the_fabric_fc_iscsi_or_nfs_r: uses
4_check_the_fabric_fc_iscsi_or_nfs_r -> 5_vmcp_policy_apd_timeout_behaviour: uses
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


```text title="Expected output"
2024-01-15T08:23:45.123Z cpu15:2048)ScsiPath: 4282: Path vmhba4:C0:T5:L0 to device naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2 state change: On -> Dead
2024-01-15T08:23:47.456Z cpu22:2105)ScsiPath: 4283: Marking path vmhba4:C0:T5:L0 as APD (All Paths Down)
2024-01-15T08:24:12.789Z cpu18:2156)ScsiPath: 4284: SCSI sense data: Key=0x3 ASC=0x11 ASCQ=0x00 (Medium Error)
2024-01-15T08:24:15.234Z cpu8:2201)ScsiPath: 4285: Path vmhba5:C0:T3:L2 Lost Path detected on device naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
2024-01-15T08:24:45.567Z cpu12:2289)ScsiPath: 4286: PDL (Permanent Device Loss) condition detected
2024-01-15T08:25:10.890Z cpu19:2334)ScsiPath: 4287: Path vmhba4:C0:T5:L0 state change: Dead -> On
2024-01-15T08:26:33.123Z cpu5:2445)ScsiPath: 4288: SCSI sense Key=0x5 ASC=0x24 ASCQ=0x00 (Invalid Field)
...
2024-01-15T08:23:45.123Z cpu15:2048)ScsiPath: 4282: Path vmhba4:C0:T5:L0 to device naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2 state change: On -> Dead
2024-01-15T08:23:47.456Z cpu22:2105)ScsiPath: 4283: Marking path vmhba4:C0:T5:L0 as APD (All Paths Down)
2024-01-15T08:24:12.789Z cpu18:2156)ScsiPath: 4284: SCSI sense data: Key=0x3 ASC=0x11 ASCQ=0x00 (Medium Error)
2024-01-15T08:24:15.234Z cpu8:2201)ScsiPath: 4285: Path vmhba5:C0:T3:L2 Lost Path detected on device naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
2024-01-15T08:24:45.567Z cpu12:2289)ScsiPath: 4286: PDL (Permanent Device Loss) condition detected
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /var/log/vmkernel.log: No such file or directory` | Verify you are running the command directly on the ESXi host |
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


```text title="Expected output"
HBA: vmhba0
LinkState: link up
PortName: 50:00:14:40:5a:2b:c1:a0
HBA: vmhba1
LinkState: link up
PortName: 50:00:14:40:5a:2b:c1:a1
HBA: vmhba2
LinkState: link down
PortName: 50:00:14:40:5a:2b:c1:a2

2024-01-15T08:23:47.123Z: FC link up on vmhba0, target 50:0a:0985:2c1a3b4d
2024-01-15T08:15:22.456Z: FC link down on vmhba2, target 50:0a:0985:2c1a3b4e
2024-01-15T07:42:11.789Z: FC target discovery completed, 12 LUNs found

2024-01-15T08:23:47.123Z cpu0:2048)vmhba0: [HBA Link State Change] Link up on port 50:00:14:40:5a:2b:c1:a0
2024-01-15T08:15:22.456Z cpu2:4096)vmhba2: [HBA Link State Change] Link down on port 50:00:14:40:5a:2b:c1:a2
2024-01-15T07:42:11.789Z cpu1:3072)Fibre Channel: Target discovery initiated on vmhba0
2024-01-15T07:41:55.234Z cpu3:5120)HBA vmhba1: RSCN received, rescanning targets
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `esxcli: command not found` | Verify you are running this command on an ESXi host with direct SSH access, not a vCenter Server. |
    | `grep: /var/log/vmkernel.log: No such file or directory` | Confirm the ESXi host is fully booted and the /var/log directory is mounted; try `ls -la /var/log/` to verify. |
    | `No such FC HBA found` | Check that FC HBAs are installed and recognized by running `esxcli storage san fc list` without filters to see all available adapters. |
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


```text title="Expected output"
Name    Driver      State   iscsi.MaxIoSize
------  ----------  ------  ---------------
vmhba64 iscsi       online  65536
vmhba65 iscsi       online  65536

SessionName                              Portal          PortalGroup  State
---------------------------------------  --------------  -----------  ------
iqn.1991-05.com.example:storage.lun01    192.168.1.100   1            LOGGED_IN
iqn.1991-05.com.example:storage.lun02    192.168.1.101   1            LOGGED_IN

Discovery Address  Discovery Status
------------------  ----------------
192.168.1.50        STATIC

Adapter  PortalGroup  Portal              State
-------  -----------  ------------------  -------
vmhba64  1            192.168.1.100:3260  ACTIVE
vmhba64  1            192.168.1.101:3260  ACTIVE
vmhba65  2            192.168.1.102:3260  ACTIVE
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown command or namespace iscsi.adapter` | Verify the iSCSI software adapter is installed and loaded with `esxcli iscsi adapter list`; if empty, enable it via vSphere Client or `esxcli iscsi adapter set --adapter=vmhba64 -e true`. |
    | `Error: Could not find adapter vmhba64` | Confirm the adapter name is correct by running `esxcli iscsi adapter list` first, as adapter numbers vary by host configuration. |
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


```text title="Expected output"
NFS Mount List:
Volume Name                                    Host                Port   Type  Mounted  Read-Only
nfs-datastore-prod                             192.168.10.45       2049   NFS   true     false
nfs-datastore-backup                           192.168.10.46       2049   NFS   true     false

NFS datastore nfs-datastore-prod removed successfully.
NFS datastore nfs-datastore-prod added and mounted successfully.

PING 192.168.10.45 (192.168.10.45): 56 data bytes
64 bytes from 192.168.10.45: icmp_seq=0 time=2.341 ms
64 bytes from 192.168.10.45: icmp_seq=1 time=2.156 ms
64 bytes from 192.168.10.45: icmp_seq=2 time=2.287 ms
--- 192.168.10.45 statistics ---
3 packets transmitted, 3 packets received, 0% packet loss
round-trip min/avg/max = 2.156, 2.261, 2.341 ms
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `NFS mount failed: Permission denied` | Verify NFS server export permissions include the ESXi host IP and that the export is readable/writable. |
    | `vmkping: Unknown host 192.168.10.45` | Confirm the NFS server IP is correct and that the vmk1 interface has network connectivity and a valid route to the NFS server subnet. |
    | `NFS datastore nfs-datastore-prod is still mounted` | Unmount the datastore from all VMs and remove any locks using `esxcli storage nfs list` before attempting removal. |
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


```text title="Expected output"
IsEnabled                    : True
VmStorageProtectionForAPD    : clusterWide
VmTerminateDelayForAPD       : 300
VmReactionOnAPDCleared       : reset
VmMoterationForAPDCleared    : disabled
VmStorageProtectionForPDL    : clusterWide
VmTerminateDelayForPDL       : 300
VmReactionOnPDLCleared       : reset
VmMoterationForPDLCleared    : disabled
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Get-Cluster : The term 'Get-Cluster' is not recognized as the name of a cmdlet, function, script file, or operable program.` | Import the VMware PowerCLI module with `Import-Module VMware.PowerCLI` before running the command. |
    | `Get-Cluster : Could not find cluster with name 'cluster-name'.` | Replace `"cluster-name"` with the actual cluster name; verify it exists with `Get-Cluster | Select-Object Name`. |
    | `Access to the resource is forbidden.` | Ensure your vCenter user account has at least read-only permissions on the cluster object. |
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


```text title="Expected output"
HBA Rescan: Complete
vmhba0 Rescan: Complete
vmhba1 Rescan: Complete
vmhba2 Rescan: Complete

NFS Mount Information:
Volume Name  Host          Accessible  Mounted  Read-Only
nfs-datastore-01  192.168.1.50  true       true     false
nfs-datastore-02  192.168.1.51  true       true     false
nfs-backup-vol    192.168.1.52  false      false    false
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `Error: Unknown option --all` | Use `-a` instead of `--all` for the rescan command. |
    | `Error: Could not find HBA adapter vmhba0` | Verify the HBA name with `esxcli storage core adapter list` before rescanning. |
    | `NFS mount timeout or stale NFS handle detected` | Remount the NFS datastore using `esxcli storage nfs remove -v <volume-name>` followed by `esxcli storage nfs add`. |
In vCenter: **Storage → Datastores → right-click affected datastore → Rescan Storage**.

After paths recover, monitor vmkernel.log:

```bash
grep -i "path.*active\|APD cleared\|PDL cleared" /var/log/vmkernel.log | tail -20
```


```text title="Expected output"
2024-01-15T08:23:45.123Z cpu2:2051)WARNING: NMP: nmp_PathStateChangeEvent:4782: Active path "vmhba2:C0:T1:L0" changed to "dead"
2024-01-15T08:24:12.456Z cpu5:4103)WARNING: NMP: nmp_PathStateChangeEvent:4782: Active path "vmhba3:C0:T2:L0" changed to "dead"
2024-01-15T08:25:33.789Z cpu1:1923)NMP: nmp_DeviceAttemptFailover:5421: Failing over device "naa.60060e8007a2e0000007a2e000010001" from path "vmhba2:C0:T1:L0"
2024-01-15T08:26:01.234Z cpu7:3456)APD cleared: Device naa.60060e8007a2e0000007a2e000010001 recovered after 28 seconds
2024-01-15T08:27:15.567Z cpu3:2789)PDL cleared: Device naa.60060e8007a2e0000007a2e000010002 path restored
2024-01-15T08:28:44.891Z cpu6:5012)NMP: nmp_PathStateChangeEvent:4782: Active path "vmhba4:C0:T3:L0" changed to "active"
2024-01-15T08:29:22.345Z cpu2:1834)WARNING: NMP: nmp_PathStateChangeEvent:4782: Active path "vmhba1:C0:T0:L0" changed to "dead"
2024-01-15T08:30:55.678Z cpu4:3267)APD cleared: Device naa.60060e8007a2e0000007a2e000010003 recovered after 45 seconds
```

!!! warning "Common errors"
    | Error | Fix |
    |---|---|
    | `grep: /var/log/vmkernel.log: No such file or directory` | Verify the ESXi host is accessible and the vmkernel.log path is correct; on some versions it may be in `/var/log/vmkernel` or rotated to dated files like `vmkernel.1.log`. |
    | `grep: (standard input): No such file or directory` | Ensure you have read permissions on the vmkernel.log file; run the command with `sudo` or as root if access is denied. |
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
| NFS | Network File System — a file-level storage protocol; NFS datastores can experience APD/PDL events the same way block-storage (FC/iSCSI) datastores do, though the failure signaling differs slightly |
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

- [VM Inaccessible / HA Failover](vm-inaccessible-ha-failover.md) — Host failure also triggers VMCP; the distinction is that APD/PDL affects VMs on the lost storage while host failure affects all VMs on that host.
- [Datastore Full / Capacity Alarm](datastore-full-capacity-alarm.md) — A nearly full VMFS datastore can cause write failures that look like path issues; always check capacity alongside path state.
- [vSAN Disk or Component Failure](vsan-disk-component-failure.md) — For vSAN clusters, the disk component failure scenario covers the equivalent storage loss scenario; APD/PDL applies to traditional SAN and NFS datastores.
- [VM Snapshot Consolidation Required](vm-snapshot-consolidation-required.md) — APD events frequently leave orphaned snapshot delta files that trigger a consolidation-needed warning post-recovery.
