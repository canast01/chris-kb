---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
description: "Diagnosing inaccessible datastores across VMFS, NFS, and vSAN — APD/PDL states, HBA path failures, NFS mount errors, and vSAN component health."
---
# Datastore Issues

<div class="kb-summary">
Diagnosing inaccessible datastores across VMFS, NFS, and vSAN — APD/PDL states, HBA path failures, NFS mount errors, and vSAN component health.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
datastore_inaccessible_apd_vs_pdl: "Datastore Inaccessible — APD vs PDL" {shape: rectangle}
datastore_full: "Datastore Full" {shape: rectangle}
high_datastore_latency: "High Datastore Latency" {shape: rectangle}
vmfs_lock_failed_to_lock_the_file: "VMFS Lock — Failed to Lock the File" {shape: rectangle}
vsan_object_noncompliant_or_degraded: "vSAN Object Non-Compliant or Degraded" {shape: rectangle}
verify: "Verify" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> datastore_inaccessible_apd_vs_pdl: investigate
symptom -> datastore_full: investigate
symptom -> high_datastore_latency: investigate
symptom -> vmfs_lock_failed_to_lock_the_file: investigate
symptom -> vsan_object_noncompliant_or_degraded: investigate
symptom -> verify: investigate
datastore_inaccessible_apd_vs_pdl -> resolution
datastore_full -> resolution
high_datastore_latency -> resolution
vmfs_lock_failed_to_lock_the_file -> resolution
vsan_object_noncompliant_or_degraded -> resolution
verify -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## Datastore Inaccessible — APD vs PDL

An inaccessible datastore is either **APD (All Paths Down)** — temporary, paths may recover — or **PDL (Permanent Device Loss)** — the storage array has returned SCSI sense codes indicating the LUN is gone.

```bash
# From ESXi host — check path state for a specific device
esxcli storage nmp device list
esxcli storage nmp path list -d <naa.xxxx>

# Check for APD/PDL events in vmkernel log
grep -i "APD\|PDL\|permanently" /var/log/vmkernel.log | tail -50

# Check datastore status from vCenter (PowerCLI)
Get-Datastore | Where-Object {$_.State -ne "Available"} | Select Name, State
```


```text title="Expected output"
Name                                    Device                                State  Runtime Name
SAN-LUN-001                             naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2  active naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
SAN-LUN-002                             naa.60001405b2c3d4e5f6g7h8i9j0k1l2m3  active naa.60001405b2c3d4e5f6g7h8i9j0k1l2m3
Local-SSD                               naa.5000c5f0a1b2c3d4         active naa.5000c5f0a1b2c3d4
...

Runtime Name: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2
Paths: vmhba2:C0:T0:L0 (active/on), vmhba3:C0:T0:L0 (active/on), vmhba4:C0:T0:L0 (standby/on)

2024-01-15T08:23:44.567Z cpu2:2048)WARNING: NMP: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2: APD condition detected
2024-01-15T08:24:12.891Z cpu5:4096)WARNING: NMP: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2: PDL condition detected on path vmhba2:C0:T0:L0
2024-01-15T08:25:01.234Z cpu1:1024)ERROR: NMP: naa.60001405a1b2c3d4e5f6g7h8i9j0k1l2: Permanently lost device

Name                 State
Datastore-Prod-01    Available
Datastore-Prod-02    Unavailable
Datastore-DR-Sync    Inaccessible
```

!!! warning "Common errors"
    **`esxcli: command not found`** — Run this command directly on the ESXi host via SSH or vSphere Client console, not from a Windows management station.
    **`Get-Datastore : The term 'Get-Datastore' is not recognized`** — Install VMware PowerCLI module with `Install-Module -Name VMware.PowerCLI -Force` and connect to vCenter using `Connect-VIServer` before running the cmdlet.
**APD resolution:**

1. Identify which hosts report the datastore as inaccessible — if only some hosts, isolate to a specific fabric path or HBA.
2. Check SAN switch for zoning errors and ISL state.
3. Check storage array for controller failover, LUN masking, or port errors.
4. Rescan storage adapters from all affected hosts:

```bash
# Rescan from ESXi CLI
esxcli storage core adapter rescan -A all

# Or from vCenter — right-click cluster → Storage → Rescan Storage
```


```text title="Expected output"
Rescan of adapter vmhba0 started.
Rescan of adapter vmhba1 started.
Rescan of adapter vmhba2 started.
Rescan of adapter vmhba3 started.
Rescan of adapter vmhba4 started.
Rescan of adapter vmhba5 started.
Rescan of adapter vmhba6 started.
Rescan of adapter vmhba7 started.
All adapters rescanned successfully.
```

!!! warning "Common errors"
    **`Error: Unknown option or malformed command`** — Verify the ESXi host shell is enabled and you are using the correct esxcli syntax with proper spacing around `-A all`.
    **`Error: Permission denied`** — Run the command as root or with appropriate ESXi administrative privileges; non-root users cannot execute storage rescans.
    **`Error: Unable to rescan adapter vmhbaX: Device or resource busy`** — Wait for any ongoing storage operations to complete, then retry the rescan after 30–60 seconds.
