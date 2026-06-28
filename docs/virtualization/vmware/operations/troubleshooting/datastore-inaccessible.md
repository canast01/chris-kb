---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
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

---

## High Datastore Latency

Latency over 20ms for VMFS/SAN or 30ms for NFS is a concern. Over 50ms will impact most workloads.

```bash
# Check per-device latency from ESXi using esxtop
esxtop
# Press 'u' for storage device view — look at GAVG (guest average latency in ms)
# KAVG = kernel latency, DAVG = device latency; GAVG = KAVG + DAVG
```

**Triage path:**

1. Correlate the latency spike time — was a snapshot being committed, a backup running, or a replication cycle active?
2. Check array-side performance counters (PowerMax Unisphere Performance, Pure1 Analytics, ONTAP Performance Manager).
3. Check queue depth — if `QAVG` in esxtop is consistently high, the array is saturated:

```bash
# Check queue depth for a device
esxcli storage core device list -d <naa.xxxx> | grep -i queue
```

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
