# VM Performance Issues


<div class="kb-summary">
Part of the [Troubleshooting](../index.md) hub.
</div>
```text
┌────────────────────────────── Virtualization Operations Troubleshooting ──────────────────────────────┐
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │                 Operations: Virtualization Operations Troubleshooting platform                │   │
│   │                                  Protocols: Various protocols                                 │   │
│   │            Management: Virtualization Operations Troubleshooting management console           │   │
│   │                Sections: Architecture · Operations · Security · Troubleshooting               │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Architecture → Operations → Security → Troubleshooting → Escalation                                │
│                                                                                                       │
│                  ▼                                ▼                                ▼                  │
│                                                                                                       │
│   ┌─────────────────────────────┐  ┌─────────────────────────────┐  ┌─────────────────────────────┐   │
│   │            Layer            │  │          Component          │  │            Notes            │   │
│   │             Core            │  │       Primary service       │  │        Main function        │   │
│   │          Management         │  │        Control plane        │  │         Admin access        │   │
│   │          Monitoring         │  │         Health/perf         │  │      Alerts/dashboards      │   │
│   │           Security          │  │         Auth/encrypt        │  │        Access control       │   │
│   │         Integration         │  │        APIs/plug-ins        │  │         Third-party         │   │
│   └─────────────────────────────┘  └─────────────────────────────┘  └─────────────────────────────┘   │
│                                                                                                       │
│                          ▼                                                 ▼                          │
│                                                                                                       │
│   ┌───────────────────────────────────────────────────────────────────────────────────────────────┐   │
│   │      Layer       │    Component     │      Function     │      Notes       │       Auth       │   │
│   │       Core       │ Primary service  │   Main function   │     See docs     │       RBAC       │   │
│   │    Management    │  Control plane   │    Admin access   │     See docs     │       RBAC       │   │
│   │    Monitoring    │   Health/perf    │  Alerts/dashboard │     See docs     │       RBAC       │   │
│   │     Security     │   Auth/encrypt   │   Access control  │     See docs     │       RBAC       │   │
│   └───────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                       │
│    Physical: Virtualization Operations Troubleshooting infrastructure · management network · monitor  │
│                                                                                                       │
│    Key terms:                                                                                         │
│                                                                                                       │
│    Operations         = Virtualization Operations Troubleshooting platform overview and core concept  │
│    Management         = management console and command-line interface for administration              │
│    Monitoring         = health and performance monitoring dashboards and alerting                     │
│    Automation         = REST API, scripting, and pipeline integration capabilities                    │
│    Security           = access control, authentication, and encryption configuration                  │
│    Backup             = backup and recovery procedures and schedule configuration                     │
│    Upgrade            = software version upgrades and firmware patching procedures                    │
│    Troubleshooting    = diagnostic procedures and common issue resolution steps                       │
│    Escalation         = vendor support escalation path and severity triage process                    │
│    Documentation      = vendor knowledge base and official product documentation                      │
│    Change management  = change ticket requirements for production modifications                       │
│    Audit log          = admin action logging for compliance and security review                       │
│                                                                                                       │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


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