5. If paths recover, verify VMs resume I/O and check for filesystem consistency warnings.

**PDL action:**

- Do NOT rescan repeatedly into a PDL — it can cause VM kernel panics.
- Confirm with the storage team whether the LUN was decommissioned or is experiencing a controller failure.
- If unintentional, escalate to the storage team for LUN restoration before taking any ESXi action.

---

## Datastore Full

**Step 1 — Identify top consumers from vCenter:**

Right-click datastore → Browse → sort by file size. Or use PowerCLI:

```powershell
# Find all snapshots across all VMs consuming space on a datastore
Get-VM | Get-Snapshot | Where-Object {$_.ExtensionData.Config.Files.SnapshotDirectory -like "*DatastoreName*"} |
  Select VM, Name, Created, SizeGB | Sort-Object SizeGB -Descending
```

**Common culprits:**

| Item | Where to Check | Action |
|---|---|---|
| Snapshots | vCenter → VM → Snapshots | Consolidate or delete stale snapshots |
| ISO files | Datastore browser → ISO folder | Move ISOs to a dedicated ISO datastore |
| Orphaned VMDKs | Datastore browser — files with no associated VM | Verify orphaned, then delete |
| Old templates | vCenter inventory | Remove stale or duplicate templates |
| Swap files (.vswp) | One per powered-on VM | Reduce memory overcommit or set swap to dedicated datastore |

**Step 2 — Snapshot cleanup:**

```powershell
# Find all snapshots older than 3 days
Get-VM | Get-Snapshot | Where-Object {$_.Created -lt (Get-Date).AddDays(-3)} |
  Select VM, Name, Created, SizeGB | Sort-Object SizeGB -Descending

# Remove a specific snapshot (verify with VM owner first)
Get-VM "VMName" | Get-Snapshot -Name "SnapshotName" | Remove-Snapshot -RunAsync
```

**Step 3 — Check for delta VMDKs not visible in Snapshot Manager:**

```bash
# From ESXi — look for delta VMDKs that should have been committed
find /vmfs/volumes/<datastore-uuid>/<vmname>/ -name "*-delta.vmdk" -o -name "*-000*.vmdk"
# If delta files exist but no snapshot shows in vCenter, run VM → Consolidate
```


```text title="Expected output"
/vmfs/volumes/5a3c8e2f-7b4a-41e2-9c3a-2d1b8e9f4c6a/web-server-01/web-server-01-delta.vmdk
/vmfs/volumes/5a3c8e2f-7b4a-41e2-9c3a-2d1b8e9f4c6a/web-server-01/web-server-01-000001.vmdk
/vmfs/volumes/5a3c8e2f-7b4a-41e2-9c3a-2d1b8e9f4c6a/web-server-01/web-server-01-000002.vmdk
/vmfs/volumes/5a3c8e2f-7b4a-41e2-9c3a-2d1b8e9f4c6a/db-prod-02/db-prod-02-delta.vmdk
```

!!! warning "Common errors"
    **`find: '/vmfs/volumes/<datastore-uuid>': No such file or directory`** — Replace `<datastore-uuid>` with the actual datastore UUID from `ls /vmfs/volumes/` and `<vmname>` with the actual VM folder name.
    **`find: Filesystem loop detected; '-fstype' not used; skipping directory`** — Add `-fstype local` to the find command to avoid symlink loops in VMFS.
---

## High Datastore Latency

Latency over 20ms for VMFS/SAN or 30ms for NFS is a concern. Over 50ms will impact most workloads.

```bash
# Check per-device latency from ESXi using esxtop
esxtop
# Press 'u' for storage device view — look at GAVG (guest average latency in ms)
# KAVG = kernel latency, DAVG = device latency; GAVG = KAVG + DAVG
```


```text title="Expected output"
esxtop 7.0.3 build-21930508
Press 'q' to quit, 'h' for help
DEVICE                READS/s  WRITES/s  GAVG(ms)  KAVG(ms)  DAVG(ms)  QAVG  ACTV
naa.6001405a1b2c3d4e    145.2     89.7      12.4      3.2       9.2     2.1   1.8
naa.6001405a1b2c3d4f    203.1     156.3     18.7      4.1      14.6     3.5   2.9
naa.6001405a1b2c3d50     78.4      42.1      8.3      2.8       5.5     0.9   0.7
naa.6001405a1b2c3d51    312.5     201.8     24.3      5.1      19.2     4.2   3.6
naa.6001405a1b2c3d52     91.3      67.2     11.1      3.5       7.6     1.4   1.2
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are running this command directly on an ESXi host via SSH or console, not from a vCenter server or external system.
    **`Error: Cannot open /proc/vmware/sched/pcpu/stats`** — Verify the ESXi host is fully booted and the monitoring service is running with `systemctl status vmware-stats`.
**Triage path:**

1. Correlate the latency spike time — was a snapshot being committed, a backup running, or a replication cycle active?
2. Check array-side performance counters (PowerMax Unisphere Performance, Pure1 Analytics, ONTAP Performance Manager).
3. Check queue depth — if `QAVG` in esxtop is consistently high, the array is saturated:

```bash
# Check queue depth for a device
esxcli storage core device list -d <naa.xxxx> | grep -i queue
```


```text title="Expected output"
Queue Depth: 32
Queue Depth Limit: 32
Queue Depth Threshold: 28
```

!!! warning "Common errors"
    **`Error: Unknown option or esxcli command 'storage core device list'`** — Verify you are running this command on an ESXi host with proper esxcli access, not on a vCenter server.
    **`Device <naa.xxxx> not found`** — Replace `<naa.xxxx>` with an actual NAA identifier from `esxcli storage core device list` output without the angle brackets.
4. Check for path imbalance — one path handling all I/O while others are idle.

---

## VMFS Lock — Failed to Lock the File

**Symptom:** VM fails to power on with "Failed to lock the file" or "Unable to access a file since it is locked."

```bash
# Identify which host holds the lock
vmkfstools -D /vmfs/volumes/<datastore>/<vm>/<vmdk>.vmdk
# Output shows the MAC address of the locking host

