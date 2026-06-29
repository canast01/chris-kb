---
tags:
  - reference
---
# VM Performance Quick Checks

<div class="kb-summary">
VM performance quick checks: CPU ready %, memory balloon/swap, storage latency via `esxtop`, network packet drops, and vSAN resync — run in this order for slow VM triage.

*Applies to: vSphere 7.x / 8.x*
</div>

```d2
direction: down

cpu: "CPU" {shape: rectangle}
memory: "Memory" {shape: rectangle}
storage: "Storage" {shape: rectangle}
network: "Network" {shape: rectangle}
recent_changes: "Recent Changes" {shape: rectangle}
quick_commands_from_esxi: "Quick Commands from ESXi" {shape: rectangle}

cpu -> memory: uses
memory -> storage: uses
storage -> network: uses
network -> recent_changes: uses
recent_changes -> quick_commands_from_esxi: uses
```

## CPU

- **CPU Ready** — time the VM is waiting for a physical CPU. Above 5% is worth investigating.
- **CPU Usage** — high usage may indicate the VM needs more vCPUs or the guest application is busy.

## Memory

- **Memory Ballooning** — VMware is reclaiming memory from this VM. Indicates memory pressure on the host.
- **Memory Swapping** — severe memory pressure. The VM's memory is being swapped to disk.

## Storage

- **Datastore Latency** — above 20ms is worth investigating. Check the storage array and paths.
- **Snapshot Age** — old or large snapshots degrade VM storage performance.
- **Guest Disk Usage** — confirm the guest OS disk is not full.

## Network

- **Packet Drops** — check the VM's NIC stats and the physical switch port.
- **VMware Tools** — confirm Tools is installed and current; outdated Tools can cause NIC performance issues.

## Recent Changes

- Was the VM migrated recently?
- Was the host patched or rebooted?
- Was a snapshot taken?
- Was a storage vMotion performed?

## Quick Commands from ESXi

```bash
# Check VM disk stats (run from the ESXi host)
esxtop
# Press 'u' for storage view, 'd' for disk adapter view
```


```text title="Expected output"
ESXTOP - Virtual Machine Monitor Performance Monitor
Press 'h' for help, 'q' to quit
CPU MEMORY NETWORK DISK ADAPTER STORAGE POWER

PCPU USED(%): 45.2  PCPU RUN(%): 12.8  PCPU WAIT(%): 2.1
VMKERNEL MEM: 2048 MB  VM MEM: 28672 MB  FREE: 1024 MB

DISK ADAPTER VIEW
Adapter      CMDS/s  READS/s  WRITES/s  MBPS/s  LATENCY(ms)
vmhba0       125.4   45.2     80.1      234.5   2.3
vmhba1       89.3    32.1     57.2      156.8   1.8
vmhba2       12.1    5.3      6.8       18.2    0.9

STORAGE VIEW
Datastore              READS/s  WRITES/s  MBPS/s  LATENCY(ms)
datastore1-ssd         234.5    189.3     1024.2  1.2
datastore2-sata        45.2     23.1      156.8   4.5
datastore3-nfs         12.3     8.9       45.1    8.7
```

!!! warning "Common errors"
    **`esxtop: command not found`** — Ensure you are logged into an ESXi host directly via SSH (not vCenter); esxtop is only available on ESXi.
    **`Error: Unable to initialize display`** — Set the DISPLAY variable or use esxtop in batch mode with `esxtop -b -n 1` if running remotely.