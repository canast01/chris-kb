# ESXi — Common Issues

## Quick Reference

| Symptom | First Check | Key Command |
|---|---|---|
| Host disconnected from vCenter | vpxa / hostd service | `/etc/init.d/vpxa restart` |
| Host not responding | PSOD, mgmt network partition | IPMI/iLO console access |
| All paths down (APD) | Storage fabric, HBA | `esxcli storage core path list` |
| VMFS datastore inaccessible | APD/PDL state, rescan | `esxcli storage core adapter rescan --all` |
| High CPU ready | NUMA, DRS, overcommit | `esxtop` — `%CSTP`, `%RDY` |
| High balloon / swap | Memory overcommit | `esxtop` — `MCTLSZ`, `SWR/s` |
| NTP drift | Clock skew, auth failures | `esxcli system ntp get` |
| PSOD | Hardware fault, driver bug | `/var/core/` vmss/vmem dumps |
| VM stuck in consolidate | Snapshot delta chain | `vim-cmd vmsvc/snapshot.removeall <vmid>` |
| Dead storage paths | HBA, SAN fabric, zoning | `esxcli storage core path list \| grep dead` |
| vCenter loses host trust | Certificate mismatch | Reconnect host from vCenter |
| SSH blocked after lockdown | Lockdown mode enabled | DCUI → Lockdown Mode |

---

## Host Disconnected from vCenter

### Symptoms

- Host shows `Disconnected` or `Not Responding` in vCenter
- vCenter cannot start tasks on the host
- VMs still running on the host (data plane unaffected)

### Diagnosis

```bash
# Can you SSH or reach the DCUI console?
# If yes — check management agents

# Check hostd status
/etc/init.d/hostd status

# Check vpxa (vCenter agent) status
/etc/init.d/vpxa status

# Review log errors
tail -100 /var/log/hostd.log | grep -i "error\|fail"
tail -100 /var/log/vpxa.log | grep -i "error\|disconnected\|cert"
```

### Resolution Steps

1. **Restart management agents** (attempt first — low risk, no VM impact):

```bash
/etc/init.d/hostd restart
/etc/init.d/vpxa restart
```

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
esxcli system ntp set --server=ntp1.corp.local --server=ntp2.corp.local --enabled=true

# Restart NTP daemon
/etc/init.d/ntpd restart

# Force time synchronisation immediately
ntpdate ntp1.corp.local

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