# Match MAC address to a hostname
esxcli network nic list | grep <mac-address>
```


```text title="Expected output"
Lock [type 10001c, val 00000000:00000000, hgen 0] [host 1, gen 247, mode 1, owner 1]
RO Lock [type 10001c, val 00000000:00000000, hgen 0] [host 2, gen 247, mode 1, owner 2]
LVID [1048576, 1048576, 0, 0] [host 1, gen 247, mode 1, owner 1]
Addr <4, 1048576>, gen 247, links [0, 0]
00:50:56:a1:2f:8c  vmnic0  Up     1000Mbps  Full    e1000  00:50:56:a1:2f:8c

Name       PCI Driver    Admin Status  Runtime Status  MTU  Enabled
vmnic0     0000:02:01.0 e1000         Up               1500 True
vmnic1     0000:02:02.0 e1000         Down             1500 False
```

!!! warning "Common errors"
    **`Unable to open VMDK file: No such file or directory`** — Verify the datastore name, VM folder path, and VMDK filename are correct and the file exists on the datastore.
    **`Could not find a matching NIC for MAC address`** — The MAC address from the lock output may be a vMotion or management NIC; cross-reference with `esxcli network ip interface list` or check the ESXi host's network configuration directly.
Once you identify the locking host:
- If that host is not running the VM, restart its management agents (`/etc/init.d/hostd restart`)
- If the locking host crashed, the lock is stale — power off the VM completely in vCenter, then power it back on

---

## vSAN Object Non-Compliant or Degraded

```bash
# Check vSAN health from ESXi
esxcli vsan health cluster list

# Check object compliance
esxcli vsan debug object list | grep -i "non-compliant\|absent\|degraded"

# Check active resync
esxcli vsan debug resync list
```


```text title="Expected output"
Cluster UUID: 52d4a8f1-7c2e-4d9a-b1e3-8f9c2a5d6e7f
Cluster Health: HEALTHY
Members: 4
Disk Groups: 4

Object UUID                          Compliance Status    Policy Compliance
52d4a8f1-7c2e-4d9a-b1e3-8f9c2a5d6e7f COMPLIANT            OK
7f6e5d4c-3b2a-1f0e-9d8c-7b6a5f4e3d2c NON-COMPLIANT        Policy mismatch
9c8b7a6f-5e4d-3c2b-1a0f-9e8d7c6b5a4f DEGRADED             1 component absent
4d3c2b1a-0f9e-8d7c-6b5a-4f3e2d1c0b9a COMPLIANT            OK

Resync UUID                          Object Count    Bytes Remaining    ETA
52d4a8f1-7c2e-4d9a-b1e3-8f9c2a5d6e7f 12              2147483648         00:45:30
7f6e5d4c-3b2a-1f0e-9d8c-7b6a5f4e3d2c 3               536870912          00:12:15
```

!!! warning "Common errors"
    **`vSAN health cluster list: Unknown command or namespace`** — Ensure you are running this command on an ESXi host with vSAN enabled and the vSAN license is active.
    **`grep: (standard input) is empty`** — Run `esxcli vsan debug object list` without grep first to verify the command executes; if empty, all objects are compliant.
    **`Error: The vSAN service is not running`** — Restart the vSAN service with `services.sh restart vsanmgmt` or check cluster membership with `esxcli vsan cluster get`.
| State | Meaning | Action |
|---|---|---|
| Non-compliant | Does not meet storage policy | Check if a host or disk is offline; restore host to restore compliance |
| Degraded | A component is missing — fault tolerance is used up | Restore the failed host/disk before another failure occurs |
| Absent | Component on a temporarily disconnected host | Resync starts automatically after the host reconnects |
| Inaccessible | Quorum lost — cannot read the object | Restore majority of cluster hosts; contact VMware GSS if unrecoverable |

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificate Issues](certificate-issue.md)
- [Host Disconnected / Not Responding](host-disconnected.md)
- [Known Issues and Fix Patterns](known-issues.md)
- [Virtualization Troubleshooting](index.md)
