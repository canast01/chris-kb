---
tags:
  - esxi
  - troubleshooting
  - vmware
  - vsphere-8
search:
  boost: 2
---
# ESXi — Common Issues

<div class="kb-summary">
Common Issues reference covering Resolution Steps, All Paths Down (APD) — Storage, High CPU Ready Time, High Memory Ballooning or Swapping, PSOD (Purple Screen of Death) and 3 more sections.

*Applies to: vSphere 7.x / 8.x*
</div>
![ESXi — Common Issues](../../../../assets/virtualization-vmware-esxi-troubleshooting-common-issues.svg)

ESXi Common Issue Resolution Paths

2. **Check for clock skew** — certificate validation fails if the host clock is more than 5 minutes off:

```bash
esxcli system ntp get
date
```

3. **Check for certificate mismatch** — if the host was recently reinstalled or had its cert replaced, vCenter may not trust the new cert. Reconnect via vCenter: **Right-click host → Reconnect**

4. **Check management network connectivity** — confirm vmk0 IP is reachable from vCenter:

```bash
ping <vmk0-ip>
esxcli network ip interface ipv4 get
```

5. **Full services restart** (higher risk — verify no active vMotion or provisioning):

```bash
services.sh restart
```

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
diagnostic_flow: "Diagnostic Flow" {shape: rectangle}
all_paths_down_apd_storage: "All Paths Down (APD) — Storage" {shape: rectangle}
high_cpu_ready_time: "High CPU Ready Time" {shape: rectangle}
high_memory_ballooning_or_swapping: "High Memory Ballooning or Swapping" {shape: rectangle}
psod_purple_screen_of_death: "PSOD (Purple Screen of Death)" {shape: rectangle}
vmfs_datastore_inaccessible: "VMFS Datastore Inaccessible" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> diagnostic_flow: investigate
symptom -> all_paths_down_apd_storage: investigate
symptom -> high_cpu_ready_time: investigate
symptom -> high_memory_ballooning_or_swapping: investigate
symptom -> psod_purple_screen_of_death: investigate
symptom -> vmfs_datastore_inaccessible: investigate
diagnostic_flow -> resolution
all_paths_down_apd_storage -> resolution
high_cpu_ready_time -> resolution
high_memory_ballooning_or_swapping -> resolution
psod_purple_screen_of_death -> resolution
vmfs_datastore_inaccessible -> resolution
```

## Diagnostic Flow

```d2
direction: right

S: "What is the symptom?" {shape: rectangle}
A: "Host shows PSOD" {shape: rectangle}
B: "Host disconnected in vCenter" {shape: rectangle}
C: "VM slow / high latency" {shape: rectangle}
D: "Storage inaccessible / APD" {shape: rectangle}
E: "Auth / certificate failure" {shape: rectangle}
A1: "Collect vmkernel.log + crash dump\nfrom DCUI or iDRAC" {shape: rectangle}
A2: "A2" {shape: rectangle}
A3: "Update driver or firmware\n→ PSOD section" {shape: rectangle}
A4: "Escalate to VMware GSS\nwith vm-support bundle" {shape: rectangle}
B1: "B1" {shape: rectangle}
B2: "Restart management agents\n→ Host Disconnected section" {shape: rectangle}
B3: "Check network / DNS / NTP\n→ Host Disconnected section" {shape: rectangle}
C1: "C1" {shape: rectangle}
C2: "→ High CPU Ready section" {shape: rectangle}
C3: "→ Memory Ballooning section" {shape: rectangle}
C4: "→ VMFS Inaccessible section" {shape: rectangle}
D1: "→ All Paths Down section" {shape: rectangle}
E1: "→ Certificate Thumbprint section" {shape: rectangle}

S -> A
S -> B
S -> C
S -> D
S -> E
A -> A1
A2 -> A3
A2 -> A4
B1 -> B2
B1 -> B3
C1 -> C2
C1 -> C3
C1 -> C4
D -> D1
E -> E1
```

---

## Before you begin

- **Access:** SSH to vCenter Shell and ESXi hosts; vSphere Client read access
- **Gather first:** recent error message text, event timestamps, and affected object names
- **Scope:** confirm whether the issue affects a single object, host, cluster, or site
- **Escalation:** open a vendor support ticket before running any destructive step
- **Logging:** document each command and output — required if escalation is needed

---

## All Paths Down (APD) — Storage

APD (All Paths Down) occurs when all storage paths to a LUN become unavailable. VMs using that LUN pause with I/O timeout errors.

### Diagnosis

```bash
# Check for dead paths
esxcli storage core path list | grep "State: dead"
esxcli storage core path list | grep -c "State: dead"

