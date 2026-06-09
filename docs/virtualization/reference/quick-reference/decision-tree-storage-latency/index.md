# Decision Tree: Storage Latency


<div class="kb-summary">
Use this when VMs are slow, I/O latency is elevated in monitoring, or vSAN latency alarms trigger.
</div>

```text
               Latency alert / VM storage slow
                              │
                              ▼
               ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
               │ esxtop: GAVG > 20ms?         │
               │ DAVG > 5ms?  KAVG > 2ms?     │
               └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
                              │
               ┌────────────────────────────────────────────────── ┼ ──────────────────────────────────────────────────┐
               ▼              ▼              ▼
        ┌───────────────────────────────────────── ┐ ┌────────────┐ ┌ ──────────────────────────────────────────┐
        │ vSAN active│ │ Array      │ │ Network /      │
        │ resync?    │ │ health OK? │ │ HBA fabric?    │
        │ Throttle   │ │ Check ctrl │ │ vmkping vSAN   │
        │ resync     │ │ CPU/queue  │ │ FC HBA stats   │
        └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
               │
               ▼
        ┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
        │ Hot-spot VM?  esxtop MBRS/MBWS  │
        │ Snapshot chain > 3 deep?        │
        │ Backup job running against VM?  │
        └───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```
## Step 1 — Confirm Latency Baseline Breach

```bash
# On ESXi host — check current device latency
esxtop -b -n 1 | grep -E "DAVG|KAVG|GAVG" | sort -k7 -n -r | head -20
# GAVG (guest average) > 20ms = elevated
# DAVG (device average) > 5ms = elevated
# KAVG (kernel average) > 2ms = kernel queue issues
```

Via Aria Operations: vSphere → Datastores → select datastore → Performance → I/O Latency.

## Step 2 — Is vSAN Resync Active?

```bash
esxcli vsan debug resync summary
# If bytes_remaining > 0, resync is ongoing and contributing to latency
```

**Active resync causing latency:**
→ Throttle resync: `esxcli vsan debug resync throttle -p 25`
→ Wait for resync to complete before performing additional storage changes
→ If resync is unexpectedly large: check if a disk or host just returned from failure

## Step 3 — Check Storage Array Health

**For vSAN:**
```bash
esxcli vsan health cluster list | grep -v Green   # Disk health warnings?
esxcli vsan debug controller list                  # Controller health?
```

**For external storage (NFS/iSCSI/FC):**
- Log in to array management (Unisphere, ONTAP, Pure FlashArray)
- Check array-level latency, queue depth, and controller CPU utilisation
- Check backend disk response time (array-internal metric)

**For Pure FlashArray specifically:**
```bash
# Via REST API or purearray CLI
purearray get   # Throughput and latency summary
```

## Step 4 — Check Network / Fabric

For vSAN: high network latency on the vSAN VMkernel can cause I/O latency:
```bash
# Test vSAN network latency between hosts
vmkping -I vmk1 <other-host-vsan-vmk-ip>   # <1ms expected on 10GbE
```

For FC (iSCSI/FC block storage): check HBA port statistics:
```bash
esxcli storage san fc stats get
# Look for: Link failures, Tx/Rx errors, queue_depth exhaustion
```

## Step 5 — Check for Hot-Spot VMs

High I/O from a single VM can saturate a datastore or disk group:

```bash
# Identify top I/O consumers
esxtop -b -n 1 | grep -E "Virtual Machine|MBRS|MBWS" | head -20

# Sort by GAVG in esxtop interactive mode: press 'u' → sort by GAVG
```

If a single VM is driving all the I/O:
- Check if the VM has a stuck snapshot (common cause of write amplification)
- Check if a backup job is running hot-backup against this VM right now

## Step 6 — Snapshot Chain

Long snapshot chains dramatically increase latency on writes:

```powershell
Get-VM | Where-Object {$_.ExtensionData.Snapshot} | Get-Snapshot |
    Where-Object {$_.SizeMB -gt 10240} |
    Select-Object VM, Name, Created, SizeMB
```

VMs with snapshot chains > 3 deep or snapshots older than 24 hours during normal operation should be investigated immediately.

## Escalation

If storage latency persists > 30 minutes with no obvious cause:
1. Generate vSAN support bundle: vCenter → Cluster → Monitor → vSAN → Support → Generate Bundle
2. Capture esxtop output: `esxtop -b -n 30 > /tmp/esxtop_$(date +%Y%m%d_%H%M).txt`
3. Open SR with VMware or storage vendor as appropriate
