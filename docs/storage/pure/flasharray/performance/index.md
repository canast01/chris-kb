# FlashArray Performance

## Array-Level Performance

```bash
# Real-time array performance (reads, writes, IOPS, latency)
purecli array list --performance

# Bandwidth and IOPS summary
purecli array list --performance | grep -E "read_bytes|write_bytes|reads_per_sec|writes_per_sec|usec_per_read|usec_per_write"
```

## Volume-Level Performance

```bash
# Performance stats for all volumes
purecli volume list --performance

# Performance for a specific volume
purecli volume list <volume_name> --performance
```

Key metrics:
| Metric | Normal Range | Action if High |
|---|---|---|
| `usec_per_read_op` | < 500 µs | Investigate host I/O pattern |
| `usec_per_write_op` | < 500 µs | Check queue depth |
| `reads_per_sec` | Workload-dependent | Correlate with application |
| `write_bytes_per_sec` | Workload-dependent | Check for runaway writes |

## Host-Level Performance

```bash
purecli host list --performance
purecli hgroup list --performance
```

## FlashArray Latency Targets

Pure FlashArray (all-NVMe) typical latency:
- **< 500 µs** read/write — normal
- **500 µs – 1 ms** — elevated; investigate
- **> 1 ms** — abnormal; check for queue depth, host connectivity, or array load

## Pure1 Performance Analysis

For historical trending and anomaly detection:
- **Pure1 → Analysis → Performance** — array-wide IOPS/latency/bandwidth over time
- **Pure1 → Analysis → Workload** — per-volume breakdown
- AI-driven anomaly alerts surfaced in Pure1

## QoS Limits (Bandwidth Throttling)

```bash
# Show QoS settings on a volume
purecli volume list <volume_name> --details

# Set IOPS limit on a volume
purecli volume setattr <volume_name> --iops-limit 5000

# Set bandwidth limit
purecli volume setattr <volume_name> --bandwidth-limit 1G

# Remove QoS limit
purecli volume setattr <volume_name> --iops-limit 0
```

## Common Issues

| Symptom | Check | Action |
|---|---|---|
| High latency (> 1ms) | Volume performance | Check queue depth, host I/O pattern |
| Array fully loaded | IOPS at max | Apply QoS to top consumers |
| Latency spikes | Specific volume | Investigate host application |
| Low data reduction | Workload incompressible | Expected for encrypted/compressed data |