# Check for APD state
grep -i "APD\|all path\|PDL" /var/log/vmkernel.log | tail -20
```

| State | Meaning | Action |
|---|---|---|
| APD (All Paths Down) | Temporary — paths expected to return | Wait; ESXi will recover automatically when paths return |
| PDL (Permanent Device Loss) | Permanent — the LUN is gone | Power off VMs; storage remediation required |

### Resolution — APD

```bash
# Check HBA status
esxcli storage san fc list
esxcli storage san fc stats get -A vmhba0

# Rescan storage after fixing the underlying issue
esxcli storage core adapter rescan --all

# Verify paths are active again
esxcli storage core path list | grep -c "State: active"
```

Investigate the root cause: SAN fabric zoning, HBA driver, storage array port failure, or cable issue.

### Resolution — PDL

If the LUN is permanently lost (confirmed with the storage team), power off affected VMs and unregister them. Do not attempt to start VMs that have I/O to a PDL device — the disk writes will be lost.

---

## High CPU Ready Time

CPU Ready (`%RDY` in esxtop) indicates VM vCPUs waiting for a physical CPU to become available. Values above 10% per vCPU cause perceptible VM performance degradation.

### Diagnosis with esxtop

```bash
esxtop
# Press 'c' for CPU view
# Key columns: %RDY (ready), %CSTP (co-stop), %WAIT (waiting), %USED (actual CPU usage)
```

| Column | Normal | Investigate |
|---|---|---|
| `%RDY` per vCPU | < 5% | > 10% |
| `%CSTP` | ~0% | > 3% — vCPU co-scheduling issue |
| `%MLMTD` | 0% | > 0% — CPU limit configured on VM |

### Common Causes and Fixes

| Cause | Fix |
|---|---|
| Too many vCPUs on VM | Right-size the VM — reduce vCPUs to actual workload need |
| NUMA boundary crossing | Place VM on host with enough free NUMA node capacity; check NUMA topology |
| CPU limit set on VM | Remove the CPU limit in VM settings (limits cause artificial starvation) |
| Host overcommit | DRS migration or add hosts to cluster |
| Co-stop (CSTP) high | Reduce vCPU count — VMs with many vCPUs need simultaneous scheduling |

```powershell
# Find VMs with CPU ready > 10% via PowerCLI
Get-VM | Get-Stat -Stat cpu.ready.summation -Instance "" -Start (Get-Date).AddHours(-1) |
    Select-Object Entity, Value |
    Where-Object { $_.Value -gt 1000 } |    # 1000ms per 20s = ~5% ready
    Sort-Object Value -Descending
```

---

## High Memory Ballooning or Swapping

Memory balloon (`MCTLSZ` in esxtop) and swap (`SWR/s`, `SWW/s`) indicate memory overcommitment on the host.

### Diagnosis

```bash
esxtop
# Press 'm' for Memory view
# Key columns: MCTLSZ (balloon driver active), SWR/s, SWW/s (swap activity)
# SWCUR (current swap used by VM), SWTGT (swap target)
```

### Memory Reclamation Hierarchy

ESXi uses memory reclamation in this order (least impactful to most impactful):

1. **Transparent Page Sharing (TPS)** — deduplicate identical memory pages
2. **Ballooning** — VMCI balloon driver causes guest OS to swap its own memory
3. **Host swap** — ESXi swaps VM memory to the host's swap file (vmx-.vswp)
4. **Host cache swap** — uses SSD as swap tier

Ballooning is expected and acceptable. Active host swapping (non-zero SWR/s, SWW/s) is a performance problem requiring immediate attention.

### Resolution

```bash
# Check memory reservation on the host
esxcli system stats memory get

# Identify which VMs are ballooning most
# In esxtop: sort by MCTLSZ descending (key: shift+S → column name)
```

Options:
- Migrate VMs off the host with DRS
- Add memory to host (requires maintenance mode)
- Set memory reservation on critical VMs (prevents ballooning for those VMs)
- Remove memory overcommit by reducing total vRAM allocated across cluster

---

## PSOD (Purple Screen of Death)

PSOD is an ESXi kernel panic. The host halts and displays a purple screen with a backtrace.

### Immediate Actions

1. If IPMI/iDRAC is available: take a screenshot of the PSOD screen — the backtrace is needed for support
2. Reboot the host (physical power cycle or IPMI reboot)
3. After reboot, collect the core dump:

```bash
# Core dumps are stored here
ls -lh /var/core/
ls -lh /vmfs/volumes/<scratch-datastore>/vmkdump/

