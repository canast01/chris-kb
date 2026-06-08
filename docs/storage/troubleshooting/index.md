# Storage — Troubleshooting

<div class="kb-summary">
Storage troubleshooting — APD/PDL conditions, multipath failures, replication lag, snapshot failures, host I/O errors, and array health alerts.
</div>

## Symptom Index

| Symptom | Likely Cause | First Command |
|---|---|---|
| All Paths Down (APD) in vCenter | Fabric or array outage | `esxcli storage core path list` |
| Permanent Device Loss (PDL) | LUN removed or array offline | Check array health; check zoning |
| Multipath path degraded | HBA or switch port issue | `multipath -ll` (Linux) |
| I/O latency spike | Overloaded storage pool; dedup/compression | Check array I/O stats |
| Snapshot job failing | Snapshot policy conflict; quota exceeded | Check array event log |
| Replication lag growing | WAN bandwidth; source I/O rate high | Check replication stats on array |
| Filesystem read-only | Underlying LUN error; I/O timeout | `dmesg | grep -i 'error\|read-only\|EXT4-fs'` |

## Linux Host I/O Diagnostics

```bash
# Check for multipath failures
multipath -ll
dmesg | grep -i 'scsi\|sd[a-z]\|mpath\|failed'

# I/O error log
journalctl -k | grep -i 'error\|i/o error\|EXT4\|XFS' | tail -50

# Check disk queue depth and wait
iostat -xz 1 5
# await > 20ms on SSD is abnormal

# Check LUN presence
lsblk; ls -la /dev/mapper/
```

## VMware APD Recovery

```bash
# Rescan datastores after fabric restoration
esxcli storage core adapter rescan --all
esxcli storage core path list | grep -E 'State:|Device:|Adapter:'

# If APD persists after fabric is restored:
# 1. Put host in maintenance mode
# 2. Remove and re-add storage adapter in vCenter
# 3. Rescan
```

## Replication Lag Diagnosis

```bash
# Pure FlashArray — check active replication
purepod list
purepod show replication --pod <pod_name>

# Dell PowerMax SRDF — check link state
symrdf -g <dg_name> query

# Generic: check WAN utilisation
iperf3 -c <target-site-ip> -t 10   # bandwidth test between sites
```

## Array Health Check Commands

```bash
# Pure FlashArray
purearray monitor             # latency, IOPS, bandwidth
purevolume monitor <volume>   # per-volume stats

# Dell PowerMax
symcfg show -sid <sid>        # array health summary
symdev list -sid <sid>        # device list

# NetApp ONTAP
storage aggregate show -state !online   # degraded aggregates
volume show -state !online
```
