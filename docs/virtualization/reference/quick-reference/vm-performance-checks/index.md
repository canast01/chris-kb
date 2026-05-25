# VM Performance Quick Checks

When a VM is reported as slow, check these in order:

```text
┌──────────────┬───────────────────────────┬──────────────────────────────┐
│  Metric      │  esxtop Field / Location  │  Threshold / Action          │
├──────────────┼───────────────────────────┼──────────────────────────────┤
│ CPU Ready    │ esxtop → %RDY             │ > 5% → contention, check DRS │
│ CPU Usage    │ esxtop → %USED            │ > 90% sustained → rightsize  │
│ Mem Balloon  │ esxtop → MCTLSZ           │ > 0 → host memory pressure   │
│ Mem Swap     │ esxtop → SWR/SWW          │ > 0 → critical, add memory   │
│ Disk DAVG    │ esxtop → DAVG/cmd         │ > 5ms → array or path issue  │
│ Disk GAVG    │ esxtop → GAVG/cmd         │ > 20ms → investigate storage │
│ Net drops    │ esxtop → DRPTX/DRPRX      │ > 0 → vDS config or uplink   │
│ Tools state  │ vCenter VM Summary        │ Not current → update Tools   │
├──────────────┴───────────────────────────┴──────────────────────────────┤
│  Start esxtop: SSH to host → esxtop  │  Press 'u' = disk  'd' = adapter │
└─────────────────────────────────────────────────────────────────────────┘
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