# Identify the most recent vmkernel dump
find /vmfs/volumes/ -name "*.dumpFile" -newer /etc -ls 2>/dev/null | tail -5
```

4. Generate a support bundle before further investigation:

```bash
vm-support -w /tmp/
```

5. Open a P1 case with Broadcom Support, providing:
   - PSOD screenshot (exact panic string, offset, and module)
   - vmkernel core dump file
   - ESXi support bundle
   - Hardware model and recent driver/firmware changes

### Common PSOD Causes

| Panic String Pattern | Likely Cause |
|---|---|
| `NMI IPI` | Hardware error (CPU, memory, PCIe) |
| `ASSERT` in NMP / storage module | Storage driver bug |
| `ASSERT` in network module | NIC driver bug |
| `Out of memory` | Memory leak in driver or kernel module |
| No panic string (black screen reset) | Hardware fault, IPMI |

After a PSOD, compare recent hardware changes, driver updates, or VIB installations.

---

## VMFS Datastore Inaccessible

### Scenarios

| Scenario | Symptom | First Check |
|---|---|---|
| APD | Datastore greyed out; VMs paused | `esxcli storage core path list \| grep dead` |
| Mount failure | Datastore missing after reboot | `esxcli storage vmfs extent list` |
| Snapshot delta chain corruption | Consolidation error | `vim-cmd vmsvc/snapshot.get <vmid>` |
| VMFS header corruption | Datastore UUID mismatch | `vmkfstools -P /vmfs/volumes/<ds>` |

### Rescan and Remount

```bash
# Rescan all adapters
esxcli storage core adapter rescan --all

# List VMFS filesystems and mount state
esxcli storage filesystem list | grep -v "^Name"

# Mount a VMFS volume that appears unmounted
esxcli storage filesystem mount -v <volume-uuid>
```

### Recover from Snapshot Consolidation Failure

```bash
# Check snapshot chain
vim-cmd vmsvc/snapshot.get <vmid>

# Remove all snapshots (destructive — only if the snapshot content is no longer needed)
vim-cmd vmsvc/snapshot.removeall <vmid>

# If snapshots cannot be removed via API, check for orphaned delta files
find /vmfs/volumes/<datastore>/<vm-folder>/ -name "*-delta.vmdk" -o -name "*-0000*.vmdk"

# Consolidate via PowerCLI
Get-VM "<vm-name>" | Invoke-VMConsolidation
```

---

## NTP Drift Causing Authentication Failures

Clock skew causes certificate validation failures, SSO authentication errors, and AD join failures.

### Check NTP Status

```bash
# NTP service state
esxcli system ntp get

# Current NTP peer status (ntpq)
ntpq -p
# Look for '*' (synced peer) or '+' (candidate)
# offset column: drift in milliseconds — should be < 500ms

# Host clock
date
```

### Fix NTP Configuration

```bash
# Set NTP servers (replace with your NTP infrastructure)
esxcli system ntp set --server=ntp1.example.local --server=ntp2.example.local --enabled=true

# Restart NTP daemon
/etc/init.d/ntpd restart

# Force time synchronisation immediately
ntpdate ntp1.example.local

# Verify
ntpq -p
```

If the ESXi host is a VM guest (rare in production), disable host-time synchronisation in the VM settings and use NTP independently.

---

## Certificate Thumbprint Mismatch

After re-deploying a host or replacing its SSL certificate, vCenter may refuse to reconnect due to a thumbprint mismatch.

### Resolution

1. In vCenter: **Right-click host → Reconnect**
2. When prompted about the new thumbprint, review and accept
3. Or remove and re-add the host: **Right-click host → Remove** → **Add Host** (preserves VMs if in the same datacenter)

```powershell
# PowerCLI — force reconnect all disconnected hosts
Get-VMHost | Where-Object {$_.ConnectionState -eq "Disconnected"} | ForEach-Object {
    Connect-VMHost -VMHost $_ -Confirm:$false
}
```

For bulk certificate replacement across all hosts, use vCenter Certificate Manager or vSphere Lifecycle Manager certificate remediation.

---

## See also

- [Cluster Services — Internals](../../../internals/cluster-services/)
- [HA Deep Dive — Internals](../../../internals/ha-deep-dive/)
- [Scenarios — ESXi Host Disconnected](../../../topics/scenarios/esxi-host-disconnected/)

---

## Verify resolution

- **Alarms cleared:** Home → Alarms — the triggering alarm is no longer active
- **Event log:** confirm no new related error events in the last 5 minutes
- **Functional test:** perform the action that was failing (connect, vMotion, storage I/O) — confirm it succeeds
- **Monitor:** leave the vSphere Client open for 10 minutes and confirm the issue does not recur
