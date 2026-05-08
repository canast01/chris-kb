# PowerScale — Diagnostics

## Diagnostic Commands

```bash
# Cluster node and drive health summary
isi status

# Per-node hardware component status
isi devices node list

# List all cluster background jobs and their state
isi job list

# Show CPU and throughput statistics per node
isi statistics query current --keys CPU,BYTES_OUT,BYTES_IN --nodes all

# Show storage pool and tier capacity
isi storagepool list

# Show SyncIQ policy status and last run result
isi sync policies list
isi sync reports list

# Show recent cluster events (filter by severity)
isi event list --severity critical

# List all quotas and their consumption
isi quota list

# Show network interfaces per node
isi network interfaces list

# Verify AD join status per zone
isi auth ads list

# Show snapshot space usage
isi snapshot list
```

## Log Locations

| Log | Location / Command | Notes |
|---|---|---|
| OneFS system log | `/var/log/messages` (on any node) | Node-level OS and OneFS daemon messages |
| Cluster event log | `isi event list` | Authoritative source for hardware and software events |
| SyncIQ job log | `isi sync reports view --id <report-id>` | Per-policy replication details including errors |
| Audit log (protocol) | `isi audit settings global view` | Configures syslog forwarding of NFS/SMB access events |
| isi_logs bundle | `isi_gather_info` (run on any node as root) | Collects full cluster diagnostic bundle for Dell Support |

## Capacity Diagnostics

```bash
# Overall cluster used vs. free
isi statistics system list | grep -E "Cluster Capacity|Used|Free|HDD|SSD"

# Capacity by storage pool / node pool
isi storagepool nodepools list
isi storagepool tiers list

# Live statistics query
isi statistics query current \
    --stats cluster.disk.xfers.rate.read,cluster.disk.xfers.rate.write,\
cluster.disk.bytes.rate.read,cluster.disk.bytes.rate.write

# Node pool capacity breakdown
isi storagepool nodepools list -v

# File pool policies and tiering
isi filepool policies list
isi filepool default-policy view

# Largest directories under /ifs (run from cluster shell)
du -sh /ifs/* 2>/dev/null | sort -h | tail -20

# Directories nearing quota threshold
isi quota quotas list --type directory | awk '
    NR>1 {
        if ($3 != "---" && $2 != "---") {
            pct = $3/$2*100
            if (pct > 80) print "WARNING:", pct"%", $1
        }
    }'

# Historical capacity statistics
isi statistics history list \
    --stats cluster.disk.bytes.used,cluster.disk.bytes.free
```

## Capacity Management Actions

| Situation | Action |
|---|---|
| > 80% used | Alert, review quotas, identify top consumers |
| > 90% used | Emergency — identify and remove/archive data |
| Node pool full but cluster has free space | File pool policy not moving data — check SmartPools job |
| SSD tier full | Check SSD caching policies; consider adding SSD nodes |
| Quota exceeded by application | Increase quota with change approval |

## Before Calling Support

1. OneFS version: `isi version`
2. Cluster serial number: `isi config`
3. Node health summary: `isi status > /tmp/status.txt`
4. Event log: `isi event list > /tmp/events.txt`
5. For SyncIQ issues: `isi sync reports list > /tmp/synciq.txt`
6. For node hardware faults: note the node number and drive bay from `isi status`
7. Collect a full diagnostic bundle: `isi_gather_info` — saves to `/ifs/data/Isilon_Support/`

Upload the `isi_gather_info` bundle via the Dell Support case portal or via SupportAssist auto-collection.
