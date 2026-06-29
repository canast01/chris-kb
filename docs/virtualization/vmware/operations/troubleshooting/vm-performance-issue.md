---
tags:
  - operations
  - troubleshooting
search:
  boost: 1.5
---
# VM Performance Issues

<div class="kb-summary">
Diagnosing VM performance degradation across the VMware stack — CPU ready, memory balloon, storage latency, and network saturation. Covers esxtop analysis, vSAN I/O queues, and NSX DFW overhead.

*Applies to: vSphere 7.x / 8.x*
</div>

---

```d2
direction: down

symptom: Identify Symptom {shape: diamond}
vm_will_not_power_on: "VM Will Not Power On" {shape: rectangle}
vm_is_slow_cpu: "VM Is Slow — CPU" {shape: rectangle}
vm_is_slow_memory: "VM Is Slow — Memory" {shape: rectangle}
vm_is_slow_disk: "VM Is Slow — Disk" {shape: rectangle}
vm_lost_network: "VM Lost Network" {shape: rectangle}
vm_disk_full_guest_os_level: "VM Disk Full (Guest OS Level)" {shape: rectangle}
resolution: Resolve or Escalate {shape: oval}

symptom -> vm_will_not_power_on: investigate
symptom -> vm_is_slow_cpu: investigate
symptom -> vm_is_slow_memory: investigate
symptom -> vm_is_slow_disk: investigate
symptom -> vm_lost_network: investigate
symptom -> vm_disk_full_guest_os_level: investigate
vm_will_not_power_on -> resolution
vm_is_slow_cpu -> resolution
vm_is_slow_memory -> resolution
vm_is_slow_disk -> resolution
vm_lost_network -> resolution
vm_disk_full_guest_os_level -> resolution
```

## Before you begin

- **Access:** Admin credentials on all affected systems
- **Timing:** safe to run during business hours unless a step is marked ⚠ (causes interruption)
- **Dependencies:** no active upgrades or migrations on the same infrastructure
- **Logging:** capture command output — paste into the change record on completion

---

## VM Will Not Power On

**Step 1 — Check the error message in vCenter Tasks** — it usually tells you exactly what failed.

Common errors and resolutions:

| Error | Cause | Resolution |
|---|---|---|
| Insufficient disk space on datastore | Datastore full or thin disk cannot expand | Free space on the datastore |
| Failed to lock the file | Another host holds a stale lock on a VMDK | Identify the locking host with `vmkfstools -D`; restart hostd there |
| No compatible host found | DRS cannot place the VM (HA, resource reservation, affinity rules) | Check cluster resources; check affinity/anti-affinity rules |
| Configuration file not found | VMX file missing or datastore inaccessible | Check datastore health; re-register the VM from its VMX file |
| Cannot open the disk — SCSI device busy | Snapshot delta VMDK held by another process | Run VM consolidation first |

**Step 2 — Check the host where the VM is being placed** for resource availability:

```powershell
# PowerCLI — check host CPU and memory
Get-VMHost | Select Name, CpuUsageMhz, CpuTotalMhz, MemoryUsageGB, MemoryTotalGB
```

---

## VM Is Slow — CPU

**CPU Ready** is the key metric. It measures how long a vCPU was ready to run but waiting for a physical CPU.

- Under 5% — normal
- 5–10% — investigate; may impact latency-sensitive workloads
- Over 10% — significant contention; action required

```bash
# Check CPU ready from esxtop
esxtop
# Press 'c' for CPU view — look at %RDY column per VM/vCPU
```


