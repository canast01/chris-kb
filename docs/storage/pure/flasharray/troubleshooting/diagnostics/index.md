# FlashArray — Diagnostics

## Diagnostic Commands

```bash
# Overall array health and Purity version
purearray list
purearray list --controller

# Active alerts (all severities)
purealert list

# Drive health and rebuild status
puredrive list
puredrive list --progress

# Array capacity and data reduction
purearray list --space

# Real-time performance (latency, IOPS, bandwidth)
purearray monitor

# Per-volume performance
purevol list --monitor

# Host path and connection status
purehost list
purehost list --connection
purehgroup list
purehgroup list --connection

# FC/iSCSI/NVMe port status
pureport list

# Protection group schedules and replication status
purepgroup list
purepgroup list --schedule

# ActiveCluster pod status and failover preference
purepod list
purepod list --replicating
purepod list --failover-preference

# Snapshot space usage
puresnap list --space

# Collect diagnostic bundle for support
purediag --send     # sends to Pure Support directly if phone-home is active
purediag --output /tmp/diag.tgz   # saves locally if phone-home is unavailable
```

## Performance Diagnostics

```bash
# Real-time array performance (reads, writes, IOPS, latency)
purearray monitor

# Bandwidth and IOPS summary
purearray monitor --latency
purearray monitor --bandwidth
purearray monitor --iops

# Per-volume performance
purevol monitor --latency
purevol monitor --iops
purevol monitor --historical 24h

# Per-host performance
purehost monitor --bandwidth
purehost monitor --iops
```

**Latency targets:**

| Range | Status | Action |
|---|---|---|
| < 500 µs read/write | Normal | None |
| 500 µs – 1 ms | Elevated | Investigate |
| > 1 ms | Abnormal | Check queue depth, host connectivity, array load |

## Log Locations

| Log | Location / Command |
|---|---|
| Purity system log (controller events, upgrades) | `purearray list --log` or `/var/log/purity/` on the controller via SSH |
| Alert history | `purealert list --flagged true` (flagged/resolved alerts) |
| Audit log (admin actions) | `pureadmin list --audit` |
| Replication log | `purepgroup list --replication` |
| Diagnostic bundle | `purediag --output <path>` — includes all logs, configs, and metrics |
| Drive event log | `puredrive list` — per-drive state history visible in diagnostic bundle |
| Pure1 event timeline | Pure1 portal > Arrays > select array > Events |
