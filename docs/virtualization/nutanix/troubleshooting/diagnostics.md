---
tags:
  - nutanix
  - troubleshooting
  - diagnostics
  - logs
  - support-bundle
---
# Nutanix — Diagnostics

<div class="kb-summary">
Nutanix diagnostic tools — key log file locations, NCC full run and log collection, support bundle (log bay) generation, per-service debugging, and Insights (Pulse) data review.

*Applies to: AOS 6.x · AHV*
</div>

---

## Before you begin

- **Access:** CVM SSH (nutanix) for log access and NCC; Prism Element admin for Log Collector and analysis charts
- **Collect early:** Gather NCC output and support bundle as soon as you open a case — logs roll over on busy clusters

---

## Quick Diagnostics Flow

```text
1. Run NCC and capture output              → identifies most issues automatically
2. Check service status (genesis status)   → identifies down services
3. Read service-specific logs              → identifies root cause
4. Collect support bundle                  → required for Nutanix GSS cases
```

---

## NCC — Automated Diagnostics

```bash
# Full NCC run — captures all 400+ checks
ncc --health_checks run_all 2>&1 | tee /tmp/ncc-$(date +%Y%m%d).txt

# Show only failures
grep "^FAIL" /tmp/ncc-$(date +%Y%m%d).txt

# Run a specific check
ncc --health_checks disk_usage_check
ncc --health_checks cluster_services_status_check
ncc --health_checks data_resiliency_status_check

# List all available NCC checks
ncc --health_checks list

# View previous NCC run results without re-running
ncli ncc get-ncc-result | head -50
```

---

## Key Log Locations (CVM)

All logs live on the CVM under `/home/nutanix/data/logs/`.

| Service | Log file |
|---|---|
| Stargate (I/O) | `/home/nutanix/data/logs/stargate.INFO` / `.ERROR` |
| Curator (background) | `/home/nutanix/data/logs/curator.INFO` / `.ERROR` |
| Cassandra (metadata) | `/home/nutanix/data/logs/cassandra/system.log` |
| Zeus / ZooKeeper | `/home/nutanix/data/logs/zookeeper/zookeeper.log` |
| Cerebro (replication) | `/home/nutanix/data/logs/cerebro.INFO` |
| Acropolis (AHV API) | `/home/nutanix/data/logs/acropolis.INFO` |
| Prism gateway | `/home/nutanix/data/logs/prism_gateway.log` |
| Genesis (service mgr) | `/home/nutanix/data/logs/genesis.out` |
| NCC | `/home/nutanix/data/logs/ncc/` |
| Alert manager | `/home/nutanix/data/logs/alert_manager.INFO` |

```bash
# Live tail Stargate errors (I/O issues)
tail -f /home/nutanix/data/logs/stargate.ERROR

# Check recent Curator activity (dedup, tiering, rebuild)
tail -100 /home/nutanix/data/logs/curator.INFO | grep -i "scan\|task\|error"

# Check Prism gateway errors (UI issues, API failures)
tail -50 /home/nutanix/data/logs/prism_gateway.log | grep -i "error\|exception"

# Find errors across all CVM logs from the last hour
allssh "grep -l ERROR /home/nutanix/data/logs/*.ERROR 2>/dev/null"
```

---

## AHV Hypervisor Logs

```bash
# SSH to AHV host (requires root or nutanix user with IPMI console)
ssh root@<ahv-host-ip>

# Kernel messages — hardware errors, disk failures
dmesg | grep -i "error\|fail\|warn\|crit" | tail -30

# System journal — AHV OS and service messages
journalctl -n 100 --no-pager | grep -i "error\|fail"

# libvirt (VM management) logs
cat /var/log/libvirt/libvirtd.log | tail -50

# QEMU logs per VM (one file per VM)
ls /var/log/libvirt/qemu/
cat /var/log/libvirt/qemu/<vm-name>.log | tail -50
```

---

## Genesis Service Status Diagnostics

```bash
# On affected CVM — list all services and their state
genesis status

# Look for any service NOT in "UP" state
genesis status | grep -v " UP$" | grep -v "^Genesis"

# Restart a specific failing service (safer than genesis restart)
# (Nutanix GSS may guide specific service restarts for their service)
# For most purposes:
genesis restart   # restarts all CVM services — brief I/O disruption
```

---

## Cassandra (Metadata Store) Diagnostics

```bash
# Check ring health across all CVMs
allssh "nodetool status"
# Expected: all nodes UN (Up/Normal)
# Problem: DN = Down, ? = Unknown status

# Check compaction queue (large queue = catch-up after node recovery)
allssh "nodetool compactionstats"

# Ring token distribution
allssh "nodetool ring 2>/dev/null | head -5"
```

---

## Stargate (I/O) Diagnostics

Stargate handles all cluster I/O. High Stargate errors indicate storage problems.

```bash
# Count errors in Stargate log
grep -c "ERROR\|FATAL" /home/nutanix/data/logs/stargate.ERROR

# Check for specific I/O patterns
grep "disk" /home/nutanix/data/logs/stargate.ERROR | tail -20
grep "timeout" /home/nutanix/data/logs/stargate.ERROR | tail -20

# Check Stargate stats (Prism → Analysis → I/O metrics is easier)
# CLI: check Stargate port for responsiveness
curl -s http://localhost:2009/ | head -5
```

---

## Curator (Background Jobs) Diagnostics

```bash
# What Curator tasks have run recently?
curator_cli get_last_successful_scans

# Any active Curator tasks running now?
curator_cli display_curator_tasks

# Details of a specific scan
curator_cli get_last_successful_scans   # get scan_id
curator_cli get_scan_info --scan_id=<id>
```

---

## Support Bundle (Log Bay) Collection

A support bundle packages all relevant logs for Nutanix GSS.

### Via Prism Element (recommended)

```text
Prism Element → Settings → Log Collector → Collect Logs
  Time Range: last 4 hours (or cover the incident window)
  Include NCC: Yes
  Click Collect
  Download the .zip when ready (may take 5–15 minutes)
```

### Via CLI

```bash
# Collect logs for last 4 hours
logbay collect --start_time=$(date -d "4 hours ago" +%Y-%m-%dT%H:%M:%S) \
               --end_time=$(date +%Y-%m-%dT%H:%M:%S)

# Monitor progress
logbay status

# Collected bundle location
ls /home/nutanix/data/logbay/bundles/

# Upload directly to Nutanix support case (requires internet access)
logbay upload --bundle=<bundle-file.tar.gz> --case=<support-case-number>
```

---

## Prism Analysis — Performance Diagnostics

For performance issues (latency, throughput), Prism Element provides built-in analysis charts:

```text
Prism Element → Analysis → create an Analysis Chart
  Metrics: Storage I/O Bandwidth, Latency, IOPS, CPU usage
  Scope: cluster, VM, storage container, or host
  Time range: overlay the incident window
```

Key metrics to check during performance incidents:
- **Read/Write latency > 10ms** → possible disk degradation or controller saturation
- **IOPS at limit** → cluster IOPS ceiling; check disk tier (SSD vs HDD ratio)
- **CPU steal on hosts** → AHV scheduling contention

---

## See also

- [Nutanix — Common Issues](common-issues/)
- [Nutanix — Escalation](escalation/)