```text title="Expected output"
CPU STATS - esxtop interactive mode
GID  NAME                                   PCPU  %USED  %RDY  %SYS  %WAIT
  1  vcpu-0:web-prod-01                      0    45.2   8.3   2.1  44.4
  2  vcpu-1:web-prod-01                      1    52.1  12.7   1.8  33.4
  3  vcpu-0:db-cluster-02                    2    78.9   3.2   1.5  16.4
  4  vcpu-1:db-cluster-02                    3    81.4   2.1   1.2  15.3
  5  vcpu-0:app-cache-03                     4    38.5  18.9   2.3  40.3
  6  vcpu-1:app-cache-03                     5    41.2  22.1   2.1  34.6
  7  vcpu-0:monitoring-04                    6    15.3   1.2   0.8  82.7
  8  vcpu-1:monitoring-04                    7    16.8   0.9   0.9  81.4
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are running this command directly on an ESXi host via SSH or console, not from vCenter Server.
    **`Unable to open /proc/vmware/sched/cpu: Permission denied`** — Run esxtop with root privileges or as a user with administrative permissions on the ESXi host.
**Resolutions:**

- Reduce vCPU count on oversized VMs (a 16-vCPU VM may schedule worse than an 8-vCPU VM on a 20-core host)
- Check NUMA topology — a VM spanning NUMA nodes suffers remote memory access latency
- Migrate the VM off a saturated host via vMotion

---

## VM Is Slow — Memory

```bash
# esxtop memory view
esxtop
# Press 'm' for memory — look at MCTLSZ (balloon), SWCUR (swap current), LLSWR (swap read rate)
```


```text title="Expected output"
ESXTOP - VMware ESXi performance monitoring tool
Press 'h' for help, 'q' to quit
────────────────────────────────────────────────────────────────────────────────
Memory Stats (m pressed):
PMEM:16384MB  FREE:2847MB  PMEM%:17.4  VMKMEM:2156MB  VMKSWAP:512MB
MCTLSZ:4521MB  SWCUR:1247MB  LLSWR:12.3MB/s  LLSWW:8.7MB/s  MEMCTL:3891MB
────────────────────────────────────────────────────────────────────────────────
WORLD    NAME                    PMEM    VMEM    MCTLSZ   SWCUR   LLSWR
2048     vm-prod-web-01          4096    6144    892      156     2.1
2156     vm-prod-db-02           8192    10240   2156     487     5.8
2287     vm-dev-test-03          2048    3072    412      89      1.2
2401     vm-backup-04            1024    2048    61       0       0.0
────────────────────────────────────────────────────────────────────────────────
Press 'q' to exit esxtop
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are logged into an ESXi host directly via SSH (not vCenter); esxtop is a local ESXi utility.
    **`Cannot open /proc/vmware/sched/cpu: Permission denied`** — Run esxtop with root privileges or as a user with administrative ESXi permissions.
Key indicators:

| Metric | Meaning |
|---|---|
| MCTLSZ > 0 | VMware balloon driver is reclaiming memory from the VM |
| SWCUR > 0 | VM memory is being swapped to disk — severe performance impact |
| LLSWR > 0 | Active swap reads from disk — immediate impact on all VM operations |

**Resolutions:**

- If SWAP is active: the host is severely memory-overcommitted — migrate VMs to a less loaded host
- If BALLOON is active: consider adding memory to the host or reducing VM memory reservations
- Check if VMware Tools is installed — balloon driver requires VMware Tools

---

## VM Is Slow — Disk

```bash
# esxtop storage view
esxtop
# Press 'u' for storage — look at GAVG (guest average latency in ms)
# KAVG (kernel queue latency) + DAVG (device latency) = GAVG
```


```text title="Expected output"
CPU  MEMORY NETWORK DISK SWAP MODULES                                    12:34:56
0    0      0      0    0    0
ADAPTER  NPATHS  QFULL  WORLD  GAVG  KAVG  DAVG  LOAD  %BUSY
vmhba0   4       0      128    2.45  0.32  2.13  45%   67%
vmhba1   2       0      64     1.89  0.28  1.61  32%   54%
vmhba2   8       0      256    5.67  1.23  4.44  78%   89%
vmhba3   4       0      128    3.12  0.45  2.67  52%   71%

(Press 'q' to exit esxtop)
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are running this command directly on an ESXi host (SSH session), not from vCenter; esxtop is ESXi-only.
    **`Error: Cannot open /proc/vmware/sched/pcpu`** — Verify the ESXi host is fully booted and the hostd service is running with `systemctl status hostd`.
    **`Permission denied`** — Run esxtop as root or a user with administrative privileges; use `su -` or ensure your SSH user has root access.
- Under 10ms GAVG — normal for most workloads
- 10–20ms — acceptable for non-latency-sensitive workloads
- Over 20ms — investigate array-side performance

Also check for snapshots — even a single large snapshot delta can cause significant I/O overhead during commit operations:

```powershell
# Find VMs with snapshots
Get-VM | Get-Snapshot | Select VM, Name, Created, SizeGB
```

---

## VM Lost Network

**Step 1 — Confirm from inside the guest** that the NIC is up and has an IP:

```cmd
# Windows guest
ipconfig /all
ping <gateway>

# Linux guest
ip addr show
ping <gateway>
```

**Step 2 — Check the virtual NIC in vCenter** — is it connected?

```powershell
Get-VM "VMName" | Get-NetworkAdapter | Select Name, NetworkName, ConnectionState, MacAddress
```

**Step 3 — Check the port group** — has the VLAN ID changed or has the port group been removed?

```bash
# From ESXi
esxcli network vswitch dvs vmware portgroup list | grep -A5 "PortgroupName"
```


```text title="Expected output"
PortgroupName: VM Network
   VLAN ID: 0
   Uplink Portgroup: false
   Portgroup Type: earlyBinding
   Bound VMs: 12

PortgroupName: vMotion
   VLAN ID: 100
   Uplink Portgroup: false
   Portgroup Type: earlyBinding
   Bound VMs: 0

PortgroupName: Management Network
   VLAN ID: 1
   Uplink Portgroup: false
   Portgroup Type: earlyBinding
   Bound VMs: 3
```

!!! warning "Common errors"
    **`Error: Unknown command or namespace network.vswitch.dvs.vmware.portgroup.list`** — Verify the ESXi version supports DVS commands; use `esxcli network vswitch standard portgroup list` for standard vSwitches instead.
    **`Error: Unable to connect to management daemon`** — Restart the hostd service with `services.sh restart` or reboot the ESXi host.
**Step 4 — Check for MAC address conflict** — duplicate MAC addresses on the same VLAN will cause flapping.

---

## VM Disk Full (Guest OS Level)

This is a guest OS issue, but often manifests as VM slowness first (writes begin failing, applications error).

**Windows:**

```powershell
# Find large files (run inside the guest)
Get-ChildItem C:\ -Recurse -ErrorAction SilentlyContinue | Sort-Object Length -Descending | Select -First 20 FullName, Length
```

Common causes: IIS log files, Windows Update cache (`C:\Windows\SoftwareDistribution`), application logs, user profile data.

**Linux:**

```bash
# Find top disk consumers
du -sh /* 2>/dev/null | sort -rh | head -20
du -sh /var/log/* | sort -rh | head -10
```


```text title="Expected output"
16G	/var
12G	/usr
8.5G	/home
4.2G	/opt
3.1G	/boot
2.8G	/tmp
1.9G	/srv
1.2G	/lib
892M	/etc
512M	/root
256M	/dev
128M	/sys
64M	/proc
32M	/run
16M	/mnt
8M	/media

2.3G	/var/log/vmware
1.8G	/var/log/audit
956M	/var/log/messages
512M	/var/log/syslog
384M	/var/log/kern.log
256M	/var/log/auth.log
128M	/var/log/httpd
64M	/var/log/mysql
```

!!! warning "Common errors"
    **`du: cannot read directory '/proc/kcore': Permission denied`** — Run the command with `sudo` or redirect stderr to /dev/null (already done in the first command).
    **`du: cannot access '/var/log/vmware': Permission denied`** — Execute with `sudo du -sh /var/log/*` to access restricted log directories.
**Extending the VMDK (hot-extend):**

```powershell
# Extend VMDK from vCenter (PowerCLI) — VM does not need to be powered off for thin disks
Get-VM "VMName" | Get-HardDisk -Name "Hard disk 1" | Set-HardDisk -CapacityGB <new-size> -Confirm:$false
```

After extending the VMDK, the guest OS disk partition also needs to be extended:
- **Windows:** Disk Management → Extend Volume, or `diskpart`
- **Linux:** `growpart /dev/sda 1` then `resize2fs /dev/sda1` (ext4) or `xfs_growfs /` (XFS)

---

## VMware Tools Warning

Outdated or missing VMware Tools causes: balloon driver not working (memory management fails), quiesced snapshots fail, VM network adapter type warnings, and vCenter console slowness.

```powershell
# Check VMware Tools status across all VMs
Get-VM | Select Name, @{N="ToolsStatus";E={$_.ExtensionData.Guest.ToolsStatus}},
  @{N="ToolsVersion";E={$_.ExtensionData.Guest.ToolsVersion}} |
  Where-Object {$_.ToolsStatus -ne "toolsOk"}
```

Update VMware Tools:
- **Windows:** Right-click VM in vCenter → Guest OS → Install/Upgrade VMware Tools → follow the wizard
- **Linux:** `vmware-toolsd --version` then update via package manager (open-vm-tools) or VMware installer

---

## Verify

- Confirm the operation completed without errors in the log or management UI
- Verify the expected state change is visible (service running, object created, config applied)
- Document the outcome in the change record

## See also

- [Certificate Issues](certificate-issue.md)
- [Datastore Issues](datastore-inaccessible.md)
- [Host Disconnected / Not Responding](host-disconnected.md)
- [Virtualization Troubleshooting](index.md)
